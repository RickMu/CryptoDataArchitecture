import time
import urllib.request
import urllib.parse
import urllib.error
from threading import Thread
import solution.server.cointrade_pb2 as cointrade_pb2

def getRequest(url):

    with urllib.request.urlopen(url) as response:
        raise Exception("Fail Whale")
        body = response.read()

        print(body)

def load_test():
    t0 = time.time()
    threads = []
    for i in range(2):
        thread=Thread(target=getRequest, args= ('http://localhost:10001/findinbetween?database=gdx&market=BTC-USD&start_date=2018-05-05T20:03&day=0&hour=1',))
        thread.start()
        threads.append(thread)
    for i in threads :
        i.join()
    print(str(time.time()-t0))

def protobuf_test():
    request = "http://ec2-35-169-63-106.compute-1.amazonaws.com/findinbetween?database=gdx&market=BTC-USD&start_date=2018-05-05T20:03&day=0&hour=1"
    t0 = time.time()
    with urllib.request.urlopen(request) as response:
        body = response.read()
    trades = cointrade_pb2.Trades()
    trades.ParseFromString(body)
    print(trades)

    print(str(time.time() - t0))
    return trades

if __name__ == "__main__":

    load_test()
