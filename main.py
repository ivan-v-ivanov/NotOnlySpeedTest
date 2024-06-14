# -*- coding: utf-8 -*-
import os
import telebot
import time
from datetime import datetime
import subprocess
from methods import get_host_info, check_latency, speedtest, get_home_ping, check_webserver

headers = {'User-Agent': 'ENTER YOUR USER AGENT'}

hostname, host_ip = get_host_info()

bot = telebot.TeleBot("ENTER_YOUR_TOKEN")
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
speedtest_button = telebot.types.KeyboardButton(f'📄Speedtest for {hostname}')
latency_button = telebot.types.KeyboardButton(f'⏱️Pingcheck for {hostname}')
webserver_button = telebot.types.KeyboardButton(f'Webserver status')
keyboard.row(speedtest_button, latency_button, webserver_button)

welcome_message = f'''Hi dude. You can make some tests of your servers. Also I\'ll show you some alerts.'''

output_header = f"VPN server: {hostname}\nIP: {host_ip}\n\n"
speedtest_output = "Speedtest results:\n📥 {}\n📤 {}"
latency_output = "🏓Ping results:\nENTER_SERVER_1: {}\nENTER_SERVER_2: {}\nENTER_SERVER_3: {}\nHOME: {}"

def get_output(input_message):
    print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} {input_message}")
    if input_message == speedtest_button.text:
        result = speedtest()
        result_message = output_header + speedtest_output.format(result[1], result[2])
    elif input_message == latency_button.text:
        result = check_latency('server_1'), check_latency('server_2'), check_latency('server_3'), get_home_ping()
        result_message = output_header + latency_output.format(result[0], result[1], result[2], result[3])
    elif input_message == webserver_button.text:
        result = check_webserver()
        result_message = output_header + result
    else:
        cmd = subprocess.Popen(['./command_line', input_message], stdout=subprocess.PIPE)
        result_message = ''#str(cmd.communicate()[0])[2:-3]
    print(input_message)
    return {'message': result_message}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     welcome_message,
                     reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def send_result(message):
    result = get_output(message.text)
    bot.send_message(message.chat.id,
                     result['message'],
                     disable_web_page_preview=True)

print(f"Bot starts {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
bot.infinity_polling(timeout=20, long_polling_timeout = 5)
