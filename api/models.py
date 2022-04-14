import json

class Location:
    def __init__(self, latitude, longitude, country):
        self.latitude = latitude
        self.longitude = longitude
        self.country = country
        
class Article:
    def __init__(self, link: str, heading: str, text: str):
        self.link = link
        self.heading = heading
        self.text = text
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        
class Response:
    def __init__(self, message, data):
        self.message = message
        self.data = data