from telegram.ext import CommandHandler, MessageHandler, filters
from phishing_detection import contiene_phishing
import re

# Función para el comando /start.
async def start(update, context):
    welcome_text = (
        "¡Hola! Soy tu asistente de seguridad en Telegram. Mi trabajo es revisar enlaces por ti y asegurarme de que "
        "no te lleven a sitios peligrosos. Envíame un enlace cuando quieras, y te diré si es seguro.\n\n"
        "¿Necesitas saber más? Usa /help para ver todos los comandos que tengo disponibles."
    )
    await update.message.reply_text(welcome_text)

# Función para el comando /help
async def help_command(update, context):
    help_text = (
        "Aquí tienes los comandos disponibles:\n\n"
        "/start - Inicia la interacción con el bot.\n"
        "/help - Muestra esta lista de comandos.\n"
        "/info - Proporciona información sobre el bot.\n"
        
    )
    await update.message.reply_text(help_text)

# Función para el comando /info
async def info_command(update, context):
    info_text = (
        "Bot de Detección de URLs Maliciosas v1.0\n\n"
        "Este bot analiza URLs en tiempo real para detectar posibles amenazas de phishing, malware, "
        "y otros enlaces peligrosos. Utiliza las APIs de Google Safe Browsing y VirusTotal para verificar "
        "la seguridad de los enlaces. \n\n"
        "Comandos disponibles:\n"
        "/start - Inicia la interacción con el bot.\n"
        "/help - Muestra esta lista de comandos.\n"
        "/info - Proporciona información sobre el bot.\n"
      
    )
    await update.message.reply_text(info_text)

# Función para analizar mensajes generales en busca de URLs.
async def mensaje_general(update, context):
    mensaje = update.message.text
    # Flag para seguir si se encontró una URL maliciosa.
    encontrada_url_maliciosa = False
    # Extrae URLs del mensaje usando regex.
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', mensaje)

    for url in urls:
        if await contiene_phishing(url):
            # Si se detecta una URL maliciosa
            encontrada_url_maliciosa = True
            await update.message.reply_text("⚠️ Precaución: Este enlace podría ser peligroso.")
            break
    
    # Si después de revisar todas las URLs no se encontró ninguna maliciosa, informa que parecen seguras.
    if not encontrada_url_maliciosa and urls:
        await update.message.reply_text("✅ Este enlace parece seguro.")


# Función para registrar los manejadores en la aplicación del bot.
def register_handlers(application):
    # Registra el comando /start.
    application.add_handler(CommandHandler("start", start))
    # Registra el comando /help.
    application.add_handler(CommandHandler("help", help_command))
    #Registra el comando /info.
    application.add_handler(CommandHandler("info", info_command))
    # Registra el manejador para analizar textos de mensajes que no sean comandos.
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje_general))
