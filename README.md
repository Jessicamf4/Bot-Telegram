

async def setcommands(update_result, update, selfult):
    await update.message.reply_text(f'Por quanto tempo quer investir?')
    {
            "commands": json.dumps[
            {
                "command": "seisMeses",
                "description" : "Por 6 meses"
            },
            {
                "command": "/umAno",
                "description" : "Por 1 ano"
            },
            {
                "command": "/quatroAnos",
                "description" : "Por 4 anos"
            },
            {
                "command": "trintaAnos",
                "description" : "Por 30 anos"
            }
            ],
            "language_code": "en"

        }

        # @Bot.message_handler(func=lambda message: True)
  #  def echo_message(message):
   #     cid = message.chat.id
#    mid = message.message_id 
#        message_text = message.text 
#        user_id = message.from_user.id 
#        user_name = message.from_user.first_name 
#        periodo = message.text
    

 
