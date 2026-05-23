import datetime as dt
class TimeHandler:
    @staticmethod
    def get_month_str():
        prefix = '0'
        current_month = dt.datetime.now().month
        if current_month < 9:
            return prefix + str(current_month)
        return current_month
            
            
    
    @staticmethod
    def get_year_str():
        return dt.datetime.now().year
    
print(TimeHandler.get_month_str())
print(TimeHandler.get_year_str())