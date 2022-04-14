import os
from api.models import Location
import geopy
from geopy.extra.rate_limiter import RateLimiter
from random import randrange
import spacy
import reverse_geocoder as rg
import csv

class Geocoder:
    def __init__(self):
        self.geocoders = []
        
        locator_nominatim = geopy.geocoders.Nominatim(user_agent="geocoder-awefawefawefawefawef")
        self.geocoders.append(RateLimiter(locator_nominatim.geocode, min_delay_seconds=1))

        mapbox_token = os.environ['MAPBOX_TOKEN'];
        locator_mapbox = geopy.geocoders.MapBox(api_key=mapbox_token)
        self.geocoders.append(RateLimiter(locator_mapbox.geocode, min_delay_seconds=1))

        geonames_username = os.environ['GEONAMES_USERNAME']
        locator_geonames = geopy.geocoders.GeoNames(username=geonames_username)
        self.geocoders.append(RateLimiter(locator_geonames.geocode, min_delay_seconds=1))
        
        bing_key = os.environ['BING_MAPS_KEY']
        locator_bing = geopy.geocoders.Bing(api_key=bing_key)
        self.geocoders.append(RateLimiter(locator_bing.geocode, min_delay_seconds=1))
        
        open_cage_key = os.environ['OPEN_CAGE_KEY']
        locator_open_cage = geopy.geocoders.OpenCage(api_key=open_cage_key)
        self.geocoders.append(RateLimiter(locator_open_cage.geocode, min_delay_seconds=1))
        
        mapquest_key = os.environ['MAPQUEST_KEY']
        locator_mapquest = geopy.geocoders.OpenMapQuest(api_key=mapquest_key)
        self.geocoders.append(RateLimiter(locator_mapquest.geocode, min_delay_seconds=1))
        
        maptiler_key = os.environ['MAPTILER_KEY']
        locator_maptiler = geopy.geocoders.MapTiler(api_key=maptiler_key)
        self.geocoders.append(RateLimiter(locator_maptiler.geocode, min_delay_seconds=1))
        
        geocodio_key = os.environ['GEOCODIO_KEY']
        locator_geocodio = geopy.geocoders.Geocodio(api_key=geocodio_key)
        self.geocoders.append(RateLimiter(locator_geocodio.geocode, min_delay_seconds=1))
        
        here_key = os.environ['HERE_KEY']
        locator_here = geopy.geocoders.HereV7(apikey=here_key)
        self.geocoders.append(RateLimiter(locator_here.geocode, min_delay_seconds=1))
        
        

        dic = {}
        with open("/app/api/wikipedia-iso-country-codes.csv") as f:
            file= csv.DictReader(f, delimiter=',')
            for line in file:
                dic[line['Alpha-2 code']] = line['English short name lower case']
                
        self.country_from_alpha2 = dic
        
        self.nlp_en = spacy.load('en_core_web_md')
        
        self.cache = {}
        
    def get_all_locations(self, text: str):
        location_strings = []
        doc = self.nlp_en(text)
        for ent in doc.ents:
            if(ent.label_ == 'GPE'):
                location_strings.append(ent.text)
                
        locations_coordinates = []
        
        for location_string in location_strings:
            if location_string in self.cache:
                locations_coordinates.append(self.cache[location_string].__dict__)
            else:
                random_service = randrange(len(self.geocoders))
                geocode_result = self.get_location_from_geocoder(random_service, location_string)
                count = 0
                while geocode_result is None:
                    random_service = (random_service + 1) % len(self.geocoders)
                    geocode_result = self.get_location_from_geocoder(random_service, location_string)
                    count = count + 1
                    if count >= len(self.geocoders):
                        break
                
                if geocode_result is not None:
                    results = rg.search((geocode_result.latitude, geocode_result.longitude),mode=1)
                    print(self.country_from_alpha2[results[0]['cc']])
                    location = Location(geocode_result.latitude, geocode_result.longitude, self.country_from_alpha2[results[0]['cc']])
                    locations_coordinates.append(location.__dict__)
                    self.cache[location_string] = location
                
        # print(locations_coordinates)
                
        return locations_coordinates
    
    def get_location_from_geocoder(self, service: int, location_string: str):
        try:
            return self.geocoders[service](location_string)
        except:
            new_service = (service + 1) % len(self.geocoders)
            return self.get_location_from_geocoder(new_service, location_string)