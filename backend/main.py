from fastapi import FastAPI, Path
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
import os
from geopy.geocoders import Nominatim
from models import NodeInput

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
def add_node(node: NodeInput):
    data = geolocator.geocode(node.name)
    location_exists = nodes_collection.find_one({
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [data.longitude, data.latitude]
                },
                "$maxDistance": 20
            }
        }
    })
    if location_exists:
        return {"message": "Location already exists"}
    else: 
        nodes_collection.insert_one({
            "location": {
                "type": "Point",
                "coordinates": [data.longitude, data.latitude]
            }
        })
        return {"message": "Location successfully added"}

