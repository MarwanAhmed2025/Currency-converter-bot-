import os
import telebot
from telebot import types
import requests
import re  # مكتبة جديدة لاستخراج الأرقام من النصوص العربية

# ==========================================
# 0. الإعدادات والتوكن والمدير
# ==========================================
TOKEN = os.getenv("BOT_TOKEN", "8963858897:AAE8SRUCJhTvlTj5_Lxz6RHncIMM5IxbDIQ")
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = "320878111"

local_rates = {
    "sanaa_usd": 530.0,
    "sanaa_sar": 140.0,
    "aden_usd": 1900.0,
    "aden_sar": 500.0
}

# ==========================================
# 1. القاموس الذكي (يشمل أسماء الدول والكلمات العامية)
# ==========================================
currencies_ar = {
    "الدولار": "USD", "دولار": "USD", "الأمريكي": "USD", "الامريكي": "USD", "امريكي": "USD", "امريكا": "USD", "أمريكا": "USD",
    "اليورو": "EUR", "يورو": "EUR", "اوروبا": "EUR", "أوروبا": "EUR",
    "الجنيه الاسترليني": "GBP", "استرليني": "GBP", "البريطاني": "GBP", "بريطاني": "GBP", "بريطانيا": "GBP",
    "الين الياباني": "JPY", "الين": "JPY", "الياباني": "JPY", "ياباني": "JPY", "اليابان": "JPY",
    "اليوان الصيني": "CNY", "يوان": "CNY", "الصيني": "CNY", "صيني": "CNY", "الصين": "CNY",
    "الروبل الروسي": "RUB", "روبل": "RUB", "الروسي": "RUB", "روسي": "RUB", "روسيا": "RUB",
    "الريال السعودي": "SAR", "ريال سعودي": "SAR", "السعودي": "SAR", "سعودي": "SAR", "السعودية": "SAR", "سعودية": "SAR",
    "الدرهم الاماراتي": "AED", "درهم اماراتي": "AED", "الاماراتي": "AED", "اماراتي": "AED", "الامارات": "AED", "الإمارات": "AED",
    "الدينار الكويتي": "KWD", "دينار كويتي": "KWD", "الكويتي": "KWD", "كويتي": "KWD", "الكويت": "KWD",
    "الريال القطري": "QAR", "ريال قطري": "QAR", "القطري": "QAR", "قطري": "QAR", "قطر": "QAR",
    "الريال العماني": "OMR", "ريال عماني": "OMR", "العماني": "OMR", "عماني": "OMR", "عمان": "OMR", "عُمان": "OMR",
    "الدينار البحريني": "BHD", "دينار بحريني": "BHD", "البحريني": "BHD", "بحريني": "BHD", "البحرين": "BHD",
    "الريال اليمني": "YER", "ريال يمني": "YER", "اليمني": "YER", "يمني": "YER", "اليمن": "YER", "يمن": "YER",
    "الجنيه المصري": "EGP", "جنيه مصري": "EGP", "المصري": "EGP", "مصري": "EGP", "مصر": "EGP",
    "الدينار الاردني": "JOD", "دينار اردني": "JOD", "الاردني": "JOD", "اردني": "JOD", "الاردن": "JOD", "الأردن": "JOD",
    "الشيكل": "ILS", "شيكل": "ILS", "الشيكل الفلسطيني": "ILS", "شيكل فلسطيني": "ILS", "فلسطين": "ILS", "الفلسطيني": "ILS", "فلسطيني": "ILS",
    "الليرة اللبنانية": "LBP", "ليرة لبنانية": "LBP", "اللبناني": "LBP", "لبناني": "LBP", "لبنان": "LBP",
    "الليرة السورية": "SYP", "ليرة سورية": "SYP", "السوري": "SYP", "سوري": "SYP", "سوريا": "SYP",
    "الدينار العراقي": "IQD", "دينار عراقي": "IQD", "العراقي": "IQD", "عراقي": "IQD", "العراق": "IQD",
    "الدرهم المغربي": "MAD", "درهم مغربي": "MAD", "المغربي": "MAD", "مغربي": "MAD", "المغرب": "MAD",
    "الدينار الجزائري": "DZD", "دينار جزائري": "DZD", "الجزائري": "DZD", "جزائري": "DZD", "الجزائر": "DZD",
    "الدينار التونسي": "TND", "دينار تونسي": "TND", "التونسي": "TND", "تونسي": "TND", "تونس": "TND",
    "الدينار الليبي": "LYD", "دينار ليبي": "LYD", "الليبي": "LYD", "ليبي": "LYD", "ليبيا": "LYD",
    "الجنيه السوداني": "SDG", "جنيه سوداني": "SDG", "السوداني": "SDG", "سوداني": "SDG", "السودان": "SDG",
    "السوم الاوزبكي": "UZS", "سوم اوزبكي": "UZS", "اوزبكي": "UZS", "اوزبكستان": "UZS",
    "التنج الكازاخستاني": "KZT", "تنج كازاخستاني": "KZT", "كازاخستان": "KZT",
    "السوموني الطاجيكي": "TJS", "طاجيكي": "TJS", "طاجيكستان": "TJS",
    "الروبيه الهنديه": "INR", "روبيه هندية": "INR", "روبيه": "INR", "الهندي": "INR", "هندي": "INR", "الهند": "INR",
    "التاكا البنجلاديشي": "BDT", "تاكا بنجلاديشي": "BDT", "تاكا": "BDT", "بنجلاديش": "BDT",
    "الليرة التركية": "TRY", "ليرة تركية": "TRY", "التركي": "TRY", "تركي": "TRY", "تركيا": "TRY",
    "البيزو المكسيكي": "MXN", "بيزو مكسيكي": "MXN", "المكسيك": "MXN",
    "الريال البرازيلي": "BRL", "ريال برازيلي": "BRL", "البرازيل": "BRL"
}

