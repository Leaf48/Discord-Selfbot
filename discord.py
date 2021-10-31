import requests
from requests.api import request
import urllib3
from random import randrange, choice
from rich import print
from proxy import Proxy

urllib3.disable_warnings()

class Discord:

    ENDPOINT = "https://discord.com/api/v9/"

    HEADERS = {
        "cookie": "",
        "Authorization": "",
        "Content-Type": "application/json"
    }

    TARGET = None

    def __init__(self, proxy, target, token=HEADERS["Authorization"]) -> None:
        self.token = token
        self.TARGET = target
        self.proxy = {"https": proxy}

    def postRequest(self, url, payload={}):
        response = requests.post(url=self.ENDPOINT + url, json=payload, headers=self.HEADERS, proxies=self.proxy, verify=False, timeout=10)
        print(response.json())
        return response

    def getRequest(self, url, payload={}):
        response = requests.get(url=self.ENDPOINT + url, headers=self.HEADERS, proxies=self.proxy, verify=False, timeout=10)
        print(response.json())
        return response

    def sendDM(self, payload={}, targetID=TARGET):
        payload_dm = {"recipient_id": targetID}
        makeDM = self.postRequest(f"users/@me/channels", payload_dm).json()
        print(makeDM)
        channelID = makeDM["id"]

        # testPayload = {
        #     "content": "Hello, World!",
        #     "tts": True,
        #     "embeds": [
        #         {
        #             "title": "Hello, Embed!",
        #             "description": "This is an embedded message."
        #         }
        #     ]
        # }
        
        self.postRequest(f"channels/{channelID}/messages", payload).json()

    # 参加してるサーバーのIDをリスト化します
    def get_allserver_id(self):
        guilds = self.getRequest("users/@me/guilds").json()
        guildList = [i["id"] for i in guilds]
        print(guildList)
        return guildList

    def sendDMall(self, payload={}):
        guildlist = self.get_allserver_id()

        

        for i in guildlist:
            res = self.getRequest(f"guilds/{i}").json()
            print(res)


client = Proxy()
proxylist = client.sortProxyTXT()
proxyget = client.checkRandomProxies(proxylist)
# currentproxy = client.checkAvailableProxy()

test = Discord(proxyget, "")

# message = {
#             "content": "こんばんは",
#             "tts": True,
#         }
# test.sendDM(message)

test.get_allserver_id()