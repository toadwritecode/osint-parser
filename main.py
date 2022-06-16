import os


from parser.censys import CensysParser


if __name__ == '__main__':

    ip = input('Введите айпи в формате x.x.x.x')

    os.environ['CENSYS_API_URL'] = 'https://search.censys.io/hosts/' + ip

    parser = CensysParser()

    parser\
        .request()\
        .perform()\
        .parse()\
        .export()
