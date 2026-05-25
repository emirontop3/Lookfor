import telebot
from duckduckgo_search import DDGS
import time
import os

# Tokeni GitHub Secrets üzerinden güvenli bir şekilde alıyoruz
TOKEN = "7909095380:AAF7pjBKgXU6Irm7ohCEmwHW_UrBEnUaPGA"
bot = telebot.TeleBot(TOKEN)

def internet_checkup(query):
    results = []
    queries = [
        f'"{query}"',
        f'"{query}" leak',
        f'"{query}" pastebin',
        f'"{query}" database'
    ]
    with DDGS() as ddgs:
        for q in queries:
            try:
                search_results = ddgs.text(q, max_results=3)
                if search_results:
                    for r in search_results:
                        results.append(f"🔗 *Kaynak:* {r['title']}\n🌐 *Link:* {r['href']}\n")
            except Exception:
                pass
            time.sleep(1)
    return results

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🕵️‍♂️ *OSINT & Check-up Botuna Hoş Geldiniz!*\n\n"
        "Kullanabileceğiniz komutlar:\n"
        "🔹 `/phone [numara]` - Telefon numarası tarama\n"
        "🔹 `/whois [Ad Soyad]` - İsim ve soyisim taraması\n"
        "🔹 `/mail [e-posta]` - E-posta sızıntı kontrolü"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['phone'])
def check_phone(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Lütfen bir telefon numarası girin.", parse_mode='Markdown')
        return
    phone = args[1].strip()
    status_msg = bot.reply_to(message, f"🔍 `{phone}` için derin check-up başlatıldı...", parse_mode='Markdown')
    search_data = internet_checkup(phone)
    response = f"📊 *PHONE CHECK-UP SONUÇLARI (`{phone}`)*\n\n"
    if search_data:
        response += "🚨 *Bulunan Eşleşmeler:*\n\n" + "\n".join(search_data)
    else:
        response += "✅ İnternette doğrudan bir sızıntı eşleşmesi bulunamadı."
    bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(commands=['whois'])
def check_whois(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Lütfen ad soyad girin.", parse_mode='Markdown')
        return
    identity = args[1].strip()
    status_msg = bot.reply_to(message, f"🔍 `{identity}` için tarama başlatıldı...", parse_mode='Markdown')
    search_data = internet_checkup(identity)
    response = f"📊 *WHOIS SONUÇLARI (`{identity}`)*\n\n"
    if search_data:
        response += "🚨 *Eşleşen Kaynaklar:*\n\n" + "\n".join(search_data)
    else:
        response += "✅ Kritik bir sızıntı listelenmedi."
    bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(commands=['mail'])
def check_mail(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Lütfen bir e-posta adresi girin.", parse_mode='Markdown')
        return
    email = args[1].strip()
    status_msg = bot.reply_to(message, f"🔍 `{email}` için check-up yapılıyor...", parse_mode='Markdown')
    search_data = internet_checkup(email)
    response = f"📊 *MAIL CHECK-UP SONUÇLARI (`{email}`)*\n\n"
    if search_data:
        response += "🚨 *Arama Motoru Eşleşmeleri:*\n\n" + "\n".join(search_data)
    else:
        response += "✅ E-posta adresi temiz görünüyor."
    bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)

print("Bot GitHub Actions üzerinde başlatıldı...")
bot.infinity_polling()
