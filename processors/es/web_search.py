import re

from urllib.parse import urlencode

class processor:
    example = "Busca informacion sobre energía eólica"
    keywords = [
        "busca",
        "buscame",
        "buscá"
    ]

    @staticmethod
    def check_string(string, context):
        pidebuscador = re.search(r"\W*(busc(a|á)|buscame)\s+(?P<buscar>.+)", string, re.IGNORECASE)
        text = None
        if pidebuscador:
            params = urlencode( {"q": pidebuscador.group('buscar')} )
            text = "http://duckduckgo.com/?{0}".format(params)

            new_context = {"wiki.last_search": pidebuscador.group("buscar")}
            return {"text": text, "confidence": 0.5, "context": new_context}
