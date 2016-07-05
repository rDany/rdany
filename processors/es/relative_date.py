import re

class processor:
    example = "¿Qué día fue ayer?"
    keywords = [
        "fecha",
        "día",
        "dia"
    ]

    @staticmethod
    def check_string(string, context):

        pidefecha_relativa = re.search(r"(qu(e|é))\s+(fecha|d(i|í)a)\s+(es|ser(a|á)|va\sa\sser|fue)\s+(?P<buscar>.+)", string, re.IGNORECASE)

        if pidefecha_relativa:
            parameter = pidefecha_relativa.group('buscar')
            before_yesterday = re.search(r"\W*antes\s*de\s*ayer", parameter, re.IGNORECASE)
            yesterday = re.search(r"\W*ayer", parameter, re.IGNORECASE)
            tomorrow = re.search(r"\W*mañana", parameter, re.IGNORECASE)
            day_before = re.search(r"\W*pasado\s+mañana", parameter, re.IGNORECASE)

            parameters = {
                "before_yesterday": before_yesterday,
                "yesterday": yesterday,
                "tomorrow": tomorrow,
                "day_before": day_before
            }

            return {"actuator": "relative_date", "parameters": parameters, "confidence": 0.7, "context": {}}
