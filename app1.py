import os
import base64
import pathlib
import secrets
import requests

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import plotly.graph_objs as go
import dash_daq as daq
import dash_bootstrap_components as dbc
import visdcc
from flask import request

import dash_auth
from assets.users import USERNAME_PASSWORD_PAIRS

import pandas as pd
import glob

secure_random = secrets.SystemRandom()
external_scripts = [{'src': '//localhost:8290/divolte.js'}]
external_stylesheets = [dbc.themes.BOOTSTRAP]

recommender_api = 'http://localhost:8080/recommend'

app = dash.Dash(__name__,
external_scripts=external_scripts,
external_stylesheets=external_stylesheets,
)

server = app.server
app.config["suppress_callback_exceptions"] = True
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

APP_PATH = str(pathlib.Path(__file__).parent.resolve())
styles = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "styles_processed.csv")))

img_list = glob.glob('data/*.jpg')

def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Fashion Recommender Dashboard"),
                    html.H6("suggesting your favorite fashion products"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Button(
                        id="learn-more-button", children="LEARN MORE", n_clicks=0
                    ),
                    html.Img(id="logo", src=app.get_asset_url("my-logo-2.svg")),
                ],
            ),
        ],
    )
def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="my-tab1",
                        label="Home Page",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="my-tab2",
                        label="Personalized Recommendations",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )
  

def item_info(ipath):
    _id = int(os.path.basename(ipath).split('.jpg')[0])
    _imgmeta = styles[styles.id==_id].productDisplayName.values[0]
    return _id, _imgmeta

img_ids = []
img_list_pop = img_list.copy()
img_list_pop = secure_random.sample(img_list_pop, 6)
for x in img_list_pop:
    _id, _ = item_info(x)
    img_ids.append(_id)

def create_card(ipath):
    encoded_image = base64.b64encode(open(ipath, 'rb').read())
    id, imgmeta = item_info(ipath)
    item_id = str(id)
    view_id = item_id+'_view'
    jsst_view = "divolte.signal('view',{{'item_id':{}}})".format(id)
    return dbc.Card(className="imagegrid", id=item_id+'_card',
    children=[dbc.CardBody([
                            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                            style={'height':'100%', 'width':'100%'}, title=imgmeta, id=item_id),
                            visdcc.Run_js(id=view_id, run=jsst_view)
                        ])
                        ])

def build_image_grid(imglist, idflag='pop'):
    child_list = []
    for ipath in imglist:
        child_list.append(dbc.Col([create_card(ipath)], width={"size": 2}))
    return html.Div([
        dbc.Row(id="big-app-container2-{}".format(idflag),
        children=child_list)])


app.layout = html.Div(
    className="big-app-container",
    children=[
        build_banner(),
        html.Div(
            className="big-app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        visdcc.Run_js(id='click_log')
    ]
)


@app.callback(
    Output("app-content", "children"),
    Input("app-tabs", "value")
)
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        return build_image_grid(img_list, 'catalog'),
    return (
        html.Div(className="section-banner", id='popularity-banner', children='Popular Products'),
        build_image_grid(img_list_pop),
        html.Div(className="section-banner", id='similarity-banner', children='Inspired by your history'),
        html.Div(id='sim_reco_img_grid')
    )

@app.callback(
    Output('sim_reco_img_grid', 'children'),
    [Input('similarity-banner', 'children')]
)
def update_output_div(n_clicks):
    username = request.authorization['username']
    if username:
        img_ids = requests.get("{}/{}".format(recommender_api, username))
        img_ids = img_ids.json()
        img_list_sim = [f'data/{id}.jpg' for id in img_ids]
        print(username, img_list_sim)
    return build_image_grid(img_list_sim, 'sim')


input_list = [eval(f"Input(str({x}), 'n_clicks')") for x in img_ids]

@app.callback(
    Output('click_log','run'),
    input_list,
    )
def logclicks(*args):
    if any(args):
        ctx = dash.callback_context
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        return "divolte.signal('click',{{'item_id':{}}})".format(int(button_id))
    return ""


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8051, host='127.0.0.1')