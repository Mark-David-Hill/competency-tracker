from datetime import datetime

def get_date_time_str():
  current_date_time = datetime.now()
  date_str = current_date_time.strftime("%Y/%m/%d %H:%M:%S")
  return date_str