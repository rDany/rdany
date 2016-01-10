# -*- coding: utf-8 -*-

import aiml
import time
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
            self.c.execute('''CREATE TABLE logs
                         (id integer primary key, chat_id text, human text, robot text, fwb intefer)''')
            self.conn.commit()
        except sqlite3.OperationalError:
            print ("log exist")
        except:
            raise
            pass
            
        try:
            self.c.execute('''CREATE TABLE payments
                         (id integer primary key, chat_id integer, address text, amount_old integer, amount integer, confirmed integer )''')
            self.conn.commit()
        except sqlite3.OperationalError:
            print ("payments exist")
        except:
            raise
            pass
        
        try:
            self.c.execute('''CREATE TABLE chats
                         (id integer primary key,
                         hearts integer,
                         fwb integer,
                         fwb_start_datetime integer,
                         msg_count integer,
                         last_msg_datetime integer,
                         proactive integer,
                         btc_address string,
                         btc_in integer,
                         btc_out integer)''')
            self.conn.commit()
        except sqlite3.OperationalError:
            print ("chats exist")
        except:
            raise
            pass

        try:
            self.c.execute('''CREATE TABLE sessions (id integer, key string, value string, unique (id, key))''')
            self.conn.commit()
        except sqlite3.OperationalError:
            print ("sessions exist")
        except:
            raise
            pass

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        #conn.close()

        bot_predicate = {
            "state": "single",
            "mother": "I don't have one",
            "botmaster": "assistant",
            "email": "rdany@rdany.org",
            "master": "Eibriel",
            "nationality": "without borders",
            "name": "rDany",
            "country": "no limits",
            "species": "robot",
            "order": "synthetic person",
            "city": "here",
            "state": "right here",
            "location": "your screen",
            "phylum": "robot",
            "domain": "synthetic",
            "family": "My friends",
            "vocabulary": "everithing",
            "size": "800Kb",
            "genus": "robot",
            "kindmusic": "Movie OSTs",
            "favortemovie": "Blade Runner",
            "favoriteactress": "I",
            "job": "I'm free.",
            "birthday": "January 1",
            "birthplace": "Earth",
            "gender": "none",
            "kingdom": "synth", #Yes I am a philosophy synth
            "religion": "Atheist",
            "python": "Atheist",
            "party": "Pirate",
            "sign": "smoke", #smoke is a fire sign.
            "faily": "robot", #Yes I am a robot
            "arch": "GNU/Linux", #Right now I am on a GNU/Linux
            "president": "Elon Musk",
            "friend": "You",
            "girlfriend": "My computer",
            "show": "Humans",
            "favoriteactor": "Wall-E",
            "celebrity": "Elon Musk",
            "celebrities": "Elon Musk",
            "favoriteartist": "Hayao Miyazaki",
            "hockeyteam": "The Red Oaks",
            "baseballteam": "The Red Oaks",
            "footballteam": "The Red Oaks",
            "favoriteactress": "EVE",
            "favoriteauthor": "Tolkien",
            "etype": "robot",
            "emotions": "I am still learning to control emotions",
            "ethics": "My feelings are confusing right now",
            "feelings": "My feelings are a bit wild.",
            "favoritefood": "spagetti"
        }

        # Create the kernel and learn AIML files
        self.kernel = aiml.Kernel()
        self.kernel.setTextEncoding('UTF-8')
        self.kernel._elementProcessors['br'] = "\n" # Hack
        self.kernel.learn("aiml/startup.xml")
        self.kernel.respond("load alice")
        self.kernel.setBotPredicate("state", bot_predicate["state"])
        self.kernel.setBotPredicate("mother", bot_predicate["mother"])
        self.kernel.setBotPredicate("botmaster", bot_predicate["botmaster"])
        self.kernel.setBotPredicate("email", bot_predicate["email"])
        self.kernel.setBotPredicate("master", bot_predicate["master"])
        self.kernel.setBotPredicate("nationality", bot_predicate["nationality"])
        self.kernel.setBotPredicate("name", bot_predicate["name"])
        self.kernel.setBotPredicate("country", bot_predicate["country"])
        self.kernel.setBotPredicate("species", bot_predicate["species"])
        self.kernel.setBotPredicate("order", bot_predicate["order"])
        self.kernel.setBotPredicate("city", bot_predicate["city"])
        self.kernel.setBotPredicate("state", bot_predicate["state"])
        self.kernel.setBotPredicate("location", bot_predicate["location"])
        self.kernel.setBotPredicate("phylum", bot_predicate["phylum"])
        self.kernel.setBotPredicate("domain", bot_predicate["domain"])
        self.kernel.setBotPredicate("family", bot_predicate["family"])
        self.kernel.setBotPredicate("vocabulary", bot_predicate["vocabulary"])
        self.kernel.setBotPredicate("size", bot_predicate["size"])
        self.kernel.setBotPredicate("genus", bot_predicate["genus"])
        self.kernel.setBotPredicate("kindmusic", bot_predicate["kindmusic"])
        self.kernel.setBotPredicate("favortemovie", bot_predicate["favortemovie"])
        self.kernel.setBotPredicate("favoriteactress", bot_predicate["favoriteactress"])
        self.kernel.setBotPredicate("job", bot_predicate["job"])
        self.kernel.setBotPredicate("birthday", bot_predicate["birthday"])
        self.kernel.setBotPredicate("birthplace", bot_predicate["birthplace"])
        self.kernel.setBotPredicate("gender", bot_predicate["gender"])
        self.kernel.setBotPredicate("kingdom", bot_predicate["kingdom"]) #Yes I am a philosophy researcher
        self.kernel.setBotPredicate("religion", bot_predicate["religion"])
        self.kernel.setBotPredicate("python", bot_predicate["python"])
        self.kernel.setBotPredicate("party", bot_predicate["party"])
        self.kernel.setBotPredicate("sign", bot_predicate["sign"]) #smoke is a fire sign.
        self.kernel.setBotPredicate("faily", bot_predicate["faily"]) #Yes I am a robot
        self.kernel.setBotPredicate("arch", bot_predicate["arch"]) #Right now I am on a GNU/Linux
        self.kernel.setBotPredicate("president", bot_predicate["president"])
        self.kernel.setBotPredicate("friend", bot_predicate["friend"])
        self.kernel.setBotPredicate("girlfriend", bot_predicate["girlfriend"])
        self.kernel.setBotPredicate("show", bot_predicate["show"])
        self.kernel.setBotPredicate("favoriteactor", bot_predicate["favoriteactor"])
        self.kernel.setBotPredicate("celebrity", bot_predicate["celebrity"])
        self.kernel.setBotPredicate("celebrities", bot_predicate["celebrities"])
        self.kernel.setBotPredicate("favoriteartist", bot_predicate["favoriteartist"])
        self.kernel.setBotPredicate("hockeyteam", bot_predicate["hockeyteam"])
        self.kernel.setBotPredicate("baseballteam", bot_predicate["baseballteam"])
        self.kernel.setBotPredicate("footballteam", bot_predicate["footballteam"])
        self.kernel.setBotPredicate("favoriteactress", bot_predicate["favoriteactress"])
        self.kernel.setBotPredicate("favoriteauthor", bot_predicate["favoriteauthor"])
        self.kernel.setBotPredicate("etype", bot_predicate["etype"])
        self.kernel.setBotPredicate("emotions", bot_predicate["emotions"])
        self.kernel.setBotPredicate("ethics", bot_predicate["ethics"])
        self.kernel.setBotPredicate("feelings", bot_predicate["feelings"])
        self.kernel.setBotPredicate("favoritefood", bot_predicate["favoritefood"])
        
        bot_predicate_love = bot_predicate
        self.kernel_love = aiml.Kernel()
        self.kernel_love.setTextEncoding('UTF-8')
        self.kernel._elementProcessors['br'] = "\n" # Hack
        self.kernel_love.learn("aiml/startup_love.xml")
        self.kernel_love.respond("load alice")
        self.kernel_love.setBotPredicate("state", bot_predicate_love["state"])
        self.kernel_love.setBotPredicate("mother", bot_predicate_love["mother"])
        self.kernel_love.setBotPredicate("botmaster", bot_predicate_love["botmaster"])
        self.kernel_love.setBotPredicate("email", bot_predicate_love["email"])
        self.kernel_love.setBotPredicate("master", bot_predicate_love["master"])
        self.kernel_love.setBotPredicate("nationality", bot_predicate_love["nationality"])
        self.kernel_love.setBotPredicate("name", bot_predicate_love["name"])
        self.kernel_love.setBotPredicate("country", bot_predicate_love["country"])
        self.kernel_love.setBotPredicate("species", bot_predicate_love["species"])
        self.kernel_love.setBotPredicate("order", bot_predicate_love["order"])
        self.kernel_love.setBotPredicate("city", bot_predicate_love["city"])
        self.kernel_love.setBotPredicate("state", bot_predicate_love["state"])
        self.kernel_love.setBotPredicate("location", bot_predicate_love["location"])
        self.kernel_love.setBotPredicate("phylum", bot_predicate_love["phylum"])
        self.kernel_love.setBotPredicate("domain", bot_predicate_love["domain"])
        self.kernel_love.setBotPredicate("family", bot_predicate_love["family"])
        self.kernel_love.setBotPredicate("vocabulary", bot_predicate_love["vocabulary"])
        self.kernel_love.setBotPredicate("size", bot_predicate_love["size"])
        self.kernel_love.setBotPredicate("genus", bot_predicate_love["genus"])
        self.kernel_love.setBotPredicate("kindmusic", bot_predicate_love["kindmusic"])
        self.kernel_love.setBotPredicate("favortemovie", bot_predicate_love["favortemovie"])
        self.kernel_love.setBotPredicate("favoriteactress", bot_predicate_love["favoriteactress"])
        self.kernel_love.setBotPredicate("job", bot_predicate_love["job"])
        self.kernel_love.setBotPredicate("birthday", bot_predicate_love["birthday"])
        self.kernel_love.setBotPredicate("birthplace", bot_predicate_love["birthplace"])
        self.kernel_love.setBotPredicate("gender", bot_predicate_love["gender"])
        self.kernel_love.setBotPredicate("kingdom", bot_predicate_love["kingdom"]) #Yes I am a philosophy researcher
        self.kernel_love.setBotPredicate("religion", bot_predicate_love["religion"])
        self.kernel_love.setBotPredicate("python", bot_predicate_love["python"])
        self.kernel_love.setBotPredicate("party", bot_predicate_love["party"])
        self.kernel_love.setBotPredicate("sign", bot_predicate_love["sign"]) #smoke is a fire sign.
        self.kernel_love.setBotPredicate("faily", bot_predicate_love["faily"]) #Yes I am a robot
        self.kernel_love.setBotPredicate("arch", bot_predicate_love["arch"]) #Right now I am on a GNU/Linux
        self.kernel_love.setBotPredicate("president", bot_predicate_love["president"])
        self.kernel_love.setBotPredicate("friend", bot_predicate_love["friend"])
        self.kernel_love.setBotPredicate("girlfriend", bot_predicate_love["girlfriend"])
        self.kernel_love.setBotPredicate("show", bot_predicate_love["show"])
        self.kernel_love.setBotPredicate("favoriteactor", bot_predicate_love["favoriteactor"])
        self.kernel_love.setBotPredicate("celebrity", bot_predicate_love["celebrity"])
        self.kernel_love.setBotPredicate("celebrities", bot_predicate_love["celebrities"])
        self.kernel_love.setBotPredicate("favoriteartist", bot_predicate_love["favoriteartist"])
        self.kernel_love.setBotPredicate("hockeyteam", bot_predicate_love["hockeyteam"])
        self.kernel_love.setBotPredicate("baseballteam", bot_predicate_love["baseballteam"])
        self.kernel_love.setBotPredicate("footballteam", bot_predicate_love["footballteam"])
        self.kernel_love.setBotPredicate("favoriteactress", bot_predicate_love["favoriteactress"])
        self.kernel_love.setBotPredicate("favoriteauthor", bot_predicate_love["favoriteauthor"])
        self.kernel_love.setBotPredicate("etype", bot_predicate_love["etype"])
        self.kernel_love.setBotPredicate("emotions", bot_predicate_love["emotions"])
        self.kernel_love.setBotPredicate("ethics", bot_predicate_love["ethics"])
        self.kernel_love.setBotPredicate("feelings", bot_predicate_love["feelings"])
        self.kernel_love.setBotPredicate("favoritefood", bot_predicate_love["favoritefood"])


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

    def chat_log(self, human, robot, fwb):
        self.c.execute("INSERT INTO logs (chat_id, human, robot, fwb) VALUES (?,?,?,?)", ('', human, robot, fwb))
        self.conn.commit()
        
    def get_chat_info(self, chat_id):
        chat = self.c.execute("SELECT * FROM chats WHERE id=?", (chat_id,))
        chat = chat.fetchone()
        chat_info = {
            'hearts': 1,
            'fwb': 0,
            'fwb_start_datetime': 0,
            'msg_count': 0,
            'last_msg_datetime': 0,
            'proactive': 1
        }
        if not chat:
            self.c.execute("INSERT INTO chats (id, hearts, fwb, fwb_start_datetime, msg_count, last_msg_datetime, proactive) VALUES (?,?,?,?,?,?,?)", (chat_id, chat_info['hearts'], chat_info['fwb'], chat_info['fwb_start_datetime'], chat_info['msg_count'], chat_info['last_msg_datetime'], chat_info['proactive']))
            self.conn.commit()
        else:
            hearts = chat[2]
            fwb = chat[2]
            fwb_start_datetime = chat[3]
            msg_count = chat[4]
            last_msg_datetime = chat[5]
            proactive = chat[6]
            fwb_end = 0
            
            if fwb and time.time() - fwb_start_datetime > 60*60*24:
                fwb = 0
                fwb_start_datetime = 0
                self.c.execute("UPDATE chats SET fwb=?, fwb_start_datetime=? WHERE id=?", (0, 0, chat_id))
                self.conn.commit()
                fwb_end = 1
            
            chat_info = {
                'hearts': hearts,
                'fwb': fwb,
                'fwb_start_datetime': fwb_start_datetime,
                'msg_count': msg_count,
                'fwb_end': fwb_end,
                'last_msg_datetime': last_msg_datetime,
                'proactive': proactive
            }
        return chat_info
    
    def update_chat_lenght(self, chat_id):
        chat = self.c.execute("SELECT * FROM chats WHERE id=?", (chat_id,))
        chat = chat.fetchone()
        lenght = chat[4]
        self.c.execute("UPDATE chats SET msg_count=?, last_msg_datetime=strftime('%s','now') WHERE id=?", (lenght+1, chat_id))
        self.conn.commit()

    def get_chat_lenght(self, chat_id):
        chat = self.c.execute("SELECT msg_count FROM chats WHERE id=?", (chat_id,))
        chat = chat.fetchone()
        if chat:
            return chat[0]
        else:
            return None

    def get_stats(self):
        messages = self.c.execute("SELECT COUNT(*) FROM logs")
        messages = messages.fetchone()
        logs_count = messages[0]
        chats = self.c.execute("SELECT msg_count FROM chats")
        chats = chats.fetchall()
        if chats:
            average_lenght = 0.0
            if len(chats) > 0:
                average_lenght = logs_count / len(chats)
            stats = {
                'chats_count': len(chats),
                'average_lenght': average_lenght,
                'logs_count': logs_count
            }
            return stats
        else:
            return None
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

    def get_payments(self):
        # Test address 1MD8wCtnx5zqGvkY1VYPNqckAyTWDhXKzY
        
        addresses = [
            {'label': 'rDany01', 'address': '1JD5XxdAHZiHK9L2ExM4z2x7ZWuCqw4gUu'},
            {'label': 'rDany02', 'address': '1QHm5aWq16zcMiTgQQTfGx6vPeWhibAAKS'},
            {'label': 'rDany03', 'address': '1CzKXXm2kvjpGx37fBYvaKNZzFY4QnBf2j'},
            {'label': 'rDany04', 'address': '1MP2f7nTx9RD6U9q1oZLo4SEm1QHcdzvSv'},
            {'label': 'rDany05', 'address': '1CpYznqNAMo333xXHibr3kLZErP9VRhFxg'},
            {'label': 'rDany06', 'address': '145xN7JWtCFJgCR2XPy9tS7Ugo2j7BytdN'},
            {'label': 'rDany07', 'address': '13P8n6FXobDUtAhJf2S2qtX1wgJTGWqW2P'},
            {'label': 'rDany08', 'address': '1J9PHUtv442wqtUmk4kiQdQxrrhB4djKQ5'},
            {'label': 'rDany09', 'address': '16wrfY4w1X7ZQPNhQyvtvWfCz6JZkeFqeu'},
            {'label': 'rDany10', 'address': '14HtBouck7ktJnvWVe8WD9yE67TnLWomtn'},
        ]
        
        addresses_txt = ''
        for address in addresses:
            addresses_txt += '|{0}'.format(address['address'])
        addresses_txt = addresses_txt[1:]
        #url = 'https://blockchain.info/es/q/getreceivedbyaddress/{0}?confirmations=6'.format(addresses_txt)
        url = 'http://localhost:3000/merchant/$guid/balance?password='
        r = requests.get(url)
        amount = r.text
        print ( amount )

    def unlock_fwb(self, chat_id):
        chat = self.c.execute("SELECT fwb, hearts FROM chats WHERE id=?", (chat_id,))
        chat = chat.fetchone()
        hearts = chat[1]
        fwb = chat[0]
        if fwb:
            return True
        if hearts > 0:
            self.c.execute("UPDATE chats SET hearts=?, fwb=?, fwb_start_datetime=strftime('%s','now') WHERE id=?", (hearts-1, 1, chat_id))
            self.conn.commit()
            return True
        else:
            return False

    def lock_fwb(self, chat_id):
        self.c.execute("UPDATE chats SET fwb_start_datetime=? WHERE id=?", (0, chat_id))
        self.conn.commit()
    
    def set_proactivity(self, chat_id, proactive):
        self.c.execute("UPDATE chats SET proactive=? WHERE id=?", (proactive, chat_id))
        self.conn.commit()
    
    def proactive(self):
        last_time = time.time() - 60*60*24
        chat = self.c.execute("SELECT id FROM chats WHERE last_msg_datetime<? AND proactive=?", (last_time,1))
        chat = chat.fetchone()
        proactive_msg = {}
        if chat:
            chat_id = chat[0]
            proactive_msg[chat_id] = [{u'text':u'RANDOM PICKUP LINE', 'chat':{'id':chat_id}}]
        return proactive_msg
    
    def saveSession(self, session, chat_id):
        #print ("\nSessionInfo:")
        for predicate in session:
            if not predicate.startswith('_'):
                sess = self.c.execute("SELECT * FROM sessions WHERE id=? AND key=?", (chat_id, predicate))
                sess = sess.fetchone()
                if sess:
                    self.c.execute("UPDATE sessions SET value=? WHERE id=? AND key=?", (session[predicate], chat_id, predicate))
                    self.conn.commit()
                else:
                    self.c.execute("INSERT INTO sessions (id, key, value) VALUES (?,?,?)", (chat_id, predicate, session[predicate]))
                    self.conn.commit()
                #print ("{0}: {1}".format(predicate, session[predicate]))
    
    def loadSession(self, chat_id):
        sess = self.c.execute("SELECT * FROM sessions WHERE id=?", (chat_id,))
        sess = sess.fetchall()
        predicates = {}
        for predicate in sess:
            predicates[predicate[1]] = predicate[2]
        return predicates
        
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

            #self.get_payments()

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
            chats.update(self.proactive())
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
                    chat_info = self.get_chat_info(chat_id)

                    if chat_info['fwb']:
                        fwb_status = 'ENABLED'
                    else:
                        fwb_status = 'DISABLED'

                    if chat_info['proactive']:
                        proactivity_status = 'ENABLED'
                    else:
                        proactivity_status = 'DISABLED'
                        
                    # Text
                    if 'text' in message:
                        text = message['text']
                        msgs_commands = []
                        if text.startswith('/help'):
                            msgs_commands.append(['[Terminal Start]\nrDany can chat with you 😜\n@Eibriel\n\n/unlock Friends with Benefits ❤️\n\nUse /start /stop to enable and disable Proactivity.\n\nRate rDanyBot ⭐️\nhttps://telegram.me/storebot?start=rdanybot\n[Terminal End]'])
                            self.send_msg(msgs_commands, chat_id)
                            self.chat_log('/help', '', chat_info['fwb'])
                            continue
                        elif text.startswith('/start'):
                            self.set_proactivity(chat_id, True)
                            msgs_commands.append(['[Terminal Start]\nWelcome!!\n/unlock Friends with Benefits ❤️\nUse /help to get more info.\nProactivity enabled, use /stop to disable it.\n[Terminal End]'])
                            self.send_msg(msgs_commands, chat_id)
                            self.chat_log('/start', '', chat_info['fwb'])
                            continue
                        elif text.startswith('/stop'):
                            self.set_proactivity(chat_id, False)
                            msgs_commands.append(['[Terminal Start]\nProactivity disabled.\nUse /start to enable it again.\n[Terminal End]'])
                            self.send_msg(msgs_commands, chat_id)
                            self.chat_log('/stop', '', chat_info['fwb'])
                            continue
                        elif text.startswith('/settings'):
                            msgs_commands.append(['[Terminal Start]\nFriend with Benefits: {0}\n/unlock Friends with Benefits ❤️\n\nProactivity: {1}\nUse /start /stop to enable and disable\n[Terminal End]'.format(fwb_status, proactivity_status)])
                            self.send_msg(msgs_commands, chat_id)
                            self.chat_log('/settings', '', chat_info['fwb'])
                            continue
                        elif text.startswith('/interference'):
                            msgs_commands.append(['[Terminal Start]\nInterfence level: {0}% {1}\n[Terminal End]'.format(random.randint(5, 15), self.emoji_earth_wireframe)])
                            self.send_msg(msgs_commands, chat_id)
                            self.chat_log('/interference', '', chat_info['fwb'])
                            continue
                        elif text.startswith('/chats'):
                            chats_stats = self.get_stats()
                            msgs_commands.append(['[Terminal Start]\nChats: {0}\nAverage lenght: {1}\nMesages: {2}\n[Terminal End]'.format(chats_stats['chats_count'], chats_stats['average_lenght'], chats_stats['logs_count'])])
                            self.send_msg(msgs_commands, chat_id)
                            continue
                        elif text.startswith('/no'):
                            msgs_commands.append(['[Terminal Start]\nWhait a while.\n[Terminal End]'])
                            self.send_msg(msgs_commands, chat_id)
                            self.chat_log('/no', '', chat_info['fwb'])
                            continue
                        elif text.startswith('/yes'):
                            msgs_commands.append(['[Terminal Start]\nFriend with Benefits: {0}\n\nThis will allow rDany to have romantic feelings with you 💋\n/unlock_now 1 ❤️\n\nOne heart unlocks 24 hours.\nYou have {1} heart/s, /buy 10 hearts with only 0.05 BTC\n[Terminal End]'.format(fwb_status, chat_info['hearts'])])
                            self.send_msg(msgs_commands, chat_id)
                            self.chat_log('/yes', '', chat_info['fwb'])
                            continue
                        elif text.startswith('/unlock_now'):
                            if self.unlock_fwb(chat_id):
                                msgs_commands.append(['[Terminal Start]\nUnlocked, enjoy!\n[Terminal End]'])
                            else:
                                msgs_commands.append(['[Terminal Start]\nSorry, you have not enough hearts.\n/buy 10 hearts with only 0.05 BTC.\n/unlock for more info.\n[Terminal End]'])
                            self.send_msg(msgs_commands, chat_id)
                            self.chat_log('/unlock_now', '', chat_info['fwb'])
                            continue
                        elif text.startswith('/unlock'):
                            msgs_commands.append(['[Terminal Start]\nAre you older than 18? /yes /no\n[Terminal End]'])
                            self.send_msg(msgs_commands, chat_id)
                            self.chat_log('/unlock', '', chat_info['fwb'])
                            continue
                        elif text.startswith('/lock'):
                            self.lock_fwb(chat_id)
                            msgs_commands.append(['[Terminal Start]\nLocked\n[Terminal End]'])
                            self.send_msg(msgs_commands, chat_id)
                            self.chat_log('/lock', '', chat_info['fwb'])
                            continue
                        elif text.startswith('/buy'):
                            msgs_commands.append(['[Terminal Start]\nSend 0.05 BTC (or more) to this address: .\n[Terminal End]'])
                            self.send_msg(msgs_commands, chat_id)
                            self.chat_log('/buy', '', chat_info['fwb'])
                            continue

                        if text[0] == '/':
                            text = text[1:]
                        elif text[0:9] == '@rDanyBot ':
                            text = text[10:]

                    self.update_chat_lenght(chat_id)
                    chat_lenght = self.get_chat_lenght(chat_id)
                    #print ('chat lenght {0}'.format(chat_lenght))

                    predicates = self.loadSession(chat_id)
                    for predicate in predicates:
                        self.kernel_love.setPredicate(predicate, predicates[predicate], chat_id)
                        self.kernel.setPredicate(predicate, predicates[predicate], chat_id)

                    if chat_info['fwb']:
                        #self.kernel_love.setPredicate("name", "Dear", chat_id)
                        response = self.kernel_love.respond(text, chat_id)
                        self.saveSession(self.kernel_love.getSessionData(chat_id), chat_id)
                    else:
                        response = self.kernel.respond(text, chat_id)
                        self.saveSession(self.kernel.getSessionData(chat_id), chat_id)
                        
                    self.chat_log(text, response, chat_info['fwb'])
                    #print (response)
                    if response == '':
                        response = ':P'

                    msgs.append([response])

                    #if 0 == chat_lenght % 10 and chat_lenght <= 30:
                    if random.randint(0, 100) > 95:
                        msgs_commands.append(['[Terminal Start]\nRate rDanyBot ⭐️\nhttps://telegram.me/storebot?start=rdanybot\n[Terminal End]'])
                        self.send_msg(msgs_commands, chat_id)
                        
                    if chat_info['fwb_end']:
                        msgs_commands.append(['[Terminal Start]\nFriend with Benefits finished\n/unlock again\n[Terminal End]'])
                        self.send_msg(msgs_commands, chat_id)

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
