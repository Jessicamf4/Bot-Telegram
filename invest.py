import logging
from typing import Dict
from matplotlib import pyplot as plt
import numpy as np

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_REPLY2, TYPING_CHOICE = range(4)

reply_keyboard = [
    ['Seis Meses', 'Um ano'],
    ['Quatro anos', 'Aposentadoria'],
    ['Mais informações...','Done'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user for input."""
    update.message.reply_text(
        "Olá! Vamos fazer uma estimativa de rendimento? \n"
        "Para isso, selecione o tempo médio que você deseja deixar seu dinheiro investido",
        reply_markup=markup,
    )

    return CHOOSING


def regular_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'Deseja manter seu investimento por {text.lower()}? Certo! Agora, diga o valor que você deseja investir todo mês')

    return TYPING_REPLY


def custom_choice(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(f"Para simular a aposentadoria, iremos considerar um único investimento inicial, o qual será quardado por 30 anos. \n Digite agora o valor que deseja guardar!"
    )
    
    return TYPING_REPLY2

def aposentadoria_receive(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    text = update.message.text
    rendimentoTotal = (float(text)*1.12**30)
    
    update.message.reply_text("Legal! Então, essas são as informações que temos:"
    f"{(user_data)} você deseja investir {text} e deixá-lo guardado durante 30 anos! Ótimo! \n"
    f"Então, o valor total do investimento será de: {rendimentoTotal:.2f}",
    reply_markup=markup,)
    anos=[1, 30]
    renda=[int(text), int(rendimentoTotal)]
    plt.xlabel("Anos")
    plt.ylabel("Rendimento")
    plt.title("Valor inicial X Rendimento final")
    plt.plot(anos, renda, linestyle='dotted', marker='o', color='blue', markersize=4)
    plt.savefig(f"img/{rendimentoTotal}.png")
    update.message.reply_photo(photo=open(f'img/{rendimentoTotal}.png', 'rb'))


def received_information(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    text = update.message.text
    float(text)
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    if category == "Seis Meses":
        m1 = float(text) * 1.04
        m2 = (m1 + float(text)) * 1.04
        m3 = (m2 + float(text)) * 1.04
        m4 = (m3 + float(text)) * 1.04
        m5 = (m4 + float(text)) * 1.04
        m6 = (m5 + float(text)) * 1.04
        valorInvestido = float(text) * 6
        calculoTotal = (valorInvestido + (m6 - valorInvestido)*0.775)
        meses=[m1, m2, m3, m4, m5, m6]
        ordem=[1,2,3,4,5,6]
        plt.xlabel("Número de meses")
        plt.ylabel("Investimento")
        plt.plot(ordem, meses, label='Rendimento', linestyle='--', marker='o', color='blue', markersize=4)
        plt.title('Investimeto durante 6 meses')
        plt.savefig(f"img/{calculoTotal}.png")
        update.message.reply_text("Legal! Então, essas são as informações que temos:"
        f"{facts_to_str(user_data)} você deseja investir {text} todo mês durante o período de {category}! Ótimo! \n"
        f"Então, o valor total do investimento será de: {calculoTotal:.2f}",
        reply_markup=markup,
        )
        update.message.reply_photo(photo=open(f'img/{calculoTotal}.png', 'rb'))
        update.message.reply_text("Vamos ver um gráfico comparando o valor investido e o seu rendimento!")
        valorTotal = valorInvestido+1
        rendimentoTotal = m6 +1
        valor=[valorTotal, rendimentoTotal]
        compare=[1,2]
        def compara():
            plt.xlabel("Valor investido X Valor com rendimento")
            plt.ylabel("Rendimento")
            plt.bar(compare, valor)
            plt.savefig(f"img/{calculoTotal:.2f}.png")
            update.message.reply_photo(photo=open(f'img/{calculoTotal:.2f}.png', 'rb'))
        compara()
        user_data.clear()


    elif category == "Um ano":
        m1 = float(text) * 1.04
        m2 = (m1 + float(text)) * 1.04
        m3 = (m2 + float(text)) * 1.04
        m4 = (m3 + float(text)) * 1.04
        m5 = (m4 + float(text)) * 1.04
        m6 = (m5 + float(text)) * 1.04
        m7 = (m6 + float(text)) * 1.04
        m8 = (m7 + float(text)) * 1.04
        m9 = (m8 + float(text)) * 1.04
        m10 = (m9 + float(text)) * 1.04
        m11 = (m10 + float(text)) * 1.04
        m12 = (m11 + float(text)) * 1.04
        valorInvestido = float(text)*12
        calculoTotal = valorInvestido + (m12 - valorInvestido)*0.8
        meses=[m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12]
        ordem=[1,2,3,4,5,6, 7, 8,9,10,11,12]
        plt.xlabel("Número de meses")
        plt.ylabel("Rendimento")
        plt.plot(ordem,meses)
        plt.savefig(f"img/{calculoTotal}.png")
        update.message.reply_text("Legal! Então, essas são as informações que temos:"
        f"{facts_to_str(user_data)} você deseja investir {text} todo mês durante o período de {category}! Ótimo! \n"
        f"Então, o valor total do investimento será de: {calculoTotal:.2f}",
        reply_markup=markup,
        )
        update.message.reply_photo(photo=open(f'img/{calculoTotal}.png', 'rb'))
        user_data.clear()

    elif category == "Quatro anos":
        m1 = float(text) * 1.04
        m2 = (m1 + float(text)) * 1.04
        m3 = (m2 + float(text)) * 1.04
        m4 = (m3 + float(text)) * 1.04
        m5 = (m4 + float(text)) * 1.04
        m6 = (m5 + float(text)) * 1.04
        m7 = (m6 + float(text)) * 1.04
        m8 = (m7 + float(text)) * 1.04
        m9 = (m8 + float(text)) * 1.04
        m10 = (m9 + float(text)) * 1.04
        m11 = (m10 + float(text)) * 1.04
        m12 = (m11 + float(text)) * 1.04
        m13 = (m12 + float(text)) * 1.04
        m14 = (m13 + float(text)) * 1.04
        m15 = (m14 + float(text)) * 1.04
        m16 = (m15 + float(text)) * 1.04
        m17 = (m16 + float(text)) * 1.04
        m18 = (m17 + float(text)) * 1.04
        m19 = (m18 + float(text)) * 1.04
        m20 = (m19 + float(text)) * 1.04
        m21 = (m20 + float(text)) * 1.04
        m22 = (m21 + float(text)) * 1.04
        m23 = (m22 + float(text)) * 1.04
        m24 = (m23 + float(text)) * 1.04
        m25 = (m24 + float(text)) * 1.04
        m26 = (m25 + float(text)) * 1.04
        m27 = (m26 + float(text)) * 1.04
        m28 = (m27 + float(text)) * 1.04
        m29 = (m28 + float(text)) * 1.04
        m30 = (m29 + float(text)) * 1.04
        m31 = (m30 + float(text)) * 1.04
        m32 = (m31 + float(text)) * 1.04
        m33 = (m32 + float(text)) * 1.04
        m34 = (m33 + float(text)) * 1.04
        m35 = (m34 + float(text)) * 1.04
        m36 = (m35 + float(text)) * 1.04
        m37 = (m36 + float(text)) * 1.04
        m38 = (m37 + float(text)) * 1.04
        m39 = (m38 + float(text)) * 1.04
        m40 = (m39 + float(text)) * 1.04
        m41 = (m40 + float(text)) * 1.04
        m42 = (m41 + float(text)) * 1.04
        m43 = (m42 + float(text)) * 1.04
        m44 = (m43 + float(text)) * 1.04
        m45 = (m44 + float(text)) * 1.04
        m46 = (m45 + float(text)) * 1.04
        m47 = (m46 + float(text)) * 1.04
        m48 = (m47 + float(text)) * 1.04
        valorInvestido = float(text)*48
        calculoTotal = (valorInvestido + (m48 - valorInvestido)*0.85)
        meses=[m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,m22,m23,m24,m25,m26,m27,m28,m29,m30,m31,m32,m33,m34,m35,m36,m37,m38,m39,m40,m41,m42,m43,m44,m45,m46,m47,m48]
        ordem=[1,2,3,4,5,6, 7, 8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48]
        plt.xlabel("Número de meses")
        plt.ylabel("Rendimento")
        plt.plot(ordem,meses)
        plt.savefig(f"img/{calculoTotal}.png")
        update.message.reply_text("Legal! Então, essas são as informações que temos:"
        f"{facts_to_str(user_data)} você deseja investir {text} todo mês durante o período de {category}! Ótimo! \n"
        f"Então, o valor total do investimento será de: {calculoTotal:.2f}",
        reply_markup=markup,
        )
        update.message.reply_photo(photo=open(f'img/{calculoTotal}.png', 'rb'))
        user_data.clear()



    


def done(update: Update, context: CallbackContext) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        f"I learned these facts about you: {facts_to_str(user_data)}Until next time!",
        reply_markup=ReplyKeyboardRemove(),)

    user_data.clear()
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^(Seis Meses|Um ano|Quatro anos)$'), regular_choice
                ),
                MessageHandler(Filters.regex('^(Mais informações...|Aposentadoria)$'), custom_choice),
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    received_information, 
                )
            ],
             TYPING_REPLY2: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    aposentadoria_receive, 
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,

    updater.idle()


if __name__ == '__main__':
    main()