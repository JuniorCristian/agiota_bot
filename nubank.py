import configparser
from pynubank import Nubank
import json

config = configparser.ConfigParser()
config.read_file(open('config.ini'))

nu = Nubank()

nu.authenticate_with_refresh_token(config['NUBANK']['token'], config['NUBANK']['cert_path'])

print(list(filter(lambda x: "Teste" in x['node']['detail'], nu.get_account_feed_paginated()['edges'])))

pretty_json = json.dumps(nu.get_account_feed_paginated())

print(pretty_json)