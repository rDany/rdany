import re
import datetime

class processor:
    example = "¿Qué hora es?"
    keywords = [
        "qué",
        "que",
        "hora",
        "es"
    ]

    @staticmethod
    def check_string(string, context):
        pidehora = re.search(r"hora", string, re.IGNORECASE)
        text = None
        if pidehora:
            now = datetime.datetime.now()
            if now.hour == 1:
                text = "Es la {0:02d}:{1:02d}".format(now.hour, now.minute)
            else:
                text = "Son las {0:02d}:{1:02d}".format(now.hour, now.minute)

            return {"text": text, "confidence": 0.5, "context": {}}
