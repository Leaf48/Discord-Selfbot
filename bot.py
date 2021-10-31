from rich import print
from proxy import Proxy

proxyClient = Proxy()

# print(proxyClient.PROXY)

# proxyClient.checkAvailableProxy()

# print(proxyClient.PROXY)

proxyList = proxyClient.sortProxyTXT()
a = proxyClient.checkRandomProxies(proxyList, False)