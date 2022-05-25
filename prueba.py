
from telegram import Update,ReplyKeyboardMarkup,ReplyKeyboardRemove,Bot,InlineKeyboardButton,InlineKeyboardMarkup,KeyboardButton,CallbackQuery,ParseMode
from telegram.ext import CommandHandler,Updater,Dispatcher,MessageHandler,Filters,CallbackContext,CallbackQueryHandler
#from yugiAPI import get_info
import logging
import requests
import os
tkn = os.environ["TOKEN_TEL"]
texto_start = """Hola soy un bot que da información acerca de cartas de yugioh!
Si introduces el nombre de una carta en inglés, te daré información acerca de ella. También, puedes introducir los siguientes parámetros tras el nombre:
    /precio: te dará el precio de la carta
    /descripcion: te dará la descripción de la carta
    /imagen: te dará la imagen de la carta
    /arte: te dará la imagen del arte de la carta"""
## FUNCIONES
def get_info(palabra):

    url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?name='+palabra
    print(url)
    response = requests.get(url)

# return a custom response if an invalid word is provided
    data = response.json()

    if type(data.get("error")) == str:
        error_response = 'La busqueda introducida no coincide con ningun elemento de la base de datos'
        return error_response


    else:
        return data["data"][0]


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(tkn,use_context=True)
bot = Bot(tkn)
dispatcher : Dispatcher = updater.dispatcher

def start(update:Update, context:CallbackContext):
    chat_id = update.effective_chat.id
    txt = update.effective_message.text

    keyboard = [
       [KeyboardButton('/carta')],
       [KeyboardButton('/ayuda')]
    ]
    key = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)


    if txt=="/start":
        context.bot.send_message(chat_id=chat_id, text=texto_start)
        reply_to_message_id=update.effective_message.message_id,
        reply_markup=key
    else:
        opciones = txt.split(" /")
        parametros = opciones[0]
        carta = get_info(opciones.pop(0))

        if type(carta) == str:
            update.message.reply_text(carta)
            return
        nombre = carta["name"]

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
            elif opcion == "arte":
                pagina = "https://storage.googleapis.com/ygoprodeck.com/pics_artgame/" + str(carta["id"]) + ".jpg"
                message += "\n" + pagina
            elif opcion == "sets":
                message += "\nLa carta se encuentra en los siguientes sets: "
                for carta_set in carta['card_sets']:
                    message += "\n  " + carta_set['set_name']
        context.bot.send_message(chat_id=chat_id, text=message)



def main():

    dispatcher.add_handler(MessageHandler(Filters.text,start))
    #dispatcher.add_handler(MessageHandler(Filters.text, conseguir_carta))

    updater.start_polling()


if __name__ == '__main__':
    main()
