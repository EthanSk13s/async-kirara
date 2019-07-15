from .enums import enum, blood_types, constellations, hands, home_towns

class Idol:
    def __init__(self, char_data: dict):
        self.age = char_data['age']
        self.bday = char_data['birth_day']
        self.bmonth = char_data['birth_month']
        self.btype = enum(blood_types, char_data['blood_type'])
        self.bust = char_data['body_size_1']
        self.waist = char_data['body_size_3']
        self.hip = char_data['body_size_3']
        self.horoscope = enum(constellations, char_data['constellation'])
        self.conventional = char_data['conventional']
        self.favorite = char_data['favorite']
        self.hand = enum(hands, char_data['hand'])
        self.height = char_data['height']
        self.home_town = enum(home_towns, char_data['home_town'])
        self.kana_spaced = char_data['kana_spaced']
        self.kanji_spaced = char_data['kanji_spaced']
        self.name = char_data['name']
        self.name_kana = char_data['name_kana']
        self.personality = char_data['personality']
        self.type = char_data['type']
        self.voice = char_data['voice']
        self.weight = char_data['weight']
        self.icon = char_data['icon_image_ref']