import asyncio
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

async def start_bot():
    from bot.handlers import dp, bot
    await dp.start_polling(bot)

async def start_api():
    config = uvicorn.Config(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(
        start_bot(),
        start_api(),
    )

if __name__ == "__main__":
    asyncio.run(main())