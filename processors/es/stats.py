import re
import time

from urllib.parse import urlencode

class processor:
    example = "¿Cuanto hablamos?"
    keywords = [
        "cuanto",
        "hablamos"
    ]

    @staticmethod
    def check_string(string, context):
        timestamp = int(time.time())
        confidence = 1.0

        pidestats = re.search(r"\W*cuanto\s+hablamos", string, re.IGNORECASE)

        if pidestats:

            return {"actuator": "stats", "parameters": {}, "confidence": confidence, "context": {}}
