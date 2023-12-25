from telegram import Update
import whois
from datetime import datetime
from telegram.ext.filters import Filters
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from decouple import config
token = config('token')
bot_username = config('bot_username')


def start_command(update: Update, context):
    update.message.reply_text('Hello there! How are you doing?')


def help_command(update: Update, context):
    update.message.reply_text('I can only help with validating websites and checking urls and giving information about them....To know about a specific website or url just paste the website name e.g web-website name')


greetings = ['hello', 'hi', 'yo', 'whatsup', 'guy', 'gee']


def handle_responses(text: str):
    change_text = text.lower()
    if change_text in greetings:
        return 'Hey there!'

    elif 'how are you' in change_text:
        return 'I am good'
    elif 'web' in change_text:
        new_text = change_text
        update_text = new_text.split('--')
        get_website_name = update_text[1]
        try:
            check_online = whois.whois(get_website_name)
            current_year = datetime.now().year  # Change this line
            website_date = check_online.creation_date.year
            date_gap = (current_year - website_date)
            if date_gap > 4:
                  response = f'Company Name:{check_online.org}\nCreation Date:{check_online.creation_date}\nEmail:{check_online.emails}....The site has gained {date_gap} of experience, which is quite moderate for a normal business based on the facts that it has gained and gathered knowledge enough due to past experiences but you can still do well to make further findings'
                  return response
            else:
                  response = f'Company Name:{check_online.org}\nCreation Date:{check_online.creation_date}\nEmail:{check_online.emails}....The site has gained {date_gap} of experience, which is not up to the requirements given.........'
                  return response
        except:
            return f'There was an error made,cannot not verify this website {get_website_name}'

    else:
        return 'I do not understand what you wrote....'

def handle_message(update: Update, context):
    message_type = update.message.chat.type
    text = update.message.text

#     print(f'User ({update.message.chat.id}) in {message_type}:"{text}"')

    if message_type == 'group':
        if bot_username in text:
            new_text = text.replace(bot_username, '').strip()
            response = handle_responses(new_text)
        else:
            return

    else:
        response = handle_responses(text)

    print('Bot', response)
    update.message.reply_text(response)


def error(update: Update, context):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot.....')
    app = Updater(token)
    dp = app.dispatcher

    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    print('Polling....')
    app.start_polling()
    app.idle()