# ==========================================
# 2. قاعدة بيانات البحث (مخفية للاختصار لكنها موجودة كما هي)
# ==========================================
currency_search_db = [
    "🇺🇸 الولايات المتحدة (USA) | الدولار الأمريكي (Dollar) | الرمز: USD",
    "🇪🇺 أوروبا (Europe) | اليورو (Euro) | الرمز: EUR",
    "🇬🇧 بريطانيا (UK) | الجنيه الإسترليني (Pound) | الرمز: GBP",
    "🇨🇭 سويسرا (Switzerland) | الفرنك السويسري (Franc) | الرمز: CHF",
    "🇯🇵 اليابان (Japan) | الين الياباني (Yen) | الرمز: JPY",
    "🇨🇳 الصين (China) | اليوان الصيني (Yuan) | الرمز: CNY",
    "🇷🇺 روسيا (Russia) | الروبل الروسي (Ruble) | الرمز: RUB",
    "🇸🇦 السعودية (Saudi Arabia) | الريال السعودي (Riyal) | الرمز: SAR",
    "🇦🇪 الإمارات (UAE) | الدرهم الإماراتي (Dirham) | الرمز: AED",
    "🇰🇼 الكويت (Kuwait) | الدينار الكويتي (Dinar) | الرمز: KWD",
    "🇶🇦 قطر (Qatar) | الريال القطري (Riyal) | الرمز: QAR",
    "🇴🇲 عُمان (Oman) | الريال العماني (Riyal) | الرمز: OMR",
    "🇧🇭 البحرين (Bahrain) | الدينار البحريني (Dinar) | الرمز: BHD",
    "🇾🇪 اليمن (Yemen) | الريال اليمني (Riyal) | الرمز: YER",
    "🇪🇬 مصر (Egypt) | الجنيه المصري (Pound) | الرمز: EGP",
    "🇯🇴 الأردن (Jordan) | الدينار الأردني (Dinar) | الرمز: JOD",
    "🇵🇸 فلسطين (Palestine) | الشيكل (Shekel) | الرمز: ILS",
    "🇮🇶 العراق (Iraq) | الدينار العراقي (Dinar) | الرمز: IQD",
    "🇸🇾 سوريا (Syria) | الليرة السورية (Pound) | الرمز: SYP",
    "🇱🇧 لبنان (Lebanon) | الليرة اللبنانية (Pound) | الرمز: LBP",
    "🇲🇦 المغرب (Morocco) | الدرهم المغربي (Dirham) | الرمز: MAD",
    "🇩🇿 الجزائر (Algeria) | الدينار الجزائري (Dinar) | الرمز: DZD",
    "🇹🇳 تونس (Tunisia) | الدينار التونسي (Dinar) | الرمز: TND",
    "🇱🇾 ليبيا (Libya) | الدينار الليبي (Dinar) | الرمز: LYD",
    "🇸🇩 السودان (Sudan) | الجنيه السوداني (Pound) | الرمز: SDG",
    "🇺🇿 أوزبكستان (Uzbekistan) | السوم الأوزبكي (Som) | الرمز: UZS",
    "🇰🇿 كازاخستان (Kazakhstan) | التنج الكازاخستاني (Tenge) | الرمز: KZT",
    "🇹🇲 تركمانستان (Turkmenistan) | المانات (Manat) | الرمز: TMT",
    "🇹🇯 طاجيكستان (Tajikistan) | السوموني (Somoni) | الرمز: TJS",
    "🇰🇬 قيرغيزستان (Kyrgyzstan) | السوم القيرغيزي (Som) | الرمز: KGS",
    "🇮🇳 الهند (India) | الروبية الهندية (Rupee) | الرمز: INR",
    "🇧🇩 بنغلاديش (Bangladesh) | التاكا (Taka) | الرمز: BDT",
    "🇵🇰 باكستان (Pakistan) | الروبية (Rupee) | الرمز: PKR",
    "🇹🇷 تركيا (Turkey) | الليرة التركية (Lira) | الرمز: TRY",
    "🇮🇷 إيران (Iran) | الريال الإيراني (Rial) | الرمز: IRR",
    "🇦🇫 أفغانستان (Afghanistan) | الأفغاني (Afghani) | الرمز: AFN",
    "🇲🇾 ماليزيا (Malaysia) | الرينجت (Ringgit) | الرمز: MYR",
    "🇮🇩 إندونيسيا (Indonesia) | الروبية (Rupiah) | الرمز: IDR",
    "🇿🇦 جنوب أفريقيا (South Africa) | الراند (Rand) | الرمز: ZAR",
    "🇨🇦 كندا (Canada) | الدولار الكندي (Dollar) | الرمز: CAD",
    "🇦🇺 أستراليا (Australia) | الدولار الأسترالي (Dollar) | الرمز: AUD"
]

