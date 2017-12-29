import re
from bs4 import BeautifulSoup
import requests
import logging


class MoviePageScraper:
    '''
    Class: MoviePageScraper
        A class that scrapes information from an Movies Wikipedia Page
    '''

    @staticmethod
    def parseMovie(soup, link):
        '''
        This function parses infor from Movie Wikipedia Pages

        :param soup: object for parsing Data
        :param link: the Wikipedia page link
        :return: movie info
        '''

        logging.info("Parsing an Movie")

        # parse movie title
        title = soup.find('h1', class_='firstHeading').text
        if title is None or title is "":
            logging.error("Could not parse the movies title, returning. {0}".format(link))
            return None

        # get info box
        infobox = soup.find('table', class_='infobox vevent')
        if infobox is None:
            logging.error("Could not find the movies info box, returning. {0}".format(link))
            return None

        # Release Date

        query = infobox.find('span', {'class': 'bday dtstart published updated'})
        if query is None:
            logging.error("Error with finding the movies release date, returning. {0}".format(link))
            return None

        releaseDate = query.find(text=True)
        releaseDateParts = releaseDate.split('-')
        releaseDateStr = ""

        for part in releaseDateParts:
            releaseDateStr += part

        if len(releaseDateStr) != 8:
            logging.error("Error with finding the movies release date, returning. {0}".format(link))
            return None

        # parse the starring cast
        cast = infobox.find('th', text='Starring')
        if cast is None:
            logging.error("Error finding the starring cast, returning. {0}".format(link))
            return None

        cast = cast.next_sibling.next_sibling
        if cast is None:
            logging.error("Error finding the starring cast, returning. {0}".format(link))
            return None

        starringCast = {}

        cast = cast.find_all('a')
        if cast is None:
            logging.error("Error finding the starring cast, returning. {0}".format(link))
            return None

        else:
            for actor in cast:
                if MoviePageScraper.hasNumbers(actor.getText()):
                    continue
                starringCast[actor.getText()] = 'http://en.wikipedia.org' + actor.get('href')

        reducedCast = {}

        i = 0
        for actor in starringCast:
            if i < 10:
                reducedCast[actor] = starringCast[actor]
                i += 1
            else:
                break

        print("Name: ", title)
        print("Release Date: ", releaseDateStr)
        for castMember in reducedCast:
            print("\t", castMember)

        return (reducedCast, title, releaseDateStr)

    @staticmethod
    def hasNumbers(inputString):
        return any(char.isdigit() for char in inputString)
