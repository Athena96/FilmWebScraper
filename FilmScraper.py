import logging
import requests
from datetime import datetime
from Vertex import Actor, Movie
from bs4 import BeautifulSoup
from Graph import Edge
from ActorPageScraper import ActorPageScraper
from MoviePageScraper import MoviePageScraper
from Graph import Graph


class FilmScraper:
    '''
    A Class that scrapes wikipedia for information about actors and movies and fills a graph with the data.
    '''

    def __init__(self):
        '''
        Initializes the classes filmGraph and sets its movie and actor threshold.
        '''
        self.filmGraph = Graph()
        self.movieThreshold = None
        self.numMoviesSkipped = None
        self.numActorsSkipped = None
        self.actorThreshold = None

    def scrapeWebAndFillGraph(self, startingLink, movieThreshold, actorThreshold):
        '''
        This is the interfacing function that the user calls to start a search.
        A starting link and movie/actor thresholds are supplied to start the search.

        :param startingLink:
        :param movieThreshold:
        :param actorThreshold:
        :return:
        '''

        self.movieThreshold = movieThreshold
        self.numMoviesSkipped = 0
        self.actorThreshold = actorThreshold
        self.numActorsSkipped = 0
        self.search([startingLink], None)

        return self.filmGraph

    def search(self, links, root):
        '''
        The main search algorithm. Takes an array of links and for each link determines if it is a
        movie or actor page then parses the page and recursively calls itself to search the list of links passed
        to it (which is either an actors filmography or a movies starring cast).

        The Root is also passed which lets an actor know which movie its linked to visa versa.

        :param links: array of links
        :param root: root for all the links
        :return:
        '''

        # base case
        if len(links) is 0:
            return

        for link in links:

            # base case
            if self.filmGraph.numMovies >= self.movieThreshold and self.filmGraph.numActors >= self.actorThreshold:
                return

            # useful print
            print("num movies skipped: ", self.numMoviesSkipped)
            print("num actors skipped: ", self.numActorsSkipped)
            print("num actors: ", self.filmGraph.numActors)
            print("num movies: ", self.filmGraph.numMovies)

            # get the html from the webpage
            response = requests.get(link, headers={
                'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko)'})
            xmlForPage = BeautifulSoup(response.text, 'lxml')
            pageType = self.parsePageType(xmlForPage)

            if pageType is 'actor':

                # try to parse the page as an actor page
                actorInfo = ActorPageScraper.parseActor(xmlForPage, link)
                if actorInfo is None:
                    logging.error("Could not parse the page as an actor page: {0}".format(link))
                    # numActorsSkipped += 1
                    continue

                # add the actor vertex to the graph
                actorVertex = Actor(name=actorInfo[1], dateOfBirth=actorInfo[2])
                if self.filmGraph.vertexIsInGraph(actorVertex):
                    print("Actor is in graph, skipping")
                    continue

                self.filmGraph.addVertex(actorVertex)

                # add connecting edge
                if root != None:
                    if type(root) is Actor:
                        logging.critical(
                            "Attempting to connect two actors: {0} : {1}, Ending".format(root.name, actorVertex.name))
                        # save graph
                        continue

                    print("Adding edge between : ", root, " and ", actorVertex)
                    self.filmGraph.addEdge(Edge(endpointA=root, endpointB=actorVertex))
                    self.filmGraph.printGraph()

                # search the trimmed list of the actors filmography links
                followMovies = list(actorInfo[0].values())

                print("Root is ", actorVertex.name)

                # RECURSE
                self.search(followMovies, actorVertex)

            elif pageType is 'movie':

                # try to parse the page as an movie page
                movieInfo = MoviePageScraper.parseMovie(xmlForPage, link)
                if movieInfo is None:
                    logging.error("Could not parse the page as an movie page: {0}".format(link))
                    # numMoviesSkipped += 1

                    continue

                # add the actor vertex to the graph
                movieVertex = Movie(name=movieInfo[1], releaseDate=movieInfo[2])
                if self.filmGraph.vertexIsInGraph(movieVertex):
                    print("Movie is in graph, skipping")
                    continue

                self.filmGraph.addVertex(movieVertex)

                # add connecting edge
                if root != None:
                    if type(root) is Movie:
                        logging.critical(
                            "Attempting to connect two movies: {0} : {1}, Ending".format(root.name, movieVertex.name))
                        # save graph
                        continue

                    print("Adding edge between : ", root, " and ", movieVertex)
                    self.filmGraph.addEdge(Edge(endpointA=root, endpointB=movieVertex))
                    self.filmGraph.printGraph()

                # search the trimmed list of the actors filmography links
                followActors = list(movieInfo[0].values())

                print("Root is ", movieVertex.name)

                # RECURSE
                self.search(followActors, movieVertex)

            else:
                logging.warning("Could not determine page type")
                continue


    def parsePageType(self, soup):

        movieInfo = [soup.find('table', class_='infobox vevent')]
        bio = [soup.find('table', class_='infobox biography vcard'), soup.find('table', class_='infobox vcard')]

        for tp in bio:
            if tp != None:
                return 'actor'

        for tp in movieInfo:
            if tp != None:
                return 'movie'

        return 'error'
