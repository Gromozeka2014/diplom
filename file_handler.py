import configparser


def read_file(sours):
    id_list = []
    with open(sours, 'r', encoding='utf8') as f:
        for line in f:
            id_list.append(line.strip())
    return id_list


def pars_secure_config():
    conf = configparser.RawConfigParser()
    conf.read('support_files/config.cfg')
    return conf
