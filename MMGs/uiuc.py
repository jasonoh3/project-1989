from flask import Flask, request, make_response
from sklearn.neighbors import KDTree
from PIL import Image # PIL-SIMD
import numpy as np
import requests
import glob
import io
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# ---------------- #
#   UIUC FACULTY   #
# ---------------- #

# ------- (GLOBAL) UIUC Faculty Variables ------- #
gTileSize = -1 # pixels of the mosaic
tiles = []
avg_color_tiles = []
tree : KDTree
# ----------------------------------------------- #

# ------------ ALL FILE PATHS ------------ #
# Get every image of a to-be tile
tile_path = './images/uiuc_faculty/'
tiles_path = glob.glob(tile_path + '*.jpg')
# ---------------------------------------- #

# --------- CONNECT TO MIDDLEWARE --------- #
id = {
  "name" : "UIUC Faculty",
  "url" : os.getenv('SERVER_URL') + ':' + os.getenv('UIUC_MS_PORT'),
  "author" : "Jason H Oh (jasonoh3)",
  "tileImageCount" : len(tiles_path)
}
requests.put(os.getenv('MIDDLEWARE_URL') + ':' + os.getenv('MIDDLEWARE_PORT') + "/addMMG", data=id)
# ----------------------------------------- #

def process_tiles(tileSize):
  global gTileSize, tiles, avg_color_tiles, tree

  # Check if there is a need to re-process tiles
  if gTileSize == tileSize:
    return

  # Reset global variables
  gTileSize = tileSize
  tiles.clear()
  avg_color_tiles.clear()

  # Process tiles
  tile_dim = (tileSize, tileSize)
  for tile in tiles_path:
    image = Image.open(tile).resize(tile_dim)
    tiles.append(image)
    avg_color_tiles.append(np.array(image).mean(axis=(0,1)))
  tree = KDTree(avg_color_tiles) # place into kd-tree

@app.route('/', methods=["POST"])
def gen_mosaic():
  tilesAcross = int(request.args.get('tilesAcross'))
  tileSize = int(request.args.get('renderedTileSize'))
  fileFormat = str(request.args.get('fileFormat'))
  image = Image.open(request.files['image']).convert('RGB')

  # Process tiles into respective tileSize (if necessary)
  process_tiles(tileSize)

  # Width & Height of Mosaic
  tilesBaseSize = image.width / tilesAcross # pixels x pixels of the base image
  width = tilesAcross * tileSize
  height = int(image.height / tilesBaseSize) * tileSize

  # Paste tiles onto the empty mosaic of the base image
  mosaic = Image.new(mode="RGB", size=(width, height))
  np_image = np.array(image)
  for i in np.arange(int(image.width / tilesBaseSize)):
    for j in np.arange(int(image.height / tilesBaseSize)):
      pixel = np.reshape(np_image[int(j * tilesBaseSize): int(j * tilesBaseSize + tilesBaseSize), int(i * tilesBaseSize): int(i * tilesBaseSize + tilesBaseSize)].mean(axis=(0,1)), (1,-1))
      mosaic.paste(tiles[tree.query(X=pixel, k=1, return_distance=False)[0,0]], (i * tileSize, j * tileSize))
  
  buffer = io.BytesIO()
  mosaic.save(buffer, fileFormat)
  buffer.seek(0)
  return make_response(buffer), 200

if __name__ == '__main__':
  app.run(host=os.getenv('FLASK_RUN_HOST'), port=os.getenv('UIUC_MS_PORT'))