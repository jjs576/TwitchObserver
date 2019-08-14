import requests
import time

from utils import *

class User:
    def __init__(self,_user_id,_user_name):
        self.user_id = _user_id
        self.user_name = _user_name

class Finder:
    def __init__(self, _user_name):
        self.headers = {'Client-ID': 'd7f9ki5mmw2t8ogxphzdgyqaheglmt',}
        self.debug = False
        self.language = 'ko'
        self.streamer = []
        
        self.target = _user_name

        self.module_name = '(Finder)'
        
    def SetLanguage(self, _lang):
        self.language = _lang
        print_log(self.module_name + ' SetLanguage to ' + _lang)
        
    
    def GetStreamerIds(self):
        url = 'https://api.twitch.tv/helix/streams?first=100&language=' + self.language
        response = requests.get(url, headers=self.headers)
        if response.status_code is not 200:
            print_log(self.module_name + ' Error GetStreamerIds')
            return
        resjson = response.json()
        
        #print_log('Finder GET stream')

        
        for i in range(len(resjson['data'])):
            self.streamer.append(User(resjson['data'][i]['user_id'],''))
            
        if self.debug:
            print_log(self.module_name+ ' GetStreamids')
   
    def GetStreamerNames(self):
        url = 'https://api.twitch.tv/helix/users?'
    
        for s in self.streamer:
            url = url + 'id=' + s.user_id + '&'
        url = url[:-1]
        response = requests.get(url, headers=self.headers)
        if response.status_code is not 200:
            print_log(self.module_name + ' Error GetStreamerNames')
            return
        resjson = response.json()
        #print_log('Finder GET users')
    
        
        for i in range(len(resjson['data'])):
            self.streamer[i].user_name = (resjson['data'][i]['login'])
            
        if self.debug:
            print_log(self.module_name + ' GetStreamerNames')

    def RefreshList(self):
        self.streamer = []
        self.GetStreamerIds()
        self.GetStreamerNames()

    
    def FindUser(self, streamer_name):
        url = "http://tmi.twitch.tv/group/user/" + streamer_name +  "/chatters"

        response = requests.get(url)
        if response.status_code is not 200:
            print_log(self.module_name + ' Error FindUser')
            return False

        chatter_list = requests.get(url).json()
        chatter_type = ['broadcaster','vips','moderators','staff','admins','global_mods','viewers']

        if self.debug:
            print_log(self.module_name + ' GET ' + streamer_name+ '/chatters')

        for t in chatter_type:
            index = binary_search(chatter_list['chatters'][t],self.target)
            if index >= 0:
                return True
        return False

    def FindUserByChannels(self):
        result = []
        for s in self.streamer:
            if(self.FindUser(s.user_name)):
                result.append(s.user_name)
        return result

    def Run(self):
        while True:
            self.RefreshList()
            result = self.FindUserByChannels()
            resultString = ''
            for r in result:
                resultString = resultString + r + ', '
            resultString = resultString[:-2]
            print_log(self.module_name + ' ' + resultString)
            time.sleep(180)
    
if __name__ == "__main__":
    n = input()
    finder = Finder(n)
    finder.Run()
