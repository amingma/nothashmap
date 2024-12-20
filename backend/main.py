from fastapi import FastAPI, Path, Response
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
import os
from geopy.geocoders import Nominatim
from models import NodeInput
from functions import location_exists

load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PASS")
app = FastAPI()

connection_string = f"mongodb+srv://jiama19999:{password}@maps.r1ish.mongodb.net/?retryWrites=true&w=majority&appName=maps"
client = MongoClient(connection_string)
db = client["route_planner"]

nodes_collection = db["road_nodes"]
nodes_collection.create_index({"location": "2dsphere"})
edges_collection = db["road_edges"]
routes_collection = db["routes"]

geolocator = Nominatim(user_agent="geoapi")

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/add-node")
def add_node(node: NodeInput, response: Response):
    data = geolocator.geocode(node.name)
    try:
        coords = [data.longitude, data.latitude]
    except:
        response.status_code = 400
        return {"message": "Invalid query"}
    if location_exists(nodes_collection, coords, 20):
        return {"message": "Location already exists"}
    else: 
        nodes_collection.insert_one({
            "location": {
                "type": "Point",
                "coordinates": [data.longitude, data.latitude]
            }
        })
        return {"message": "Location successfully added"}

