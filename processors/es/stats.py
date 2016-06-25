import re
import time

from urllib.parse import urlencode

class processor:
    example = "¿Cuanto hablamos?"

    @staticmethod
    def check_string(string, context):
        timestamp = int(time.time())
        confidence = 1.0

        pidestats = re.search(r"\W*cuanto\s+hablamos", string, re.IGNORECASE)

        text = None
        if pidestats:
            if context["general.total_questions"] == 1:
                total_questions = "{0} vez".format(context["general.total_questions"])
            else:
                total_questions = "{0} veces".format(context["general.total_questions"])

            if context["general.succesful_answers"] == 1:
                succesful_answers = "{0} vez".format(context["general.succesful_answers"])
            else:
                succesful_answers = "{0} veces".format(context["general.succesful_answers"])

            text = "Tu última busqueda fue: \"{0}\". Me escribiste {1} y yo respondí {2}.".format(\
                context["general.last_search"], \
                total_questions, \
                succesful_answers
            )
            return {"text": text, "confidence": confidence, "context": {}}
