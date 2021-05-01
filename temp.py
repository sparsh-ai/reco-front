import requests

userid = 'user0'
response = requests.get("http://localhost:8080/recommend/{}".format(userid))

print(response.json())

/Users/sparshagarwal/anaconda3/envs/env/bin/python /Users/sparshagarwal/Desktop/work/Recofront/dash/test_app/app1.py

