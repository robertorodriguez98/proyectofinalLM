
from telegram import Update,ReplyKeyboardMarkup,ReplyKeyboardRemove,Bot,InlineKeyboardButton,InlineKeyboardMarkup,KeyboardButton,CallbackQuery,ParseMode
from telegram.ext import CommandHandler,Updater,Dispatcher,MessageHandler,Filters,CallbackContext,CallbackQueryHandler
#from yugiAPI import get_info
import logging
from funciones_bot import *
import os
tkn = os.environ["TOKEN_TEL"]
texto_start = """Hola soy un bot que da información acerca de cartas de yugioh!
"""
ayuda_cartas = """Si introduces el nombre de una carta en inglés, te daré información acerca de ella.
La sintaxis para buscar una carta es:
    /carta nombrecarta [opciones]

Las opciones que se pueden introducir son:
        /precios: te dará el precio de la carta
        /descripcion: te dará la descripción de la carta
        /imagen: te dará la imagen de la carta
        /arte: te dará la imagen del arte de la carta

EJEMPLOS:
    /carta Dark Magician
    /carta Kuriboh /precios
    /carta Blue-Eyes White Dragon /arte /sets
"""
ayuda_arquetipo = """Con el comando /arquetipo obtendrás todas las cartas pertenecientes
al arquetipo especificado, pudiendo además seleccionar cualquiera de las cartas para
acceder a sus detalles.

La sintaxis para buscar una arquetipo es:
    /arquetipo nombrearquetipo
    
Algunos arquetipos de ejemplo son:
    /arquetipo abc
    /arquetipo Dark Magician
    /arquetipo Prank-Kids
"""
modificadores = ["/descripcion","/imagen","/arte","/precios","/sets"]


updater = Updater(tkn,use_context=True)
bot = Bot(tkn)
dispatcher : Dispatcher = updater.dispatcher

def start(update:Update, context:CallbackContext):
    chtiD = update.effective_chat.id

    txt = update.effective_message.text

    keyboard = [
        [KeyboardButton('/start')],
        [KeyboardButton('/ayuda cartas')],
        [KeyboardButton('/ayuda arquetipo')],
        [KeyboardButton('/ayuda aleatoria')]
    ]
    key = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)


    if txt=="/start":
        #context.bot.send_message(chat_id=chat_id, text=texto_start)
        bot.send_message(
            chat_id=chtiD,
            text=texto_start,
            reply_to_message_id=update.effective_message.message_id,
            reply_markup=key
        )

    elif txt.startswith("/ayuda"):
        opciones = txt.replace("/ayuda ","")
        if opciones == "cartas":
            keyboard = [
            [KeyboardButton('/carta Dark Magician')],
            [KeyboardButton('/carta Kuriboh /precios')],
            [KeyboardButton('/carta Blue-Eyes White Dragon /arte /sets')]
            ]
            key = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
            bot.send_message(
                chat_id=chtiD,
                text=ayuda_cartas,
                reply_to_message_id=update.effective_message.message_id,
                reply_markup=key
            )
            #context.bot.send_message(chat_id=chtiD, text=ayuda_cartas)
        elif opciones == "arquetipo":
            keyboard = [
            [KeyboardButton('/arquetipo abc')],
            [KeyboardButton('/arquetipo Dark Magician')],
            [KeyboardButton('/arquetipo Prank-Kids')]
            ]
            key = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
            bot.send_message(
                chat_id=chtiD,
                text=ayuda_arquetipo,
                reply_to_message_id=update.effective_message.message_id,
                reply_markup=key
            )
            #context.bot.send_message(chat_id=chtiD, text=ayuda_arquetipo)

    elif txt.startswith("/carta"):
        opciones = txt.replace("/carta ","").split(" /")
        parametros = opciones[0]
        carta = get_info('name',opciones.pop(0))

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


    elif txt.startswith("/arquetipo"):
        opciones = txt.replace("/arquetipo ","")
        #parametros = opciones[0]
        cartas = get_info('archetype',opciones)
        if type(cartas) == str:
            update.message.reply_text(cartas)
            return
        message= f"Arquetipo: {opciones}"
        keyboard = []
        for carta in cartas:
            #carta = carta.json()
            nombre = carta["name"]
            message += "\n  "+nombre
            keyboard.append([KeyboardButton('/carta '+nombre)])
            
        key = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
        bot.send_message(
            chat_id=chtiD,
            text=message,
            reply_to_message_id=update.effective_message.message_id,
            reply_markup=key
        )
        #context.bot.send_message(chat_id=chtiD, text=message)
    elif txt.startswith("/aleatoria"):
        carta = get_info('random',"da igual")

        if type(carta) == str:
            update.message.reply_text(carta)
            return
        #si no es un string, es una lista
        nombre = carta["name"]
        message = f"Carta: {nombre}"+"\nDescripción: "+ carta['desc']+"\n" + carta['card_images'][0]['image_url']
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
        #context.bot.send_message(chat_id=chtiD, text=message)

def main():

    dispatcher.add_handler(MessageHandler(Filters.text,start))
    #dispatcher.add_handler(MessageHandler(Filters.text, conseguir_carta))

    updater.start_polling()


if __name__ == '__main__':
    main()
