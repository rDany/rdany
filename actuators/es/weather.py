import logging
import requests

class actuator:

    @staticmethod
    def generate_string(parameters, context):
        logger = logging.getLogger("weather actuator")

        headers = {'user-agent': "rDany/1.1 (http://www.rdany.org/rdany/; botmaster@rdany.org)"}
        par = {
            "id": 3435259,
            "APPID": "3d81c3d84f4d0c617799eb16a73449df"
        }
        url = "http://api.openweathermap.org/data/2.5/weather"
        try:
            r = requests.get(url, timeout=1, headers=headers, params=par)
        except Timeout:
            logging.warning('ConnectionTimeout: {0}'.format(url))
        #print (r)

        if r.status_code == requests.codes.ok:
            response = r.json()
            #print (response)
        else:
            response = {"cod": "0"}

        if response["cod"] == "200":
            #self.city_id = response['id']
            #self.latitude = response['coord']['lat']
            #self.longitude = response['coord']['lon']
            #self.weather_id = response['weather'][0]['id']
            #self.temperature = response['main']['temp'] - 273.15
            #self.wind_speed = response['wind']['speed']
            #self.clouds = response['clouds']['all']
            text = "{0:.1f} C.".format(response['main']['temp'] - 273.15)
        else:
            text = "No pude conectarme a Openweathermap.org"
        return {"text": text }
