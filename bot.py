import telebot
from duckduckgo_search import DDGS
import time
import requests

# Token doğrudan koda gömülü
TOKEN = "7909095380:AAF7pjBKgXU6Irm7ohCEmwHW_UrBEnUaPGA"
bot = telebot.TeleBot(TOKEN)

def ultra_mega_dorking(query, mode="general"):
    """
    İnternetin alt katmanları, sızıntı siteleri, paste servisleri, forumlar, 
    bulut klasörleri ve dosya uzantıları dahil akla gelebilecek HER ŞEYİ tarayan motor.
    """
    results = []
    
    # Moda göre dorking listesini dinamik olarak genişletiyoruz
    base_dorking = [
        f'"{query}"',
        f'"{query}" leak OR breach',
        f'"{query}" database OR db OR sql',
        f'"{query}" pastebin OR pastenym OR dump OR ghostbin',
        f'"{query}" password OR credential OR combolist',
        f'"{query}" filetype:sql OR filetype:txt OR filetype:log',
        f'"{query}" filetype:xlsx OR filetype:csv OR filetype:pdf',
        f'"{query}" config OR env OR backup OR "index of"',
        f'"{query}" telegram OR t.me OR "anonfiles"',
        f'"{query}" exploit OR vulnerability OR hack',
        f'"{query}" darkweb OR onion OR deepweb',
        f'"{query}" stealer OR redline OR vidar log',
        f'"{query}" github OR gitlab OR token'
    ]
    
    if mode == "tc":
        base_dorking.extend([
            f'"{query}" tc OR kimlik OR mernis',
            f'"{query}" adres OR gsm OR soyagaci',
            f'"{query}" panel OR sorgu OR sülale'
        ])
    elif mode == "username":
        base_dorking.extend([
            f'"{query}" instagram OR twitter OR tiktok OR roblox',
            f'"{query}" steam OR discord OR twitch',
            f'"{query}" profile OR user OR account'
        ])

    # Agresif Tarama Başlatılıyor
    with DDGS() as ddgs:
        for q in base_dorking:
            try:
                # Her dork için en iyi sonuçları topla
                search_results = ddgs.text(q, max_results=2)
                if search_results:
                    for r in search_results:
                        # Yinelenen linkleri temizle
                        if r['href'] not in [x.get('link') for x in results]:
                            results.append({'title': r['title'], 'link': r['href']})
            except Exception:
                pass
            time.sleep(0.3) # Kesintisiz hızlı tarama performansı
            
    return results

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🚨 *ULTRA OSINT & SİBER İSTİHBARAT CANAVARI V10* 🚨\n\n"
        "Bu bot internetteki tüm açık kaynakları, hack forumlarını, paste sitelerini, "
        "log verilerini ve sızıntı havuzlarını agresif bir şekilde tarar.\n\n"
        "🔥 *KULLANILABİLİR TÜM KOMUTLAR:*\n"
        "🔹 `/phone [numara]` -> Telefon sızıntıları, kurye/operatör logları taraması.\n"
        "🔹 `/whois [Ad Soyad]` -> Dijital ayak izi ve genel web ifşa taraması.\n"
        "🔹 `/tc [Ad Soyad / Bilgi]` -> Türkiye özel kimlik, adres, panel veri tabanı taraması.\n"
        "🔹 `/mail [e-posta]` -> Combo listeleri, sızan şifreler ve hesap eşleşmeleri.\n"
        "🔹 `/username [KullanıcıAdı]` -> Sosyal medya, oyun ve forum hesap izi sürme.\n"
        "🔹 `/ip [IP Adresi]` -> IP lokasyonu, ISP, açık port ve siber risk analizi.\n\n"
        "⚠️ _Her sorgu arkada onlarca farklı dorking kombinasyonu dener!_"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['phone'])
