from pymongo import MongoClient


class MongoRepo:

    def __init__(self,db, collection):
        self.source = MongoClient('localhost', 27017)[db][collection]

    def findAll(self):
        return self.source.find({},{'_id':0})

    def findLastTrade(self):
        return self.findMax("id")

    def findMax(self, column):
        return self.sort(column, limit=1)

    def findMin(self, column):
        return self.sort( column, ascending=False, limit=1)

    def sort(self, column, largestFirst=True, limit=None):
        order = -1
        if (largestFirst == False):
            order = 1
        if (limit is not None):
            return self.source.find(projection={"_id":False}).sort([(column, order)]).limit(limit)
        return self.source.find(projection={"_id":False}).sort([(column, order)]).limit(100)

    def findAfterTime(self, time):
        return self.source.find({'created_at': {'$gt': time}},{"_id":0})

    def findInBetweenTime(self,top_limit, bottom_limit):
        return self.source.find({'created_at': {'$gte': bottom_limit, "$lt":top_limit}}, projection={"_id": 0})


