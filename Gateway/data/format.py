class Format:
    def __init__(self):
        pass

    @staticmethod
    def parse(str_in):
        parsed = str_in.split(":")
        dico = dict()
        dico["temperature"] = parsed[0]
        dico["luminosity"] = parsed[1]
        return dico

    @staticmethod
    def reform(obj):
        return str(str(obj["temperature"]) + ":" + str(obj["luminosity"]))
       