import time
import logging

class process:
    def __init__(self, useragent):
        self.logger = logging.getLogger("process")
        self.useragent = useragent
        # Processors
        es_processors = [
            "date",
            #"hello_world",
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
        en_processors = [
            "time"
        ]
        self.processor_list = {
            "es": es_processors,
            "en": en_processors
        }
        self.processor_modules = {}
        self.load_processors()

        # Actuators
        es_actuators = [
            "date",
            #"hello_world",
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
        en_actuators = [
            "time"
        ]
        self.actuators_list = {
            "es": es_actuators,
            "en": en_actuators
        }
        self.actuator_modules = {}
        self.load_actuators()
        #self.logger.setLevel(logging.INFO)

    def load_processors (self):
        for lan in self.processor_list:
            self.processor_modules[lan] = {}
            for pr in self.processor_list[lan]:
                module_name = "processors.{0}.{1}".format(lan, pr)
                processor = None
                try:
                    module_loader = __import__(
                        module_name, globals(), locals(), ['processor'], 0)
                    self.processor_modules[lan][pr] = module_loader.processor
                except ImportError as e:
                    self.logger.error('loading module {0}, {1}'.format(module_name, e))

    def load_actuators (self):
        for lan in self.actuators_list:
            self.actuator_modules[lan] = {}
            for pr in self.actuators_list[lan]:
                module_name = "actuators.{0}.{1}".format(lan, pr)
                actuator = None
                try:
                    module_loader = __import__(
                        module_name, globals(), locals(), ['actuator'], 0)
                    self.actuator_modules[lan][pr] = module_loader.actuator
                except ImportError as e:
                    self.logger.error('loading module {0}, {1}'.format(module_name, e))

    def get_examples (self):
        examples = {}
        for lan in self.processor_list:
            text = ""
            for processor_name in self.processor_modules[lan]:
                processor = self.processor_modules[lan][processor_name]
                text = "{0}\n{1}".format(text, processor.example)
            examples[lan] = text
        return examples

    def process_question (self, question, context):
        text = None
        new_context = None
        results = {}

        # detect language
        keywords = {}
        for lan in self.processor_list:
            for processor_name in self.processor_modules[lan]:
                processor = self.processor_modules[lan][processor_name]
                if not lan in keywords:
                    keywords[lan] = []
                keywords[lan] += processor.keywords
            # Removing duplicated
            keywords[lan] = list(set(keywords[lan]))

        language = "es"
        for lan in keywords:
            lang_match = False
            for keyword in keywords[lan]:
                if question.find(keyword) > -1:
                    lang_match = True
            if lang_match:
                language = lan
                self.logger.info('language match: {0}'.format(lan))
                break

        #for lan in self.processor_list:
        for processor_name in self.processor_modules[language]:
            processor = self.processor_modules[language][processor_name]
            answer = processor.check_string(question, context)
            if answer:
                results[processor_name] = answer

        last_confidence = 0
        for result in results:
            self.logger.info(results[result])
            if results[result]["confidence"] > last_confidence:
                last_confidence = results[result]["confidence"]
                #text = results[result]["text"]
                actuator_name = results[result]["actuator"]
                actuator = self.actuator_modules[language][actuator_name]
                actuator_result = actuator.generate_string(results[result]["parameters"], context)
                text = actuator_result["text"]
                #text = "{0}\n{1}".format(text, answer["text"])
                new_context = {}

                for nc in results[result]["context"]:
                    if not nc.startswith("general."):
                        new_context[nc] = results[result]["context"][nc]

                new_context["general.last_time"] = int(time.time())
                new_context["general.last_processor"] = result
                new_context["general.last_language"] = language
                new_context["general.last_confidence"] = results[result]["confidence"]
                if "{0}.last_search".format(result) in new_context:
                    new_context["general.last_search"] = new_context["{0}.last_search".format(result)]
        return text, new_context
