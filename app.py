from flask import Flask, jsonify, render_template, request
from PIL import Image # PIL-SIMD
import threading
import requests
import base64
import time
import io
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

### (GLOBAL) PARAMETERS

TILEACROSS = 352
RENDEREDTILESIZE = 32
MMG_SERVERS = {}
RESPONSE = []
LOCK = threading.Lock()

###

# ---------------- #
# Middlware server #
# ---------------- #

@app.route('/', methods=["GET"])
def GET_index():
  '''Route for "/" (frontend)'''
  return render_template("index.html")

@app.route('/addMMG', methods=["PUT"])
def add_mosaic_generator():
  global MMG_SERVERS

  data = request.json
  if not data:
    return 'No JSON!', 400
  
  for requiredKey in ['name', 'url']:
    if requiredKey not in data.keys():
      return f'Invalid JSON - Missing {requiredKey}', 400
  
  MMG_SERVERS[data['name']] = data['url']
  return "Connected!", 200

def POST_MMG(mmg_url, b64):
  global RESPONSE
  # POST to all MMG microservices to get mosaic
  url = mmg_url + '/mosaic'
  try:
    mosaic = requests.post(url = url, 
                          data = b64, 
                          headers = {'Content-Type':'image/png'}, 
                          params = {'tilesacross':TILEACROSS, 'tilesize':RENDEREDTILESIZE})
    with LOCK:
      RESPONSE.append(mosaic.json()) # Response will come back as PNG
  except requests.ConnectionError:
    print("FAILED TO CONNECT TO", mmg_url)

@app.route('/makeMosaic', methods=["POST"])
def POST_makeMosaic():
  before = time.time()
  # Clear response
  global RESPONSE
  RESPONSE.clear()

  # Open base_image and transform to base64
  base_image = Image.open(request.files['image'])
  buffer = io.BytesIO()
  base_image.save(buffer, 'png')
  buffer.seek(0)
  b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

  # Multi-threading POST to MMGs
  threads = []
  for mmg_url in MMG_SERVERS.values():
    thread = threading.Thread(target=POST_MMG, args=(mmg_url, b64))
    threads.append(thread)

  for thread in threads:
    thread.start()

  for thread in threads:
    thread.join()

  after = time.time()

  print("TOTAL TIME:", after-before)

  return jsonify(RESPONSE)

if __name__ == '__main__':
  app.run(host=os.getenv('FLASK_RUN_HOST'), port=os.getenv('MIDDLEWARE_PORT'))