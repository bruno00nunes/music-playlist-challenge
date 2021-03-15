from configparser import ConfigParser

parser = ConfigParser()


def config(section='postgresql', filename='config.ini'):
    # create a parser
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    options = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            options[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return options
