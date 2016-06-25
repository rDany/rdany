import re

class processor:
    example = "¿Qué puedo preguntarte?"
    keywords = ["qué", "que", "puedo", "preguntarte", "puedes", "sabés", "podés", "hacer"]

    @staticmethod
    def check_string(string, context):
        confidence = 1.0
        pidehelp = re.search(r"\W*qu(é|e)\s+puedo\s+preguntarte", string, re.IGNORECASE)
        if not pidehelp:
            pidehelp = re.search(r"\W*qu(é|e)\s+(puedes|sabes|pod(é|e)s)\s+hacer", string, re.IGNORECASE)
            confidence = 0.7

        text = None
        if pidehelp:

            text = "Algunas cosas que podés preguntarme:{0}".format(\
                context["general.processors_examples"]
            )
            return {"text": text, "confidence": confidence, "context": {}}
