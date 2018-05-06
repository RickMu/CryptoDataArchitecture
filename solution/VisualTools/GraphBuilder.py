from solution.VisualTools.graph.customgraph import CustomGraph

class GraphBuilder:

    def __init__(self):
        self._graphs = []

    def addGraph(self):
        g = CustomGraph()
        self._graphs.append(g)
        return self

    def addPlot(self,tuples):

        if tuples[1] != "" and CustomGraph.TRUNCATE_LENGTH < tuples[1]:
            CustomGraph.TRUNCATE_LENGTH = tuples[1]

        self._graphs[-1].addPlot(tuples)
        return self

    def Graph(self,app):
        for i in self._graphs:
            app.addGraph(i)

