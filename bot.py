import asyncio
import nest_asyncio
nest_asyncio.apply()
from telegram.ext import ApplicationBuilder
from config import TOKEN  # Importa el token de configuración.
import handlers  # Importa el módulo de manejadores de mensajes.

async def main():
    # Crea una nueva aplicación de bot con el token provisto.
    application = ApplicationBuilder().token(TOKEN).build()

    # Llama a la función definida en handlers.py para registrar los manejadores en la aplicación.
    handlers.register_handlers(application)

    # Inicia el bot para que comience a sondear mensajes.
    await application.run_polling()

# Punto de entrada principal de Python.
if __name__ == '__main__':
    asyncio.run(main())
