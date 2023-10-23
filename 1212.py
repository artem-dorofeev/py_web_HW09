import configparser


config = configparser.ConfigParser()
config.read('config.ini')

url_pars = config.get('URL', 'uri')

print(url_pars)