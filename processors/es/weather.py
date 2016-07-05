import re

class processor:
    example = "¿Cómo está el clima?"
    keywords = ["clima"]

    @staticmethod
    def check_string(string, context):
        pideweather = re.search(r"\W*clima", string, re.IGNORECASE)
        if pideweather:
            return {"actuator": "weather", "parameters": {}, "confidence": 0.4, "context": {}}
