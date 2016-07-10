import re

class processor:
    example = "Cuentame un cuento"
    keywords = [
        "cuentame",
        "contame"
    ]

    @staticmethod
    def check_string(string, context):
        askstory = re.search(r"\W*(cu(e|é)ntame|cont(a|á)me)\s+un(a)?\s+(cuento|historia)", string, re.IGNORECASE)
        if not askstory:
            askstory = re.search(r"\W*(cu(e|é)ntame|cont(a|á)me)\s+(un(a)|el)?\s+(cuento|historia)\s+(de|del|acerca\s+de)\s+(?P<story_name>.+)", string, re.IGNORECASE)
        if askstory:
            try:
                story_name = askstory.group('story_name')
            except:
                story_name = None
            return {"actuator": "story", "parameters": {"story_name": story_name}, "confidence": 0.9, "context": {}}
