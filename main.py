from parser.censys import CensysParser


if __name__ == '__main__':

    parser = CensysParser()

    parser\
        .request()\
        .perform()\
        .parse()\
        .export()
