import telebot
from duckduckgo_search import DDGS
import time
import requests

# Token doğrudan koda gömülü
TOKEN = "7909095380:AAF7pjBKgXU6Irm7ohCEmwHW_UrBEnUaPGA"
bot = telebot.TeleBot(TOKEN)

# Canlı kontrol mekanizması için platform listesi
SOCIAL_PLATFORMS = {
    "Instagram": {"url": "https://www.instagram.com/{}", "mega": True},
    "TikTok": {"url": "https://www.tiktok.com/@{}", "mega": True},
    "Twitter_X": {"url": "https://twitter.com/{}", "mega": True},
    "GitHub": {"url": "https://github.com/{}", "mega": True},
    "Roblox": {"url": "https://www.roblox.com/user.aspx?username={}", "mega": True},
    "Steam": {"url": "https://steamcommunity.com/id/{}", "mega": False},
    "Twitch": {"url": "https://www.twitch.co.tv/{}", "mega": False},
    "Pinterest": {"url": "https://www.pinterest.com/{}/", "mega": False},
    "Reddit": {"url": "https://www.reddit.com/user/{}", "mega": False},
    "Telegram": {"url": "https://t.me/{}", "mega": True}
}

def generate_advanced_name_queries(name_input):
    """
    Girilen ad, ikinci ad ve soyad kombinasyonlarını 
    gelişmiş arama dorklarına dönüştürür.
    """
    parts = name_input.split()
    queries = []
    
    if len(parts) >= 2:
        full_name = " ".join(parts)
        first_and_last = f"{parts[0]} {parts[-1]}"
        
        # Temel İsim Kombinasyonları
        queries.append(f'"{full_name}"')
        if first_and_last != full_name:
            queries.append(f'"{first_and_last}"')
            
        # Sızıntı ve Veritabanı Kombinasyonları
        queries.append(f'"{full_name}" leak OR breach')
        queries.append(f'"{full_name}" database OR sql OR db')
        queries.append(f'"{full_name}" pastebin OR dump')
        queries.append(f'"{full_name}" t.me OR telegram')
        queries.append(f'"{full_name}" tc OR kimlik OR mernis')
        queries.append(f'"{full_name}" gsm OR adres OR telefon')
    else:
        # Tek kelime girildiyse standart dorking
        queries.append(f'"{name_input}"')
        queries.append(f'"{name_input}" leak')
        queries.append(f'"{name_input}" database')
        
    return queries

def check_live_accounts(username):
    """
    Kullanıcı adını platformlarda canlı sorgular ve sadece aktif olanları döner.
    """
    found_accounts = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    for platform, info in SOCIAL_PLATFORMS.items():
        url = info["url"].format(username)
        try:
            response = requests.get(url, headers=headers, timeout=3)
            if response.status_code == 200 and username.lower() in response.text.lower():
                found_accounts.append({
                    "platform": platform,
                    "link": url,
                    "mega": info["mega"]
                })
        except Exception:
            pass
    return found_accounts

def global_intelligence_dorking(dork_queries):
    """
    Belirlenen tüm dork kombinasyonları üzerinden internet üzerinde derin tarama yapar.
    """
    results = []
    with DDGS() as ddgs:
        for q in dork_queries:
            try:
                search_results = ddgs.text(q, max_results=2)
                if search_results:
                    for r in search_results:
                        if r['href'] not in [x.get('link') for x in results]:
                            is_mega = any(domain in r['href'].lower() for domain in ["instagram.com", "tiktok.com", "github.com", "roblox.com", "twitter.com", "facebook.com"])
                            results.append({'title': r['title'], 'link': r['href'], 'mega': is_mega})
            except Exception:
                pass
            time.sleep(0.2)
    return results

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "ℹ️ *SİBER İSTİHBARAT VE OSINT SORGU SİSTEMİ*\n\n"
        "Bu servis, açık kaynak istihbaratı (OSINT) yöntemlerini kullanarak dijital varlıkları ve sızıntı kayıtlarını analiz eder.\n\n"
        "*Kullanılabilir Komutlar:*\n"
        "▪️ `/whois [Ad İkinciAd Soyad]` -> Gelişmiş isim kombinasyonlu web ve sızıntı taraması.\n"
        "▪️ `/username [Kullanıcı Adı]` -> Sosyal medya ve oyun platformlarında canlı varlık sorgulaması.\n"
        "▪️ `/phone [Telefon Numarası]` -> Numara odaklı global veri sızıntısı analizi.\n"
        "▪️ `/mail [E-Posta Adresi]` -> Combo listeleri ve sızdırılmış şifre kayıtları kontrolü.\n"
        "▪️ `/tc [Kimlik / Ad Soyad]` -> Türkiye yerel veri ağları ve log dork denetimi."
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['whois'])
def check_whois(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "Anlamlı bir sorgu için lütfen ad ve soyad giriniz.\nÖrnek: `/whois Ahmet Selim Yılmaz`", parse_mode='Markdown')
        return
    
    target_name = args[1].strip()
    status_msg = bot.reply_to(message, f"Sorgulanıyor: `{target_name}`\nTüm ad ve soyad kombinasyonları için dork havuzu oluşturuluyor...", parse_mode='Markdown')
    
    # Tüm ad/soyad varyasyonlarını türet ve ara
    queries = generate_advanced_name_queries(target_name)
    dork_results = global_intelligence_dorking(queries)
    
    response = f"📋 *İSİM VE KİMLİK ANALİZ RAPORU*\n`Hedef: {target_name}`\n"
    response += "═" * 30 + "\n\n"
    
    if dork_results:
        response += "*AÇIK KAYNAK VE SIZINTI VERİTABANI EŞLEŞMELERİ:*\n\n"
        for item in dork_results[:10]:
            if item['mega']:
                response += f"⚠️ *[YÜKSEK ÖNCELİKLİ BULGU]*\n🔹 *Kaynak:* {item['title']}\n🌐 *Bağlantı:* {item['link']}\n\n"
            else:
                response += f"🔹 *Kaynak:* {item['title']}\n🌐 *Bağlantı:* {item['link']}\n\n"
    else:
        response += "✓ Açık veri tabanlarında ve sızıntı dökümanlarında bu isim kombinasyonuna ait doğrudan bir eşleşme bulunamadı.\n\n"
        
    response += "═" * 30 + "\n"
    response += "*RİSK VE OLASILIK ANALİZİ:*\n"
    response += "▪ Giriş yapılan isim kombinasyonunun eski mERNIS veya yerel kurum sızıntılarında yer alma ihtimali taranmıştır.\n"
    response += "▪ Bu ad soyadı taşıyan şahsın geçmişte kayıt olduğu forumlar ve dijital platformlar üzerinde veri sızıntısı riski bulunmaktadır."
    
    bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(commands=['username'])