# ==========================================
# 3. دوال جلب الأسعار والمحلل اللغوي الذكي (جديد)
# ==========================================
def get_exchange_rate(base_currency, target_currency):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url, timeout=5)
        data = response.json()
        if target_currency in data['rates']:
            return data['rates'][target_currency]
        return None
    except:
        return None

def get_crypto_price(symbol):
    urls = [
        f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}",
        f"https://api.binance.us/api/v3/ticker/price?symbol={symbol}",
        f"https://api1.binance.com/api/v3/ticker/price?symbol={symbol}"
    ]
    for url in urls:
        try:
            response = requests.get(url, timeout=7)
            if response.status_code == 200:
                return float(response.json()['price'])
        except:
            continue
    return None

def extract_info_from_arabic(text):
    """
    محلل لغوي يستخرج: الرقم (المبلغ) + العملة الأساسية + العملة المحول إليها 
    بناءً على الترتيب الفعلي للكلمات في الجملة.
    """
    amount = 1.0
    # 1. استخراج الأرقام من الجملة (مثل 500 أو 15.5)
    numbers = re.findall(r'\d+(?:\.\d+)?', text)
    if numbers:
        amount = float(numbers[0])

    # 2. البحث عن العملات وتحديد موقعها في الجملة
    found_items = []
    sorted_keys = sorted(currencies_ar.keys(), key=len, reverse=True)
    temp_text = text
    
    for key in sorted_keys:
        if key in temp_text:
            index = temp_text.find(key)
            found_items.append((index, currencies_ar[key]))
            temp_text = temp_text.replace(key, " " * len(key))
            
    # 3. ترتيب العملات بناءً على موقع ظهورها في الكلام (من اليمين لليسار)
    found_items.sort(key=lambda x: x[0])
    found_currencies = [item[1] for item in found_items]
    
    # 4. إزالة التكرار (في حال قال: ريال سعودي السعودية)
    unique_currencies = []
    for curr in found_currencies:
        if not unique_currencies or unique_currencies[-1] != curr:
            unique_currencies.append(curr)
            
    base_curr, target_curr = None, None
    if len(unique_currencies) >= 2:
        base_curr = unique_currencies[0]
        target_curr = unique_currencies[1]
    elif len(unique_currencies) == 1:
        if unique_currencies[0] != "YER":
            base_curr = unique_currencies[0]
            target_curr = "YER"
            
    return amount, base_curr, target_curr

