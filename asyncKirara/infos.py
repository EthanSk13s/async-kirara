class Info:
    def __init__(self, info_data: dict):
        self.truth = info_data['truth_version']
        self._api_major = info_data['api_major']
        self._api_revision = info_data['api_revision']
        
class Gacha:
    def __init__(self, gacha_data: dict):
        self.id = gacha_data['id']
        self.name = gacha_data['name']
        self.start_date = gacha_data['start_date']
        self.end_date = gacha_data['end_date']
        self.type = gacha_data['type']
        self.subtype = gacha_data['subtype']
        self.rates = gacha_data['rates']

class Event:
    def __init__(self, gacha_data):
        self.id = gacha_data['id']
        self.name = gacha_data['name']
        self.start_date = gacha_data['start_date']
        self.end_date = gacha_data['end_date']
        self.result_end_date = gacha_data['result_end_date']