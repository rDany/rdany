import re
import logging
import requests

class processor:
    example = "¿Quién fue Nicola Tesla?"
    keywords = [
        "quién",
        "qué",
        "es",
        "fue",
        "era",
        "será",
        "sera"
    ]

    @staticmethod
    def check_string(string, context):

        pidewiki = re.search(r"\W*qu(e|é|ien|ién)\s+(es|fue|era|sera|será)\s*(el|la|un|una)*\s+(?P<buscar>.+?)\s*\?*$", string, re.IGNORECASE)
        if not pidewiki:
          pidewiki = re.search(r"\W*conoc(e|é)s\s*(el|la|a)*\s+(?P<buscar>.+?)\s*\?*$", string, re.IGNORECASE)
        if not pidewiki:
          pidewiki = re.search(r"\W*c(o|ó)mo\s*funciona\s*(el|la|un|una)*\s+(?P<buscar>.+?)\s*\?*$", string, re.IGNORECASE)
        if not pidewiki:
          pidewiki = re.search(r"\W*donde\s*est(a|á)\s*(el|la)*\s+(?P<buscar>.+?)\s*\?*$", string, re.IGNORECASE)

        if not pidewiki and context["general.last_processor"] == "wiki":
          pidewiki = re.search(r"\W*y\s+((el|la|una|un|las|los)\s+)?(?P<buscar>.+?)\s*\?*$", string, re.IGNORECASE)

        if pidewiki:
            search = pidewiki.group("buscar")
            new_context = {"wiki.last_search": search}
            return {"actuator": "wiki", "parameters": {"search": search}, "confidence": 0.7, "context": new_context}