def handle_local_yemen_conversion(amount, base, target):
    """حساب التحويل بناءً على السوق المحلي اليمني فقط"""
    if target == "YER":
        if base == "USD":
            return amount * local_rates['sanaa_usd'], amount * local_rates['aden_usd']
        elif base == "SAR":
            return amount * local_rates['sanaa_sar'], amount * local_rates['aden_sar']
        else:
            rate_to_usd = get_exchange_rate(base, "USD")
            if rate_to_usd:
                usd_amt = amount * rate_to_usd
                return usd_amt * local_rates['sanaa_usd'], usd_amt * local_rates['aden_usd']
            return None, None
            
    elif base == "YER":
        if target == "USD":
            return amount / local_rates['sanaa_usd'], amount / local_rates['aden_usd']
        elif target == "SAR":
            return amount / local_rates['sanaa_sar'], amount / local_rates['aden_sar']
        else:
            rate_usd_to_target = get_exchange_rate("USD", target)
            if rate_usd_to_target:
                usd_sanaa = amount / local_rates['sanaa_usd']
                usd_aden = amount / local_rates['aden_usd']
                return usd_sanaa * rate_usd_to_target, usd_aden * rate_usd_to_target
            return None, None
            
    return None, None

# ==========================================
# 4. أوامر البوت والترحيب وتحديث الأسعار
# ==========================================
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "مرحباً بك في بوت الصرف والعملات! 💱\n\n"
        "🔹 **التحويل الذكي المباشر:**\n"
        "• اكتب ببساطة: `500 دولار كم سعودي`\n"
        "• أو: `كم سعر اليورو مقابل الكويتي`\n"
        "• أو اسم الدولة فقط: `بريطانيا`\n\n"
        "🔹 **القوائم والأسواق:**\n"
        "اضغط على /currencies لعرض أسعار السوق المحلي، الكريبتو، والقوائم."
    )
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['update'])
def admin_update_rates(message):
    if str(message.chat.id) != str(ADMIN_ID):
        bot.reply_to(message, "❌ هذا الأمر مخصص لإدارة البوت فقط.")
        return

    try:
        parts = message.text.split()
        if len(parts) != 3:
            bot.reply_to(message, "⚠️ الصيغة:\n`/update المفتاح السعر`\n\nأمثلة:\n`/update sanaa_usd 535`\n`/update aden_sar 505`", parse_mode="Markdown")
            return
            
        key = parts[1].lower()
        new_price = float(parts[2])

        if key in local_rates:
            local_rates[key] = new_price
            bot.reply_to(message, f"✅ تم تحديث السعر بنجاح:\n`{key}` = {new_price} ريال يمني", parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ المفتاح غير صحيح. الخيارات:\n- `sanaa_usd`\n- `sanaa_sar`\n- `aden_usd`\n- `aden_sar`", parse_mode="Markdown")
    except ValueError:
        bot.reply_to(message, "❌ الرجاء كتابة السعر كأرقام فقط.")

# ==========================================
# 5. القوائم والأزرار التفاعلية
# ==========================================
@bot.message_handler(commands=['currencies'])
def show_currencies_menu(message):
    send_main_menu(message.chat.id)

def send_main_menu(chat_id, message_id=None):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn_yemen = types.InlineKeyboardButton("🇾🇪 أسعار السوق المحلي (اليمن)", callback_data="local_yemen")
    btn_crypto = types.InlineKeyboardButton("💎 أسعار الكريبتو (Binance)", callback_data="crypto_prices")
    
    btn1 = types.InlineKeyboardButton("🌍 أهم العملات", callback_data="cat_world")
    btn2 = types.InlineKeyboardButton("🦅 الدول العربية", callback_data="cat_arab")
    btn3 = types.InlineKeyboardButton("🌏 آسيا", callback_data="cat_asia")
    btn4 = types.InlineKeyboardButton("💶 أوروبا", callback_data="cat_europe")
    btn5 = types.InlineKeyboardButton("🌍 أفريقيا", callback_data="cat_africa")
    btn6 = types.InlineKeyboardButton("🌎 الأمريكيتين", callback_data="cat_americas")
    
    search_btn = types.InlineKeyboardButton("🔍 بحث عن دولة أو عملة", callback_data="search_currency")
    
    markup.add(btn_yemen)
    markup.add(btn_crypto)
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    markup.add(search_btn)

    text = "📊 **دليل الصرف والعملات الشامل:**\n\nاختر من الأقسام التالية للاستعلام المباشر أو البحث:"
    
    if message_id:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "search_currency":
        msg = bot.send_message(call.message.chat.id, "🔍 **البحث نشط الآن:**\n\nاكتب اسم الدولة، العملة، أو الرمز (مثلاً: اليمن، يورو، USD):", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_search)
        return

    markup = types.InlineKeyboardMarkup()
    back_btn = types.InlineKeyboardButton("⬅️ رجوع", callback_data="main_menu")
    markup.add(back_btn)
    
    if call.data == "local_yemen":
        text = (
            "🇾🇪 **أسعار الصرف في السوق المحلي اليمني:**\n\n"
            "📍 **صنعاء / ذمار:**\n"
            f"🇺🇸 الدولار: `{local_rates['sanaa_usd']}` ريال\n"
            f"🇸🇦 السعودي: `{local_rates['sanaa_sar']}` ريال\n\n"
            "📍 **عدن والمحافظات المجاورة:**\n"
            f"🇺🇸 الدولار: `{local_rates['aden_usd']}` ريال\n"
            f"🇸🇦 السعودي: `{local_rates['aden_sar']}` ريال\n\n"
            "💡 _يتم تحديث الأسعار يدوياً بحسب حركة السوق الفعلي._"
        )
    elif call.data == "crypto_prices":
        bnb = get_crypto_price("BNBUSDT")
        btc = get_crypto_price("BTCUSDT")
        
        bnb_str = f"{bnb:,.2f} $" if bnb else "غير متوفر"
        btc_str = f"{btc:,.2f} $" if btc else "غير متوفر"
        
        text = (
            "💎 **أسعار العملات الرقمية لحظياً (Binance):**\n\n"
            f"🟡 **BNB:** `{bnb_str}`\n"
            f"🟠 **BTC:** `{btc_str}`\n\n"
            "🔄 **سعر صرف الـ USDT التقريبي محلياً (P2P):**\n"
            f"• صنعاء / ذمار: ~`{local_rates['sanaa_usd']}` ريال\n"
            f"• عدن: ~`{local_rates['aden_usd']}` ريال"
        )
    elif call.data == "cat_world":
        text = "🌍 **أهم العملات العالمية:**\n🇺🇸 أمريكا: USD\n🇪🇺 أوروبا: EUR\n🇬🇧 بريطانيا: GBP\n🇨🇭 سويسرا: CHF\n🇯🇵 اليابان: JPY\n🇨🇳 الصين: CNY\n🇷🇺 روسيا: RUB"
    elif call.data == "cat_arab":
        text = "🦅 **الدول العربية:**\n🇸🇦 السعودية: SAR\n🇦🇪 الإمارات: AED\n🇰🇼 الكويت: KWD\n🇶🇦 قطر: QAR\n🇴🇲 عُمان: OMR\n🇾🇪 اليمن: YER\n🇵🇸 فلسطين: ILS\n🇪🇬 مصر: EGP\n🇯🇴 الأردن: JOD\n🇮🇶 العراق: IQD\n🇸🇾 سوريا: SYP\n🇱🇧 لبنان: LBP\n🇲🇦 المغرب: MAD\n🇩🇿 الجزائر: DZD"
    elif call.data == "cat_asia":
        text = "🌏 **آسيا:**\n🇺🇿 أوزبكستان: UZS\n🇰🇿 كازاخستان: KZT\n🇹🇯 طاجيكستان: TJS\n🇮🇳 الهند: INR\n🇧🇩 بنغلاديش: BDT\n🇵🇰 باكستان: PKR\n🇹🇷 تركيا: TRY\n🇲🇾 ماليزيا: MYR\n🇮🇩 إندونيسيا: IDR"
    elif call.data == "cat_europe":
        text = "💶 **أوروبا:**\n🇪🇺 دول اليورو: EUR\n🇬🇧 بريطانيا: GBP\n🇨🇭 سويسرا: CHF\n🇵🇱 بولندا: PLN\n🇸🇪 السويد: SEK\n🇩🇰 الدنمارك: DKK"
    elif call.data == "cat_africa":
        text = "🌍 **أفريقيا:**\n🇿🇦 جنوب أفريقيا: ZAR\n🇳🇬 نيجيريا: NGN\n🇰🇪 كينيا: KES\n🇪🇹 إثيوبيا: ETB\n🌍 غرب أفريقيا: XOF"
    elif call.data == "cat_americas":
        text = "🌎 **الأمريكيتين وأوقيانوسيا:**\n🇨🇦 كندا: CAD\n🇲🇽 المكسيك: MXN\n🇧🇷 البرازيل: BRL\n🇦🇷 الأرجنتين: ARS\n🇦🇺 أستراليا: AUD\n🇳🇿 نيوزيلندا: NZD"
    elif call.data == "main_menu":
        send_main_menu(call.message.chat.id, call.message.message_id)
        return

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")

def process_search(message):
    query = message.text.lower()
    results = [line for line in currency_search_db if query in line.lower()]
    
    if results:
        response_text = "✅ **نتائج البحث:**\n\n" + "\n\n".join(results) + "\n\n💡 _استخدم الرمز (مثال: USD) للتحويل._"
        bot.send_message(message.chat.id, response_text, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "❌ لم يتم العثور على نتائج. جرب كلمة أخرى.")

# ==========================================
# 6. معالجة الرسائل النصية
# ==========================================
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    text_upper = text.upper().split()
    
    # التحويل بالطريقة الإنجليزية الصريحة
    if len(text_upper) == 4 and text_upper[2] == "TO":
        try:
            amount = float(text_upper[0])
            base_currency = text_upper[1]
            target_currency = text_upper[3]
            
            if base_currency == "YER" or target_currency == "YER":
                sanaa_val, aden_val = handle_local_yemen_conversion(amount, base_currency, target_currency)
                if sanaa_val and aden_val:
                    bot.reply_to(message, f"🇾🇪 **بحسب أسعار السوق المحلي:**\n\n{amount:,.2f} {base_currency} =\n📍 **صنعاء/ذمار:** `{sanaa_val:,.2f}` {target_currency}\n📍 **عدن/الجنوب:** `{aden_val:,.2f}` {target_currency}", parse_mode="Markdown")
                else:
                    bot.reply_to(message, "❌ تأكد من رموز العملات.")
                return
                
            rate = get_exchange_rate(base_currency, target_currency)
            if rate:
                result = amount * rate
                bot.reply_to(message, f"🌍 التحويل العالمي:\n{amount:,.2f} {base_currency} = `{result:,.2f}` {target_currency}", parse_mode="Markdown")
            else:
                bot.reply_to(message, "❌ تأكد من رموز العملات. اضغط /currencies للبحث.")
            return
        except ValueError:
            pass 

    # التحويل الذكي للغة العربية
    amount, base_curr, target_curr = extract_info_from_arabic(text)
    
    if base_curr and target_curr:
        # إذا كان التحويل يخص اليمن محلياً
        if base_curr == "YER" or target_curr == "YER":
            sanaa_val, aden_val = handle_local_yemen_conversion(amount, base_curr, target_curr)
            if sanaa_val and aden_val:
                bot.reply_to(message, f"🇾🇪 **السعر المباشر (سوق محلي):**\n\n{amount:,.2f} {base_curr} =\n📍 **صنعاء/ذمار:** `{sanaa_val:,.2f}` {target_curr}\n📍 **عدن/الجنوب:** `{aden_val:,.2f}` {target_curr}", parse_mode="Markdown")
            else:
                bot.reply_to(message, "❌ عذراً، حدث خطأ في حساب السعر المحلي.")
        
        # تحويل بين أي دولتين في العالم
        else:
            rate = get_exchange_rate(base_curr, target_curr)
            if rate:
                result = amount * rate
                bot.reply_to(message, f"🌍 السعر المباشر (عالمي):\n{amount:,.2f} {base_curr} = `{result:,.2f}` {target_curr}", parse_mode="Markdown")
            else:
                bot.reply_to(message, "❌ عذراً، لم أتمكن من جلب السعر حالياً.")
    else:
        bot.reply_to(message, "🤔 عذراً، لم أفهم. جرب:\n- `كم سعر الدولار مقابل السعودي`\n- `500 يورو كم تساوي بالاماراتي`")

print("🤖 البوت يعمل بكامل الميزات ويدعم الذكاء اللغوي الآن...")
bot.polling(none_stop=True)