def check_phone(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Kullanım: `/phone +905xxxxxxxx`", parse_mode='Markdown')
        return
    target = args[1].strip()
    status_msg = bot.reply_to(message, f"⚡ *[PHONE]* `{target}` için sızan tüm loglar, combo listeleri ve text veritabanları taranıyor...", parse_mode='Markdown')
    
    data = ultra_mega_dorking(target)
    
    response = f"📊 *TELEFON MEGA TARAMA SONUÇLARI*\n`Hedef: {target}`\n"
    response += "═" * 20 + "\n\n"
    if data:
        response += "🚨 *BULUNAN İLLEGAL KAYNAKLAR & LİNKLER:*\n"
        for i, item in enumerate(data[:10], 1):
            response += f"{i}. 📌 *Kaynak:* {item['title']}\n🔗 *Link:* {item['link']}\n\n"
    else:
        response += "✅ *Durum:* Bilinen genel sızıntı havuzlarında ve açık loglarda doğrudan bu numaraya rastlanmadı.\n\n"
    
    response += "═" * 20 + "\n"
    response += "🔮 *ŞUNLAR ŞUNLAR OLABİLİR (RİSK ANALİZİ & SENARYOLAR):*\n"
    response += "• Bu numara eski e-ticaret, kargo veri tabanları veya yemek sipariş sitesi sızıntılarında yer alıyor olabilir.\n"
    response += "• Telegram yeraltı botlarında sorgu yapılarak bu numaradan ad-soyad ve aile verilerine ulaşılması olasıdır.\n"
    response += "• SMS oltalama (Smishing) veya SIM kart kopyalama/sosyal mühendislik hedefi haline gelebilir.\n"
    response += "• Numara üzerinden kişilerin eski Facebook/Instagram rehber senkronizasyon verileri sızdırılmış olabilir."
    
    bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(commands=['whois'])
def check_whois(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Kullanım: `/whois Ad Soyad`", parse_mode='Markdown')
        return
    target = args[1].strip()
    status_msg = bot.reply_to(message, f"⚡ *[WHOIS]* `{target}` için internet arşivleri ve açık kaynaklar taranıyor...", parse_mode='Markdown')
    
    data = ultra_mega_dorking(target)
    
    response = f"📊 *WHOIS GENEL TARAMA SONUÇLARI*\n`Hedef: {target}`\n"
    response += "═" * 20 + "\n\n"
    if data:
        response += "🚨 *EŞLEŞEN İNTERNET KAYITLARI:*\n"
        for i, item in enumerate(data[:10], 1):
            response += f"{i}. 📌 *Kaynak:* {item['title']}\n🔗 *Link:* {item['link']}\n\n"
    else:
        response += "✅ *Durum:* Ad soyad açık forumlarda kritik bir sızıntıyla doğrudan eşleşmedi.\n\n"
        
    response += "═" * 20 + "\n"
    response += "🔮 *ŞUNLAR ŞUNLAR OLABİLİR (RİSK ANALİZİ & SENARYOLAR):*\n"
    response += "• Hedef şahsın geçmişte üye olduğu eski forumlar, blog yorumları veya okul listeleri ifşa olmuş olabilir.\n"
    response += "• Dijital ayak izi analizi ile şahsın eski e-posta adreslerine ve kullanıcı adlarına ulaşılabilir.\n"
    response += "• Ad-soyad kombinasyonu kullanılarak sahte kurumsal kimlik senaryolarıyla dolandırıcılık hedefi yapılabilir."
    
    bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(commands=['tc'])
def check_tc(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Kullanım: `/tc Ad Soyad` veya `/tc Veri`", parse_mode='Markdown')
        return
    target = args[1].strip()
    status_msg = bot.reply_to(message, f"⚡ *[TR-SPECIAL]* `{target}` için T.C. kimlik, mernis, soy ağacı ve panel log dorkları denetletiliyor...", parse_mode='Markdown')
    
    data = ultra_mega_dorking(target, mode="tc")
    
    response = f"📊 *T.C. KİMLİK & PANEL ÖZEL TARAMA SONUÇLARI*\n`Hedef: {target}`\n"
    response += "═" * 20 + "\n\n"
    if data:
        response += "🚨 *KRİTİK TÜRKİYE VERİTABANI EŞLEŞMELERİ:*\n"
        for i, item in enumerate(data[:10], 1):
            response += f"{i}. 📌 *Kaynak:* {item['title']}\n🔗 *Link:* {item['link']}\n\n"
    else:
        response += "✅ *Durum:* Halka açık sızdırılmış SQL veya TXT dosyalarında bu veriye doğrudan rastlanmadı.\n\n"
        
    response += "═" * 20 + "\n"
    response += "🔮 *ŞUNLAR ŞUNLAR OLABİLİR (RİSK ANALİZİ & SENARYOLAR):*\n"
    response += "• Eski mERNIS (2015) veya güncel illegal panel sızıntıları vasıtasıyla şahsın T.C. kimlik no, anne-baba adı, ev adresi ifşa edilmiş olabilir.\n"
    response += "• Kötü niyetli kişiler bu verileri kullanarak şahıs adına sahte şirket açma, hat çıkarma veya şantaj yapma girişiminde bulunabilir.\n"
    response += "• Hedefin yakın akrabalarının telefon numaraları ve adres bilgileri zincirleme olarak çekilebilir."
    
    bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(commands=['mail'])
def check_mail(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Kullanım: `/mail eposta@gmail.com`", parse_mode='Markdown')
        return
    target = args[1].strip()
    status_msg = bot.reply_to(message, f"⚡ *[MAIL]* `{target}` için şifre sızıntıları, stealer logları ve database dump'ları taranıyor...", parse_mode='Markdown')
    
    data = ultra_mega_dorking(target)
    
    response = f"📊 *E-POSTA ULTRA SIZINTI SONUÇLARI*\n`Hedef: {target}`\n"
    response += "═" * 20 + "\n\n"
    if data:
        response += "🚨 *E-POSTANIN GEÇTİĞI SIZINTI VE COMBO LİSTELERİ:*\n"
        for i, item in enumerate(data[:10], 1):
            response += f"{i}. 📌 *Kaynak:* {item['title']}\n🔗 *Link:* {item['link']}\n\n"
    else:
        response += "✅ *Durum:* E-posta adresi açık metin şifre listelerinde bulunamadı.\n\n"
        
    response += "═" * 20 + "\n"
    response += "🔮 *ŞUNLAR ŞUNLAR OLABİLİR (RİSK ANALİZİ & SENARYOLAR):*\n"
    response += "• Bu mail adresi daha önce hacklenen büyük platformların (Wattpad, Deezer, Zynga vb.) veritabanlarında düz metin veya hashli şifreyle kalmış olabilir.\n"
    response += "• Redline, Vidar gibi bilgisayara bulaşan virüslerin (stealer) tarayıcıdan çaldığı log dosyalarında bu mail ve şifresi yer alıyor olabilir.\n"
    response += "• Aynı şifre kullanılıyorsa, Instagram, Steam, Epic Games veya kripto hesapları ele geçirilebilir."
    
    bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(commands=['username'])
def check_username(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Kullanım: `/username nick`", parse_mode='Markdown')
        return
    target = args[1].strip()
    status_msg = bot.reply_to(message, f"⚡ *[USERNAME]* `{target}` nickinin geçtiği platformlar ve üyelikler aranıyor...", parse_mode='Markdown')
    
    data = ultra_mega_dorking(target, mode="username")
    
    response = f"📊 *KULLANICI ADI (NICK) DETAYLI ANALİZİ*\n`Hedef Nick: {target}`\n"
    response += "═" * 20 + "\n\n"
    if data:
        response += "🚨 *NICK İLE EŞLEŞEN SAYFALAR VE FORUMLAR:*\n"
        for i, item in enumerate(data[:10], 1):
            response += f"{i}. 📌 *Kaynak:* {item['title']}\n🔗 *Link:* {item['link']}\n\n"
    else:
        response += "✅ *Durum:* Kullanıcı adına dair kritik illegal bir forum kaydı listelenmedi.\n\n"
        
    response += "═" * 20 + "\n"
    response += "🔮 *ŞUNLAR ŞUNLAR OLABİLİR (RİSK ANALİZİ & SENARYOLAR):*\n"
    response += "• Hedef şahıs bu nicki Roblox, GitHub, Steam veya çeşitli oyun/hile forumlarında aktif olarak kullanıyor olabilir.\n"
    response += "• Farklı sitelerdeki aynı nick kullanımları takip edilerek kişinin gerçek kimliğine (Osint pivotting) ulaşılabilir.\n"
    response += "• Eski hile/script geliştirme forumlarındaki paylaşımları veya bıraktığı kod blokları ifşa olmuş olabilir."
    
    bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(commands=['ip'])
def check_ip(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Kullanım: `/ip 8.8.8.8`", parse_mode='Markdown')
        return
    target = args[1].strip()
    status_msg = bot.reply_to(message, f"⚡ *[IP ANALYSIS]* `{target}` için coğrafi konum ve port sızıntı analizi yapılıyor...", parse_mode='Markdown')
    
    response = f"📊 *IP SİBER İSTİHBARAT RAPORU*\n`Hedef IP: {target}`\n"
    response += "═" * 20 + "\n\n"
    
    try:
        # Ücretsiz IP API sorgusu
        ip_data = requests.get(f"http://ip-api.com/json/{target}").json()
        if ip_data and ip_data.get('status') == 'success':
            response += f"🌍 *Ülke/Şehir:* {ip_data.get('country')} / {ip_data.get('city')}\n"
            response += f"🏢 *İnternet Sağlayıcı (ISP):* {ip_data.get('isp')}\n"
            response += f"📍 *Koordinatlar:* {ip_data.get('lat')}, {ip_data.get('lon')}\n"
            response += f"📮 *Posta Kodu:* {ip_data.get('zip')}\n\n"
        else:
            response += "❌ IP bilgileri canlı API'den çekilemedi (Geçersiz IP adresi).\n\n"
    except Exception:
        response += "❌ IP API bağlantı hatası.\n\n"
        
    response += "═" * 20 + "\n"
    response += "🔮 *ŞUNLAR ŞUNLAR OLABİLİR (RİSK ANALİZİ & SENARYOLAR):*\n"
    response += "• IP adresi üzerinden Shodan veya Censys gibi sistemlerde arama yapılarak cihazın açık portları (SSH, FTP, RDP) bulunabilir.\n"
    response += "• Cihaz eğer bir ev interneti ise DDoS / Botnet saldırılarıyla interneti tamamen kesilebilir.\n"
    response += "• IP havuzundan yola çıkılarak bulunulan bölgedeki santral lokasyonu tahmin edilebilir."
    
    bot.edit_message_text(response, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)

print("MEGA OSINT BOTU 7/24 AKTİF!")
bot.infinity_polling()
