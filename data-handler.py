import requests 
import os
import json
from dotenv import load_dotenv

load_dotenv()

# passing in some user (future admin) api key via .env for post requests
api_key = os.getenv('API_KEY')

class DataHandler:
    def counter(self, total_count: int):
        total = []
        for n in range(1, total_count+1):
            total.append(n)
        return total

    # get data from external URL - TESTING remote endpoint
    # note: ibjjf data formatting won't work for use as geojson for map rendering - coords also required for map
    # def fetch_json(self):
    #     headers = {
    #             'Accept': 'application/json, text/plain, */*',
    #             'Accept-Language': 'en-US',
    #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
    #             'Content-Type': 'application/json; charset=utf-8',
    #             'Referer': 'https://ibjjf.com/registered-academies',
    #             'Host': 'ibjjf.com',
    #             'X-Requested-With': 'XMLHttpRequest'
    #         }
    #     try: 
    #         # construct custom param payload
    #         page_count = self.counter(2)
    #         for p in page_count:
    #             param = {'page': p} # new params to assign to url

    #             target_url = 'https://ibjjf.com/api/v1/academies/list.json'
    #             res = requests.get(str(target_url), params=param, headers=headers)

    #             if res.status_code == 200:
    #                 data = res.json() 
    #                 json_str = {"data": data['list']}

    #                 self.post_json(json_str)
    #             else:
    #                 print('There was a problem with the request: {}'.format(res.status_code))

    #     except requests.exceptions.RequestException as err:
    #         print('Unable to fetch resource: {}'.format(err))
    #         raise SystemExit(err)


    # read & write data
    def render_json(self):
        file_path = os.path.join('data', 'data.json')
        try:
            with open(file_path) as file:
                data = json.load(file)
                json_result = {"data": data['academies']}

                # post data file to API
                self.post_json(json_result)
        except:
            print('Unable to read file')
    
    # post json body to API
    def post_json(self, json_data: dict):
        try: 
            post_headers = {'Content-Type': 'application/json'}
            session = requests.Session()
            session.headers.update(post_headers)

            post_res = requests.post(str('http://localhost:8000/api/v1/academies?api_key={}'.format(api_key)), json=json_data)

            if post_res.status_code == 200:
                print('Success! Data posted')
            else:
                print('There was a problem with the request: {}, {}, \n {}'.format(post_res.status_code, post_res.reason, post_res.content))
        except requests.exceptions.RequestException as err:
            print('Unable to post to resource: {}'.format(err))
    

    def main(self):
        # return self.fetch_json()
        return self.render_json()

# instantiate
new_data_handler = DataHandler()
new_data_handler.main()