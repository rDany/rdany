import re
import logging
import datetime
import requests

class actuator:

    @staticmethod
    def generate_string(parameters, context):
        logger = logging.getLogger("currency_converter actuator")
        error_text = "No pude conectarme a Google Finance :("

        #search = parameters["search"]

        headers = {'user-agent': "rDany/1.1 (http://www.rdany.org/rdany/; botmaster@rdany.org)"}
        error = False

        try:
            data = {
                "a": 1,
                "from": "AED",
                "to": "ANG"
            }
            r = requests.get("https://www.google.com/finance/converter", params=data, timeout=20, headers=headers)
        except requests.exceptions.ConnectionError:
            text = "Connection Error"
            logger.error("Connection Error")
            error = True
        except requests.exceptions.Timeout:
            text = "Connection Timeout"
            logger.error("Connection Timeout")
            error = True

        if error:
            return {"text": error_text }

        value = re.search(r"<span\sclass=bld>(?P<value>.+?)\s", r.text)
        if not value:
            return {"text": error_text }

        if not error:
            text = value.group("value")
        else:
            return {"text": error_text }
        return {"text": text }
