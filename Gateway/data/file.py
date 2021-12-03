from .log import Log, LogSystem

class File(LogSystem):
    def __init__(self, filename):
        self.filename = f"{filename}.txt"
        self.f = open(self.filename, "w+")

        self.last_log = None

    def save(self, log):
        self.f.write(f"{str(log.__dict__())}\n")

        self.last_log = log

    def get_last_log(self):
        return self.last_log

    def close(self):
        self.f.close()
    