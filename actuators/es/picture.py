import logging
import datetime
import requests

class actuator:

    @staticmethod
    def generate_string(parameters, context):
        logger = logging.getLogger("picture actuator")

        search = parameters["search"]
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
        return {"text": text }
