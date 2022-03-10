import json
import requests
import logging
from datetime import datetime, timedelta

import pytz

token = os.environ('TOKEN')
database_id = os.environ('DB_ID')

logger = logging.getLogger(__name__)

class Notion:
    def __init__(self):
        self.list_1 = []
        self.list_2 = []
        

    def get_data(self):
        url = f'https://api.notion.com/v1/databases/{database_id}/query'

        r = requests.post(url, headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2021-08-16"
        })

        result_dict = r.json()
        hb_list_result = result_dict['results']

        for res in hb_list_result:
            res_dict = self.get_values(res)
                if res_dict['status'] == '1':
                    self.list_1.append(res_dict)
                else:
                   self.list_2.append(res_dict)


    def check_values(self, condition, end_part, end=''):
        if condition is not None:
            if condition[end_part] is not None:
                return condition[end_part]
            return end
        else:
            return end


    def get_values(self, result):
        properties = result['properties']
        id = properties['id']['title']['text']['content']
        date = self.check_values(properties['date']['date'], 'start')
        type = self.check_values(properties['type']['select'], 'name')
        status = self.check_values(properties['status']['select'], 'name')
        
        return {
            'id': id,
            'date': date,
            'type': type,
            'status': status
        }


    def get_lists(self):
        self.get_data()
        return self.list_1, self.list_2

