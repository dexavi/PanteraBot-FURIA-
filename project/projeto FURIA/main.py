from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN: Final = '7984505258:AAE1tlBMl7WdlDrW5Lzaa4UNRbqqRM2h6gE'
BOT_USERNAME: Final = '@pantera_furiabot'

# Comandos
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Opa Furioso(a), seja bem vindo(a) ao chat da Pantera!\n' 'Digite /help para ver os comandos que poderão ser respondidos.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Digite /menu para ver as opções que posso responder.\n' '/custom 👀')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Você descobriu o comando secreto... mas e agora? 👀')

# Comando /menu 
async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("O que é FURIA?", callback_data='pergunta_furia')],
        [InlineKeyboardButton("O que é o projeto?", callback_data='pergunta_projeto')],
        [InlineKeyboardButton("Redes Sociais", callback_data='pergunta_redes')],
        [InlineKeyboardButton("Eventos", callback_data='pergunta_eventos')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Escolha uma opção:", reply_markup=reply_markup)

# Respostas baseadas nos botões
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'pergunta_furia':
        await query.edit_message_text("A FURIA é uma organização brasileira de eSports conhecida mundialmente no cenário de CS:GO e outros jogos.")
    elif query.data == 'pergunta_projeto':
        await query.edit_message_text("O projeto é um chatbot criado para interagir com fãs da FURIA, oferecendo informações de forma automatizada.\n" "A principio a criação deste chatbot é para um complemento de uma landing page para um processo seletivo dentro da FURIA!!")
    elif query.data == 'pergunta_redes':
        await query.edit_message_text("Siga a FURIA nas redes sociais:\n- Instagram: @furiagg\n- Twitter: @furiagg\n- YouTube: FURIA")
    elif query.data == 'pergunta_eventos':
        await query.edit_message_text("Os próximos eventos da FURIA você consegue acessar aqui:\n- Link: https://draft5.gg/equipe/330-FURIA/campeonatos \n- ")
    else:
        await query.edit_message_text("Opção inválida.")

#Mensagens
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'oi' in processed:
        return 'Eai!!'
    if 'como você está?' in processed:
        return 'Estou bem!'
    if 'irei passar nesta vaga?' in processed:
        return 'Simmm!!'

    return 'Eu não entendi o que você quis dizer!'

#Mensagens gerais
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    if text is None:
        return

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return 
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

# Tratamento de erro
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

# Inicializador
if __name__ == '__main__':
    print ('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('menu', menu_command))  

    
    app.add_handler(CallbackQueryHandler(button_callback))

    
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Erro
    app.add_error_handler(error)

    #Ao rodar o bot
    print('Polling...')
    app.run_polling(poll_interval=3)
