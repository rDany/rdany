import re
import requests

from urllib.parse import urlencode

class processor:
    example = "Mostrame un video de un avistamiento de ballenas"
    keywords = [
        "mostrame",
        "muestrame",
        "buscá",
        "busca",
        "un",
        "video",
        "vídeo"
    ]

    @staticmethod
    def check_string(string, context):
        use_last_search = False
        pideyoutube = re.search(r"\W*(m(ue|o)strame|busca|buscá)(\s+(un|el))?\s+(v(i|í­)deo|videos|videoclip)\s+(acerca\s+de|sobre|de|del|de\s+(la|las))\s+(?P<buscar>.+)", string, re.IGNORECASE)
        if not pideyoutube and context["general.last_processor"] == "video":
            pideyoutube = re.search(r"\W*(y|o)\s+(de\s+)?((el|la|una|un|las|los)\s+)?(?P<buscar>.+?)\s*\?*$", string, re.IGNORECASE)
            confidence = 0.5
        if not pideyoutube:
            pideyoutube = re.search(r"\W*((un|el)\s+)?(v(i|í)deo|videos|videoclip)\s*\?*$", string, re.IGNORECASE)
            use_last_search = True
            confidence = 0.6

        text = None
        if pideyoutube:
            #params = urlencode( {"q": pideyoutube.group('buscar'), "ia": "videos", "iax": "1"} )
            #text = "https://duckduckgo.com/?{0}".format(params)

            if not use_last_search:
                search = pideyoutube.group('buscar')
            else:
                search = context["general.last_search"]

            headers = {'user-agent': "rDany/1.1 (http://www.rdany.org/rdany/; botmaster@rdany.org)"}
            try:
                data = {
                    "search_query": search,
                    "spf": "navigate",
                }
                r = requests.get("https://www.youtube.com/results", params=data, timeout=20, headers=headers)
            except requests.exceptions.ConnectionError:
                text = "Connection Error"
                return
            except requests.exceptions.Timeout:
                text = "Connection Timeout"
                return
            r_json = r.json()

            yt_content = r_json[1]["body"]["content"]
            revideo = re.search(r"\"(?P<buscar>\/watch\?v=\w+?)\"", yt_content)
            if revideo:
                text = "http://www.youtube.com{0}".format(revideo.group("buscar"))

            new_context = {"video.last_search": search}
            return {"text": text, "confidence": 0.8, "context": new_context}
