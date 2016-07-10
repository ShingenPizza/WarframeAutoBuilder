# -*- coding: utf-8 -*-

class Polarities(object):
    class __metaclass__(type):
        def __str__(self):
            return self.__name__

        def __unicode__(self):
            return unicode(self.__name__)

        def __repr__(self):
            return self.__name__

    def __str__(self):
        return self.__class__.__name__

    def __unicode__(self):
        return unicode(self.__class__.__name__)

    def __repr__(self):
        return self.__class__.__name__

class Madurai(Polarities):
    pass

class Vazarin(Polarities):
    pass

class Naramon(Polarities):
    pass

class Zenurik(Polarities):
    pass

class Penjaga(Polarities):
    pass

class Koneksi(Polarities):
    pass

class Unairu(Polarities):
    pass
