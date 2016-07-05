from urllib.parse import urlencode

class actuator:

    @staticmethod
    def generate_string(parameters, context):
        message = parameters["message"]
        params = urlencode( {"source": "rdany", "text": message} )
        text = "https://twitter.com/intent/tweet?{0}".format(params)

        return {"text": text }
