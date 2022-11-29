import logging
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackContext


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def estimativa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Vamos fazer uma estimativa sobre investimentos de acondo com as informações dadas, para isso digite /caucular')


async def calcular(self, update_result, lastMsg=False):
        update = self.getCurrentUpdate(update_result)
        if self.previous_update_id != self.current_update_id:
            _message_obj = self.getMessage(update)
            _message_obj.m_from = self.getUser(update)
            self.getInitialTime(_message_obj)
            data = {self.current_update_id: _message_obj}
            del _message_obj

            if lastMsg:
                self.datas = {}     

            self.datas.update(data)
        
        await update.message.reply_text(f'Hello {lastMsg}')
        return

async def gerar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Digite o perído que você deseja recolher o dinheiro')
    @Bot.message_handler(func=lambda message: True)
    def echo_message(message):
        cid = message.chat.id
        mid = message.message_id 
        message_text = message.text 
        user_id = message.from_user.id 
        user_name = message.from_user.first_name 
        periodo = message.text
    
async def lucro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Digite o lucro desejavo:')
    @Bot.message_handler(func=lambda message: True)
    def echo_message(message):
        cid = message.chat.id
        mid = message.message_id 
        message_text = message.text 
        user_id = message.from_user.id 
        user_name = message.from_user.first_name 
        lucro = message.text
 




app = ApplicationBuilder().token("").build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("estimativa", estimativa))

app.run_polling()




