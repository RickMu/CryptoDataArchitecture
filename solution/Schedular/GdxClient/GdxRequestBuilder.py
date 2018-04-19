import urllib.request
import json
from solution.Schedular.IClient.IApiBuilder import IApiBuilder
from solution.Schedular import ApiEndPoints
class GdxApiBuilder(IApiBuilder):
    class Services:
        TRADES = 'trades'

    def __init__(self):
        self._endPoint = ApiEndPoints.EndPoints.endPoints[ApiEndPoints.EndPointProviders.Gdx]
        self._cachedRequest = self._endPoint

    def clear(self):
        self._cachedRequest = self._endPoint
        return self
    def getRequest(self):
        api = self._cachedRequest
        self.clear()
        return api

    def products(self):
        self._cachedRequest += "/products"
        return self

    def currency(self, ticker):
        self._cachedRequest += "/products/" + ticker
        return self

    def limit(self, lim):
        self._cachedRequest += "limit=" + str(lim)
        return self

    def service(self, service):
        self._cachedRequest += "/" + service
        return self

    def PARAMS(self):
        self._cachedRequest += "?"
        return self

    def before(self, id):
        self._cachedRequest += "before=" + str(id)
        return self

    def after(self, id):
        self._cachedRequest += "after=" + str(id)
        return self

    def builFetchRequestGivenId(self, ticker, id):
        request= self.currency(ticker).service(GdxApiBuilder.Services.TRADES) \
            .PARAMS().before(id).getRequest()
        return request

    def builFetchRequest(self,ticker):
        request = self.currency(ticker).service(GdxApiBuilder.Services.TRADES) \
            .getRequest()
        return request



if __name__ == "__main__":
    import pandas as pd
