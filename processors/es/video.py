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
            new_context = {"video.last_search": search}
            return {"actuator": "video", "parameters": {"search": search}, "confidence": 0.8, "context": new_context}
