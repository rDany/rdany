import os
import re
import json
import time
import datetime
import requests

from urllib.parse import urlencode
from config import Config


class bot:
    bot_username = Config.bot_username
    bot_token = Config.bot_token
    admin_id = Config.admin_id
    useragent = "User-Agent: rDany/1.1 (http://www.rdany.org/rdany/; botmaster@rdany.org)"

    chats = {}

    emoji_oh = '😱'

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
        headers = {'user-agent': self.useragent}
        try:
            r = requests.get('https://api.telegram.org/bot{0}/{1}'.format(self.bot_token, access_point), data=data, timeout=40, headers=headers)
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
            #print (data)
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
                "language": "es",
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

    def process_question (self, question):
        if question == "":
            return None

        pidehora = re.search(r"hora", question, re.IGNORECASE)
        #
        pidefecha = re.search(r"(fecha|qu(e|é)\s+d(i|í)a\s+es)", question, re.IGNORECASE)
        #
        pidefecha_relativa = re.search(r"(qu(e|é))\s+(fecha|d(i|í)a)\s+(es|ser(a|á)|va\sa\sser|fue)\s+(?P<buscar>.+)", question, re.IGNORECASE)
        #
        pidewiki = re.search(r"\W*qu(e|é|ien|ién)\s+(es|fue|fué|era|sera|será)\s*(el|la|un|una)*\s+(?P<buscar>.+?)\s*\?*$", question, re.IGNORECASE)
        if not pidewiki:
          pidewiki = re.search(r"\W*conoc(e|é)s\s*(el|la|a)*\s+(?P<buscar>.+)\s*\?*$", question, re.IGNORECASE)
        if not pidewiki:
          pidewiki = re.search(r"\W*c(o|ó)mo\s*funciona\s*(el|la|un|una)*\s+(?P<buscar>.+)\s*\?*$", question, re.IGNORECASE)
        if not pidewiki:
          pidewiki = re.search(r"\W*donde\s*est(a|á)\s*(el|la)*\s+(?P<buscar>.+)\s*\?*$", question, re.IGNORECASE)
        ##
        pidebuscador = re.search(r"\W*(googleame|buscame|buscá)\s+(?P<buscar>.+)", question, re.IGNORECASE)
        ##
        pidetwitter = re.search(r"\W*(twit(t)*eame|twi(t)*e(a|á))\s+(?P<buscar>.+)", question, re.IGNORECASE)
        ##
        pidefacebook = re.search(r"\W*posteame\s+(?P<buscar>.+)\s+en\s+(el\s+)*facebook", question, re.IGNORECASE)
        ##
        pideyoutube = re.search(r"\W*(m(ue|o)strame|busca|buscá)\s+(un|el)\s+(video|videoclip)\s+(acerca\s+de|sobre|de|del|de\s+(la|las))\s+(?P<buscar>.+)", question, re.IGNORECASE)
        ##
        pideimagen = re.search(r"\W*(m(ue|o)strame|busca|buscá)\s+(una|la)\s+(foto|imagen|imágen)*\s+(de|del|de\s+la)\s+(?P<buscar>.+)", question, re.IGNORECASE)
        ##

        week_day_name = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        month_name = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        now = datetime.date.today()

        text = None

        if pidewiki:
            #return "pidewiki {0}".format(pidewiki.group('buscar'))
            headers = {'user-agent': self.useragent}
            try:
                data = {
                    "format": "json",
                    "action": "opensearch",
                    "search": pidewiki.group("buscar")
                }
                r = requests.get("http://es.wikipedia.org/w/api.php", params=data, timeout=20, headers=headers)
            except requests.exceptions.ConnectionError:
                text = "Connection Error"
                print (text)
            except requests.exceptions.Timeout:
                text = "Connection Timeout"
                print (text)
            rres = r.json()
            rres = rres[1][0]

            try:
                data = {
                    "format": "json",
                    "action": "query",
                    "redirects": "true",
                    "prop": "extracts",
                    "exintro": "true",
                    "explaintext": "true",
                    "titles": rres
                }
                r = requests.get("http://es.wikipedia.org/w/api.php", params=data, timeout=20, headers=headers)
            except requests.exceptions.ConnectionError:
                text = "Connection Error"
                print (text)
            except requests.exceptions.Timeout:
                text = "Connection Timeout"
                print (text)

            resf = ""
            for pag in r.json()['query']['pages']:
                #print (r.json()['query']['pages'][pag])
                resf = "{0}{1}".format(resf, r.json()['query']['pages'][pag]['extract'])

            if len(resf)<200:
              resf = "La información es insuficiente. Por ejemplo si escribió \"¿Quién es Daneel?\" pruebe con \"¿Quién es Daneel Olivaw?\"." ;

            if r.status_code == requests.codes.ok:
                text = "\"{0}\" según Wikipedia: {1}".format(pidewiki.group("buscar"), resf) ;
            else:
                text = "Error"
        elif pidetwitter:
            params = urlencode( {"source": "rdany", "text": pidetwitter.group('buscar')} )
            text = "https://twitter.com/intent/tweet?{0}".format(params)
        elif pidefacebook:
            text = "Pide facebook ".format(pidefacebook.group('buscar'))
        elif pideyoutube:
            #params = urlencode( {"search_query": pideyoutube.group('buscar')} )
            #text = "http://www.youtube.com/results?{0}".format(params)
            params = urlencode( {"q": pideyoutube.group('buscar'), "ia": "videos", "iax": "1"} )
            text = "https://duckduckgo.com/?{0}".format(params)
        elif pideimagen:
            params = urlencode( {"q": pideimagen.group('buscar'), "ia": "images", "iax": "1"} )
            text = "http://duckduckgo.com/?{0}".format(params)
        #elif pidemailto:
        #    text = "Pide mailto" ;
        #elif pideimdb:
        #    text = "http://www.imdb.com/find?q={0}&s=all".format(urlencode(pideimdb.group('buscar')))
        #elif pidecuevana:
        #    text = "http://www.cuevana.tv/#!/buscar/q:{0}".format(urlencode(pidecuevana.group('buscar')))
        elif pidehora:
            now = datetime.datetime.now()
            if now.hour == 1:
                text = "Es la {0:02d}:{1:02d}".format(now.hour, now.minute)
            else:
                text = "Son las {0:02d}:{1:02d}".format(now.hour, now.minute)
        elif pidefecha_relativa:
            parameter = pidefecha_relativa.group('buscar')
            before_yesterday = re.search(r"\W*antes\s*de\s*ayer", parameter, re.IGNORECASE)
            yesterday = re.search(r"\W*ayer", parameter, re.IGNORECASE)
            tomorrow = re.search(r"\W*mañana", parameter, re.IGNORECASE)
            day_before = re.search(r"\W*pasado\s+mañana", parameter, re.IGNORECASE)

            if day_before:
                text = "Pasado mañana será"
                relative_date = now + datetime.timedelta(days=2)
            elif tomorrow:
                text = "Mañana será"
                relative_date = now + datetime.timedelta(days=1)
            elif before_yesterday:
                text = "Antes de ayer fue"
                relative_date = now + datetime.timedelta(days=-2)
            elif yesterday:
                text = "Ayer fue"
                relative_date = now + datetime.timedelta(days=-1)

            text = "{0} {1} {2} de {3} de {4}".format(text, week_day_name[relative_date.weekday()], relative_date.day, month_name[relative_date.month], relative_date.year)
            text = "{0}\nFecha estelar {1}.{2}".format(text, relative_date.year, relative_date.timetuple()[7])
            #text = pidefecha_relativa.group('buscar')
        elif pidefecha:
            text = "Hoy es {0} {1} de {2} de {3}".format(week_day_name[now.weekday()], now.day, month_name[now.month], now.year)
            text = "{0}\nFecha estelar {1}.{2}".format(text, now.year, now.timetuple()[7])
        elif pidebuscador:
            params = urlencode( {"q": pidebuscador.group('buscar')} )
            text = "http://duckduckgo.com/?{0}".format(params)

        return text


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
                language = "es"
                history = chat_data["history"]
                # Too much messages to handle?
                messages_count = len(chats[chat])
                msgs_prev = []
                if messages_count > 3:
                    msgs_prev = ['{0} Me distraje un momento y ya tengo {1} notificaciones!'.format(self.emoji_oh, messages_count)]
                    # Process only first message
                    #chats[chat] = [chats[chat][0]]

                keyboard = None

                for message in chats[chat]:
                    chat_data["chat_lenght"] += 1
                    children = None
                    infer = None
                    if_not = None
                    keys = []
                    msgs = msgs_prev
                    msgs_prev = []

                    chat_id = message['chat']['id']

                    # Text
                    if 'text' not in message:
                        continue

                    text = message['text']

                    print (text)
                    history.append(text)

                    msgs_commands = []
                    if text == '/help' or text == '/help@{0}'.format(self.bot_username):
                        #msgs_commands.append([ self.get_language(self.script["help_text"], language) ])
                        msgs_commands.append([ "Algunas de las cosas que puedes consultarle a rDany:\n¿Quién es Daneel Olivaw?\nBuscá una foto de la luna\nBuscá un video acerca de SpaceX\n¿Qué hora es?\n¿Qué día es?" ])
                        self.send_msg(msgs_commands, chat_id)
                        continue
                    elif text == '/stop' or text == '/stop@{0}'.format(self.bot_username):
                        msgs_commands.append([ "No hay nada que detener" ])
                        self.send_msg(msgs_commands, chat_id)
                        continue
                    #elif text == '/start' or text == '/start@{0}'.format(self.bot_username):
                    #    msgs_commands.append([ "Hola, mi nombre es Dany", "Puedes comenzar preguntandome cosas como la hora, la fecha o qué es algo, por ejemplo:\n¿Quién es Daneel Olivaw?\nBuscá una foto de la luna\nBuscá un video acerca de SpaceX\n¿Qué hora es?\n¿Qué día es?" ])
                    #    self.send_msg(msgs_commands, chat_id)
                    #    continue
                    elif text == '/settings' or text == '/settings@{0}'.format(self.bot_username):
                        msgs_commands.append([ "No hay nada que setear" ])
                        self.send_msg(msgs_commands, chat_id)
                        continue
                    elif text == '/language' or text == '/language@{0}'.format(self.bot_username):
                        continue
                        msgs_commands.append([ self.get_language(self.script["settings_text"], language)])
                        keyboard = {
                            "keyboard": [["/language Español"], ["/language English"]],
                            "resize_keyboard": True,
                            "one_time_keyboard": True
                        }
                        self.send_msg(msgs_commands, chat_id, keyboard)
                        continue

                    if text.startswith("/language") or text.startswith("/language@{0}".format(self.bot_username)):
                        continue
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

                    processed = self.process_question(text)

                    ##### GUION ####
                    current_msg = None
                    print ("last:")
                    print (chat_data["last_message"])
                    if processed == None:
                        answers = []
                        #msgs = []
                        if chat_data["last_message"] == "":
                            message = self.script["script"][0]
                            chat_data["last_message"] = message["uuid"]
                            msgs = msgs + self.get_language(message["message"], language)

                            for answer in message["answers"]:
                                answers.append(self.get_language(message["answers"][answer], language))
                            if len(answer) > 0:
                                keyboard = {
                                    "keyboard": [answers],
                                    "resize_keyboard": True,
                                    "one_time_keyboard": True
                                }
                        else:
                            last_message = True
                            for message in self.script["script"]:
                                if current_msg:
                                    last_message = False
                                    answer_id = None

                                    for cma in current_msg["answers"]:
                                        if self.get_language(current_msg["answers"][cma], language) == text:
                                            answer_id = cma
                                            break

                                    if answer_id:
                                        chat_data["last_message"] = message["uuid"]
                                        if "contextual_message" in message:
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
                                    old_answers = []
                                    current_msg = message
                                    old_msgs = self.get_language(current_msg["message"], language)
                                    for answer in message["answers"]:
                                        old_answers.append(self.get_language(message["answers"][answer], language))
                                    if len(old_answers) > 0:
                                        keyboard = {
                                            "keyboard": [old_answers],
                                            "resize_keyboard": True,
                                            "one_time_keyboard": True
                                        }
                            if last_message:
                                msgs.append("Vuelvo al rato!")
                    #######

                    chat_data["last_time"] = int(time.time())
                    chat_data["history"] = history

                    if processed != None:
                        msgs = [processed]

                    if len(msgs) == 0:
                        msgs = ["No entendí, prueba con /help"]+old_msgs
                        #keyboard = old_keyboard

                    self.send_msg(msgs, chat_id, keyboard, False)
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
