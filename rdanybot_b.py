import os
import json
import time
import requests
from config import Config


class bot:
    bot_username = Config.bot_username
    bot_token = Config.bot_token
    admin_id = Config.admin_id

    chats = {}

    def __init__ (self):
        print ("Init")
        self.savefile = "bot_data.json"
        self.bot_data = {
            "last_update": 0
        }

        scriptfile = "script.json"

        if not os.path.exists(scriptfile):
            self.script = {}
            print ("Error: No Script")
        else:
            with open(scriptfile) as data_file:
                self.script = json.load(data_file)

    #### Telegram API ####

    def send_to_bot(self, access_point, data=None):
        try:
            r = requests.get('https://api.telegram.org/bot{0}/{1}'.format(self.bot_token, access_point), data=data, timeout=40)
        except requests.exceptions.ConnectionError:
            print ("Connection Error")
            return None
        except requests.exceptions.Timeout:
            print ("Connection Timeout")
            return None
        return r

    def send_msg(self, msgs, chat_id, keyboard=None, action=False):
        count = 0
        for msg in msgs:
            count +=1
            if action:
                data = {
                    'chat_id': chat_id,
                    'action': 'typing'
                }
                r = self.send_to_bot('sendChatAction', data = data)
            data = {
                'chat_id': chat_id,
                'text': msg,
            }
            if keyboard and count == len(msgs):
                data["reply_markup"] = json.dumps(keyboard)
            print (data)
            r = self.send_to_bot('sendMessage', data = data)

    #### ####

    def get_bot_data(self):
        if not os.path.exists(self.savefile):
            return
        else:
            with open(self.savefile) as data_file:
                self.bot_data = json.load(data_file)

    def set_bot_data(self):
        with open(self.savefile, 'w') as data_file:
            json.dump(self.bot_data, data_file, sort_keys=True, indent=4, separators=(',', ': '))

    def get_last_update(self):
        return self.bot_data["last_update"]

    def set_last_update(self, update_id):
        self.bot_data["last_update"] = update_id
        self.set_bot_data()

    def get_chat_data(self, chat_id):
        chatdatafile = os.path.join("chats", "{0}.json".format(chat_id))
        if not os.path.exists(chatdatafile):
            chat_data = {
                "chat_lenght": 0,
                "last_message": "",
                "last_time": 0,
                "language": "en",
                "history": []
            }
        else:
            with open(chatdatafile) as data_file:
                chat_data = json.load(data_file)
            if not "language" in chat_data:
                chat_data["language"] = "en"
        return chat_data

    def set_chat_data(self, chat_data, chat_id):
        chatdatafile = os.path.join("chats", "{0}.json".format(chat_id))
        with open(chatdatafile, 'w') as data_file:
            json.dump(chat_data, data_file, sort_keys=True, indent=4, separators=(',', ': '))

    def get_language(self, dictionary, language):
        if language in dictionary:
            return dictionary[language]
        elif "en" in dictionary:
            return dictionary["en"]
        else:
            for key in dictionary:
                return dictionary[key]

        return ".3dfsd.cv..corrupteddatabase..78"


    def bot_loop(self):
        while 1:
            last_update = self.get_last_update()
            if last_update != 0:
                last_update = last_update + 1
            r = self.send_to_bot('getUpdates?timeout=30&offset={0}'.format(last_update))
            if not r:
                continue
            r_json = r.json()
            if not r_json['ok']:
                break

            # Detect acumulated messages
            chats = {}
            for result in r_json['result']:
                chat_id = result['message']['chat']['id']
                if chat_id not in chats:
                    chats[ chat_id ] = []
                chats[ chat_id ].append(result['message'])
                if result['update_id'] >= self.get_last_update():
                    self.set_last_update (result['update_id'])

            for chat in chats:
                chat_data = self.get_chat_data(chat)
                language = chat_data["language"]
                msgs = []
                history = chat_data["history"]
                # Too much messages to handle?
                messages_count = len(chats[chat])
                if messages_count > 3:
                    #msgs.append(['{0} Me distraje un momento y ya tengo {1} notificaciones!'.format(self.emoji_oh, messages_count)])
                    # Process only first message
                    chats[chat] = [chats[chat][0]]

                keyboard = None

                for message in chats[chat]:
                    chat_data["chat_lenght"] += 1
                    children = None
                    infer = None
                    if_not = None
                    keys = []

                    chat_id = message['chat']['id']

                    # Text
                    if 'text' not in message:
                        continue

                    text = message['text']

                    print (text)
                    history.append(text)

                    msgs_commands = []
                    if text == '/help' or text == '/help@{0}'.format(self.bot_username):
                        msgs_commands.append([ self.get_language(self.script["help_text"], language) ])
                        self.send_msg(msgs_commands, chat_id)
                        continue
                    elif text == '/stop' or text == '/stop@{0}'.format(self.bot_username):
                        continue
                    elif text == '/settings' or text == '/settings@{0}'.format(self.bot_username):
                        msgs_commands.append([ self.get_language(self.script["settings_text"], language) ])
                        self.send_msg(msgs_commands, chat_id)
                        continue
                    elif text == '/language' or text == '/language@{0}'.format(self.bot_username):
                        msgs_commands.append([ self.get_language(self.script["settings_text"], language)])
                        keyboard = {
                            "keyboard": [["/language Español"], ["/language English"]],
                            "resize_keyboard": True,
                            "one_time_keyboard": True
                        }
                        self.send_msg(msgs_commands, chat_id, keyboard)
                        continue

                    if text.startswith("/language") or text.startswith("/language@{0}".format(self.bot_username)):
                        if text.endswith("Español"):
                            msgs_commands.append(["Idioma elegido: Español"])
                            chat_data["language"] = "es"
                        elif text.endswith("English"):
                            msgs_commands.append(["Choosed language: English"])
                            chat_data["language"] = "en"
                        keyboard = {
                            "keyboard": [["Continue"]],
                            "resize_keyboard": True,
                            "one_time_keyboard": True
                        }
                        self.send_msg(msgs_commands, chat_id, keyboard)
                        continue

                    if text[0] == '/':
                        pass
                        #continue
                    elif text[0:9] == '@{0} '.format(self.bot_username):
                        text = text[10:]

                    current_msg = None
                    print ("last:")
                    print (chat_data["last_message"])
                    for message in self.script["script"]:
                        if current_msg or chat_data["last_message"] == "":
                            chat_data["last_message"] = message["uuid"]

                            answers = []
                            msgs = []
                            answer_id = None

                            if current_msg:
                                for cma in current_msg["answers"]:
                                    if self.get_language(current_msg["answers"][cma], language) == text:
                                        answer_id = cma
                                        break

                            if answer_id and "contextual_message" in message:
                                msgs = msgs + self.get_language(message["contextual_message"][answer_id], language)

                            msgs = msgs + self.get_language(message["message"], language)

                            for answer in message["answers"]:
                                answers.append(self.get_language(message["answers"][answer], language))
                            if len(answer) > 0:
                                keyboard = {
                                    "keyboard": [answers],
                                    "resize_keyboard": True,
                                    "one_time_keyboard": True
                                }
                            break
                        if message["uuid"] == chat_data["last_message"]:
                            current_msg = message

                chat_data["last_time"] = int(time.time())
                chat_data["history"] = history

                self.send_msg(msgs, chat_id, keyboard, True)

                self.set_chat_data(chat_data, chat_id)

Bot = bot()

while 1:
    Bot.bot_loop()
    try:
        Bot.bot_loop()
    except KeyboardInterrupt:
        break
    except:
        print ('Exception')
