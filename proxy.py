import requests
import urllib3
from random import randrange, choice
from rich import print

urllib3.disable_warnings()

class Proxy:
    URL = "https://api.my-ip.io/ip.json"
    PROXY = None

    # ProxyScrapeを使う場合
    def proxyScrapeAPI():
        PROXYSCRAPEAPI = f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=500&country=all&ssl=all&anonymity=all"
        proxies = requests.get(PROXYSCRAPEAPI).content.decode()
        proxyConvert = proxies.replace("b'", "").replace("\r\n", "\n")
        # print(proxyConvert)

        proxyList = proxyConvert.splitlines()
        # print(proxyList)
        # print(len(proxyList))
        return proxyList

    # Proxyが利用可能かチェック
    def checkAvailableProxy(self, path="availableProxy.txt"):
        with open(path, "r+") as f:
            availableProxies = f.read().splitlines()
            print(availableProxies)

            for i in availableProxies:
                avProxy = {"https": i}
                try:
                    resp = requests.get(url=self.URL, verify=False, proxies=avProxy, timeout=10).json()

                    print(f"""
    使用可能なIPだったので利用可能プロキシリストから使用しました
    Status: SUCCESS!
    IP:     {resp["ip"]}
    TYPE:   {resp["type"]}
                    """)

                    self.PROXY = avProxy["https"]
                    return True

                except Exception as e:
                    print(e)
                    lines = f.readlines()
                    f.writelines(lines[1:])

                    print(f"""
    使用不可なIPだったので利用可能プロキシリストから削除しました
    IP : {avProxy["https"]}
                    """)        

    # 外部から取り込んだproxy.txtをソートする
    # 返り値でProxyList.txt等にする場合もこれを使う
    def sortProxyTXT(self, path="proxy.txt"):
        proxies = []
        with open(path, "r") as f:
            p = f.readlines()
            for i in p:
                # print(i.strip())
                proxies.append(i.strip())
        print(proxies)
        return proxies

    # proxy.txtの中からランダムにプロキシを選択していき、使用可能なプロキシを発見した場合にのみ停止する
    def checkRandomProxies(self, proxyList, check=False, path="proxy.txt"):
        First = True
        while not check:
            if First:
                print("利用可能プロキシリストが使用不可なのでランダムにプロキシをチェックします")
                First = False
                
            try:
                proxy = {
                    "https": choice(proxyList)
                }
                print(f"Trying to check ip: {proxy['https']}")
                resp = requests.get(url=self.URL, verify=False, proxies=proxy, timeout=10).json()
                print(f"""
        Status: SUCCESS!
        IP:     {resp["ip"]}
        TYPE:   {resp["type"]}
                """)
                
                with open("availableProxy.txt", "a+") as f:
                    if proxy["https"] in f.read():
                        print("既に同じIPアドレスがあるので書き込みません")
                        break
                    else:
                        f.write(f"{proxy['https']}\n")
                        print("新たにIPを書き込みました")
                        print("今回はこのプロキシを使用します")
                        self.PROXY = proxy['https']
                break
            except Exception as e:
                print(e)