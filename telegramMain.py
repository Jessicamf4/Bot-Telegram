import json
import logging
from typing import Self
from telegram import*
from telegram.ext import*
import responses as R

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def estimativa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Vamos fazer uma estimativa sobre investimentos de acondo com as informações dadas, para isso digite /setcommands')


def tempInvest(bot, update):
  bot.message.reply_text(main_menu_message(),
                         reply_markup=main_menu_keyboard())

def main_menu(bot, update):
    bot.callback_query.message.edit_text(main_menu_message(),
                          reply_markup=main_menu_keyboard())

def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Por seis meses', callback_data='seisMeses')],
              [InlineKeyboardButton('Menu 2', callback_data='m2')],
              [InlineKeyboardButton('Menu 3', callback_data='m3')]]
    return InlineKeyboardMarkup(keyboard)

def main_menu_message():
  return 'Escolha o tempo determinada'
        
def seisMeses(update, context, input_text):
    return Self.filters.check_update(update) 
    update.message.reply_text(f'Simule um valor a investir todo mês: ')
    user_message = str(input_text).lower()
    text = update.Message.Text
    valorEstimado = ((user_message *1,16) + user_message) * 1,16
    update.message.reply_text(f'Valor em seis meses: f{valorEstimado}')

def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_responses(text)
    update.message.reply_text(response)






app = ApplicationBuilder().token("").build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("estimativa", estimativa))
app.dispatcher.add_handler(CommandHandler('tempInvest', tempInvest))
app.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
app.add_handler(CommandHandler("seisMeses", seisMeses))

app.add_handler(MessageHandler(filters.Text, handle_message, Update))

app.run_polling(120)



 