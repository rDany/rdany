import re
import requests

class processor:
    example = "¿Cómo está el clima?"
    keywords = ["clima"]

    @staticmethod
    def check_string(string, context):
        pideweather = re.search(r"\W*clima", string, re.IGNORECASE)
        text = None
        if pideweather:
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
                return None

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
                return None

            return {"text": text, "confidence": 0.4, "context": {}}
