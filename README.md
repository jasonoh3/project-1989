# Mosaic Microservice API

Project 1989 is a GRAND project in CS 340, where each student creates 13 independent mosaics. By the end of the semester, if all goes to plan, the middleware will call every single mosaic generator and create 1989 mosaics. Then, using a map-reduce architecture, we would reduce each mosaic into one beautiful mosaic.

## Project Tree Directory

```
project-1989
│   API.md
|   app.py
│   .env
│
└───MMGs
│   │   launch.sh
│   │   reducer.py
│   │   movies.py
│   │   nature.py
│   │   nintendo.py
│   │   pokemon.py
│   │   amongus.py
│   │   burger.py
│   │   cat.py
│   │   dog.py
│   │   korea.py
│   │   memes.py
│   │   painting.py
│   │   uiuc.py
│   │   vegetable.py
│   │
│   └───images
│       │   movies
│       │   nature
│       │   nintendo
│       │   pokemon
│       │   amongus
│       │   burger
│       │   cat
│       │   dog
│       │   korea
│       │   memes
│       │   painting
│       │   uiuc_faculty
│       │   vegetable
│   
└───setup
    │   setup.sh
    │   requirements.txt
```

## High-Level Overview: System

The middleware and MMGs communicate with each other through simple HTTP POST and PUT requests.

- MMG will send a [PUT request](#technical-overview:-mmg-->-middleware) to the middleware with a JSON with __name__, __url__, and __author__.

- Middleware will send a [POST request](#technical-overview:-middleware-->-mmg) to the MMG with the user's __image__.

For a user to connect their MMG to this middleware, the MMG must send a __PUT request__ and return the following JSON when a __POST request__ is asked:

```
{"image": "data:image/png;base64," + b64}
```

The __b64__ is the png image encoded in 'base64' and decoded in 'UTF-8'.

---

## Middleware

To run the middleware server, go to the [root directory](./) of the this project.
> `cd project-1989`

Then, run this python flask server: 
> `python3 app.py`

---

## Microservice Mosaic Generator (launch.sh)

__Note: Open another terminal.__

To run all the MMG servers, go to the [MMGs directory](./MMGs/).
> `cd MMGs`

Then, run this shell script: 
> `./launch.sh`

---

## Technical Overview: [MMG](./MMGs/) -> Middleware

Each MMG connects to the middleware through a __HTTP PUT__ request. At start up, the MMG will create a simple put request:

```
id = {
  "name" : "Nintendo MMG",
  "url" : os.getenv('SERVER_URL') + ':' + os.getenv('NINTENDO_MS_PORT'),
  "author" : "Jason H Oh (jasonoh3)"
}
requests.put(os.getenv('SERVER_URL') + ':' + os.getenv('MIDDLEWARE_PORT') + "/addMMG", json=id)
```

1. The identification of the MMG consists of __name__, __url__, and __author__.
    - `Name` is the name (e.g., movies) of the MMG
    - `URL` will allow the middleware to communicate with it
    - `Author` is the author (e.g., Jason) of the MMG
2. The route verb is __/addMMG__ with a json tag for the MMG's id
3. The endpoint is created at start up, each with their respective ports as listed in the [.env file](./.env)
	- e.g., "http://" + SERVER_URL + ":" + POKEMON_MS_PORT

---

## Technical Overview: [Middleware](./app.py) -> MMG

Once the middleware has all of the MMGs, the middleware will call a POST request to each MMG.

```
mosaic = requests.post(url = url, 
                        data = b64, 
                        headers = {'Content-Type':'image/png'}, 
                        params = {'tilesacross':TILEACROSS, 'tilesize':RENDEREDTILESIZE})
```

1. The request post consists of __url__, __data__, __headers__, and __params__.
    - `URL` is the url of the MMG
	- `Data` is the base image that the user uploaded, which is encoded in 'base64' and decoded in 'UTF-8'
	- `Headers` ensure that the MMG understands that the content is an image/png
	- `Params` are the string query that is sent to the MMG
		- tilesacross = the # of tiles that span across the base image
		- tilesize = the size of the tile
		- TILEACROSS & RENDEREDTILESIZE are global variables that are instantiated at the start up of the middleware
2. The route verb is __/mosaic__
3. The endpoint is created at start up, which is listed in the [.env file](./.env)
	- "http://" + SERVER_URL + ":" + MIDDLEWARE_PORT
4. Params -> __/mosaic?tilesacross=#&tilesize=#__

---

## Environment file ([.env](./.env))
The environment file contains the server url and ports.
