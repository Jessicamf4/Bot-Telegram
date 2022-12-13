import json
import logging
import token
from telegram import*
from telegram.ext import*
import responses as R

async def start(update: Update, context: CallbackContext) -> None:
    update.messagem.reply_text("Olá!")

async def hello(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def estimativa(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f'Vamos fazer uma estimativa sobre investimentos de acordo com as informações dadas, para isso selecione o tempo para manter seu dinheiro investido: \n /seisMeses \n umAno \n quatroAnos \n /trintaAnos')

logger = logging.getLogger(__name__)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def seisMeses(update, context, args):
    update.message.reply_text(int(context.args[0]))
    #update.message.reply_text(f'Simule um valor a investir todo mês: ')
    #text = int(context.args[0])

    #valorEstimado = (((text *1,16) + text) * 1,16)
    #update.message.reply_text('Valor em seis meses:' + valorEstimado )



def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_responses(text)
    update.message.reply_text(response)



app = ApplicationBuilder().token("").build()

updater = Updater('', use_context=True)
app = updater.dispatcher
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("estimativa", estimativa))
app.add_handler(CommandHandler('seisMeses', seisMeses))
app.add_handler(CommandHandler("seisMeses", seisMeses))
updater.dispatcher.add_handler(CommandHandler('cmd', seisMeses, pass_args=True))

#app.add_handler(MessageHandler(filters.Text, seisMeses))

app.run_polling(120)

app.idle()

 