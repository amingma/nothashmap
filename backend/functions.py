def location_exists(collection, coords, max_dist):
    return collection.find_one({
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": coords
                },
                "$maxDistance": max_dist
            }
        }
    })