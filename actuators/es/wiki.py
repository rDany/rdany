import logging
import requests

class actuator:

    @staticmethod
    def generate_string(parameters, context):
        logger = logging.getLogger("wiki actuator")

        headers = {'user-agent': "rDany/1.1 (http://www.rdany.org/rdany/; botmaster@rdany.org)"}
        try:
            data = {
                "format": "json",
                "action": "opensearch",
                "search": parameters["search"]
            }
            r = requests.get("http://es.wikipedia.org/w/api.php", params=data, timeout=20, headers=headers)
        except requests.exceptions.ConnectionError:
            text = "Connection Error"
            #print (text)
            return
        except requests.exceptions.Timeout:
            text = "Connection Timeout"
            #print (text)
            return
        rres = r.json()
        if len(rres[1]) > 0:
            rres = rres[1][0]
            try:
                data = {
                    "format": "json",
                    "action": "query",
                    "redirects": "true",
                    "prop": "extracts",
                    "exintro": "true",
                    "explaintext": "true",
                    "titles": rres
                }
                r = requests.get("http://es.wikipedia.org/w/api.php", params=data, timeout=20, headers=headers)
            except requests.exceptions.ConnectionError:
                text = "Connection Error"
                #print (text)
                return
            except requests.exceptions.Timeout:
                text = "Connection Timeout"
                #print (text)
                return

            resf = ""
            for pag in r.json()['query']['pages']:
                resf = "{0}{1}".format(resf, r.json()['query']['pages'][pag]['extract'])

            if len(resf)<200:
              resf = "La información es insuficiente. Por ejemplo si escribió \"¿Quién es Daneel?\" pruebe con \"¿Quién es Daneel Olivaw?\"." ;

            if r.status_code == requests.codes.ok:
                text = "\"{0}\" según Wikipedia: {1}".format(parameters["search"], resf) ;
            else:
                text = "Error"
        else:
            text = "No pude encontrar información acerca de \"{0}\" en Wikipeda".format(parameters["search"])
        return {"text": text }
