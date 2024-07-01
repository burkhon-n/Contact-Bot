import telebot
from config import *
from functions import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '🇺🇿 Assalomu alaykum!\n🛍️ Lolo Store Telegram botiga xush kelibsiz!\n\n💌 Buyurtma berish, taklif va murojaatlar uchun botga xabar yuboring:\n\n---------------------\n\n🇺🇿 Здравствуйте!\n🛍️ Добро пожаловать в Telegram-бот Lolo Store!\n\n💌 Для заказа, предложений и вопросов пишите боту:')

@bot.message_handler(['user'])
def return_user(message: types.Message):
    messages = get_messages()
    if str(message.from_user.id) == ADMIN:
        if message.reply_to_message:
            rp_msg_id = get_id_with_admin(message.reply_to_message.message_id)
            if rp_msg_id != None:
                rp_msg = messages[rp_msg_id]['message']
                bot.send_message(ADMIN, "Username: @" + rp_msg['from'].get('username') + "\nName: " + rp_msg['from'].get('first_name') + (" " + rp_msg['from'].get('last_name') if rp_msg['from'].get('last_name') else ""), reply_to_message_id=message.reply_to_message.message_id)
            else:
                bot.send_message(ADMIN, "Reply to user's message to get the user details.")
        else:
            bot.send_message(ADMIN, "Reply to a message to get the user details.")
    elif str(message.from_user.id) == GUEST:
        if message.reply_to_message:
            rp_msg_id = get_id_with_guest(message.reply_to_message.message_id)
            if rp_msg_id != None:
                rp_msg = messages[rp_msg_id]['message']
                bot.send_message(GUEST, "Username: @" + rp_msg['from'].get('username') + "\nName: " + rp_msg['from'].get('first_name') + (" " + rp_msg['from'].get('last_name') if rp_msg['from'].get('last_name') else ""), reply_to_message_id=message.reply_to_message.message_id)
            else:
                bot.send_message(GUEST, "Reply to user's message to get the user details.")
        else:
            bot.send_message(GUEST, "Reply to a message to get the user details.")


#all content types
@bot.message_handler(content_types=['text', 'photo', 'video', 'video_note', 'sticker', 'location', 'contact', 'file', 'document', "audio", 'voice'])
def echo_all(message: types.Message):
    clear_messages(30)
    if not (str(message.from_user.id) == ADMIN or str(message.from_user.id) == GUEST):
        messages = get_messages()
        admin_msg = bot.forward_message(ADMIN, message.chat.id, message.message_id)
        guest_msg = bot.forward_message(GUEST, message.chat.id, message.message_id)
        messages.append({
            'admin': admin_msg.message_id,
            'guest': guest_msg.message_id,
            'message': message.json
        })
        save_messages(messages)
    elif str(message.from_user.id) == ADMIN and message.reply_to_message:
        messages = get_messages()
        rp_msg = messages[get_id_with_admin(message.reply_to_message.message_id)]
        if rp_msg:
            bot.copy_message(rp_msg['message']['from']['id'], message.chat.id, message.message_id)
            if message.content_type == "text":
                bot.send_message(GUEST, message.text, reply_to_message_id=rp_msg['guest'])
            elif message.content_type == "photo":
                bot.send_photo(GUEST, message.photo[-1].file_id, reply_to_message_id=rp_msg['guest'])
            elif message.content_type == "video":
                bot.send_video(GUEST, message.video.file_id, reply_to_message_id=rp_msg['guest'])
            elif message.content_type == "video_note":
                bot.send_video_note(GUEST, message.video_note.file_id, reply_to_message_id=rp_msg['guest'])
            elif message.content_type == "sticker":
                bot.send_sticker(GUEST, message.sticker.file_id, reply_to_message_id=rp_msg['guest'])
            elif message.content_type == "location":
                bot.send_location(GUEST, message.location.latitude, message.location.longitude, reply_to_message_id=rp_msg['guest'])
            elif message.content_type == "contact":
                bot.send_contact(GUEST, message.contact.phone_number, message.contact.first_name, reply_to_message_id=rp_msg['guest'])
            elif message.content_type == "file":
                bot.send_document(GUEST, message.document.file_id, reply_to_message_id=rp_msg['guest'])
            elif message.content_type == "document":
                bot.send_document(GUEST, message.document.file_id, reply_to_message_id=rp_msg['guest'])
            elif message.content_type == "audio":
                bot.send_audio(GUEST, message.audio.file_id, reply_to_message_id=rp_msg['guest'])
            elif message.content_type == "voice":
                bot.send_voice(GUEST, message.voice.file_id, reply_to_message_id=rp_msg['guest'])
            else:
                bot.send_message(GUEST, "Unsupported content type.", reply_to_message_id=rp_msg['guest'])
    elif str(message.from_user.id) == ADMIN and not message.reply_to_message:
        bot.send_message(message.chat.id, "Reply to a message to send it to the user.")

bot.polling()
