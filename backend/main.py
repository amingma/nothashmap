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
edges_collection = db["road_edges"]
routes_collection = db["routes"]
# node_data = {
#     "node_id": 123,
#     "latitude": 41.8781,
#     "longitude": -87.6298
# }
# nodes_collection.insert_one(node_data)

geolocator = Nominatim(user_agent="geoapi")

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/add-node")
def add_node(node: NodeInput):
    location = geolocator.geocode(node.name)
    data = {
        "latitude": location.latitude,
        "longitude": location.longitude
    }
    nodes_collection.insert_one(data)
    return {"message": "Location successfully added"}

