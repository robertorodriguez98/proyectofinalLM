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
    context.bot.send_message(chat_id=chat_id, text="""Hola soy un bot que da información acerca de cartas de yugioh!
Si introduces el nombre de una carta en inglés, te daré información acerca de ella. También, puedes introducir los siguientes parámetros tras el nombre:
    /precio: te dará el precio de la carta
    /descripcion: te dará la descripción de la carta
    /imagen: te dará la imagen de la carta""")



# obtain the information of the word provided and format before presenting.

def get_word_info(update, context):
    # get the word info
    opciones = update.message.text.split(" /")
    parametros = opciones[0]
    carta = get_info(opciones.pop(0))
    print(carta)

    # If the user provides an invalid English word, return the custom response from get_info() and exit the function
    if type(carta) == str:
        update.message.reply_text(carta)
        return

    # get the word the user provided
    nombre = carta["name"]
    # get the origin of the word

    if len (opciones) == 0:
        opciones=["descripcion","imagen"]
    
    message = f"Carta: {nombre}"
    for opcion in opciones:
        if opcion == "precios":
            message += "\nLa carta tiene los siguientes precios:"
            for pagina, precio in carta["card_prices"][0].items():
                nombrepag=pagina.split("_")
                message += "\n  "+nombrepag[0]+": $"+ str(precio)
        elif opcion == "descripcion":
            message += "\nDescripción: "+ carta['desc']
        elif opcion == "imagen":
            message += "\n" + carta['card_images'][0]['image_url']
        elif opcion == "sets":
            message += "\nLa carta se encuentra en los siguientes sets: "
            for carta_set in carta['card_sets']:
                message += "\n  " + carta_set['set_name']


    update.message.reply_text(message)

# run the start function when the user invokes the /start command 
dispatcher.add_handler(CommandHandler("start", start))

# invoke the get_word_info function when the user sends a message 
# that is not a command.
dispatcher.add_handler(MessageHandler(Filters.text, get_word_info))
#updater.start_polling()
updater.start_webhook(listen="0.0.0.0",
                      port=int(os.environ.get('PORT', 5000)),
                      url_path=telegram_bot_token,
                      webhook_url=  + telegram_bot_token
                      )