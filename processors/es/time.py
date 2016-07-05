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
        if pidehora:
            return {"actuator": "time", "parameters": {}, "confidence": 0.5, "context": {}}
