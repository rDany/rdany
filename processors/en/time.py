import re
import datetime

class processor:
    example = "What time is it?"
    keywords = [
        "what",
        "time",
    ]

    @staticmethod
    def check_string(string, context):
        pidehora = re.search(r"what\s+time", string, re.IGNORECASE)
        text = None
        if pidehora:
            now = datetime.datetime.now()
            text = "It is {0:02d}:{1:02d}".format(now.hour, now.minute)

            return {"text": text, "confidence": 0.5, "context": {}}
