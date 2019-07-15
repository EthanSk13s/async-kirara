import asyncio
import json
import re
from functools import lru_cache

import aiohttp

from .card import Card
from .enums import enum, rarities
from .idol import Idol
from .infos import Event, Gacha, Info


class KiraraException(Exception):
    def __init__(self, http_status, code, msg):
        self.http_status = http_status
        self.code = code
        self.msg = msg
    
    def __str__(self):
        return f"http status: {self.http_status} {self.code} - {self.msg}"

class Kirara:
    def __init__(self, loop: asyncio.AbstractEventLoop = None, session=True, timeout=50):
        self.prefix = 'https://starlight.kirara.ca/api/v1/'
        self.loop = loop or asyncio.get_event_loop()
        self._autoclose_session = True
        self.retries = timeout

        if isinstance(session, aiohttp.ClientSession):
            self._session = session
        else:
            if session:
                self._session = aiohttp.ClientSession(loop=self.loop)
            else:
                pass

    async def internal_call(self, method, url, payload, params):
        args = dict(params=params)
        args['timeout'] = self.retries
        if not url.startswith('http'):
            url = self.prefix + url

        if payload:
            args['data'] = json.dumps(payload)

        async with self._session.request(method, url, **args) as r:
            r.raise_for_status()
            result = await r.json()
            return result

    @lru_cache(maxsize=None)
    async def get(self, url, args=None, payload=None, params=None, **kwargs):
        reconnect = self.retries

        while reconnect > 0:
            result = await self.internal_call('GET', url, payload, kwargs)
            return result

    @lru_cache(maxsize=None)
    async def post(self, url, args=None, payload=None, params=None, **kwargs):
        reconnect = self.retries

        while reconnect > 0:
            result = await self.internal_call('POST', url, payload, kwargs)
            return result

    async def translate(self, translations: tuple):
        result = await self.post('read_tl', payload=translations)

        return result

    async def get_idol(self, char_id: int):
        data = await self.get(f'char_t/{char_id}')

        return Idol(data['result'][0])

    async def get_card(self, card_id, en_translate=False):
        data = await self.get(f'card_t/{card_id}')

        if data['result'][0] is not None:
            card = Card(data['result'][0])
            if en_translate:
                translations = (card.title, card.skill.name, card.lead_skill.name)
                result = await self.translate(translations)

                for strings, translated in result.items():
                    if translated is None:
                        translated = strings
                card.title = card.title if result.get(
                    card.title) is None else result.get(card.title)
                card.skill.name = card.skill.name if result.get(
                    card.skill.name) is None else result.get(card.skill.name)
                card.lead_skill.name = card.lead_skill.name if result.get(
                    card.lead_skill.name) is None else result.get(card.lead_skill.name)
                
                return card
            else:
                return card
            
    async def get_cards(self, card_ids: list, en_translate=False):
        card_ids = str(card_ids).replace('[', '').replace(']', '')
        card_list = []

        data = await self.get(f"card_t/{card_ids}")

        for card_data in data['result']:
            card_list.append(Card(card_data))

        if en_translate:
            translations = []
            for string in card_list:
                translations.append(string.title)
                translations.append(string.skill.name)
                translations.append(string.lead_skill.name)

            result = await self.translate(tuple(translations))

            for strings, translated in result.items():
                if translated is None:
                    translated = strings
            for card in card_list:
                card.title = card.title if result.get(
                    card.title) is None else result.get(card.title)

                card.skill.name = card.skill.name if result.get(
                    card.skill.name) is None else result.get(card.skill.name)

                card.lead_skill.name = card.lead_skill.name if result.get(
                    card.lead_skill.name) is None else result.get(card.lead_skill.name)

        return card_list

    async def get_image(self, card: 'Card', category):
        categories = {
            'card': card,
            'icon': card.icon,
            'spread': card.spread,
            'sprite': card.sprite,
            'puchi': card.puchi
        }

        if category in categories:
            image = categories.get(category)

            async with await self._session.get(image) as response:

                return await response.read()

    async def get_id(self, category, name, card_rarity=None, position=None, is_title=False):
        cat_list = await self.get(f'list/{category}')
        rarity = enum(rarities, card_rarity)
        card_list = []

        for index, code in enumerate(cat_list['result']):
            if is_title:
                cat_name = cat_list['result'][index]['title']
                if cat_name is None:
                    continue
                else:
                    cat_name = cat_list['result'][index]['title'].lower()
                    match = bool(name[:5].lower() in cat_name[:5])
            else:
                cat_name = cat_list['result'][index]['conventional'].lower()
                match = bool(
                    re.search(r'\b{0}\b'.format(name.lower()), cat_name))

            if category == 'char_t':
                if match:
                    return int(cat_list['result'][index]['chara_id'])
            
            elif category == 'card_t':
                if match:
                    if card_rarity:
                        if int(rarity) == int(cat_list['result'][index]['rarity_dep']['rarity']):
                            card_list.append(
                                int(cat_list['result'][index]['id']))
                    else:
                        card_list.append(int(cat_list['result'][index]['id']))
        if position:
            return card_list[position-1]
        else:
            return card_list
    
    async def get_version(self):
        data = self.get('info')

        return Info(data)
    
    async def get_now(self, category, en_translate=False):
        happening_now = await self.get('happening/now')
        categories = {
            'event': happening_now['events'],
            'gacha': happening_now['gachas']
        }
        happening_list = []

        if category in categories:
            stuff = categories.get(category)

            for index, event in enumerate(stuff):
                if category == 'event':
                    happening_list.append(Event(event))
                else:
                    for gacha, event in enumerate(stuff):
                        happening_list.append(Gacha(event))

        if en_translate:
            for thing in happening_list:
                translations = await self.translate((thing.name,))
                for string, translated in translations.items():
                    if translated is None:
                        thing.name = string
                    else:
                        thing.name = translated

        return happening_list

    async def close(self):
        await self._session.close()
