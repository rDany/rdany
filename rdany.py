import os
import time
import json
import random
import logging
import threading

from telegram import telegram
from process import process

from config import Config
from common_data import CommonData

class rdany:

    def __init__(self):
        self.useragent = CommonData.useragent
        self.processors = process(self.useragent)

        self.telegram_conection = telegram(Config.bot_username, Config.bot_token, self.useragent)
        self.end = False
        self.context = {
            "general.last_processor": "",
            "general.last_confidence": 0,
            "general.last_time": 0,
            "general.last_search": "",
            "general.last_language": "",
            "general.total_questions": 0,
            "general.succesful_answers": 0,
            "general.processors_examples": self.processors.get_examples(),
            "shared.verbosity": False
        }

        # Logging
        logging.basicConfig(filename="rdany.log", level=logging.INFO)
        self.logger = logging.getLogger()
        self.logger.info("Initialized")

    def get_messages(self):
        while not self.end:
            self.telegram_conection.open_session()
            r = self.telegram_conection.get_update()
            #print (r.json())

            r_json = r.json()

            for result in r_json["result"]:
                timestamp = int(time.time())
                start_time = timestamp + random.randrange(60)
                expiration_time = start_time + 5000
                data = {
                    "message": result["message"]["text"],
                    "chat": result["message"]["chat"]["id"],
                    "start_time": start_time,
                    "expiration_time": expiration_time,
                    "done": False,
                    "processing": False
                }
                savefile = os.path.join("queue", "{0}_0.json".format(timestamp))
                f_count = 0
                while os.path.isfile(savefile):
                    f_count += 1
                    savefile = os.path.join("queue", "{0}_{1}.json".format(timestamp, f_count))
                with open(savefile, 'w', encoding='utf-8') as data_file:
                        json.dump(data, data_file, sort_keys=True, indent=4, separators=(',', ': '))

            self.telegram_conection.close_session()

    def process_question (self, data, ff):
        self.context["general.total_questions"] += 1
        answer, new_context = self.processors.process_question(data["message"], self.context)

        if new_context:
            self.context.update(new_context)
            self.context["general.succesful_answers"] += 1
            if self.context["shared.verbosity"]:
                answer = "{0} {1}\n{2}".format(self.context["general.last_processor"], self.context["general.last_confidence"], answer)
        if not answer:
            answer = "No entendi"

        msg = {
            'chat_id': data["chat"],
            'text': answer,
        }
        r = self.telegram_conection.send_to_bot('sendMessage', data = msg)
        data["processing"] = False
        data["done"] = True
        savefile = os.path.join("queue", ff)
        with open(savefile, 'w', encoding='utf-8') as data_file:
                json.dump(data, data_file, sort_keys=True, indent=4, separators=(',', ': '))

    def send_messages(self):
        while not self.end:
            f = []
            onlyfiles = [f for f in os.listdir("queue") if os.path.isfile(os.path.join("queue", f))]
            onlyfiles.sort()
            #print (onlyfiles)
            for ff in onlyfiles:
                timestamp = int(time.time())
                with open(os.path.join("queue", ff), encoding='utf-8') as data_file:
                    try:
                        data = json.load(data_file)
                    except:
                        continue
                if not data["done"] and not data["processing"]:
                    if 1 or timestamp > data["start_time"]:
                        #print (data["message"])
                        data["processing"] = True
                        savefile = os.path.join("queue", ff)
                        with open(savefile, 'w', encoding='utf-8') as data_file:
                                json.dump(data, data_file, sort_keys=True, indent=4, separators=(',', ': '))
                        #process_question(data, ff)
                        t = threading.Thread(target=self.process_question, args=(data, ff))
                        t.start()
                    else:
                        break

    def start(self, commandline=True):
        ## Telegram connection
        if not commandline:
            t = threading.Thread(target=self.get_messages)
            t.start()
            ts = threading.Thread(target=self.send_messages)
            ts.start()
            input("Enter para terminar ")
            self.end = True
            print ("Terminando")
            return

        ## Command Line connection

        print ("Enter para terminar")
        while 1:
            user_input = input("> ")
            if user_input == "":
                break
            self.context["general.total_questions"] += 1
            answer, new_context = self.processors.process_question(user_input, self.context)
            if new_context:
                self.context.update(new_context)
                self.context["general.succesful_answers"] += 1
                if self.context["shared.verbosity"]:
                    answer = "{0} {1}\n{2}".format(self.context["general.last_processor"], self.context["general.last_confidence"], answer)
            if not answer:
                answer = "No entendi"
            print (answer)
            print ()


rd = rdany()
rd.start(Config.command_line)
