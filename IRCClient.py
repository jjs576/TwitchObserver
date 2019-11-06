import re
import socket
import math
import random
from utils import print_log

class IRCClient:
    def __init__(self, _target):
        self.host = 'irc.twitch.tv'
        self.port = 6667
        
        self.set_nickname()
        self.oauth = "oauth:SCHMOOPIIE"
        self.joined = set([])
        self.data = ""
        self.target = _target

        self.module_name = '(IRCClient)'

    def set_nickname(self):
        self.nick = 'justinfan' + str(math.floor((random.random() * 80000)) + 1000)
        
    def connect(self):
        self.con = socket.socket()
        self.con.connect((self.host, self.port))
        
        self.send_pass(self.oauth)
        self.send_nick(self.nick)

    def send_pong(self, msg):
        self.con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))

    def send_message(self, chan, msg):
        self.con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))

    def send_nick(self, nick):
        self.con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))

    def send_pass(self, password):
        self.con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))

    def join_channel(self, chan):
        self.con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))

    def part_channel(self, chan):
        self.con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))


    def join_and_part(self, channels):
        join_list = set(channels) - self.joined
        part_list = self.joined - set(channels)

        for c in list(join_list):
            print_log(self.module_name + ' JOIN ' + c)
            #write_log(self.target, self.module_name + ' JOIN ' + c)
            self.join_channel('#' + c)
            self.joined.add(c)
        for c in list(part_list):
            print_log(self.module_name + ' PART ' + c)
            #write_log(self.target, self.module_name + ' PART ' + c)
            self.part_channel('#' + c)
            self.joined.remove(c)

    def get_sender(self, msg):
        result = msg.split('!')[0]
        return result[1:]
    
    def get_channel(self, msg):
        result = msg[1:]
        return result
        
    def get_message(self, msg):
        result = ''
        message_list = msg[3:]
        for s in message_list:
            result = result + s + ' '

        result = result[1:-1]
        return result

    def reconnect(self):
        print_log(self.module_name + ' reconnect')
        self.set_nickname()
        self.connect()
        for c in list(self.joined):
            self.join_channel('#' + c)


    def read_process(self):
        if not self.joined:
            return
        try:
            self.data = self.data + self.con.recv(1024).decode('UTF-8')
            data_split = re.split(r"[\r\n]+", self.data)
            self.data = data_split.pop()

            for line in data_split:
                line = str.rstrip(line)
                line = str.split(line)

                if len(line) >= 1:
                    if line[0] == 'PING':
                        self.send_pong(line[1])

                    if line[1] == 'PRIVMSG':
                        sender = self.get_sender(line[0])
                        channel_name = line[2]
                        message = self.get_message(line)

                        print_message = self.module_name + ' '  + channel_name + ' ' + sender + ": " + message
                        if sender == self.target:
                            print_log(print_message)
                            #write_log(self.target, print_message)

        except socket.error:
            print_log(self.module_name + ' Socket died')
            self.reconnect()
            

        except socket.timeout:
            print_log(self.module_name + ' Socket timeout')
            self.reconnect()
            
            
        except IndexError:
            print_log(self.module_name + ' IndexError')

        except UnicodeDecodeError:
            print_log(self.module_name + ' UnicodeDecodeError')
