import os
#import json
import random
import requests

from config import Config


import sqlite3


class bot:
    bot_token = Config.bot_token
    admin_id = Config.admin_id

    chats = {}

    emoji_oh = '😱'
    emoji_silent = '😁'
    emoji_earth_wireframe = '🌐'
    emoji_number = '#⃣'

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


    def add_msg(self, type_, msg, user_id):
        if user_id != self.admin_id:
            print ('Forbidden')
            return False
        self.c.execute("INSERT INTO messages (type, value) VALUES (?,?)", (type_, msg))
        self.conn.commit()

    def get_msg(self, type_):
        messages = self.c.execute("SELECT * FROM messages WHERE type=?", (type_,))
        msg = messages.fetchall()
        #print (msg)
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
            
    def get_chats_stats(self):
        messages = self.c.execute("SELECT COUNT(*) FROM messages")
        messages = messages.fetchone()
        msg_count = messages[0]
        chats = self.c.execute("SELECT lenght FROM chats")
        chats = chats.fetchall()
        if chats:
            average_lenght = 0.0
            count = 0
            ratio = 0
            for chat in chats:
                count += chat[0]
                if chat[0]>0:
                    if chat[0] > msg_count:
                        ratio += 1.0
                    else:
                        ratio += msg_count / chat[0]
            if len(chats) > 0:
                average_lenght = count / len(chats)
                average_ratio = ratio / len(chats)
            stats = {
                'count': len(chats),
                'average_lenght': average_lenght,
                'average_ratio': average_ratio,
                'msg_count': msg_count
            }
            return stats
        else:
            return None
    
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

                    # Text
                    if 'text' in message:
                        text = message['text']
                        msgs_commands = []
                        if text == '/help':
                            msgs_commands.append(['[Terminal Start]\n"Yo puse en funcionamiento a rDany, solo espero que su sufrimiento en éste mundo no sea muy grande."\n@Eibriel\n\nDejá tu comentario: https://telegram.me/storebot?start=rdanybot\n[Terminal End]'])
                            self.send_msg(msgs_commands, chat_id)
                            continue
                        elif text == '/settings':
                            msgs_commands.append(['[Terminal Start]\nERROR: Settings no ha sido implementado.\n[Terminal End]'])
                            self.send_msg(msgs_commands, chat_id)
                            continue
                        elif text == '/interference':
                            msgs_commands.append(['[Terminal Start]\nNivel de interferencia en la comunicación: {0}% {1}\n[Terminal End]'.format(random.randint(88, 100), self.emoji_earth_wireframe)])
                            self.send_msg(msgs_commands, chat_id)
                            continue
                        elif text == '/chats':
                            chats_stats = self.get_chats_stats()
                            msgs_commands.append(['[Terminal Start]\nChats: {0}\nLongitud promedio: {1}\nRatio promedio: {2}\nMensajes: {3}\n[Terminal End]'.format(chats_stats['count'], chats_stats['average_lenght'], chats_stats['average_ratio'], chats_stats['msg_count'])])
                            self.send_msg(msgs_commands, chat_id)
                            continue
                        
                        if text[0] == '/':
                            text = text[1:]
                        elif text[0:9] == '@rDanyBot ':
                            text = text[10:]

                    if text[0:18] == 'add-first-contact ':
                        self.add_msg('first-contact', text[18:], message['from']['id'])
                        continue
                    elif text[0:9] == 'add-idea ':
                        self.add_msg('idea', text[9:], message['from']['id'])
                        continue
                    elif text[0:10] == 'add-story ':
                        self.add_msg('story', text[10:], message['from']['id'])
                        continue

                    self.add_chat_lenght(chat_id)
                    chat_lenght = self.get_chat_lenght(chat_id)
                    print ('chat lenght {0}'.format(chat_lenght))

                    if chat_lenght < 4:
                        print ('first-contact')
                        msgs.append([self.get_msg('first-contact')])
                    elif chat_lenght < 6:
                        msgs.append([self.get_msg('idea')])
                    else:
                        msgs.append([self.get_msg('story')])
                    
                self.send_msg(msgs, chat_id, True)

Bot = bot()

while 1:
    #Bot.bot_loop()
    try:
        Bot.bot_loop()
    except KeyboardInterrupt:
        break
    except:
        print ('Exception')
