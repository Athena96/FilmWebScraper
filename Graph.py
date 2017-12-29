import json
from Vertex import Movie, Actor

class Graph:
    '''

    Class: Graph
        A Graph data structure represented by a dictionary where the Key is either
        a Movie or an Actor.

    '''

    def __init__(self):
        '''
        If JSONData is supplied, then we load a Graph from the JSON, otherwise
        we start with an empty Graph
        :param JSONData:
        '''
        self.graphDictionary = {}
        self.numMovies = 0
        self.numActors = 0


    def addVertex(self, vertex):
        '''
        checks to see if the vertex is in the graph or not, if not then
        it adds the vertex to graphDictionary as a key

        :param vertex: of type Vertex
        :return:
        '''

        if self.vertexIsInGraph(vertex) == False:
            self.graphDictionary[vertex] = []
            if type(vertex) is Actor:
                self.numActors += 1
            else:
                self.numMovies += 1


    def addEdge(self, edge):
        '''
        depending on whether or not the vertices of the edge are in the
        graph, we might need to add 1 or more vertices to the graph and
        add the edge or just append the edge if 1 or more of the vertices
        are already in the graph.

        * Can only add an edge between existing vertices.

        :param edge: of type Edge
        :return:
        '''

        # check for redundant adds, if the edge already exists
        edges = self.edges()

        for existingEdge in edges:
            if self.edgesConnectSame(existingEdge, edge):
                return


        # if either or both endpoints are not in the graph, return
        if self.vertexIsInGraph(edge.endpointA) == False or self.vertexIsInGraph(edge.endpointB) == False:
            return

        assert(self.vertexIsInGraph(edge.endpointA) and  self.vertexIsInGraph(edge.endpointB))

        # safe to add the edge
        self.graphDictionary[self.vertexAt(vertex=edge.endpointA)].append(edge)
        self.graphDictionary[self.vertexAt(vertex=edge.endpointB)].append(edge)


    def vertices(self):
        '''
        :return: a list of vertices in the graph
        '''

        return list(self.graphDictionary.keys())

    def edges(self):
        '''
        :return: list of edges in the
        '''

        edges = []

        # iterate over each vertex, and add its edges if they are not in our list of edges to return
        for vertex in self.graphDictionary.keys():

            # neighbors is array of edges
            neighbors = self.graphDictionary[vertex]

            for connectingEdge in neighbors:

                if self.inSet(connectingEdge, edges) == False:
                    edges.append(connectingEdge)

        return edges


    # Helper functions

    def vertexAt(self, vertex):
        '''
        Matches vertices and returns the key for that vertex in the graph.
        This is needed since a vertex with the same info but created at different times would
        be considered a different key with pythons dictionary.

        :param vertex:
        :return:
        '''
        for vertexKey in self.graphDictionary.keys():
            if vertexKey.name == vertex.name:
                return vertexKey
        return None

    def vertexAtByName(self, vertexName):
        '''
        Matches vertices and returns the key for that vertex in the graph.
        This is needed since a vertex with the same info but created at different times would
        be considered a different key with pythons dictionary.

        :param vertex:
        :return:
        '''
        for vertexKey in self.graphDictionary.keys():
            if vertexKey.name == vertexName:
                return vertexKey
        return None

    def vertexIsInGraph(self, vertex):
        '''
        checks to see if the vertex is in the graph
        :param vertex:
        :return:
        '''
        if self.vertexAt(vertex) == None:
            return False
        else:
            return True

    def inSet(self, edgeToCheck, setOfEdges):
        '''
        Checks to see if an edge is in a set of edges.

        :param edgeToCheck:
        :param setOfEdges:
        :return:
        '''
        if len(setOfEdges) == 0:
            return False

        for edge in setOfEdges:

            if self.edgesConnectSame(edge, edgeToCheck):
                return True

        return False

    @staticmethod
    def edgesConnectSame(e1, e2):
        '''
        does a comparison to see if the two edges connect the same vertices
        :param e1:
        :param e2:
        :return:
        '''
        if (e1.endpointA.name == e2.endpointA.name and e1.endpointB.name == e2.endpointB.name) or (e1.endpointA.name == e2.endpointB.name and e1.endpointB.name == e2.endpointA.name):
            return True
        else:
            return False

    def printGraph(self):
        '''
        simply prints the graph
        :return:
        '''
        for vertex in self.graphDictionary.keys():

            print(vertex.name)

            edgeStrings = []

            for edge in self.graphDictionary[vertex]:

                edgeStrings.append( "{0} : {1}".format(edge.endpointA.name, edge.endpointB.name))

            print("\t{0}".format(edgeStrings))


class Edge:
    '''

    Class: Edge
        A Edge, which is a part of the Graph data structure.

    '''

    def __init__(self, endpointA, endpointB):
        self.endpointA = endpointA
        self.endpointB = endpointB

    def toJSON(self):
        '''
        Contverts an Edge object to JSON format
        :return:
        '''
        jsonString = ""
        jsonString = json.dumps({
            'endpointA': self.endpointA.__dict__,
            'endpointB': self.endpointB.__dict__
        })
        return jsonString


    def oppositeOf(self, vertex):

        if vertex.name == self.endpointB.name:
            return self.endpointA
        else:
            return self.endpointB
