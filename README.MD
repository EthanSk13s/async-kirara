# Async-Kirara
## An async port of pyKirara, that's about it

## Usage
```py
import asyncKirara
import asyncio

async def cards(loop):
    client = asyncKirara.Kirara()
    cards = await client.get_id('card_t', 'uzuki', card_rarity='ssr') # Get all SSR card IDS for Uzuki
    stuff = await client.get_cards(cards, en_translate=True) # Converts IDS into card objects
    
    for card in stuff: # Print the cards' attributes
        print('='*30)
        print(card.title)
        print(card.lead_skill.name)
        print(card.skill.name)
        print('\n')

    await client.close()

if __name__ == '__main__': # Async loop stuff
    loop = asyncio.get_event_loop()
    loop.run_until_complete(cards(loop))
```

## Requirements
- Python 3.6+ (Mabye I'll backport it to 3.5, if I feel like it)
- [aiohttp](https://github.com/aio-libs/aiohttp) library

## License

- [MIT](https://choosealicense.com/licenses/mit/)