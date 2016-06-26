import re

from urllib.parse import urlencode

class processor:
    example = "Twittea Hola Mundo"
    keywords = [
        "twittea",
        "twitteá"
    ]

    @staticmethod
    def check_string(string, context):
        pidetwitter = re.search(r"\W*(twit(t)*eame|twi(t)*e(a|Ã¡))\s+(?P<buscar>.+)", string, re.IGNORECASE)
        text = None
        if pidetwitter:
            params = urlencode( {"source": "rdany", "text": pidetwitter.group('buscar')} )
            text = "https://twitter.com/intent/tweet?{0}".format(params)

            return {"text": text, "confidence": 0.8, "context": {}}
