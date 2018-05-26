from solution.VisualTools.graph.customgraph import CustomGraph

class GraphBuilder:

    def __init__(self):
        self._graphs = []
        self._indicatorTuples = []

    def addGraph(self):
        g = CustomGraph()
        self._graphs.append(g)
        return self

    def getIndicatorTuples(self):
        return self._indicatorTuples

    def _toIdentifier(self,idTuple:tuple) -> str:
        return str(idTuple[0]) + str(idTuple[1])

    def addPlot(self,tuples, symbol_brush = 'w'):

        if tuples[1] != "" and CustomGraph.TRUNCATE_LENGTH < tuples[1]:
            CustomGraph.TRUNCATE_LENGTH = tuples[1]
        self._indicatorTuples.append(self._toIdentifier(tuples))
        self._graphs[-1].addPlot(tuples, symbol_brush)
        return self

    def Graph(self,app):
        for i in self._graphs:
            app.addGraph(i)

