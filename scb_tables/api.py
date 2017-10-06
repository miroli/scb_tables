import requests
import pandas as pd
import json
import os

from .Table import Table

TEST = True

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, 'tables.json'), 'r') as f:
	tables = json.loads(f.read())

base_url = 'http://api.scb.se/OV0104/v1/doris/sv/ssd/'

def url_resolver(code):
	if not code:
		return base_url
	if code.upper() != code:
		path = next(filter(lambda x: x['id'] == code, tables))['path']
		return os.path.join(base_url, path, code)
	if len(code) == 2:
		return os.path.join(base_url, code)
	elif len(code) == 6:
		lvl1 = code[:2]
		lvl2 = code
		return os.path.join(base_url, lvl1, lvl2)
	elif len(code) == 7:
		lvl1 = code[:2]
		lvl2 = code[:6]
		lvl3 = code
		return os.path.join(base_url, lvl1, lvl2, lvl3)
	else:
		path = next(filter(lambda x: x['id'] == code, tables))['path']
		return os.path.join(base_url, path, code)


def get(path=None):
	url = url_resolver(path)
	r = requests.get(url)
	resp = r.json()

	if type(resp) is dict:
		return Table(resp, url)
	elif type(resp) is list:
		return pd.DataFrame.from_records(resp, index='id')
