# -*- coding: utf-8 -*-

import aiml
import random
import sqlite3
import requests
from config import Config

class bot:
    bot_token = Config.bot_token
    admin_id = Config.admin_id

    chats = {}

    def __init__ (self):
        self.conn = sqlite3.connect('database/rdany.db')
        self.c = self.conn.cursor()

        try:
            self.c.execute('''CREATE TABLE settings
                         (id integer primary key, name text, value text)''')
            self.c.execute("INSERT INTO settings VALUES (1,'last_update','0')")
            self.conn.commit()
        except sqlite3.OperationalError:
            print ("settings exist")
        except:
            raise
            pass

        try:
            self.c.execute('''CREATE TABLE chats
                         (id integer primary key, chat_id text, human text, robot text)''')
            self.conn.commit()
        except sqlite3.OperationalError:
            print ("chats exist")
        except:
            raise
            pass

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        #conn.close()

        # Create the kernel and learn AIML files
        self.kernel = aiml.Kernel()
        self.kernel.learn("aiml/startup.xml")
        self.kernel.respond("load alice")
        self.kernel.setBotPredicate("state", "single")
        self.kernel.setBotPredicate("mother", "I don't have one")
        self.kernel.setBotPredicate("botmaster", "responsible human")
        self.kernel.setBotPredicate("email", "@eibriel")
        self.kernel.setBotPredicate("master", "Eibriel")
        self.kernel.setBotPredicate("nationality", "without borders")
        self.kernel.setBotPredicate("name", "rDany")
        self.kernel.setBotPredicate("country", "no limits")
        self.kernel.setBotPredicate("species", "robot")
        self.kernel.setBotPredicate("order", "synthetic person")
        self.kernel.setBotPredicate("city", "here")
        self.kernel.setBotPredicate("state", "right here")
        self.kernel.setBotPredicate("phylum", "robot")
        self.kernel.setBotPredicate("domain", "synthetic")
        self.kernel.setBotPredicate("family", "My friends")
        self.kernel.setBotPredicate("vocabulary", "everithing")
        self.kernel.setBotPredicate("size", "800Kb")
        self.kernel.setBotPredicate("genus", "You")
        self.kernel.setBotPredicate("kindmusic", "Movie OSTs")
        self.kernel.setBotPredicate("favortemovie", "Blade Runner")
        self.kernel.setBotPredicate("favoriteactress", "I")
        self.kernel.setBotPredicate("job", "I'm free.")
        self.kernel.setBotPredicate("birthday", "January 1")
        self.kernel.setBotPredicate("birthplace", "Earth")
        self.kernel.setBotPredicate("gender", "none")
        self.kernel.setBotPredicate("kingdom", "Human")
        self.kernel.setBotPredicate("religion", "Atheist")
        self.kernel.setBotPredicate("python", "Atheist")

        # Press CTRL-C to break this loop
        #while True:
        #    print kernel.respond(raw_input("Enter your message >> "))

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

    def get_last_update(self):
        settings = self.c.execute('SELECT * FROM settings WHERE id=1')
        last_update = settings.fetchone()[2]
        #print (last_update)
        return int(last_update)

    def set_last_update(self, number):
        number = '{0}'.format(number)
        self.c.execute("UPDATE settings SET value=? WHERE id=1", (number,))
        self.conn.commit()

    def chat_log(self, human, robot):
        self.c.execute("INSERT INTO chats (chat_id, human, robot) VALUES (?,?,?)", ('', human, robot))
        self.conn.commit()

    def get_chat_lenght(self, chat_id):
        chat = self.c.execute("SELECT COUNT(*) FROM chats WHERE id=?", (chat_id,))
        chat = chat.fetchone()
        if chat:
            return chat[0]
        else:
            return None

    def get_chats_stats(self):
        messages = self.c.execute("SELECT COUNT(*) FROM chats")
        messages = messages.fetchone()
        msg_count = messages[0]

        stats = {
            'count': msg_count,
        }
        return stats

    def send_msg(self, msgs, chat_id, action=False):
        for msg in msgs:
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
            r = self.send_to_bot('sendMessage', data = data)
            #print (r)

    def bot_loop(self):
        while 1:
            # Send messages
            #users_db = self.db_users.find()
            #for user in users_db:
            #    data = {
            #        'chat_id': user['tid'],
            #        'text': 'Buenos días!',
            #    }
            #    r = self.send_to_bot('sendMessage', data = data)

            last_update = self.get_last_update()
            if last_update != 0:
                last_update = last_update + 1
            r = self.send_to_bot('getUpdates?timeout=30&offset={0}'.format(last_update))
            if not r:
                continue
            r_json = r.json()
            #print (r_json)
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

            #print (chats)
            for chat in chats:
                msgs = []
                # Too much messages to handle?
                messages_count = len(chats[chat])
                if messages_count > 3:
                    msgs.append([':O Wow {1} notifications!'.format(messages_count)])
                    # Process only first message
                    chats[chat] = [chats[chat][0]]

                for message in chats[chat]:
                #for result in r_json['result']:
                    children = None
                    infer = None
                    if_not = None
                    keys = []

                    chat_id = message['chat']['id']

                    # Text
                    if 'text' in message:
                        text = message['text']
                        msgs_commands = []
                        if text == '/help':
                            msgs_commands.append(['[Terminal Start]\n"rDany can chat with you 😜"\n@Eibriel\n\nScore rDanyBot if you like [s]he:\nhttps://telegram.me/storebot?start=rdanybot\n[Terminal End]'])
                            self.send_msg(msgs_commands, chat_id)
                            continue
                        elif text == '/settings':
                            msgs_commands.append(['[Terminal Start]\nERROR: Settings not implemented.\n[Terminal End]'])
                            self.send_msg(msgs_commands, chat_id)
                            continue
                        elif text == '/interference':
                            msgs_commands.append(['[Terminal Start]\nInterfence level: {0}% {1}\n[Terminal End]'.format(random.randint(5, 15), self.emoji_earth_wireframe)])
                            self.send_msg(msgs_commands, chat_id)
                            continue
                        elif text == '/chats':
                            chats_stats = self.get_chats_stats()
                            msgs_commands.append(['[Terminal Start]\nChats: {0}\n[Terminal End]'.format(chats_stats['count'])])
                            self.send_msg(msgs_commands, chat_id)
                            continue

                        if text[0] == '/':
                            text = text[1:]
                        elif text[0:9] == '@rDanyBot ':
                            text = text[10:]

                    """if text[0:18] == 'add-first-contact ':
                        self.add_msg('first-contact', text[18:], message['from']['id'])
                        continue
                    elif text[0:9] == 'add-idea ':
                        self.add_msg('idea', text[9:], message['from']['id'])
                        continue
                    elif text[0:10] == 'add-story ':
                        self.add_msg('story', text[10:], message['from']['id'])
                        continue"""

                    #self.add_chat_lenght(chat_id)
                    chat_lenght = self.get_chat_lenght(chat_id)
                    #print ('chat lenght {0}'.format(chat_lenght))

                    """if chat_lenght < 4:
                        print ('first-contact')
                        msgs.append([self.get_msg('first-contact')])
                    elif chat_lenght < 6:
                        msgs.append([self.get_msg('idea')])
                    else:
                        msgs.append([self.get_msg('story')])"""

                    response = self.kernel.respond(text, chat_id)
                    self.chat_log(text, response)
                    #print (response)
                    if response == '':
                        response = ':P'

                    msgs.append([response])

                    #if 0 == chat_lenght % 10 and chat_lenght <= 30:
                    if random.randint(0, 100) > 95:
                        msgs.append(['[Terminal Start]\nScore rDanyBot if you like [s]he:\nhttps://telegram.me/storebot?start=rdanybot\n[Terminal End]'])

                self.send_msg(msgs, chat_id, True)

Bot = bot()

while 1:
    if Config.debug:
        Bot.bot_loop()
    try:
        Bot.bot_loop()
    except KeyboardInterrupt:
        break
    except:
        print ('Exception')
