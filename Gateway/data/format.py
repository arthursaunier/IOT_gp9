class Format:
    def __init__(self):
        pass

    def parse(self, str_in):
        parsed = str_in.split(":")
        dico = dict()
        dico["temperature"] = parsed[0]
        dico["luminosity"] = parsed[1]
        return dico