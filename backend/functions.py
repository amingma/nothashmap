def location_exists(collection, longitude, latitude, max_dist):
    return collection.find_one({
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "$maxDistance": max_dist
            }
        }
    })