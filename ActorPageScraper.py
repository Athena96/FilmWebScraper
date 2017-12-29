import re
from bs4 import BeautifulSoup
import requests
import logging

class ActorPageScraper:
    '''
    Class: ActorPageScraper
        A class that scrapes information from an Actors Wikipedia Page
    '''

    @staticmethod
    def parseActor(soup, link):
        '''
        This function takes soup (xml) and the webpage link and extracts all the necessary info
        about the actor from the page.
        It returns a tuple filled with the actors info.

        :param link: the Wikipedia page link
        :return: Actor info
        '''
        logging.info("Parsing an Actor")

        # parse actors name
        name = soup.find('h1', class_='firstHeading')
        if name == None:
            logging.error("Could not find the actors name, returning.")
            return None

        name = name.text
        if name is "":
            logging.error("Actors name string is empty, returning.")
            return None

        # find the actors info summary box
        infobox = soup.find('table', class_='infobox biography vcard')

        if infobox == None:
            infobox = soup.find('table', class_='infobox vcard')
            if infobox == None:
                logging.error("Actors infobox box could not be found, returning. {0}".format(link))
                return None

        # parse actors birthday
        birthDay = infobox.find('span', {'class': 'bday'})
        if birthDay == None:
            logging.error("Actors birthday could not be found, returning. {0}".format(link))
            return None

        birthDayString = birthDay.text

        if birthDayString == None or birthDayString is "":
            logging.error("Actors birthday field is empty, returning. {0}".format(link))
            return None

        birthDateParts = birthDayString.split("-")
        if len(birthDateParts) != 3:
            logging.error("Error with actors birthday format, returning. {0}".format(link))
            return None

        # convert the 1999-02-30 to 19990230 string
        birthDay = ""

        for part in birthDateParts:
            birthDay += part

        # parse the actors filmography
        # on Wikipedia, there are different formats for displaying an actros
        #   filmography. The code below is able to parse 2 of the most popular types.
        filmography = {}

        filmographyListType = '1'
        films = soup.find('div', {'class': 'div-col columns column-width'})

        if films is None:

            filmographyListType = '1'
            films = soup.find('div', {'class': 'div-col columns column-count column-count-2'})

            if films is None:

                filmographyListType = '2'
                films = soup.find('table', {'class': 'wikitable'})

                if films is None:
                    logging.error(" Could not find the actors filmography table, returning. {0}".format(link))
                    return None

        # parse the actors filmography
        filmography = ActorPageScraper.parseActorFilmography(filmographyListType, films)

        if filmography is None:
            logging.error("Filmography could not be parsed, returning. {0}".format(link))
            return None

        reducedFilmography = {}

        i = 0
        for movie in filmography:
            if i < 10:
                reducedFilmography[movie] = filmography[movie]
                i += 1
            else:
                break

        print("Name: ", name)
        print("Birthday: ", birthDay)
        print("Filmography: ")
        for film in reducedFilmography:
            print("\t", reducedFilmography[film])

        return (reducedFilmography, name, birthDay)


    @staticmethod
    def parseActorFilmography(type, filmsTable):
        '''
        This is a helper function that takes the type of table and an xml filmtable then
        it determins what kind of table it is and extracts the actors filmograpgy
        from the table
        :param type:
        :param filmsTable:
        :return:
        '''

        filmographyDictionary = {}
        rowType = ""

        # get the row type
        if type is '1':
            rowType = 'li'

        elif type is '2':
            rowType = 'tr'

        # get a list of the rows (not python list)
        filmography = filmsTable.find_all(rowType)

        if filmography is None:
            logging.error("Could not get rows of type '{0}' filmography table, returning.".format(type))
            return None

        # extract the title and link for each film
        for film in filmography:

            title = ""
            link = ""

            row = film.find('a')

            if row != None:
                title = row.get('title')
                if title is None:
                    logging.error("Could not parse the title in actors filmography.")
                    return None

                ext = row.get('href')
                if ext is None:
                    logging.error("Could not parse the ext link in actors filmography.")
                    return None

                link = 'http://en.wikipedia.org' + ext

                if title is None or title is "" or link is None or link is "":
                    continue

                # save the info in the return dictionary
                filmographyDictionary[title] = link

        return filmographyDictionary
