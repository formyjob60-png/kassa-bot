
from telegram import Bot 
import asyncio 
import random 


TOKEN = "8808897780:AAFmRgjUtPDNG46GAX7h8PrQaCZo3Je8Gps" 
GROUP_ID = "-5288506356"


friends = [

    "Айбек",
    "Аслан",
    "Илияс",
    "Искендер",
    "Нурлан",
    "Чынгыз",
    "Элмурат",
    "Эрзат",
    "Эркин",
    "Шералы"
]

random.shuffle(friends) 

message = "🎲 ЖЕРЕБЬЁВКА КАССЫ\n\n" 

for i, name in enumerate(friends, start=1): 
    message += f"{i}. {name}\n" 
    
async def main(): 
    bot = Bot(token=TOKEN) 
    
    await bot.send_message( chat_id=GROUP_ID, text=message 
                               ) 
        
asyncio.run(main())
