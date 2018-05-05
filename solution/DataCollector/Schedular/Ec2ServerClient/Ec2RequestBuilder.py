
import datetime
from solution.DataCollector.Schedular import ApiEndPoints
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

    def __buildFindInBetweenRequest(self, ticker, start_datetime, timespan):

        self.Service(Ec2RequestBuilder.Services.FindInBetween)
        self.Query()

        self.database('gdx')

        self.AND()
        self.Market(ticker)

        dateInString = self.__dateTimeToString(start_datetime)
        self.AND()
        self.Date(dateInString)
        self.AND()
        self.Day(timespan[0])
        self.AND()
        self.Hour(timespan[1])

        return self.getRequest()

    def __dateTimeToString(self,date):
        format =  '%Y-%m-%dT%H:%M'
        d = datetime.datetime.strftime(date,format)
        return d

    def buildFetchRequest(self,ticker, timespan = None):
        if timespan is None:
            raise Exception("TimeSpan for EC2 shouldn't be none")
        serverTime = datetime.datetime.utcnow()+datetime.timedelta(hours=11)
        dates, timespans = self.formBatchRequest(serverTime,timespan)

        rqs = []
        for date,timespan in zip(dates,timespans):
            rq = self.__buildFindInBetweenRequest(ticker, date, timespan)
            rqs.append(rq)
        return rqs

    def formBatchRequest(self, start_time, timespan):
        #gonna hard code a 5 here
        timespans = []
        start_times = [start_time]
        timespan = [timespan[0],timespan[1]]
        intervalTime = 5

        while timespan[0] - intervalTime  >= 0:
            t = (intervalTime,0)
            timespans.append(t)

            new_date = start_times[-1] - datetime.timedelta(days = intervalTime)
            start_times.append(new_date)
            timespan[0] -= intervalTime

        timespans.append((timespan[0],timespan[1]))

        return start_times,timespans




if __name__ == "__main__":
    requestBuilder =  Ec2RequestBuilder()
    start_date = datetime.datetime.utcnow()+datetime.timedelta(hours=11)
    #rq = requestBuilder.buildFetchRequest('BTC-USD',(1,1))
    #print(rq)

    requests = requestBuilder.buildFetchRequest("BTC-USD", (10,1))

    print(requests)
