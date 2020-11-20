from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
import requests
import datetime

import stock_rank_dbmanager

class StockRankCron():
    def __init__(self):
        print ('크론 시작')
        self.scheduler = BackgroundScheduler(job_defaults={'max_instances': 10, 'coalesce': False})
        self.scheduler.start()
        self.dbManager = stock_rank_dbmanager.StockRankDBManager()

    def __del__(self): 
        self.stop()

    def exec(self):
        print ('DaumStockCron Start: ' + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

        params = {
            'page': 1,
            'perPage': 30,
            'intervalType': 'TODAY',
            'market': 'KOSPI',
            'changeType': 'RISE',
            'pagination': 'true',
            'order': 'desc'
          }

        headers = {
            'referer': 'https://finance.daum.net',
            'User-Agent': 'chrome'
        }

        URL = 'https://finance.daum.net/api/trend/price_performance'

        try: 
            self.dbManager.queryCreateStockRankTable()
            self.dbManager.queryDeleteAlltDaumStockRankTable()
            res = requests.get(URL, headers=headers, params=params)
            if res.status_code == 200:
                datas = res.json()['data']
                for data in datas:
                    self.dbManager.queryInsertStockRankTable(data)
            else:
                print ('DAUM API 연결 에러')
        except requests.exceptions.RequestException as err:
            print ('Error Requests: {}'.format(err))
    
    def run(self, mode):
        print ("실행!")
        if mode == 'once':
            self.scheduler.add_job(self.exec)
        elif mode == 'interval':
            self.scheduler.add_job(self.exec, 'interval', seconds=10)
        elif mode == 'cron mode':
            self.scheduler.add_job(self.exec, 'cron', hour='9,10,11,12,13,14,15', second='10')

    def stop(self):
        try: self.scheduler.shutdown() 
        except: pass
        try: self.dbManager.close() 
        except: pass
