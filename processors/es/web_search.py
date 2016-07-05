import re

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
        if pidebuscador:
            search = pidebuscador.group('buscar')
            new_context = {"wiki.last_search": pidebuscador.group("buscar")}
            return {"actuator": "web_search", "parameters": {"search": search}, "confidence": 0.5, "context": new_context}
