import re
import time
import logging

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
        logger = logging.getLogger("picture processor")

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

        if pideimagen:

            if not use_last_search:
                search = pideimagen.group('buscar')
            else:
                search = context["general.last_search"]

            new_context = {
                "picture.last_search": search
            }
            return {"actuator": "picture", "parameters": {"search": search}, "confidence": confidence, "context": new_context}
