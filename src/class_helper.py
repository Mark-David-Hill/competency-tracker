import sqlite3

class Crud_db:
    def __init__(self, database = 'competency_tracker.db'):
        self.database = database

    def connect(self):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        # print('connect seccesfully')

    def execute(self, query):
        self.query = query
        self.cursor.execute(self.query)

    def close(self): 
        self.connection.commit()
        self.connection.close()

    # def save_to_csv(self, day = None):
    #     if day == None:
    #         query_general_bill_all = ''' SELECT * FROM  general_bill'''
    #         query_expences_all = ''' SELECT * FROM expenses '''
    #         query_total_all = ''' SELECT * FROM total '''

    #         df1 = pd.read_sql(query_general_bill_all, sqlite3.connect(self.database))
    #         df1.to_csv('general_bill_all.csv', index = False)

    #         df2 = pd.read_sql(query_expences_all, sqlite3.connect(self.database))
    #         df2.to_csv('expenses_all.csv', index = False)

    #         df3 = pd.read_sql(query_total_all, sqlite3.connect(self.database))
    #         df3.to_csv('total_day_all.csv', index = False)
    #     if day :
    #         try:
    #             day = str(day)
    #             query_general_bill_all = f" SELECT * FROM  general_bill WHERE date_g == '{day}'"
    #             query_expences_all = f' SELECT * FROM expenses WHERE date == "{day}" '
    #             query_total_all = f' SELECT * FROM total WHERE date == "{day}" '

    #             df1 = pd.read_sql(query_general_bill_all, sqlite3.connect(self.database))
    #             # print(df1)
    #             df1.to_csv(f'general_bill_{day}.csv', index = False)

    #             df2 = pd.read_sql(query_expences_all, sqlite3.connect(self.database))
    #             df2.to_csv(f'expenses_{day}.csv', index = False)

    #             df3 = pd.read_sql(query_total_all, sqlite3.connect(self.database))
    #             df3.to_csv(f'total_day_{day}.csv', index = False)
    #         except ValueError:
    #             sys.exit('value Error')