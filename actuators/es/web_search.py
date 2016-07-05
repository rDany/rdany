from urllib.parse import urlencode

class actuator:

    @staticmethod
    def generate_string(parameters, context):
        params = urlencode( {"q": parameters["search"]} )
        text = "http://duckduckgo.com/?{0}".format(params)

        return {"text": text }
