import stock_rank_cron
import time

stockRankCron = stock_rank_cron.StockRankCron() 
stockRankCron.run('interval')

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    stockRankCron.stop()
