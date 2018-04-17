import urllib.request
import json
from enum import Enum

from solution.Schedular.IClient.IApiBuilder import IApiBuilder
from solution.Schedular import ApiEndPoints
class ServerRequest:
    class Services:
        FindInBetween = 'findinbetween'



    request = \
        'http://ec2-35-169-63-106.compute-1.amazonaws.com/findinbetween?database=gdx&market=ETH-USD&start_date=2018-04-17T08:36&day=0&hour=3'
    def __init__(self):

        self.rq = ApiEndPoints.EndPoints[ApiEndPoints.EndPointProviders.EC2]
        self.p = PARAMS()

    def database(self, db):
        self.rq += (PARAMS.DB + "=" + db.Name)
        return self

    def getRequest(self):
        request = self.rq
        self.clear()
        return request

    def clear(self):
        self.rq = ServerRequest.DNS  # +str(self.portnumber)

    def Service(self, service):
        self.rq += ("/" + service)
        return self

    def Query(self):
        self.rq += "?"
        return self

    def AND(self):
        self.rq += "&"
        return self

    def Date(self, date):
        self.rq += (PARAMS.START_DATETIME + "=" + str(date))

    def Day(self, day):
        self.rq += (PARAMS.DAY + "=" + str(day))
        return self

    def Hour(self, hour):
        self.rq += (PARAMS.HOUR + "=" + str(hour))
        return self

    def Minute(self, minute):
        self.rq += (PARAMS.MINUTE + "=" + str(minute))
        return self

    def Market(self, market):
        self.rq += (PARAMS.MARKET + "=" + str(market))
        return self

    def buildFindAllRequest(self, market):

        self.Service(ServerService.FindAll)
        self.Query()
        if (market is None):
            raise Exception("Market cannot be None")
        else:
            self.Market(market)

        return self.getRequest()

    def buildFindInBetweenRequest(self, ticker, s_year, s_month, s_day, s_hour, s_minute, to_day, to_hour=0):
        self.Service(ServerRequest.Services.FindInBetween)
        self.Query()
        self.AND()
        self.Market(ticker)

        date = self.p.constructStartDate(s_year, s_month, s_day, s_hour, s_minute)
        self.AND()
        self.Date(date)

        if (to_day is not None):
            self.AND()
            self.Day(to_day)
        if (to_hour is not None):
            self.AND()
            self.Hour(to_hour)

        return self.getRequest()

