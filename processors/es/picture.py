import re
import time
import logging
import requests

from urllib.parse import urlencode

class processor:
    example = "Busca una foto de la Luna"
    keywords = [
        "muestrame",
        "mostrame",
        "busca",
        "buscá",
        "una",
        "la",
        "foto",
        "imágen",
        "imagen",
        "imágenes",
        "de",
        "del",
        "un",
        "perdon",
        "perdón",
        "perdona",
        "disculpa",
        "quise",
        "quiero",
        "decir"
    ]

    @staticmethod
    def check_string(string, context):
        timestamp = int(time.time())
        confidence = 0.7
        logger = logging.getLogger("picture")

        use_last_search = False

        pideimagen = re.search(r"\W*(m(ue|o)strame|busca|buscá|buscame)(\s+(una|la))?\s+(foto|im(a|á)gen|im(a|á)genes)*\s+(de|del|de\s+(la|un|el|una))\s+(?P<buscar>.+)", string, re.IGNORECASE)
        if not pideimagen:
            pideimagen = re.search(r"\W*(m(ue|o)strame)(\s+(el|la|un|una|unas|los|las))?\s+(?P<buscar>.+)", string, re.IGNORECASE)
        if not pideimagen and context["general.last_processor"] == "picture":
            pideimagen = re.search(r"\W*(y|o)\s+(de\s+)?((el|la|una|un|las|los)\s+)?(?P<buscar>.+?)\s*\?*$", string, re.IGNORECASE)
            confidence = 0.5
        if not pideimagen and context["general.last_processor"] == "picture" and timestamp - context["general.last_time"] < 20:
            pideimagen = re.search(r"\W*((perd(o|ó)n|perdona|disculpa)\s+)?((quise|quiero)\s+(poner|decir)\s+)?(?P<buscar>.+?)\s*\?*$", string, re.IGNORECASE)
            confidence = 0.3
        if not pideimagen:
            pideimagen = re.search(r"\W*((una|la)\s+)?(foto|im(a|á)gen|im(a|á)genes)\s*\?*$", string, re.IGNORECASE)
            use_last_search = True
            confidence = 0.6

        text = None
        if pideimagen:
            if not use_last_search:
                search = pideimagen.group('buscar')
            else:
                search = context["general.last_search"]
            #params = urlencode( {"q": search, "ia": "images", "iax": "1"} )
            #text = "http://duckduckgo.com/?{0}".format(params)

            headers = {'user-agent': "rDany/1.1 (http://www.rdany.org/rdany/; botmaster@rdany.org)"}
            error = False
            try:
                data = {
                    "sort": "relevance",
                    "parse_tags": "1",
                    "content_type": "7",
                    "extras": "can_comment,count_comments,count_faves,description,isfavorite,license,media,needs_interstitial,owner_name,path_alias,realname,rotation,url_c,url_l,url_m,url_n,url_q,url_s,url_sq,url_t,url_z,is_marketplace_licensable",
                    "per_page": "25",
                    "page": "1",
                    "lang": "es-ES",
                    "text": search,
                    "viewerNSID": "",
                    "method": "flickr.photos.search",
                    "csrf": "",
                    "api_key": "a9547a639d2a98d40739ed60a2aa62d8",
                    "format": "json",
                    "hermes": "1",
                    "hermesClient": "1",
                    "reqId": "531e7dd7",
                    "nojsoncallback": "1"
                }
                r = requests.get("https://api.flickr.com/services/rest", params=data, timeout=20, headers=headers)
            except requests.exceptions.ConnectionError:
                text = "Connection Error"
                logger.error("Connection Error")
                error = True
            except requests.exceptions.Timeout:
                text = "Connection Timeout"
                logger.error("Connection Timeout")
                error = True
            r_json = r.json()

            if r_json["stat"] != "ok":
                logger.error("Bad Stat {0}".format(r_json))
                error = True

            if not error:
                photo = r_json["photos"]["photo"][0]
                #total = r_json["total"]

                text = "https://www.flickr.com/photos/{0}/{1}/".format(photo["owner"], photo["id"])

                #photo["title"]
                #photo["description"]["_content"]
                #photo["safe"]
            else:
                text = "No pude conectarme a Flickr :("

            new_context = {
                "picture.last_search": search
            }
            return {"text": text, "confidence": confidence, "context": new_context}