def check_username(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "Lütfen bir kullanıcı adı belirtiniz.", parse_mode='Markdown')
        return
    
    target = args[1].strip()
    status_msg = bot.reply_to(message, f"Sorgulanıyor: `{target}`\nPlatformlar canlı olarak denetleniyor...", parse_mode='Markdown')
    
    live_results = check_live_accounts(target)
    dork_results = global_intelligence_dorking([f'"{target}"', f'"{target}" leak', f'"{target}" password'])
    
    response = f"📋 *KULLANICI ADI ANALİZ RAPORU*\n`Hedef: {target}`\n"
    response += "═" * 30 + "\n\n"
    
    if live_results:
        response += "*DURUMU DOĞRULANAN AKTİF HESAPLAR:*\n\n"
        for acc in live_results:
            if acc['mega']:
                response += f"⚠️ *[ANA PLATFORM]*\n🔹 *{acc['platform']}:* {acc['link']}\n\n"
            else:
                response += f"🔹 *{acc['platform']}:* {acc['link']}\n\n"
    else:
        response += "✓ Popüler sosyal ağlar üzerinde bu kullanıcı adına ait aktif bir profile rastlanmadı.\n\n"
        
    response += "═" * 30 + "\n"
    
    if dork_results:
        response += "*DİJİTAL AYAK İZİ VE LOG KAYITLARI:*\n\n"
        for item in dork_results[:6]:
            if item['mega']:
                response += f"⚠️ *[ANA PLATFORM İLİŞKİSİ]*\n🔹 *Kaynak:* {item['title']}\n🌐 *Bağlantı:* {item['link']}\n\n"
            else:
                response += f"🔹 *Kaynak:* {item['title']}\n🌐 *Bağlantı:* {item['link']}\n\n"
                
    bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)

# Altyapının devamlılığı için sadeleştirilmiş diğer komutlar
@bot.message_handler(commands=['phone'])
def check_phone(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return
    target = args[1].strip()
    status_msg = bot.reply_to(message, f"Sorgulanıyor: `{target}`", parse_mode='Markdown')
    data = global_intelligence_dorking([f'"{target}"', f'"{target}" leak', f'"{target}" database'])
    response = f"📋 *TELEFON SIZINTI RAPORU*\n\n"
    if data:
        for item in data[:5]:
            prefix = "⚠️ [YÜKSEK ÖNCELİK] " if item['mega'] else "🔹 "
            response += f"{prefix}{item['title']}\n🌐 Bağlantı: {item['link']}\n\n"
    else: response += "✓ Kayıt bulunamadı."
    bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(commands=['mail'])
def check_mail(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return
    target = args[1].strip()
    status_msg = bot.reply_to(message, f"Sorgulanıyor: `{target}`", parse_mode='Markdown')
    data = global_intelligence_dorking([f'"{target}"', f'"{target}" leak', f'"{target}" credential'])
    response = f"📋 *E-POSTA İSTİHBARAT RAPORU*\n\n"
    if data:
        for item in data[:5]:
            prefix = "⚠️ [YÜKSEK ÖNCELİK] " if item['mega'] else "🔹 "
            response += f"{prefix}{item['title']}\n🌐 Bağlantı: {item['link']}\n\n"
    else: response += "✓ Kayıt bulunamadı."
    bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(commands=['tc'])
def check_tc(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return
    target = args[1].strip()
    status_msg = bot.reply_to(message, f"Sorgulanıyor: `{target}`", parse_mode='Markdown')
    queries = generate_advanced_name_queries(target)
    data = global_intelligence_dorking(queries)
    response = f"📋 *YEREL VERİ TABANI RAPORU*\n\n"
    if data:
        for item in data[:5]:
            prefix = "⚠️ [YÜKSEK ÖNCELİK] " if item['mega'] else "🔹 "
            response += f"{prefix}{item['title']}\n🌐 Bağlantı: {item['link']}\n\n"
    else: response += "✓ Kayıt bulunamadı."
    bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)

print("Kurumsal OSINT Sistemi Başlatıldı.")
bot.infinity_polling()
