from telegram.ext import CommandHandler, MessageHandler, filters
from phishing_detection import contiene_phishing
import re

# Función para responder al comando /start.
async def start(update, context):
    # Responde al usuario con un mensaje de bienvenida.
    await update.message.reply_text('Hola, soy tu bot de seguridad. ¿En qué puedo ayudarte hoy?')

# Función para analizar mensajes generales en busca de URLs.
async def mensaje_general(update, context):
    mensaje = update.message.text
    # Flag para seguir si se encontró una URL maliciosa.
    encontrada_url_maliciosa = False
    
    # Extrae URLs del mensaje usando regex.
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', mensaje)
    for url in urls:
        if await contiene_phishing(url):
            # Si se detecta una URL maliciosa, marca el flag y responde inmediatamente.
            encontrada_url_maliciosa = True
            await update.message.reply_text("⚠️ Precaución: Este enlace podría ser peligroso.")
            break  # Sal del bucle después de encontrar la primera URL maliciosa.
    
    # Si después de revisar todas las URLs no se encontró ninguna maliciosa, informa que parecen seguras.
    if not encontrada_url_maliciosa and urls:
        await update.message.reply_text("✅ Este enlace parece seguro.")


# Función para registrar los manejadores en la aplicación del bot.
def register_handlers(application):
    # Registra el manejador para el comando /start.
    application.add_handler(CommandHandler("start", start))
    # Registra el manejador para analizar textos de mensajes que no sean comandos.
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje_general))
