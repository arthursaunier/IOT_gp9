from .log import Log, LogSystem

class File(LogSystem):
    def __init__(self, filename) -> None:
        self.filename = f"{filename}.txt"
        self.f = open(self.filename, "r+")

        self.last_log = None

    def save(self, log: Log):
        self.f.write(f"{str(log.__dict__())}\n")

        self.last_log = log

    def get_last_log(self) -> Log:
        return self.last_log

    def close(self):
        self.f.close()
    