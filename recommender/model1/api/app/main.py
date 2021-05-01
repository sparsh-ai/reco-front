import os
import pickle5 as pickle
import numpy as np
import pandas as pd
from itemrep import topk_distance

import uvicorn
from fastapi import FastAPI

# artifact_path = 'artifacts'
artifact_path = './artifacts'

umap = pickle.load(open(os.path.join(artifact_path,"usermap.p"), "rb"))
imap_inverse = pickle.load(open(os.path.join(artifact_path,"itemmap_inv.p"), "rb"))
interactions = pd.read_pickle(os.path.join(artifact_path,"interactions.p"))

def recommend(userid, topk=2):
    uid = umap[userid]
    _temp = interactions.iloc[uid]
    _temp = _temp[_temp!=0]
    _tempdf = pd.DataFrame(columns=['itemid','distance'])
    for row in _temp.iteritems():
        _temp1 = topk_distance(imap_inverse[row[0]])
        _temp2 = pd.DataFrame(list(_temp1.items()), columns=['itemid','distance'])
        _temp2['weight'] = row[1]
        _tempdf = _tempdf.append(_temp2)
    _tempdf = _tempdf[_tempdf['distance']!=0]
    _tempdf['distance']+=1
    _tempdf['score'] = np.sqrt(_tempdf['weight'])/np.log(_tempdf['distance'])
    _tempdf = _tempdf.set_index('itemid')
    _tempdf = _tempdf[['score']].groupby(['itemid']).mean()
    _tempdf = _tempdf.sort_values(by='score', ascending=False)
    return _tempdf.index.values[:topk]

app = FastAPI()

@app.get("/recommend/{userid}")
async def read_item(userid: str):
    recs = recommend(userid).tolist()
    return recs