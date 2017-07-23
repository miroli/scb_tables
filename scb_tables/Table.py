import json
import pandas as pd
import requests


class Table():
	def __init__(self, data, url):
		self._data = data
		self._url = url

	@property
	def title(self):
		return self._data['title']

	@property
	def variables(self):
		content = [(x['code'], x['text'], x.get('elimination', False)) for x in self._data['variables']]
		return pd.DataFrame(content, columns=['code', 'text', 'optional'])

	def filters(self, var):
		blob = next(filter(lambda x: x['code'] == var, self._data['variables']))
		return pd.DataFrame({'valueTexts': blob['valueTexts'], 'values': blob['values']})

	def fetch(self, query=None):
		q = {'query': [], 'response': {'format': 'json'}}
		if query:
			for code, filters in query.items():
				if type(filters) is not list:
					filters = [filters]
				temp = {'code': code,
						'selection': {
							'filter': 'all' if filters == ['*'] else 'item', 
							'values': filters
							}
						}
				q['query'].append(temp)
		r = requests.post(self._url, data=json.dumps(q))
		j = json.loads(r.text[1:])
		columns = [x['text'] for x in j['columns']]
		rows = [x['key'] + x['values'] for x in j['data']]
		return pd.DataFrame(rows, columns=columns)

	def __repr__(self):
		return '<SCB Table: ({})>'.format(self._data['title'][:50] + '...')