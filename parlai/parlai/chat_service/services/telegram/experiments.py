from telethon import TelegramClient
from telethon.sync import TelegramClient

api_id = 11433542
api_hash = 'dd4f5726f2dff43938ca2c24d10211d7'
bot_token = '5001233718:AAEBZi0TEtU_1FLrt9ZL42hHjiqI-3-oOKs'

# The first parameter is the .session file name (absolute paths allowed)
with TelegramClient('anon', api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message(294026766, 'Hello, myself!'))
