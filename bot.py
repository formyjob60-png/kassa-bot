from telegram import Bot 
import asyncio 

TOKEN = "8808897780:AAFmRgjUtPDNG46GAX7h8PrQaCZo3Je8Gps" 
CHAT_ID = "7400308603" 

async def main(): 
    bot = Bot(token=TOKEN) 
    
    await bot.send_message(
        chat_id=CHAT_ID, 
        text="Бот работает 🚀"
    ) 

asyncio.run(main())