import datetime as dt
class TimeHandler:
    @staticmethod
    def get_month_str():
        """Gets current month 

        Returns:
            str: current month (ex. '05')
        """
        prefix = '0'
        current_month = dt.datetime.now().month
        if current_month < 9:
            return prefix + str(current_month)
        return current_month
            
            
    
    @staticmethod
    def get_year_str():
        """Gets current year

        Returns:
            str: current year (ex. 2026)
        """
        return dt.datetime.now().year
    
print(TimeHandler.get_month_str())
print(TimeHandler.get_year_str())