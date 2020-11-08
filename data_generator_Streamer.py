# -*- coding: utf-8 -*-
"""**Nativo factories.**"""
import random
import faker
import pandas as pd
from datetime import datetime
from datetime import timedelta
import requests
import csv
import time


fake = faker.Factory.create()

# SERVICE_NAMES = ['Miracle Fios']
# SERVICE_TYPES = ['Broadband', 'TV', 'Phone']
#
#
# DEVICE_TYPE = ['Laptop', 'Mobile', 'Tab', 'Smart-TV']
# APP_NAME = ['Chrome', 'Safari', 'Firefox', 'Others']
# CHOICE = ['Y', 'N']
# CTRL_REC_GEN_COUNT= 100
# CTRL_SLEEP_TIMER= 60
#
# HEADER = ['customer_id', 'ip_address', 'device_type',
#         'router_mac_address', 'device_name', 'ip_browser',
#         'website_url', 'app_name', 'is_app_flag', 'is_downloaded_flag',
#         'data_size', 'is_live_streaming', 'date', 'time']

# URLs are generated through the csv.

class ServicesOffered():
    """Factory for """
    URLs = []
    control_parameters = []
    SERVICE_NAMES = []
    SERVICE_TYPES = []
    DEVICE_TYPE = []
    APP_NAME = []
    CHOICE = []
    CTRL_REC_GEN_COUNT = None
    CTRL_SLEEP_TIMER = None
    HEADER = []

    def csv_reader(self):
        with open('URLs.csv') as rd:
            table_read = csv.reader(rd)
            for row in table_read:
                self.URLs.extend(row)

    def _remove_nan(self, column):
        filter_column = []
        for val in column:
            if type(val) is not float:
                filter_column.append(val)
        return filter_column


    def req_read_from_csv(self):
        df = pd.read_csv('Reqs.csv')
        self.HEADER = self._remove_nan(df['HEADER'].values)
        self.SERVICE_NAMES = self._remove_nan(df['SERVICE_NAMES'].values)
        self.SERVICE_TYPES = self._remove_nan(df['SERVICE_TYPES'].values)
        self.DEVICE_TYPE = self._remove_nan(df['DEVICE_TYPE'].values)
        self.APP_NAME = self._remove_nan(df['APP_NAME'].values)
        self.CHOICE = self._remove_nan(df['CHOICE'].values)
        self.CTRL_REC_GEN_COUNT = int(df['CTRL_REC_GEN_COUNT'].values[0])
        self.CTRL_SLEEP_TIMER = int(df['CTRL_SLEEP_TIMER'].values[0])

        #print 'App name: ', self.APP_NAME
        print ('service types: ', self.SERVICE_TYPES)

    def browser_history(self):

        customer_id = random.randint(1001, 2000)
        ip_address = fake.ipv4()
        device_type = random.choice(self.DEVICE_TYPE)
        router_mac_address = fake.mac_address()
        device_name = fake.user_name()
        ip_browser = fake.ipv4()
        website_url = random.choice(self.URLs)
        if device_type not in ['Laptop']:
            app_name = random.choice(self.APP_NAME)
        else:
            app_name = ''
        if device_type not in ['Laptop'] and app_name in ['Others']:
            is_app_flag = 'Y'
        else:
            is_app_flag = 'N'
        is_live_streaming = random.choice(self.CHOICE)
        is_downloaded_flag = random.choice(self.CHOICE)
        if is_live_streaming == 'Y':
            # Live stream will naturally have a bigger download size
            data_size = fake.random_int(50, 199)
        else:
            data_size = fake.random_int(1, 9)
        date = datetime.today().strftime("%Y-%m-%d")
        #time = (datetime.now() - timedelta(minutes=random.randint(1, 5))).strftime("%H:%M:%S")
        time = datetime.now().isoformat()

        return [customer_id, ip_address, device_type, router_mac_address,
                device_name, ip_browser, website_url, app_name,
                is_app_flag, is_downloaded_flag, data_size,
                is_live_streaming, date, time]


if __name__ == '__main__':
    comma = ','
    obj = ServicesOffered()
    obj.req_read_from_csv()
    obj.req_read_from_csv()
    obj.csv_reader()

    REST_API_URL = 'https://api.powerbi.com/beta/e81af6ba-a66f-4cab-90f9-9225862c5cf8/datasets/6e6c4e23-216e-4868-89af-88525ce33d0d/rows?key=88gN2ima4ucM%2BWpimRsxxbm%2B9rMl%2Fu7PxPYHQu8ZKZ6XqZznNjon2cxAApKZvht71xtONZ5Vyzp53UWcqQvShA%3D%3D'

    while True:
        browser_history = []
        for i in range(obj.CTRL_REC_GEN_COUNT):
            row = obj.browser_history()
            browser_history.append(row)

        date = datetime.today().strftime("%Y_%m_%d")
        timer = datetime.now().strftime("%H_%M")
        browser_df = pd.DataFrame(browser_history, columns=obj.HEADER)
        data = bytes(browser_df.to_json(orient='records'), encoding='utf-8')
        print(data)
        req = requests.post(REST_API_URL, data)

        # current_dir = os.getcwd()
        # dir_exists = os.path.join(current_dir, r'records')
        #
        # if not os.path.exists(dir_exists):
        #     os.makedirs(os.path.join(dir_exists))
        # #browser_df.to_csv("records/ISPLog_{}_{}.csv".format(date, timer), index=False)
        # print ('csv generated at: ', timer)
        print("Data posted")
        # This is in seconds. change this to increase / decrease frequency of csv generation
        time.sleep(5)
