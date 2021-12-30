import datetime

class Time:
    @staticmethod
    def get_time_HMS():
        return datetime.datetime.now().strftime("%H:%M:%S")