from datetime import datetime

class Log():
    def __init__(self, temperature: float, luminosity: float, id_sensor: int, date = None):
        self.temperature = temperature
        self.luminosity = luminosity
        self.id_sensor = id_sensor

        if date != None: self.create_date = date
        else: self.create_date = datetime.now()

    def __dict__(self):
        return {
            "temperature": self.temperature,
            "luminosity": self.luminosity,
            "id_sensor": self.id_sensor,
            "create_date": str(self.create_date)
        }
    
    @staticmethod
    def from_dict(obj: dict):
        return Log(obj["temperature"], obj["luminosity"], obj["id_sensor"],obj["create_date"] if "create_date" in obj.keys() else None)

    def __str__(self):
        return str(self.__dict__())

class LogSystem():
    def __init__(self, filename) -> None:
        self.filename = filename

    def save(self, log: Log):
        pass

    def get_last_log(self) -> Log:
        pass

    def get_logs(self):
        pass

    def close(self) -> None:
        pass