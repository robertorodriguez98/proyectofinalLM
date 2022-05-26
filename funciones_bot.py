import requests
from telegram import Update,ReplyKeyboardMarkup,ReplyKeyboardRemove,Bot,InlineKeyboardButton,InlineKeyboardMarkup,KeyboardButton,CallbackQuery,ParseMode
from telegram.ext import CommandHandler,Updater,Dispatcher,MessageHandler,Filters,CallbackContext,CallbackQueryHandler

def get_info(punto_busqueda,palabra):

    url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?'+punto_busqueda+'='+palabra
    print(url)
    response = requests.get(url)
    data = response.json()

    if type(data.get("error")) == str:
        error_response = 'La busqueda introducida no coincide con ningun elemento de la base de datos'
        return error_response

    else:
        return data["data"]


def datos_carta(update:Update,context:CallbackContext,carta,modificadores,chtiD,bot):
    if type(carta) == str:
        update.message.reply_text(carta)
        return
    #si no es un string, es una lista
    carta = carta[0]
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
    #context.bot.send_message(chat_id=chtiD, text=message)
    # Creamos los botones especificos para la carta que está mostrando
    keyboard = []
    for modificador in modificadores:
        keyboard.append([KeyboardButton('/carta '+nombre+" "+modificador)])
    key = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
    bot.send_message(
        chat_id=chtiD,
        text=message,
        reply_to_message_id=update.effective_message.message_id,
        reply_markup=key
    )