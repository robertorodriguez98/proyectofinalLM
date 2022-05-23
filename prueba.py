
from telegram import Update,ReplyKeyboardMarkup,ReplyKeyboardRemove,Bot,InlineKeyboardButton,InlineKeyboardMarkup,KeyboardButton,CallbackQuery,ParseMode
from telegram.ext import CommandHandler,Updater,Dispatcher,MessageHandler,Filters,CallbackContext,CallbackQueryHandler
#from yugiAPI import get_info
import logging
import requests
import os
tkn = os.environ["TOKEN_TEL"]

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

# def start(update:Update, context:CallbackContext):
#    firstname = update.effective_message.from_user.first_name
#    chtiD = update.effective_message.chat_id
#    username = update.effective_message.from_user.username
#    txt = update.effective_message.text
#    keyboard = [
#        [KeyboardButton('Help')],
#        [KeyboardButton('Contact us')]
#    ]
#    key = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)


#    if txt=="Help":
#        bot.send_message(
#            chat_id=chtiD,
#            text="How to Deploy Your Telegram bot on Heroku\n\nچگونه ربات خود را در Heroku راه اندازی کنید",
#            reply_to_message_id=update.effective_message.message_id,
#        )
#    elif txt=="Contact us":
#        bot.send_message(
#            chat_id=chtiD,
#            text="<u>Website : </u>Rexxar.ir\n\n<i>Telegram : </i>@Rexxar_ir",
#            reply_to_message_id=update.effective_message.message_id,
#            parse_mode=ParseMode.HTML
#        )
#    else:
#        bot.send_message(
#            chat_id=chtiD,
#            text=f"Nombre: {firstname}" + f"\n\ Apellido: {username}" + f"\n\ ID: {str(chtiD)}",
#            reply_to_message_id=update.effective_message.message_id,
#            reply_markup=key


#        )

def start(update:Update, context:CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="""Hola soy un bot que da información acerca de cartas de yugioh!
Si introduces el nombre de una carta en inglés, te daré información acerca de ella. También, puedes introducir los siguientes parámetros tras el nombre:
    /precio: te dará el precio de la carta
    /descripcion: te dará la descripción de la carta
    /imagen: te dará la imagen de la carta""")  


def main():

    dispatcher.add_handler(MessageHandler(Filters.text,start))
    #dispatcher.add_handler(MessageHandler(Filters.text, conseguir_carta))

    updater.start_polling()


if __name__ == '__main__':
    main()
