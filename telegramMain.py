import json
import logging
from telegram import*
from telegram.ext import*
import responses as R

async def start(update: Update, context: CallbackContext) -> None:
    update.messagem.reply_text("Olá!")

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def estimativa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Vamos fazer uma estimativa sobre investimentos de acordo com as informações dadas, para isso selecione o tempo para manter seu dinheiro investido: \n /seisMeses \n umAno \n quatroAnos \n /trintaAnos')


def tempInvest(bot, update):
  bot.message.reply_text(main_menu_message(),
                         reply_markup=main_menu_keyboard())


async def seisMeses(update, context):
    update.message.reply_text(f'Simule um valor a investir todo mês: ')
    text = int(context.args[0])
    valorEstimado = (((text *1,16) + text) * 1,16)
    update.message.reply_text('Valor em seis meses:' + valorEstimado )



#MENU

def main_menu(bot, update):
    bot.callback_query.message.edit_text(main_menu_message(),
                          reply_markup=main_menu_keyboard())

def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Por seis meses', callback_data='seisMeses')],
              [InlineKeyboardButton('Menu 2', callback_data='m2')],
              [InlineKeyboardButton('Menu 3', callback_data='m3')]]
    return InlineKeyboardMarkup(keyboard)

def main_menu_message():
  return 'Escolha o tempo determinado'
        


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_responses(text)
    update.message.reply_text(response)




app = ApplicationBuilder().token("").build()


app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("estimativa", estimativa))
app.add_handler(CommandHandler('tempInvest', tempInvest))
app.add_handler(CommandHandler('seisMeses', seisMeses))
app.add_handler(CommandHandler("seisMeses", seisMeses))

app.add_handler(MessageHandler(filters.Text, seisMeses))

app.run_polling(120)

app.idle()

 