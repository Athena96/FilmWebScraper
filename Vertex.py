import abc
import json


class Vertex(object):
    '''

    Class: Vertex
        An abstract superclass, is subclassed by a Movie and Actor classes.
    '''

    def __init__(self, vid):
        self.vid = vid


class Actor(Vertex):
    '''
    Class: Actor
        A concrete subclass of a Vertex. Holds information about actors.
    '''

    def __init__(self, name, dateOfBirth):
        Vertex.__init__(self,name)
        self.name = name
        self.dateOfBirth = dateOfBirth



class Movie(Vertex):
    '''
    Class: Movie
        A concrete subclass of a Vertex. Holds information about movies.
    '''

    def __init__(self, name, releaseDate):
        Vertex.__init__(self,name)
        self.name = name
        self.releaseDate = releaseDate
