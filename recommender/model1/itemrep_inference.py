import faiss
import numpy as np
import logging
import pickle5 as pickle
import os

import warnings
warnings.filterwarnings("ignore")

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger('itemrep-inference')

# artifact_path = 'artifacts'
artifact_path = '/Users/sparshagarwal/Desktop/work/Recofront/dash/test_app/recommender/model1/artifacts'

# logging.info("Loading item vectors")
item_vectors = pickle.load(open(os.path.join(artifact_path,"item_vectors.p"), "rb"))

# logging.info("Loading path vectors")
# item_paths = pickle.dump(open(os.path.join(artifact_path,"item_paths.p"), "rb"))

# logging.info("Loading indexer")
index = faiss.read_index(os.path.join(artifact_path,"vector.index"))

def topk_similar(itemid, topk=2):
    _, I = index.search(item_vectors[str(itemid)].reshape(1,-1), topk+1)
    return [list(item_vectors.keys())[i] for i in I.flatten()][1:]

def topk_distance(itemid, topk=2):
    D, I = index.search(item_vectors[str(itemid)].reshape(1,-1), topk+1)
    return {list(item_vectors.keys())[i]:j for (i,j) in zip(I.flatten(),D.flatten())}