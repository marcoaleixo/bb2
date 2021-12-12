import requests
import argparse

from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup

TOKEN = "5001233718:AAEBZi0TEtU_1FLrt9ZL42hHjiqI-3-oOKs"

parser = argparse.ArgumentParser(description="Telegram bot for API testing.")
parser.add_argument('--api_hostname', default="localhost", help="ParlAI API hostname.")
parser.add_argument('--api_port', type=int, default=8080, help="ParlAI API port.")

args = parser.parse_args()

api_hostname = args.api_hostname
api_port = args.api_port
api_uri = f"http://{api_hostname}:{api_port}/api"

message_history = {}


def translate_message(message, src='auto', dest='en'):
    # translation = translator.translate(message, src=src, dest=dest)

    return message


def set_lang(update, context):
    try:
        lang = context.args[0]
        translation = translate_message("Language has set:", dest=lang).text + " " + lang

        update.message.reply_text(translation)
        context.user_data["lang"] = lang
    except Exception as e:
        text = "usage: /set_lang <language>"
        update.message.reply_text(text)


def send_response(update, context, response):
    quick_replies = response.get('quick_replies')

    if quick_replies:
        keyboard = [quick_replies]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        update.message.reply_text(response.get('text'), reply_markup=markup)
        return

    update.message.reply_text(response.get('text'))


def send_message(update, context):
    chat_id = update.message.chat_id
    message_text = update.message.text

    if chat_id not in message_history:
        message_history[chat_id] = []

    message_history[chat_id].append(message_text)

    if "lang" in context.user_data:
        message_text = translate_message(message_text, src=context.user_data["lang"]).text

    # response = requests.post(f'{api_uri}/send_message', json={"message_text": message_text, "message_history": message_history[chat_id]})

    url = "http://client_core:8080/interact"

    headers = {}
    response = requests.request("POST", url, headers=headers, data=message_text)

    print(response.text)

    try:
        response = response.json()
        message_history[chat_id].append(response.get('text'))

        if "lang" in context.user_data:
            response["text"] = translate_message(response["text"], src="en", dest=context.user_data["lang"]).text

        send_response(update, context, response)
    except Exception as e:
        text = "We are unable to handle your request. Please try later."
        update.message.reply_text(text)
        raise e


def help(update, context):
    message = f"ParlAI bot.\n"
    message += f"/set_lang <language> - set language."
    message += "All messages will be passed to bot.\n"

    update.message.reply_text(message)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, send_message, pass_user_data=True)

    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("set_lang", set_lang, pass_user_data=True, pass_args=True))

    dp.add_handler(text_handler)

    print("Telegram pooling started.")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()