from flask import Flask, request, make_response
from PIL import Image # PIL-SIMD
import numpy as np
import requests
import io
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# ----------- #
#   REDUCER   #
# ----------- #

# --------- CONNECT TO MIDDLEWARE --------- #
id = {
  "name" : "Reducer",
  "url" : os.getenv('SERVER_URL') + ':' + os.getenv('REDUCER_MS_PORT'),
  "author" : "Jason H Oh (jasonoh3)"
}
requests.put(os.getenv('MIDDLEWARE_URL') + ':' + os.getenv('MIDDLEWARE_PORT') + "/registerReducer", data=id)
# ----------------------------------------- #

def betterPixel(base_color, mosaic1_color, mosaic2_color):
  mos1_distance = (base_color[0] - mosaic1_color[0])**2 + (base_color[1] - mosaic1_color[1])**2 + (base_color[2] - mosaic1_color[2])**2
  mos2_distance = (base_color[0] - mosaic2_color[0])**2 + (base_color[1] - mosaic2_color[1])**2 + (base_color[2] - mosaic2_color[2])**2
  return mos1_distance < mos2_distance

@app.route('/', methods=["POST"])
def reduce():
  baseImage = Image.open(request.files["baseImage"]).convert('RGB')
  mosaic1 = Image.open(request.files["mosaic1"]).convert('RGB')
  mosaic2 = Image.open(request.files["mosaic2"]).convert('RGB')
  
  tilesAcross = int(request.args.get('tilesAcross'))
  tileSize = int(request.args.get('renderedTileSize'))
  fileFormat = str(request.args.get('fileFormat'))

  # Width & Height of Mosaic
  tilesBaseSize = baseImage.width / tilesAcross # pixels x pixels of the base image
  width = tilesAcross * tileSize
  height = int(baseImage.height / tilesBaseSize) * tileSize

  # Paste tiles onto the empty mosaic of the base image
  best_mosaic = Image.new(mode="RGB", size=(width, height))
  np_baseImage = np.array(baseImage)
  np_mosaic1 = np.array(mosaic1)
  np_mosaic2 = np.array(mosaic2)
  for i in np.arange(int(baseImage.width / tilesBaseSize)):
    for j in np.arange(int(baseImage.height / tilesBaseSize)):
      baseImage_pixel = np_baseImage[int(j * tilesBaseSize): int(j * tilesBaseSize + tilesBaseSize), int(i * tilesBaseSize): int(i * tilesBaseSize + tilesBaseSize)].mean(axis=(0,1))
      mosaic1_section = np_mosaic1[j * tileSize: j * tileSize + tileSize, i * tileSize: i * tileSize + tileSize]
      mosaic2_section = np_mosaic2[j * tileSize: j * tileSize + tileSize, i * tileSize: i * tileSize + tileSize]
      if betterPixel(baseImage_pixel, mosaic1_section.mean(axis=(0,1)), mosaic2_section.mean(axis=(0,1))):
        best_mosaic.paste(Image.fromarray(np.uint8(mosaic1_section)).convert('RGB'), (i * tileSize, j * tileSize))
      else:
        best_mosaic.paste(Image.fromarray(np.uint8(mosaic2_section)).convert('RGB'), (i * tileSize, j * tileSize))
  
  buffer = io.BytesIO()
  best_mosaic.save(buffer, fileFormat)
  buffer.seek(0)
  return make_response(buffer), 200

if __name__ == '__main__':
  app.run(host=os.getenv('FLASK_RUN_HOST'), port=os.getenv('REDUCER_MS_PORT'))