import re
import logging
import requests

class actuator:

    @staticmethod
    def generate_string(parameters, context):
        logger = logging.getLogger("video actuator")

        search = parameters["search"]
        headers = {'user-agent': "rDany/1.1 (http://www.rdany.org/rdany/; botmaster@rdany.org)"}
        try:
            data = {
                "search_query": search,
                "spf": "navigate",
            }
            r = requests.get("https://www.youtube.com/results", params=data, timeout=20, headers=headers)
        except requests.exceptions.ConnectionError:
            text = "Connection Error"
            return
        except requests.exceptions.Timeout:
            text = "Connection Timeout"
            return
        r_json = r.json()

        yt_content = r_json[1]["body"]["content"]
        revideo = re.search(r"\"(?P<buscar>\/watch\?v=\w+?)\"", yt_content)
        if revideo:
            text = "http://www.youtube.com{0}".format(revideo.group("buscar"))
        return {"text": text }
