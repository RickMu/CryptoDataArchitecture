import sys
sys.path.append("B:\\MyGit\\CryptoCoin")
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import urllib.parse
import urllib.error
from threading import Thread
import time

from solution.server.request_handler import FindInBetweenRequestHandler


class ThreadedServer(HTTPServer):
    def process_request(self, request, client_address):
        thread = Thread(target=self.__new_request, args=(self.RequestHandlerClass, request, client_address, self))
        thread.start()

    def __new_request(self, handlerClass, request, address, server):
        handlerClass( request, address, server)
        self.shutdown_request(request)

class FascadeHandler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        time.sleep(2)
        parseResult = urllib.parse.urlparse(self.path)
        print(parseResult)
        self.worker(parseResult)

        #t = Thread( target=  self._handleRequest ,args = (queryString,))
        #t.start()

    def worker(self,parseResult):
        path = parseResult.path.replace("/","")
        queryString = parseResult.query
        param_dict = urllib.parse.parse_qs(queryString)
        try:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            returnValue = ServiceProvider().execute(path, param_dict)


            if returnValue is not None:
                self.wfile.write(returnValue)
        except:
            print("Exception ")




    def _handleRequest(self,queryString):
        self.send_response(200)
        self.send_header('Content-type', 'altcoin/html')
        self.end_headers()
        self.wfile.write(bytes(queryString,'utf-8'))


class ServiceProvider:

#http://ec2-35-169-63-106.compute-1.amazonaws.com/findinbetween?database=gdx&market=BTC-USD&start_date=2018-05-05T05:03&day=3&hour=1

    def __init__(self):
        self.router = {
            "":self.default,
            "findinbetween": self.findInBetween
        }

    def getRoutes(self):
        return self.router.keys()

    def execute(self,key,parameter):
        try:
            return self.router[key](parameter)
        except:
            #probably should log if request isn't found
            print("Path not found: "+ str(key))
            return None

    def default(self,param):

        return bytes("<!DOCTYPE html><html><head><title>Title goeself here.</title></head>"
              "<body><h1>OK</h1></body></html>", "utf-8")

    def findInBetween(self,param):

        result = FindInBetweenRequestHandler().executeQuery(param)

        return result


def run():
    try:
        #Create a web server and define the handler to manage the
        #incoming request

        allhosts = '0.0.0.0'
        localhost = 'localhost'
        server = ThreadedServer(( 'localhost', 10001), FascadeHandler)

        print("Server Started ...")
        #Wait forever for incoming htto requests
        server.serve_forever()

    except KeyboardInterrupt:
        print ('^C received, shutting down the web server')
        server.socket.close()

if __name__ == '__main__':

    serverThread = Thread(target=run)
    serverThread.start()