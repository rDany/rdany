import re
import logging
import requests

class processor:
    example = "¿Quién fue Nicola Tesla?"
    keywords = [
        "quién",
        "qué",
        "es",
        "fue",
        "era",
        "será",
        "sera"
    ]

    @staticmethod
    def check_string(string, context):

        pidewiki = re.search(r"\W*qu(e|é|ien|ién)\s+(es|fue|era|sera|será)\s*(el|la|un|una)*\s+(?P<buscar>.+?)\s*\?*$", string, re.IGNORECASE)
        if not pidewiki:
          pidewiki = re.search(r"\W*conoc(e|é)s\s*(el|la|a)*\s+(?P<buscar>.+?)\s*\?*$", string, re.IGNORECASE)
        if not pidewiki:
          pidewiki = re.search(r"\W*c(o|ó)mo\s*funciona\s*(el|la|un|una)*\s+(?P<buscar>.+?)\s*\?*$", string, re.IGNORECASE)
        if not pidewiki:
          pidewiki = re.search(r"\W*donde\s*est(a|á)\s*(el|la)*\s+(?P<buscar>.+?)\s*\?*$", string, re.IGNORECASE)

        if not pidewiki and context["general.last_processor"] == "wiki":
          pidewiki = re.search(r"\W*y\s+((el|la|una|un|las|los)\s+)?(?P<buscar>.+?)\s*\?*$", string, re.IGNORECASE)

        text = None
        if pidewiki:
            headers = {'user-agent': "rDany/1.1 (http://www.rdany.org/rdany/; botmaster@rdany.org)"}
            try:
                data = {
                    "format": "json",
                    "action": "opensearch",
                    "search": pidewiki.group("buscar")
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
                    text = "\"{0}\" según Wikipedia: {1}".format(pidewiki.group("buscar"), resf) ;
                else:
                    text = "Error"
            else:
                text = "No pude encontrar información acerca de \"{0}\" en Wikipeda".format(pidewiki.group("buscar"))

            new_context = {"wiki.last_search": pidewiki.group("buscar")}
            return {"text": text, "confidence": 0.7, "context": new_context}
