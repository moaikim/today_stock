import sqlite3

class StockRankDBManager:
    def __init__(self):
        print ("DB Manager 시작")
        self.DBName = 'stock_rank.db'
        self.db = sqlite3.connect(self.DBName, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.daum_stock_rank_table = 'daum_stock_rank'
        self.daum_stock_rank_colums = {
            'rank': 'integer PRIMARY KEY',
            'name': 'text',
            'symbolCode': 'text',
            'tradePrice': 'integer',
            'change': 'text',
            'changePrice': 'integer',
            'changeRate': 'real',
            'accTradeVolume': 'integer',
            'accTradePrice': 'integer',
            'high52wPrice': 'integer',
            'low52wPrice': 'integer'
        }

    def __del__(self):
        self.stop()

    def stop(self):
        try: self.db.close()
        except: pass
    
    def queryCreateStockRankTable(self, market):
        self.daum_stock_rank_table = 'daum_stock_rank_' + market.lower()
        cursor = self.db.cursor()
        colum_info = ",".join(col_name + ' ' + col_type for col_name, col_type in self.daum_stock_rank_colums.items())
        query = "CREATE TABLE IF NOT EXISTS {} ({})".format(self.daum_stock_rank_table, colum_info)
        cursor.execute(query)
        self.db.commit()

    def queryInsertStockRankTable(self, values):
        cursor = self.db.cursor()
        colums = ",".join(self.daum_stock_rank_colums.keys())
        values = "','".join(str(values[col_name]) for col_name in self.daum_stock_rank_colums.keys())
        query = "INSERT INTO {} ({}) VALUES ('{}')".format(self.daum_stock_rank_table, colums, values)
        cursor.execute(query)
        self.db.commit()

    def queryDeleteAlltDaumStockRankTable(self):
        query = "DELETE FROM {}".format(self.daum_stock_rank_table)
        cursor = self.db.cursor()
        cursor.execute(query)
        self.db.commit()