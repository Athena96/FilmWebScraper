
import json
from Graph import Graph, Edge
from Vertex import Actor, Movie
from MoviePageScraper import MoviePageScraper
from ActorPageScraper import ActorPageScraper
import requests
from bs4 import BeautifulSoup
import datetime
from FileIO import FileIO

class JSONConversion:
    '''

    Class: JSONConversion
        A class that convert a graph to json and can convert json (in the proper format) to a graph.

    '''

    @staticmethod
    def convertGraphToJSON(graph):
        '''
        Converts a graph to JSON, and returns an array of strings where each element
        is either a Vertex or an Edge in JSON format.

        :param graph:
        :return:
        '''
        jsonFile = []

        # add vertices to the array of json objects
        for vertex in graph.vertices():
            jsonFile.append(json.dumps(vertex.__dict__))

        # add the edges to the array of json objects
        for edge in graph.edges():
            jsonFile.append( edge.toJSON() )

        return jsonFile

    @staticmethod
    def convertJSONToGraph(jsonFile):
        '''
        Converts an array of JSON Strings, where each line is either a Movie, Actor
        or Edge, to a Graph data structure.
        :param json:
        :return:
        '''

        graphFromJSON = Graph()

        for line in jsonFile:
            # convert JSON line to python dictionary
            data = json.loads(line)

            # try to convert the data to a vertex
            vertex = JSONConversion.getVertexFromDict(data)

            # if the line was an vertex add it otherwise it's an edge.
            if vertex != None:

                graphFromJSON.addVertex(vertex)

            else: # add the edge

                endpointA = JSONConversion.getVertexFromDict(data['endpointA'])
                endpointAVertex = graphFromJSON.vertexAt(endpointA)

                endpointB = JSONConversion.getVertexFromDict(data['endpointB'])
                endpointBVertex = graphFromJSON.vertexAt(endpointB)

                edge = Edge(endpointA=endpointAVertex, endpointB=endpointBVertex)

                graphFromJSON.addEdge(edge)

        return graphFromJSON

    @staticmethod
    def convertFormattedJSONToGraph(jsonDict):
        '''
        This function converts the differently formatted json into a Graph

        :param jsonDict:
        :return:
        '''
        newGraph = Graph()

        # Add Vertices
        for actor in jsonDict[0]:

            # create an actor and add it to the graph
            actorVertex = JSONConversion.extractActorInfo(jsonDict, actor)
            newGraph.addVertexFast(actorVertex)

        for movie in jsonDict[1]:

            # create an movie and it to the the graph
            movieVertex = JSONConversion.extractMovieInfo(jsonDict, movie)
            newGraph.addVertexFast(movieVertex)


        # add edges: from actors to -> movies

        # for each actor, get its filmography and a link to it in the graph
        for actor in jsonDict[0]:

            actorFilmography = jsonDict[0][actor]["movies"]
            actorVertexInGraph = newGraph.vertexAtByName(jsonDict[0][actor]["name"])

            # for each movie in the actors filmography
            for movieTitle in actorFilmography:

                # if there is a movie vertex  in my graph that matches this film
                #   then i should retrieve that vertex and create an edge
                movieVertexInGraph = newGraph.vertexAtByName(movieTitle)

                if movieVertexInGraph != None:
                    newGraph.addEdgeFast( Edge(endpointA=actorVertexInGraph, endpointB=movieVertexInGraph) )

        return newGraph

    @staticmethod
    def extractMovieInfo(jsonDict, movie):
        '''
        This function extracts the actor info from jsonDict
        :param jsonDict:
        :param movie:
        :return:
        '''

        # 1. name
        name = Utilities.removeNonAscii(jsonDict[1][movie]["name"])

        # 2. release date
        releaseYear = int(jsonDict[1][movie]["year"])
        if releaseYear <= 0:
            releaseYear = 0000

        releaseDateStr = "{0}0101".format(str(releaseYear))
        releaseDate = int(releaseDateStr)

        # 4. actors
        actors = []

        if jsonDict[1][movie]["actors"] == None:
            actors = []
        else:
            for a in jsonDict[1][movie]["actors"]:
                actors.append(Utilities.removeNonAscii(a))

        return Movie(name=name, releaseDate=releaseDate)

    @staticmethod
    def extractActorInfo(jsonDict, actor):
        '''
        This function extracts the actor info from jsonDict
        :param jsonDict:
        :param actor:
        :return:
        '''

        # 1. name
        name = Utilities.removeNonAscii((jsonDict[0][actor]["name"]))

        # 2. age
        age = int(jsonDict[0][actor]["age"])
        if age < 0:
            age = 0

        # 3. date of birth
        dateOfBirth = Utilities.birthdayFromAge(age)

        # 5. movies
        movies = []

        if jsonDict[0][actor]["movies"] == None:
            movies = []
        else:
            for m in jsonDict[0][actor]["movies"]:
                movies.append(Utilities.removeNonAscii(m))

        return Actor(name=name, dateOfBirth=dateOfBirth)

    @staticmethod
    def getVertexFromDict(dictionary):
        '''
        Converts a single dictionary entry (previously converted from JSON) to either an Actor or a Movie
        :return:
        '''
        if 'dateOfBirth' in dictionary.keys():  # its an actor
            actor = Actor(name=str(dictionary['name']), dateOfBirth=int(dictionary['dateOfBirth']))
            return actor

        elif 'releaseDate' in dictionary.keys():  # its an movie
            movie = Movie(name=str(dictionary['name']), releaseDate=int(dictionary['releaseDate']))
            return movie

        else:
            return None
