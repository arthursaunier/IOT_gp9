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
    def reform(str_packet):
        #{'temperature': '26', 'luminosity': '47', 'create_date': '2021-12-07 09:18:26.039666'}"
        str_packet = str_packet.replace("{'temperature': '", "")
        str_packet = str_packet.replace("', 'luminosity': '", ":")
        str_packet = str_packet[:5]
        return str(str_packet)
       