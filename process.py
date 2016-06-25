import time
import logging

logging.verbosity=0

class process:
    def __init__(self, useragent):
        self.useragent = useragent
        self.processor_list = [
            "date",
            "help",
            "picture",
            "relative_date",
            "stats",
            "time",
            "twitter",
            "verbosity",
            "video",
            "weather",
            "web_search",
            "wiki"
        ]

    def get_examples (self):
        text = ""
        for pr in self.processor_list:
            module_name = "processors.es.{0}".format(pr)
            processor = None
            try:
                module_loader = __import__(
                    module_name, globals(), locals(), ['processor'], 0)
                processor = module_loader.processor
            except ImportError as e:
                logging.error(' loading module {0}, {1}'.format(module_name, e))

            if processor:
                text = "{0}\n{1}".format(text, processor.example)
        return text

    def process_question (self, question, context):
        text = None
        new_context = None
        results = {}

        for pr in self.processor_list:
            module_name = "processors.es.{0}".format(pr)
            processor = None
            try:
                module_loader = __import__(
                    module_name, globals(), locals(), ['processor'], 0)
                processor = module_loader.processor
            except ImportError as e:
                logging.error(' loading module {0}, {1}'.format(module_name, e))
            answer = processor.check_string(question, context)
            if answer:
                results[pr] = answer

        last_confidence = 0
        for result in results:
            logging.info(results[result])
            if results[result]["confidence"] > last_confidence:
                last_confidence = results[result]["confidence"]
                text = results[result]["text"]
                #text = "{0}\n{1}".format(text, answer["text"])
                new_context = {}

                for nc in results[result]["context"]:
                    if not nc.startswith("general."):
                        new_context[nc] = results[result]["context"][nc]

                new_context["general.last_time"] = int(time.time())
                new_context["general.last_processor"] = result
                new_context["general.last_confidence"] = results[result]["confidence"]
                if "{0}.last_search".format(result) in new_context:
                    new_context["general.last_search"] = new_context["{0}.last_search".format(result)]
        return text, new_context
