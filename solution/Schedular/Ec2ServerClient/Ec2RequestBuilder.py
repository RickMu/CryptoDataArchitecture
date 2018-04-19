import urllib.request
import json
from enum import Enum

from solution.Schedular.IClient.IApiBuilder import IApiBuilder
import datetime
from solution.Schedular import ApiEndPoints
class Ec2RequestBuilder:

    class Services:
        FindInBetween = 'findinbetween'

    def __init__(self):
        self._endpoint = ApiEndPoints.EndPoints.endPoints[ApiEndPoints.EndPointProviders.EC2]
        self._cachedRequest = self._endpoint

    def database(self, db):
        self._cachedRequest += ("database=" + db)
        return self

    def getRequest(self):
        request = self._cachedRequest
        self.clear()
        return request

    def clear(self):
        self._cachedRequest = self._endpoint  # +str(self.portnumber)

    def Service(self, service):
        self._cachedRequest += ("/" + service)
        return self

    def Query(self):
        self._cachedRequest += "?"
        return self

    def AND(self):
        self._cachedRequest += "&"
        return self

    def Date(self, date):

        self._cachedRequest += ("start_date=" + str(date))

    def Day(self, day):

        self._cachedRequest += ("day=" + str(day))
        return self

    def Hour(self, hour):

        self._cachedRequest += ("hour=" + str(hour))
        return self

    def Minute(self, minute):

        self._cachedRequest += ("minute=" + str(minute))
        return self

    def Market(self, market):

        self._cachedRequest += ("market=" + str(market))
        return self

    def buildFindAllRequest(self, market):

        self.Service(Ec2RequestBuilder.Service.FindAll)
        self.Query()
        if (market is None):
            raise Exception("Market cannot be None")
        else:
            self.Market(market)

        return self.getRequest()

    def buildFindInBetweenRequest(self, ticker, start_datetime, timespan):

        self.Service(Ec2RequestBuilder.Services.FindInBetween)
        self.Query()

        self.database('gdx')

        self.AND()
        self.Market(ticker)

        dateInString = self.dateTimeToString(start_datetime)
        self.AND()
        self.Date(dateInString)
        self.AND()
        self.Day(timespan[0])
        self.AND()
        self.Hour(timespan[1])

        return self.getRequest()

    def dateTimeToString(self,date):
        format =  '%Y-%m-%dT%H:%M'
        d = datetime.datetime.strftime(date,format)
        return d

if __name__ == "__main__":
    from solution.Schedular.Tickers import Tickers
    requestBuilder =  Ec2RequestBuilder()
    start_date = datetime.datetime.utcnow()+datetime.timedelta(hours=11)
    rq = requestBuilder.buildFindInBetweenRequest('BTC-USD',start_date,(1,1))
    print(rq)

