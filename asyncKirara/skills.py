class Skill:
    def __init__(self, skill_data: dict):
        self.id = skill_data['id']
        self.name = skill_data['skill_name']
        self.explain = skill_data['explain']
        self.en_explain = skill_data['explain_en']

        self.skill_type = skill_data['skill_type']
        self.judge_type = skill_data['judge_type']
        self.trigger_type = skill_data['skill_trigger_type']
        self.trigger_value = skill_data['skill_trigger_value']

        self.cutin_type = skill_data['cutin_type']
        self.condition = skill_data['condition']

        self.value = skill_data['value']
        self.value_2 = skill_data['value_2']

        self.max_chance = skill_data['max_chance']
        self.max_duration = skill_data['max_duration']
        self.skill_type_id = skill_data['skill_type_id']
        self.effect_length = skill_data['effect_length']
        self.proc_chance = skill_data['proc_chance']


class LeadSkill:
    def __init__(self, skill_data: dict):
        self.id = skill_data['id']
        self.name = skill_data['name']
        self.explain = skill_data['explain']
        self.en_explain = skill_data['explain_en']
        self.type = skill_data['type']

        self.need_cute = bool(skill_data['need_cute'])
        self.need_cool = bool(skill_data['need_cool'])
        self.need_passion = bool(skill_data['need_passion'])

        self.target_attribute = skill_data['target_attribute']
        self.target_attribute_2 = skill_data['target_attribute_2']
        self.target_param = skill_data['target_param']
        self.target_param_2 = skill_data['target_param_2']

        self.up_type = skill_data['up_type']
        self.up_type_2 = skill_data['up_type_2']
        self.up_value = skill_data['up_value']
        self.up_value_2 = skill_data['up_value_2']

        self.special_id = skill_data['special_id']
        self.need_chara = skill_data['need_chara']
