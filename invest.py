import logging
from typing import Dict
from matplotlib import pyplot as plt
import numpy as np

from telegram import Bot, ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
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
    ['Mais informações...','Feito!'],
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
        "\n Para isso, selecione o tempo médio que você deseja deixar seu dinheiro investido.",
        reply_markup=markup,
    )

    return CHOOSING


def regular_choice(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'Deseja manter seu investimento por {text.lower()}? \n Certo! Agora, diga o valor que você estima investir todo mês')

    return TYPING_REPLY


def custom_choice(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(f"Para simular a aposentadoria, iremos considerar um único investimento inicial, o qual será guardado por 30 anos. \n \nDigite agora o valor que deseja guardar!"
    )
    
    return TYPING_REPLY2

def aposentadoria_receive(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    text = update.message.text
    rendimentoTotal = (float(text)*1.12**30)
    
    update.message.reply_text("Legal! Então, essas são as informações que temos:"
    f"{(user_data)} você deseja investir {text} e deixá-lo guardado durante 30 anos!  \n"
    f"\n Então, o valor total do investimento será de: {rendimentoTotal:.2f}",
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
        a = 0
        valorMensal = float(text)
        valorTotal = 0
        meses = []
        while a < 6:
            valorTotal = (valorTotal + valorMensal)* 1.04
            a+=1
            meses.append(valorTotal)
        valorInvestido = float(text) * 6
        calculoTotal = (valorInvestido + (valorTotal - valorInvestido)*0.775)
        ordem=[1,2,3,4,5,6]
        plt.xlabel("Número de meses")
        plt.ylabel("Investimento")
        plt.plot(ordem, meses, label='Rendimento', linestyle='--', marker='o', color='blue', markersize=4)
        plt.title('Investimeto durante 6 meses')
        plt.savefig(f"img/{calculoTotal}.png")
        update.message.reply_text("Legal! Então, essas são as informações que temos:"
        f"{facts_to_str(user_data)} você deseja investir {text} todo mês durante o período de {category}! Ótimo! \n"
        f"\n Então, o valor total do investimento será de: {calculoTotal:.2f}",
        reply_markup=markup,
        )
        update.message.reply_photo(photo=open(f'img/{calculoTotal}.png', 'rb'))
        update.message.reply_text("Vamos ver um gráfico comparando o valor investido e o seu rendimento!")
        valor=[valorInvestido, valorTotal]
        compare=[1,2]
        def compara():
            plt.xlabel("Valor investido X Valor com rendimento")
            plt.ylabel("Rendimento")
            plt.bar(compare, valor)
            plt.savefig(f"img/{calculoTotal:.2f}.png")
            update.message.reply_photo(photo=open(f'img/{calculoTotal:.2f}.png', 'rb'))
        compara()
        


    elif category == "Um ano":
        a = 0
        valorMensal = float(text)
        valorTotal = 0
        meses = []

        while a < 12:
            valorTotal = (valorTotal + valorMensal)* 1.04
            a+=1
            meses.append(valorTotal)

        valorInvestido = float(text) * 12
        calculoTotal = valorInvestido + (valorTotal)*0.8
        ordem=[1,2,3,4,5,6, 7, 8,9,10,11,12]
        plt.xlabel("Número de meses")
        plt.ylabel("Rendimento")
        plt.plot(ordem,meses)
        plt.savefig(f"img/{calculoTotal}.png")
        update.message.reply_text("Legal! Então, essas são as informações que temos:"
        f"{facts_to_str(user_data)} você deseja investir {text} todo mês durante o período de {category}! Ótimo! \n"
        f"\n Então, o valor total do investimento será de: {calculoTotal:.2f}",
        reply_markup=markup,
        )
        update.message.reply_photo(photo=open(f'img/{calculoTotal}.png', 'rb'))
        

    elif category == "Quatro anos":
        a = 0
        valorMensal = float(text)
        valorTotal = 0
        meses = []

        while a < 12:
            valorTotal = (valorTotal + valorMensal)* 1.04
            a+=1
            meses.append(valorTotal)
        valorInvestido = float(text)*48
        calculoTotal = (valorInvestido + (valorTotal)*0.85)
        
        ordem=[1,2,3,4,5,6, 7, 8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48]
        plt.xlabel("Número de meses")
        plt.ylabel("Rendimento")
        plt.plot(ordem,meses)
        plt.savefig(f"img/{calculoTotal}.png")
        update.message.reply_text("Legal! Então, essas são as informações que temos:"
        f"{facts_to_str(user_data)} você deseja investir {text} todo mês durante o período de {category}! Ótimo! \n"
        f"\n Então, o valor total do investimento será de: {calculoTotal:.2f}",
        reply_markup=markup,
        )
        update.message.reply_photo(photo=open(f'img/{calculoTotal}.png', 'rb'))
        

    return TYPING_CHOICE
    


def done(update: Update, context: CallbackContext) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        f"As informações que obtivemos foram: {facts_to_str(user_data)} . Até a próxima!",
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
                    Filters.text & ~(Filters.command | Filters.regex('^Feito!$')), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Feito!$')),
                    received_information, 
                )
            ],
             TYPING_REPLY2: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Feito!$')),
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
