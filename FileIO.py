
import json
from pprint import pprint

class FileIO:
    '''

    Class: FileIO
        A class that can save and read a json file

    '''

    @staticmethod
    def writeJSONToFile(fileName, json):
        '''
        Saves an array of json strings to a file named 'fileName'.

        :param fileName:
        :param json:
        :return:
        '''

        stringOfJSON = ""

        for idx, line in enumerate(json):

            stringOfJSON += line

            if idx < (len(json)-1):
                stringOfJSON += "\n"

        # write the string to a file
        with open(fileName, "w") as text_file:
            text_file.write("{0}".format(stringOfJSON))


    @staticmethod
    def readJSONFromFile(fileName):
        '''
        reads from 'fileName' and converts its contents to an array Of Lines...

        :param fileName:
        :return:
        '''

        file = open(fileName, 'r')

        arrayOfLines = []

        for line in file:
            line = line.replace("\n", "")
            arrayOfLines.append(line)

        return arrayOfLines


    @staticmethod
    def readJSONFormattedFromFile(fileName):
        '''
        reads from the differently formatted JSON from 'fileName' and convertes is contents to
        :param fileName:
        :return:
        '''


        with open(fileName) as data_file:
            data = json.load(data_file)

        return data
