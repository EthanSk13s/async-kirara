from .enums import enum, attributes
from .skills import Skill, LeadSkill
from .idol import Idol

class Card:
    def __init__(self, card_data: dict):

        self.card_id = card_data['id']
        self.album_id = card_data['album_id']
        self.type = card_data['attribute']
        self.image = card_data['card_image_ref']
        self.has_spread = card_data['has_spread']
        self.chara_id = card_data['chara_id']
        self.chara = Idol(card_data['chara'])
        self.conventional = card_data['chara']['conventional']

        self.spread = card_data['spread_image_ref']
        self.sprite = card_data['sprite_image_ref']
        self.sign = card_data['sign_image_ref']
        self.icon = card_data['icon_image_ref']
        self.puchi = f"https://hidamarirhodonite.kirara.ca/puchi/{self.card_id}.png"

        self.evo_id = card_data['evolution_id']
        self.evo_type = card_data['evolution_type']
        self.grow_type = card_data['grow_type']
        self.name = card_data['name']
        self.title = card_data['title']
        self.open_dress_id = card_data['open_dress_id']
        self.place = card_data['place']
        self.pose = card_data['pose']
        self.series_id = card_data['series_id']
        self.skill = Skill(card_data['skill'])
        self.lead_skill = LeadSkill(card_data['lead_skill'])
        self.rarity = card_data['rarity']

        self.min_vocal = card_data['vocal_min']
        self.max_vocal = card_data['vocal_max']
        self.bonus_dance = card_data['bonus_dance']

        self.min_dance = card_data['dance_min']
        self.max_dance = card_data['dance_max']
        self.bonus_dance = card_data['bonus_dance']

        self.min_visual = card_data['visual_min']
        self.max_visual = card_data['visual_max']
        self.bonus_visual = card_data['bonus_visual']

        self.min_hp = card_data['hp_min']
        self.max_hp = card_data['hp_max']
        self.bonus_hp = card_data['bonus_hp']

    def min_max_stats(self, stat: str, level: int):

        if stat == 'dance':
            dance_formula = self.min_dance + (self.max_dance - self.min_dance) * (level/self.rarity['base_max_level'])

            return round(dance_formula)

        elif stat == 'visual':
            visual_formula = self.min_visual + (self.max_visual - self.min_visual) * (level/self.rarity['base_max_level'])

            return round(visual_formula)

        elif stat == 'vocal':
            vocal_formula = self.min_vocal + (self.max_vocal - self.min_vocal) * (level/self.rarity['base_max_level'])

            return round(vocal_formula)


    