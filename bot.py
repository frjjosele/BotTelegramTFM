import asyncio
import nest_asyncio
nest_asyncio.apply()
from telegram.ext import ApplicationBuilder
from config import TOKEN  
import handlers  

async def main():
    # Crea una nueva aplicación de bot con el token provisto.
    application = ApplicationBuilder().token(TOKEN).build()

   
    handlers.register_handlers(application)

    # Inicia el bot
    await application.run_polling()


if __name__ == '__main__':
    asyncio.run(main())
