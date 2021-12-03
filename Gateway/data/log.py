from datetime import datetime

class Log():
    def __init__(self, temperature, luminosity, date = None):
        self.temperature = temperature
        self.luminosity = luminosity

        if date != None: self.create_date = date
        else: self.create_date = datetime.now()

    def __dict__(self):
        return {
            "temperature": self.temperature,
            "luminosity": self.luminosity,
            "create_date": str(self.create_date)
        }
    
    @staticmethod
    def from_dict(obj):
        return Log(obj["temperature"], obj["luminosity"], obj["create_date"] if "create_date" in obj.keys() else None)
        
    def __str__(self):
        return str(self.__dict__())

class LogSystem():
    def __init__(self, filename):
        self.filename = filename

    def save(self, log):
        pass

    def get_last_log(self):
        pass

    def get_logs(self):
        pass

    def close(self):
        pass