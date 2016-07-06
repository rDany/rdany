import re
import logging
import datetime
import requests

class actuator:

    @staticmethod
    def generate_string(parameters, context):
        logger = logging.getLogger("picture actuator")
        error_text = "No pude conectarme a Flickr :("

        search = parameters["search"]
        #params = urlencode( {"q": search, "ia": "images", "iax": "1"} )
        #text = "http://duckduckgo.com/?{0}".format(params)

        headers = {'user-agent': "rDany/1.1 (http://www.rdany.org/rdany/; botmaster@rdany.org)"}
        error = False

        try:
            r = requests.get("https://www.flickr.com", timeout=20, headers=headers)
            #root.YUI_config.flickr.api.site_key = "78cb5f7b2704fe3eab86f416fcda2860";
        except requests.exceptions.ConnectionError:
            text = "Connection Error"
            logger.error("Connection Error")
            error = True
        except requests.exceptions.Timeout:
            text = "Connection Timeout"
            logger.error("Connection Timeout")
            error = True

        if error:
            return {"text": error_text }

        reapi = re.search(r"api\.site_key\s=\s\"(?P<api>.+?)\"", r.text)
        if not reapi:
            return {"text": error_text }

        logger.info("Detected APIKEY {0}".format(reapi.group("api")))

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
                "api_key": reapi.group("api"),
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
            return {"text": error_text }
        return {"text": text }
