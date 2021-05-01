from pathlib import Path
from img2vec_pytorch import Img2Vec
from PIL import Image
import faiss
import numpy as np
import logging
import pickle
import os

import warnings
warnings.filterwarnings("ignore")

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger('itemrep-training')

image_path = '../../data'
artifact_path = 'artifacts'

img_paths = []
for path in Path(image_path).rglob('*.jpg'):
    img_paths.append(path)
    
log.info("{} images have been found!".format(len(img_paths)))

img2vec = Img2Vec(cuda=False)
vectors = img2vec.get_vec([Image.open(ipath) for ipath in img_paths])

log.info("Image vectorization done!")

item_vectors = {ipath.stem:vectors[iindex] for iindex, ipath in enumerate(img_paths)}
item_paths = {ipath.stem:ipath for ipath in img_paths}
pickle.dump(item_vectors, open(os.path.join(artifact_path,"item_vectors.p"), "wb"))
pickle.dump(item_paths, open(os.path.join(artifact_path,"item_paths.p"), "wb"))

log.info("Item maps stored in {}".format(artifact_path))

dim = np.array(list(item_vectors.values())).shape[1]
index = faiss.IndexFlatL2(dim)
index.add(np.array(list(item_vectors.values())))
faiss.write_index(index,os.path.join(artifact_path,"vector.index"))

log.info("FAISS indexing done. Saved in {}".format(artifact_path))