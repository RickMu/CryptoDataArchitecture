from abc import abstractmethod
from solution.server.database.mongodb import MongoRepo
from solution.server.database.CollectionNames import TickerToCollectionMap
import datetime
import json
from google.protobuf import json_format
import solution.server.cointrade_pb2 as cointrade_pb
class RequestHandler:

    @abstractmethod
    def _checkQueryParams(self,params):
        return

    @abstractmethod
    def executeQuery(self,params):
        return

class FindInBetweenRequestHandler(RequestHandler):

    PARAMS = ['database', 'market', 'start_date','day','hour']
    def _checkQueryParams(self,params):

        for i in FindInBetweenRequestHandler.PARAMS:
            if i not in params:
                return False
        return True

    def executeQuery(self,params):
        if not self._checkQueryParams(params):
            return None

        format = "%Y-%m-%dT%H:%M"


        databaseName = params['database'][0].capitalize()
        collectioName = TickerToCollectionMap.Map[params['market'][0]]
        client = MongoRepo( databaseName , collectioName)

        start_date = params['start_date'][0]
        start_date = datetime.datetime.strptime(start_date,format)

        end_date = start_date - datetime.timedelta(days = int(params['day'][0]), hours = int(params['hour'][0]))
        start_date = start_date.isoformat() + "+11:00"
        end_date = end_date.isoformat() + "+11:00"
        print(start_date)
        print(end_date)
        result = client.findInBetweenTime(start_date,end_date)

        tradeSet = self._jsonToTradeSet(list(result))
        parsed_pb = tradeSet.SerializeToString()

        return parsed_pb
    def _jsonToTradeSet(self,jsonList):
        tradeSet = cointrade_pb.Trades()
        for json in jsonList:
            trade = tradeSet.trades.add()
            self._jsonToTradeMessage(json,trade)

        return tradeSet

    def _jsonToTradeMessage(self,json, trade):
        trade.price = json['price']
        trade.side = json['side']
        trade.created_at = json['created_at']
        trade.id = json['id']
        trade.volume = json['volume']
        if json['trend'] is not None:
            trade.trend = json['trend']



if __name__ == "__main__":
    client = MongoRepo("Gdx", "bitcoin")
    c = client.findAll()

    for i in c:
        print(i)


    print("OK")