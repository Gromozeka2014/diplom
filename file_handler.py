import configparser


def read_id(sours):
    id_list = []
    with open(sours, 'r') as f:
        for line in f:
            id_list.append(line.strip())
    return id_list


def pars_secure_config():
    conf = configparser.RawConfigParser()
    conf.read('config.cfg')
    return conf
