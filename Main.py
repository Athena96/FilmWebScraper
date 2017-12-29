from datetime import datetime
from JSONConversion import JSONConversion
from Graph import Graph
from Vertex import Actor, Movie
from FileIO import FileIO
from FilmScraper import FilmScraper
import sys

# If the user wants to scrape new Film Data
if sys.argv[1] != "read":
    start = sys.argv[1]
    movieThreshold = int(sys.argv[2])
    actorThreshold = int(sys.argv[3])

    print("1.")
    print("Start Scraping From: {0}".format(start))
    print("With movieThreshold = {0}".format(movieThreshold))
    print("and actorThreshold = {0}".format(actorThreshold))
    print("")
    filmScraper = FilmScraper()
    filmGraph = filmScraper.scrapeWebAndFillGraph(startingLink='https://en.wikipedia.org/wiki/{0}'.format(start), movieThreshold=movieThreshold, actorThreshold=actorThreshold)


    # CONVERT TO JSON
    print("")
    print("2.")
    print("Converting graph to JSON...")
    jsonFile = JSONConversion.convertGraphToJSON(filmGraph)

    # SAVE FILE
    print("")
    print("3.")

    print("Saving JSON Graph to: {0}".format("/Users/jaredfranzone/Desktop/FilmWebScraper/data/"))
    FileIO.writeJSONToFile("/Users/jaredfranzone/Desktop/FilmWebScraper/data/graphData.txt", jsonFile)

# if the user wants to read the data file from already scraped film data
elif sys.argv[1] == "read":

    # read graph from file
    print("")
    print("1.")
    print("Reading JSON data.")

    jsonData = FileIO.readJSONFromFile("/Users/jaredfranzone/Desktop/FilmWebScraper/data/graphData.txt")

    # get graph from JSON
    print("")
    print("2.")
    print("Converting JSON to Graph")
    newGraph = JSONConversion.convertJSONToGraph(jsonData)

    print("")
    newGraph.printGraph()

# error
else:

    print("USAGE ERROR")
