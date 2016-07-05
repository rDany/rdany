import re

class processor:
    example = "¿Qué día es?"
    keywords = ["qué", "que", "día", "día", "fecha", "es"]

    @staticmethod
    def check_string(string, context):
        confidence = 0
        pidefecha = re.search(r"(fecha|qu(e|é)\s+d(i|á­)a\s+es)", string, re.IGNORECASE)
        confidence = 0.7
        if not pidefecha:
            pidefecha = re.search(r"cu(a|á)l\s+es\s+(la|el)\s+(fecha|d(i|í)a\s+de\s+\s+hoy)", string, re.IGNORECASE)
            confidence = 1
        if pidefecha:
            return {"actuator": "date", "parameters": {}, "confidence": confidence, "context": {} }

        return None
