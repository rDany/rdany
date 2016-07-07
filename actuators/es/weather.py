import logging
import requests

class actuator:

    @staticmethod
    def generate_string(parameters, context):
        logger = logging.getLogger("weather actuator")
        light_rain = [200, 201, 210, 230, 300, 310, 500, 520]
        medium_rain = [202, 211, 221, 231, 301, 501, 502, 511, 521]
        heavy_rain = [212, 232, 221, 302, 312, 313, 314, 321, 522, 531]
        very_heavy_rain = [503, 504]

        light_snow = [600, 611, 615]
        medium_snow = [612, 616, 620]
        heavy_snow = [602, 621, 622]

        clear = [800]

        code = {
            200: "thunderstorm with light rain",
            201: "thunderstorm with rain",
            202: "thunderstorm with heavy rain",
            210: "light thunderstorm",
            211: "thunderstorm",
            212: "heavy thunderstorm",
            221: "ragged thunderstorm",
            230: "thunderstorm with light drizzle",
            231: "thunderstorm with drizzle",
            232: "thunderstorm with heavy drizzle",

            300: "light intensity drizzle",
            301: "drizzle",
            302: "heavy intensity drizzle",
            310: "light intensity drizzle rain",
            311: "drizzle rain",
            312: "heavy intensity drizzle rain",
            313: "shower rain and drizzle",
            314: "heavy shower rain and drizzle",
            321: "shower drizzle",

            500: "light rain",
            501: "moderate rain",
            502: "heavy intensity rain",
            503: "very heavy rain",
            504: "extreme rain",
            511: "freezing rain",
            520: "light intensity shower rain",
            521: "shower rain",
            522: "heavy intensity shower rain",
            531: "ragged shower rain",

            600: "light snow",
            601: "snow",
            602: "heavy snow",
            611: "sleet",
            612: "shower sleet",
            615: "light rain and snow",
            616: "rain and snow",
            620: "light shower snow",
            621: "shower snow",
            622: "heavy shower snow",

            701: "mist",
            711: "smoke",
            721: "haze",
            731: "sand, dust whirls",
            741: "fog",
            751: "sand",
            761: "dust",
            762: "volcanic ash",
            771: "squalls",
            781: "tornado",

            800: "clear sky",

            900: "tornado",
            901: "tropical storm",
            902: "hurricane",
            903: "cold",
            904: "hot",
            905: "windy",
            906: "hail",

            951: "calm",
            952: "light breeze",
            953: "gentle breeze",
            954: "moderate breeze",
            955: "fresh breeze",
            956: "strong breeze",
            957: "high wind, near gale",
            958: "gale",
            959: "severe gale",
            960: "storm",
            961: "violent storm",
            962: "hurricane"
        }

        headers = {'user-agent': "rDany/1.1 (http://www.rdany.org/rdany/; botmaster@rdany.org)"}
        par = {
            "id": 3435259,
            "APPID": "3d81c3d84f4d0c617799eb16a73449df"
        }
        url = "http://api.openweathermap.org/data/2.5/weather"
        try:
            r = requests.get(url, timeout=1, headers=headers, params=par)
        except Timeout:
            logging.error('ConnectionTimeout: {0}'.format(url))
        #print (r)

        if r.status_code == requests.codes.ok:
            response = r.json()
            #print (response)
        else:
            logging.error('HTTP Error: {0}. {1}'.format(r.status_code, r.text))
            response = {"cod": "0"}

        if response["cod"] == 200:
            #self.city_id = response['id']
            #self.latitude = response['coord']['lat']
            #self.longitude = response['coord']['lon']
            #self.weather_id = response['weather'][0]['id']
            #self.temperature = response['main']['temp'] - 273.15
            #self.wind_speed = response['wind']['speed']
            #self.clouds = response['clouds']['all']
            temp = "{0:.1f} C".format(response['main']['temp'] - 273.15)
            temp_min = "{0:.1f} C".format(response['main']['temp_min'] - 273.15)
            temp_max = "{0:.1f} C".format(response['main']['temp_max'] - 273.15)
            humidity = response['main']['humidity']
            pressure = response['main']['pressure']
            wind = response['wind']['speed']
            wind_kmh = (wind / 1000) * 60 * 60
            wind_deg = response['wind']['deg']
            if wind_deg > 0 and wind_deg < 19:
                wind_deg_name = "norte"
            elif wind_deg > 18 and wind_deg < 73:
                wind_deg_name = "noreste"
            elif wind_deg > 72 and wind_deg < 119:
                wind_deg_name = "este"
            elif wind_deg > 118 and wind_deg < 163:
                wind_deg_name = "sureste"
            elif wind_deg > 162 and wind_deg < 199:
                wind_deg_name = "sur"
            elif wind_deg > 198 and wind_deg < 253:
                wind_deg_name = "sureste"
            elif wind_deg > 252 and wind_deg < 289:
                wind_deg_name = "oeste"
            elif wind_deg > 288 and wind_deg < 343:
                wind_deg_name = "noroeste"
            elif wind_deg > 342 and wind_deg < 361:
                wind_deg_name = "norte"
            clouds = response['clouds']['all']
            weather_id = response['weather'][0]['id']

            text = "La temperatura es de {0}, {1}.".format(temp, code[weather_id])
            text = "{0}Con una humedad del {1}%,".format(text, humidity)
            text = "{0} una presion atmosferica de {1} hectopascales.".format(text, pressure)
            text = "{0} Viento del {1} de {2} kilometros por hora.".format(text, wind_deg_name, wind_kmh)
            text = "{0}\nLa maxima es de {1} y la minima de {2}.".format(text, temp_min, temp_max)
        else:
            logging.error('API Error: {0}'.format(r.text))
            text = "No pude conectarme a Openweathermap.org"
        return {"text": text }
