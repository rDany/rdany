import os
#import json
import random
import requests

from config import Config


import sqlite3


class bot:
    bot_token = Config.bot_token

    chats = {}

    emoji_oh = '😱'
    emoji_silent = '😁'

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
            self.c.execute('''CREATE TABLE messages
                         (id integer primary key, type text, value text)''')
            self.conn.commit()
        except sqlite3.OperationalError:
            print ("messages exist")
        except:
            raise
            pass
        
        try:
            self.c.execute('''CREATE TABLE chats
                         (id integer primary key, lenght integer)''')
            self.conn.commit()
        except sqlite3.OperationalError:
            print ("chats exist")
        except:
            raise
            pass
        
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        #conn.close()

    def send_to_bot(self, access_point, data=None):
        try:
            r = requests.get('https://api.telegram.org/bot{0}/{1}'.format(self.bot_token, access_point), data=data, timeout=40)
        except requests.exceptions.ConnectionError:
            print ("Connection Error")
            return None
        except requests.exceptions.ReadTimeout:
            print ("Connection Timeout")
            return None
        return r

    def get_last_update(self):
        settings = self.c.execute('SELECT * FROM settings WHERE id=1')
        last_update = settings.fetchone()[2]
        print (last_update)
        return int(last_update)


    def set_last_update(self, number):
        number = '{0}'.format(number)
        self.c.execute("UPDATE settings SET value=? WHERE id=1", (number,))
        self.conn.commit()


    def add_msg(self, type_, msg):
        self.c.execute("INSERT INTO messages (type, value) VALUES (?,?)", (type_, msg))
        self.conn.commit()

    def get_msg(self, type_):
        settings = self.c.execute("SELECT * FROM messages WHERE type=?", (type_,))
        msg = settings.fetchall()
        print (msg)
        if len(msg) > 0:
            msg = random.choice(msg)[2]
            return msg
        else:
            return ''

    def add_chat_lenght(self, chat_id):
        chat = self.c.execute("SELECT * FROM chats WHERE id=?", (chat_id,))
        chat = chat.fetchone()
        if not chat:
            self.c.execute("INSERT INTO chats (id, lenght) VALUES (?,?)", (chat_id, 0))
            self.conn.commit()
        else:
            lenght = chat[1]
            self.c.execute("UPDATE chats SET lenght=? WHERE id=?", (lenght+1, chat_id))
            self.conn.commit()
    
    def get_chat_lenght(self, chat_id):
        chat = self.c.execute("SELECT * FROM chats WHERE id=?", (chat_id,))
        chat = chat.fetchone()
        if chat:
            return chat[1]
        else:
            return None
            
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
                    msgs.append(['{0} Me distraje un momento y ya tengo {1} notificaciones!'.format(self.emoji_oh, messages_count)])
                    # Process only first message
                    chats[chat] = [chats[chat][0]]

                for message in chats[chat]:
                #for result in r_json['result']:
                    children = None
                    infer = None
                    if_not = None
                    keys = []

                    chat_id = message['chat']['id']
                    self.add_chat_lenght(chat_id)

                    # Text
                    if 'text' in message:
                        text = message['text']
                        if text[0] == '/':
                            text = text[1:]
                        elif text[0:9] == '@HovyuBot ':
                            text = text[10:]

                    if text[0:18] == 'add-first-contact ':
                        self.add_msg('first-contact', text[18:])
                    elif text[0:9] == 'add-idea ':
                        self.add_msg('idea', text[9:])
                    elif text[0:10] == 'add-story ':
                        self.add_msg('story', text[10:])

                    chat_lenght = self.get_chat_lenght(chat_id)
                    print ('chat lenght {0}'.format(chat_lenght))

                    if chat_lenght < 4:
                        print ('first-contact')
                        msgs.append([self.get_msg('first-contact')])
                    elif chat_lenght < 6:
                        msgs.append([self.get_msg('idea')])
                    else:
                        msgs.append([self.get_msg('story')])
                    
                for msg in msgs:
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

Bot = bot()

while 1:
    #Bot.bot_loop()
    try:
        Bot.bot_loop()
    except KeyboardInterrupt:
        break
    except:
        print ('Exception')
