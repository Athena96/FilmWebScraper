
from FileIO import FileIO
from JSONConversion import JSONConversion
from Vertex import Actor,Movie
from Graph import Graph
import math
import numpy as np
#import Plotting

class ClientQueries:
    '''
        Class: ClientQueries
        Used for the Queries requested by the client
    '''

    @staticmethod
    def topHubActors(topX, graph):
        '''
        This function iterates over all the actors in a graph and counts the number of connections
        each actor has.
        :param topX: int
        :param graph: graph
        :return: [(actor object, numConnections)]
        '''

        # dictionary (key: actor in the graph, value: number of 'Connections' that actor has)
        actorConnectionCounts = {}

        # for each actor in the graph, store the number of connections it has
        for actorVertex in graph.vertices():

            if type(actorVertex) is Actor:
                actorConnectionCounts[actorVertex] = ClientQueries.numConnectionsFor(actorVertex, graph)

        # return only the topX actors with most connections
        sortedDictByActorCount = [(k, actorConnectionCounts[k]) for k in sorted(actorConnectionCounts, key=actorConnectionCounts.get, reverse=True)]
        return sortedDictByActorCount[:topX]


    @staticmethod
    def numConnectionsFor(aVertex, graph):
        '''
        This function counts the number of connections actorVertex has in graph.

        :param actorVertex: Actor object
        :param graph: Graph object
        :return: int - the number of connections
        '''
        numConnections = 0

        # for each of the actors movies
        for edge in graph.graphDictionary[aVertex]:

            # get the movie vertex connected to actorVetex
            movieVertex = edge.oppositeOf(aVertex)

            # for each of the movies actors
            for secondEdge in graph.graphDictionary[movieVertex]:

                # get the neighboring actor
                neighborActorVertex = secondEdge.oppositeOf(movieVertex)

                # if the actor is not myself, add it to the number of connections
                if neighborActorVertex.name != aVertex.name:
                    numConnections += 1

        return numConnections


# 1. Read JSON From File
print("1. Reading JSON Graph file...")
newJsonData = FileIO.readJSONFromFile("/Users/jaredfranzone/Desktop/FilmWebScraper/data/graphData.txt")

# ------------------------------------------------------------------------------------------------------------

# 2. Converting JSON to Graph
print("2. Converting formatted JSON data to a Graph...")
newGraph = JSONConversion.convertJSONToGraph(newJsonData)

# ------------------------------------------------------------------------------------------------------------


#### Client Queries

newGraph.printGraph()

# ------------------------------------------------------------------------------------------------------------

# 1. Calculate the Hub Actors
num = 5
hubActors = ClientQueries.topHubActors(num, newGraph)
print("The hub actors are: ")
hubVals = []
names = []
for entry in hubActors:
    names.append(entry[0].name)
    hubVals.append(entry[1])

    print("\t{0} : {1}".format(entry[0].name, entry[1]))

# plot hub actors
#Plotting.Plotting.histogram(hubVals, names, "Actors", "Number of Connections", ("Top {0} Hub Actors".format(num)))
