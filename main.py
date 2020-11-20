import time
import argparse

import stock_rank_cron

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('Mode', type=str, choices=['once','interval','cron'], default='once', help="Choose how you want to run the code")
    parser.add_argument('Market', type=str, choices=['KOSPI','KOSDAQ'], default='KOSPI', help="Which markets would you like to crawl?")
    parser.add_argument('Max', type=int, default='30', choices=[10, 30, 50, 100], help="How many are you going to crawl?")

    args = parser.parse_args()
    try:
        stockRankCron = stock_rank_cron.StockRankCron()
        stockRankCron.run(args.Mode, args.Market, args.Max)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stockRankCron.stop()

    
if __name__=="__main__":
    main()
