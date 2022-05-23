import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from yugiAPI import get_info
import os

telegram_bot_token = os.environ["TOKEN_TEL"]

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher


# set up the introductory statement for the bot when the /start command is invoked
def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Hola soy un bot que da información acerca de cartas de yugioh!")


# obtain the information of the word provided and format before presenting.

def get_word_info(update, context):
    # get the word info
    opciones = update.message.text.split(" /")
    parametros = opciones[0]
    carta = get_info(opciones.pop(0))
    

    # If the user provides an invalid English word, return the custom response from get_info() and exit the function
    if carta.__class__ is str:
        update.message.reply_text(carta)
        return

    # get the word the user provided
    nombre = carta["name"]
    # get the origin of the word

    if len (opciones) == 0:
        opciones=["descripcion","imagen"]
    
    message = f"Carta: {nombre}"
    for opcion in opciones:
        if opcion == "precio":
            precio = carta["card_prices"][0]['tcgplayer_price']
            message += "\nPrecio: $"+ str(precio)
        elif opcion == "descripcion":
            descripcion = carta['desc']
            message += "\nDescripción: "+ descripcion
        elif opcion == "imagen":
            imagen = carta['card_images'][0]['image_url']
            message += "\n" + imagen



    update.message.reply_text(message)

# run the start function when the user invokes the /start command 
dispatcher.add_handler(CommandHandler("start", start))

# invoke the get_word_info function when the user sends a message 
# that is not a command.
dispatcher.add_handler(MessageHandler(Filters.text, get_word_info))
updater.start_polling()