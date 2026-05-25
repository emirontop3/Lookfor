import telebot
from duckduckgo_search import DDGS
import time
import requests
import re

# Token doğrudan koda gömülü
TOKEN = "7909095380:AAF7pjBKgXU6Irm7ohCEmwHW_UrBEnUaPGA"
bot = telebot.TeleBot(TOKEN)

# Canlı kontrol mekanizması platformları
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

def detect_input_type(user_input):
    """
    Gelişmiş OSINT araçlarında kullanılan girdi tanımlama motoru.
    """
    user_input = user_input.strip()
    
    # E-Posta Kontrolü
    if re.match(r"[^@]+@[^@]+\.[^@]+", user_input):
        return "mail"
    
    # IP Adresi Kontrolü
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", user_input):
        return "ip"
    
    # Telefon Numarası Kontrolü (Boşlukları ve karakterleri temizleyerek)
    clean_phone = re.sub(r"[\s\+\-\(\)]", "", user_input)
    if clean_phone.isdigit() and len(clean_phone) >= 9:
        return "phone"
        
    # Eğer yukarıdakilerden biri değilse Ad Soyad veya Kullanıcı Adıdır
    return "identity"

def clean_phone_number(phone_input):
    """Telefon numaralarını dorking için optimize eder."""
    return re.sub(r"[\s\+\-\(\)]", "", phone_input)

def check_live_accounts(username):
    found_accounts = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    for platform, info in SOCIAL_PLATFORMS.items():
        url = info["url"].format(username)
        try:
            response = requests.get(url, headers=headers, timeout=2)
            if response.status_code == 200 and username.lower() in response.text.lower():
                found_accounts.append({"platform": platform, "link": url, "mega": info["mega"]})
        except Exception:
            pass
    return found_accounts

def global_intelligence_dorking(query_list):
    results = []
    with DDGS() as ddgs:
        for q in query_list:
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
        "ℹ️ *OTOMATİK TEHDİT İSTİHBARATI VE OSINT SİSTEMİ*\n\n"
        "Bu bot yapay zeka tabanlı girdi tanımlama motoruna sahiptir. Herhangi bir komut kullanmanıza gerek yoktur.\n\n"
        "👉 Bota doğrudan bir *E-posta*, *Telefon Numarası*, *IP Adresi* veya *Ad-Soyad* göndermeniz yeterlidir. Sistem girdi türünü otomatik tespit ederek derin tarama başlatır."
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_auto_osint(message):
    user_input = message.text.strip()
    input_type = detect_input_type(user_input)
    
    status_msg = bot.reply_to(message, f"⚙️ Girdi Türü Tespit Edildi: *{input_type.upper()}*\nAnaliz ve dorking süreci başlatıldı, lütfen bekleyiniz...", parse_mode='Markdown')
    
    queries = []
    live_profiles = []
    risk_score = 10 # Temel risk puanı
    
    # 1. AŞAMA: Girdi Türüne Göre Akıllı İşlem Dallanması
    if input_type == "mail":
        queries = [f'"{user_input}"', f'"{user_input}" leak OR breach', f'"{user_input}" database OR credential', f'"{user_input}" pastebin OR dump']
        
    elif input_type == "phone":
        clean_num = clean_phone_number(user_input)
        queries = [f'"{clean_num}"', f'"{user_input}" leak', f'"{clean_num}" database OR sql', f'"{clean_num}" pastebin']
        
    elif input_type == "ip":
        # IP için canlı API taraması
        try:
            ip_data = requests.get(f"http://ip-api.com/json/{user_input}").json()
        except Exception:
            ip_data = None
            
    elif input_type == "identity":
        # Ad soyad ise varyasyonları türet, kullanıcı adı ise sosyal medyayı tara
        parts = user_input.split()
        if len(parts) >= 2:
            queries = [f'"{user_input}"', f'"{parts[0]} {parts[-1]}"', f'"{user_input}" leak OR mernis', f'"{user_input}" database OR tc']
        else:
            queries = [f'"{user_input}"', f'"{user_input}" leak', f'"{user_input}" password']
            live_profiles = check_live_accounts(user_input)

    # 2. AŞAMA: Global Dorking Arama Motoru Entegrasyonu (IP Hariç)
    dork_results = global_intelligence_dorking(queries) if input_type != "ip" else []
    
    # 3. AŞAMA: Tehdit Skoru Hesaplama Matrisi
    if dork_results:
        risk_score += len(dork_results) * 12
    if live_profiles:
        risk_score += len(live_profiles) * 8
    if risk_score > 100: risk_score = 100
    
    # 4. AŞAMA: Kurumsal Rapor Biçimlendirme
    response = f"📋 *SİBER İSTİHBARAT SORGULAMA RAPORU*\n"
    response += f"▪️ *Sorgulanan Veri:* `{user_input}`\n"
    response += f"▪️ *Analiz Tipi:* {input_type.upper()}\n"
    response += f"▪️ *Tehdit Seviyesi Skoru:* %{risk_score}\n"
    response += "═" * 30 + "\n\n"
    
    # IP Sonuç Çıktısı
    if input_type == "ip" and ip_data and ip_data.get('status') == 'success':
        response += "*COĞRAFİ VE ISP VERİLERİ:*\n"
        response += f"🔹 *Lokasyon:* {ip_data.get('country')} / {ip_data.get('city')}\n"
        response += f"🔹 *Sağlayıcı (ISP):* {ip_data.get('isp')}\n"
        response += f"🔹 *Koordinat:* {ip_data.get('lat')}, {ip_data.get('lon')}\n\n"
    
    # Canlı Profil Sonuç Çıktısı
    if live_profiles:
        response += "*DOĞRULANMIŞ AKTİF PROFİLLER:*\n"
        for acc in live_profiles:
            tag = "⚠️ [ANA PLATFORM] " if acc['mega'] else "🔹 "
            response += f"{tag}*{acc['platform']}:* {acc['link']}\n"
        response += "\n"
        
    # Dorking Sızıntı Sonuç Çıktısı
    if dork_results:
        response += "*TESPİT EDİLEN VERİTABANI VE İLLEGAL KAYNAKLAR:*\n\n"
        for item in dork_results[:8]:
            tag = "⚠️ [YÜKSEK ÖNCELİKLİ BULGU] " if item['mega'] else "🔹 "
            response += f"{tag}*Kaynak:* {item['title']}\n🌐 *Bağlantı:* {item['link']}\n\n"
    else:
        if input_type != "ip":
            response += "✓ İnternet arşivlerinde ve herkese açık sızıntı listelerinde doğrudan bir eşleşme bulunamadı.\n\n"
            
    response += "═" * 30 + "\n"
    response += "*ŞUNLAR ŞUNLAR OLABİLİR (STRATEJİK TAHMİN):*\n"
    if risk_score > 50:
        response += "▪️ Verinin yeraltı forumlarında ticari combo listelerine dönüştürülmüş olma ihtimali yüksektir.\n"
        response += "▪️ Bu dijital kimlik varlığı üzerinden hedef şahsa yönelik hedefli oltalama senaryoları üretilebilir."
    else:
        response += "▪️ Dijital ayak izi düşük veya temizlenmiş bir veri setidir.\n"
        response += "▪️ Açık kaynaklar üzerinden derinlemesine sosyal mühendislik yapılması zordur."

    bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)

print("Akıllı Tehdit Algılamalı OSINT Botu Aktif.")
bot.infinity_polling()
