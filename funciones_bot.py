import requests
from telegram import Update,ReplyKeyboardMarkup,ReplyKeyboardRemove,Bot,InlineKeyboardButton,InlineKeyboardMarkup,KeyboardButton,CallbackQuery,ParseMode
from telegram.ext import CommandHandler,Updater,Dispatcher,MessageHandler,Filters,CallbackContext,CallbackQueryHandler

def get_info(punto_busqueda,palabra):
    if punto_busqueda == "random":
        url = "https://db.ygoprodeck.com/api/v7/randomcard.php"
    else:
        url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?'+punto_busqueda+'='+palabra
    print(url)
    response = requests.get(url)
    data = response.json()

    if type(data.get("error")) == str:
        error_response = 'La busqueda introducida no coincide con ningun elemento de la base de datos'
        return error_response

    else:
        return data["data"]

