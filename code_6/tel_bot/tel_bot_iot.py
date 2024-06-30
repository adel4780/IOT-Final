import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '7424372977:AAGWFcuuAXbELpwc0kf0ngj0N10MV4DEA5E'  # جایگزین با توکن ربات تلگرام شما

API_URL_TURN_ON = 'https://danial.pythonanywhere.com/on'  # URL برای روشن کردن دستگاه
API_URL_TURN_OFF = 'https://danial.pythonanywhere.com/off'  # URL برای خاموش کردن دستگاه
API_URL_SET_TIMING = 'https://danial.pythonanywhere.com/schedule'  # URL برای تنظیم زمان‌بندی
API_URL_UPDATE_STATUS = 'https://danial.pythonanywhere.com/getStatus'  # URL برای به‌روزرسانی وضعیت

bot = telebot.TeleBot(TOKEN)

def create_inline_keyboard():
    markup = InlineKeyboardMarkup()
    row1 = [
        InlineKeyboardButton("📊 Update Status", callback_data='update_status'),
    ]
    row2 = [
        InlineKeyboardButton("💡 Turn On", callback_data='turn_on'),
        InlineKeyboardButton("🔌 Turn Off", callback_data='turn_off'),
    ]
    row3 = [
        InlineKeyboardButton("⏲️ Set Timing", callback_data='set_timing'),
    ]
    markup.add(*row1)
    markup.add(*row2)
    markup.add(*row3)
    return markup

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'update_status':
        response = requests.get(API_URL_UPDATE_STATUS)
        data = response.json()
        bot.send_message(call.message.chat.id, f"📊 Status: {data['status']}\n"
                                               f"Time On: {data['scheduling']['time_on']} ms\n"
                                               f"Time Off: {data['scheduling']['time_off']} ms",
                         reply_markup=create_inline_keyboard())
    elif call.data == 'turn_on':
        response = requests.get(API_URL_TURN_ON)
        data = response.json()
        bot.send_message(call.message.chat.id, f"💡 Status: {data['status']}\n", reply_markup=create_inline_keyboard())
    elif call.data == 'turn_off':
        response = requests.get(API_URL_TURN_OFF)
        data = response.json()
        bot.send_message(call.message.chat.id, f"🔌 Status: {data['status']}\n", reply_markup=create_inline_keyboard())
    elif call.data == 'set_timing':
        msg = bot.send_message(call.message.chat.id,
                               "⏲️ Enter on_time_millisecond and off_time_millisecond (e.g., 5000 10000):")
        bot.register_next_step_handler(msg, process_timing_step)

def process_timing_step(message):
    try:
        on_time, off_time = message.text.split()
        params = {
            'ON': int(on_time),
            'OFF': int(off_time)
        }
        response = requests.get(API_URL_SET_TIMING, params=params)
        
        # Check if response status code is OK (200)
        if response.status_code == 200:
            try:
                data = response.json()
                bot.send_message(message.chat.id,
                                 f"Timing set successfully.\n"
                                 f"Status: {data['status']}\n"
                                 f"Time On: {data['scheduling']['time_on']} ms\n"
                                 f"Time Off: {data['scheduling']['time_off']} ms",
                                 reply_markup=create_inline_keyboard())
            except ValueError as ve:
                bot.send_message(message.chat.id, f"😜 Status: blinking\nTime On: {on_time} ms\nTime Off: {off_time} ms", reply_markup=create_inline_keyboard())
            except KeyError as ke:
                bot.send_message(message.chat.id, f"Key error in JSON response: {ke}")
        else:
            bot.send_message(message.chat.id, f"Error fetching data: Status code {response.status_code}")
    
    except Exception as e:
        bot.send_message(message.chat.id, f"Error setting timing: {str(e)}")

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    """Sends a message with the inline keyboard to the user."""
    bot.send_message(
        message.chat.id,
        "Welcome! Here are the options:",
        reply_markup=create_inline_keyboard()
    )

# Start polling
bot.polling()