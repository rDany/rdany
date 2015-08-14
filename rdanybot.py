import os
#import json
import random
import requests

from config import Config


import sqlite3


class bot:
    bot_username = Config.bot_username
    bot_token = Config.bot_token
    admin_id = Config.admin_id
    help_text = Config.help_text
    settins_text = Config.settings_text
    pause_text = Config.pause_text
    continue_text = Config.continue_text

    chats = {}

    emoji_oh = '😱'
    emoji_silent = '😁'
    emoji_earth_wireframe = '🌐'
    emoji_number = '#⃣'

    def sqlite_execute(self, query, name, debug = False):
        try:
            self.c.execute(query)
            self.conn.commit()
            print ('{0} applied'.format(name))
            return True
        except sqlite3.OperationalError:
            print ('{0} already applied'.format(name))
            if debug:
                raise
            return False
        except:
            raise

    def __init__ (self):
        self.conn = sqlite3.connect('database/rdany.db')
        self.c = self.conn.cursor()
        
        exe = self.sqlite_execute('''CREATE TABLE settings
                         (id integer primary key, name text, value text)''', "settings")
        if exe:
            self.c.execute("INSERT INTO settings VALUES (1,'last_update','0')")
        
        self.sqlite_execute('''CREATE TABLE messages
                         (id integer primary key, type text, value text)''', "messages")
        
        self.sqlite_execute('''CREATE TABLE chats
                         (id integer primary key, lenght integer)''', "chats")
        
        self.sqlite_execute('''ALTER TABLE chats
                         ADD COLUMN last_message integer;''',
                         "last_message on chats")

        self.sqlite_execute('''ALTER TABLE chats
                         ADD COLUMN last_message_datetime integer;''',
                         "last_message_datetime on chats")

        self.sqlite_execute('''ALTER TABLE chats
                         ADD COLUMN subscribed integer default 1;''',
                         "subscribred on chats")

        self.sqlite_execute('''CREATE TABLE chat_message
                         (chat_id integer, message_id integer, count integer default 1, success integer default 0)''',
                         "chat_message")

        self.sqlite_execute('''CREATE UNIQUE INDEX chat_message_index
                            on chat_message (chat_id, message_id);''', "chat_message_index")

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
        self.c.execute("INSERT INTO messages (type, value) VALUES (?,?);", (type_, msg))
        self.conn.commit()

    def get_msg(self, type_, chat_id):
        messages = self.c.execute("SELECT * FROM messages WHERE type=?;", (type_,))
        msg = messages.fetchall()
        chat_message = self.c.execute("SELECT * FROM chat_message WHERE chat_id=? ORDER BY count ASC;", (chat_id,))
        cm = chat_message.fetchall()

        unread_messages = []
        for m in msg:
            readed = False
            for c in cm:
                #print('c: {0}, m: {1}'.format(c[1], m[0]))
                if c[1] == m[0]: # Matching message_id
                    readed = True
                    break
            if not readed:
                unread_messages.append(m)

        #print (unread_messages)
        if len(unread_messages) > 0:
            msg = random.choice(unread_messages)
            return msg
        elif len(cm) > 0:
            c = cm[0]
            for m in msg:
                #print('c: {0}, m: {1}'.format(c[1], m[0]))
                if c[1] == m[0]: # Matching message_id
                    return m
            print ('ERROR')
            return None
        else:
            return None

    def chat_message(self, message_id, chat_id):
        chat_message = self.c.execute("SELECT * FROM chat_message WHERE chat_id=? AND message_id=?", (chat_id, message_id))
        cm = chat_message.fetchone()
        count = 0
        if cm:
            count = cm[2] + 1
            self.c.execute("UPDATE chat_message SET count=? WHERE chat_id=? AND message_id=?", (count, chat_id, message_id))
            self.conn.commit()
        else:
            self.c.execute("INSERT INTO chat_message (chat_id, message_id) VALUES (?,?)", (chat_id, message_id))
            self.conn.commit()


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
                        ratio += chat[0] / msg_count
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
   

    def push_msg(self, msg, chat_id):
        chats = self.c.execute("SELECT id, subscribed FROM chats")
        chats = chats.fetchall()
        if chats:
            for chat in chats:
                if chat[1]: # Subscribed
                    self.send_msg([msg], chat[0], True)


    def pause(self, chat_id, active):
        if active:
            subscription = 0
        else:
            subscription = 1
        chat = self.c.execute("SELECT id FROM chats WHERE id=?;", (chat_id,))
        chat = chat.fetchone()
        if chat:
            self.c.execute("UPDATE chats SET subscribed=? WHERE id=?;", (subscription, chat_id))
        else:
            self.c.execute("INSERT INTO chats (id, lenght, subscribed) VALUES (?,0,?)", (chat_id, subscription))
        self.conn.commit()


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
                    if 'text' not in message:
                        continue
                    
                    text = message['text']
                    msgs_commands = []
                    if text == '/help' or text == '/help@{0}'.format(self.bot_username):
                        msgs_commands.append([self.help_text])
                        self.send_msg(msgs_commands, chat_id)
                        continue
                    elif text == '/settings' or text == '/settings@{0}'.format(self.bot_username):
                        msgs_commands.append([self.settins_text])
                        self.send_msg(msgs_commands, chat_id)
                        continue
                    elif text == '/pause' or text == '/pause@{0}'.format(self.bot_username):
                        msgs_commands.append([self.pause_text])
                        self.pause(chat_id, True)
                        self.send_msg(msgs_commands, chat_id)
                        continue
                    elif text == '/continue' or text == '/continue@{0}'.format(self.bot_username):
                        msgs_commands.append([self.continue_text])
                        self.pause(chat_id, False)
                        self.send_msg(msgs_commands, chat_id)
                        continue
                    elif text == '/interference' or text == '/interference@{0}'.format(self.bot_username):
                        msgs_commands.append(['[Terminal Start]\nNivel de interferencia en la comunicación: {0}% {1}\n[Terminal End]'.format(random.randint(88, 100), self.emoji_earth_wireframe)])
                        self.send_msg(msgs_commands, chat_id)
                        continue
                    elif text == '/chats' or text == '/chats@{0}'.format(self.bot_username):
                        chats_stats = self.get_chats_stats()
                        msgs_commands.append(['[Terminal Start]\nChats: {0}\nLongitud promedio: {1}\nRatio promedio: {2}\nMensajes: {3}\n[Terminal End]'.format(chats_stats['count'], chats_stats['average_lenght'], chats_stats['average_ratio'], chats_stats['msg_count'])])
                        self.send_msg(msgs_commands, chat_id)
                        continue
                    
                    if text[0] == '/':
                        continue
                    elif text[0:9] == '@{0} '.format(self.bot_username):
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
                    elif text[0:11] == 'push-story ':
                        self.push_msg(text[11:], message['from']['id'])
                        continue

                    self.add_chat_lenght(chat_id)
                    chat_lenght = self.get_chat_lenght(chat_id)
                    print ('chat lenght {0}'.format(chat_lenght))

                    if chat_lenght < 4:
                        print ('first-contact')
                        msg = self.get_msg('first-contact', chat_id)
                        if msg:
                            msgs.append([msg[2]])
                            self.chat_message(msg[0], chat_id)
                    elif chat_lenght < 6:
                        msg = self.get_msg('idea', chat_id)
                        if msg:
                            msgs.append([msg[2]])
                            self.chat_message(msg[0], chat_id)
                    else:
                        msg = self.get_msg('story', chat_id)
                        if msg:
                            msgs.append([msg[2]])
                            self.chat_message(msg[0], chat_id)
                    
                    if 0 == chat_lenght % 10 and chat_lenght <= 30 and chat_lenght > 1:
                        msgs.append(['[Terminal Start]\nCalificá a {0} en StoreBot:\nhttps://telegram.me/storebot?start={0}\n[Terminal End]'.format(self.bot_username)])

                    self.send_msg(msgs, chat_id, True)

Bot = bot()

while 1:
    Bot.bot_loop()
    try:
        Bot.bot_loop()
    except KeyboardInterrupt:
        break
    except:
        print ('Exception')
