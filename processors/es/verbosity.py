import re

class processor:
    example = "Mostrame mas info"
    keywords = ["mostrame", "muestrame", "info"]

    @staticmethod
    def check_string(string, context):
        confidence = 1.0
        askverbosity = re.search(r"\W*m(o|ue)strame\s+mas\s+info", string, re.IGNORECASE)
        text = None
        if askverbosity:
            text = "Entendido."
            new_context = {
                "shared.verbosity": True
            }
            return {"text": text, "confidence": confidence, "context": new_context}
