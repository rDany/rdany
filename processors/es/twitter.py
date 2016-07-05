import re

class processor:
    example = "Twittea Hola Mundo"
    keywords = [
        "twittea",
        "twitteá"
    ]

    @staticmethod
    def check_string(string, context):
        pidetwitter = re.search(r"\W*(twit(t)*eame|twi(t)*e(a|Ã¡))\s+(?P<buscar>.+)", string, re.IGNORECASE)
        if pidetwitter:
            message = pidetwitter.group('buscar')
            return {"actuator": "twitter", "parameters": {"message": message}, "confidence": 0.8, "context": {}}
