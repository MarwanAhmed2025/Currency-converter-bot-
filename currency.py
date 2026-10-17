import telebot
from telebot import types
import requests
import os

# التوكن الخاص بك
TOKEN = '8963858897:AAE8SRUCJhTvlTj5_Lxz6RHncIMM5IxbDIQ'
bot = telebot.TeleBot(TOKEN)

# ==========================================
# 1. القاموس للتعرف على الأسئلة العربية
# ==========================================
currencies_ar = {
    "الدولار": "USD", "دولار": "USD", "الأمريكي": "USD",
    "اليورو": "EUR", "يورو": "EUR",
    "الجنيه الاسترليني": "GBP", "استرليني": "GBP",
    "الين الياباني": "JPY", "الين": "JPY",
    "اليوان الصيني": "CNY", "يوان": "CNY",
    "الروبل الروسي": "RUB", "روبل": "RUB",
    "الريال السعودي": "SAR", "ريال سعودي": "SAR",
    "الدرهم الاماراتي": "AED", "درهم اماراتي": "AED",
    "الدينار الكويتي": "KWD", "دينار كويتي": "KWD",
    "الريال القطري": "QAR", "ريال قطري": "QAR",
    "الريال العماني": "OMR", "ريال عماني": "OMR",
    "الدينار البحريني": "BHD", "دينار بحريني": "BHD",
    "الريال اليمني": "YER", "ريال يمني": "YER",
    "الجنيه المصري": "EGP", "جنيه مصري": "EGP",
    "الدينار الاردني": "JOD", "دينار اردني": "JOD",
    "الليرة اللبنانية": "LBP", "ليرة لبنانية": "LBP",
    "الليرة السورية": "SYP", "ليرة سورية": "SYP",
    "الدينار العراقي": "IQD", "دينار عراقي": "IQD",
    "الدرهم المغربي": "MAD", "درهم مغربي": "MAD",
    "الدينار الجزائري": "DZD", "دينار جزائري": "DZD",
    "الدينار التونسي": "TND", "دينار تونسي": "TND",
    "الدينار الليبي": "LYD", "دينار ليبي": "LYD",
    "الجنيه السوداني": "SDG", "جنيه سوداني": "SDG",
    "السوم الاوزبكي": "UZS", "سوم اوزبكي": "UZS", "اوزبكي": "UZS",
    "التنج الكازاخستاني": "KZT", "تنج كازاخستاني": "KZT",
    "السوموني الطاجيكي": "TJS", "طاجيكي": "TJS",
    "الروبيه الهنديه": "INR", "روبيه هندية": "INR", "روبيه": "INR",
    "التاكا البنجلاديشي": "BDT", "تاكا بنجلاديشي": "BDT", "تاكا": "BDT",
    "الليرة التركية": "TRY", "ليرة تركية": "TRY",
    "البيزو المكسيكي": "MXN", "بيزو مكسيكي": "MXN",
    "الريال البرازيلي": "BRL", "ريال برازيلي": "BRL"
    # (يمكنك إضافة المزيد هنا للتحويل المباشر)
}

# ==========================================
# 2. قاعدة بيانات البحث (مخصصة لزر البحث)
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
# 3. الدوال الأساسية
# ==========================================
def get_exchange_rate(base_currency, target_currency):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url)
        data = response.json()
        if target_currency in data['rates']:
            return data['rates'][target_currency]
        return None
    except:
        return None

def extract_currencies_from_arabic(text):
    found_currencies = []
    sorted_keys = sorted(currencies_ar.keys(), key=len, reverse=True)
    for key in sorted_keys:
        if key in text:
            found_currencies.append(currencies_ar[key])
            text = text.replace(key, "") 
    if len(found_currencies) >= 2:
        return found_currencies[0], found_currencies[1]
    return None, None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "مرحباً بك في بوت تحويل العملات! 💱\n\n"
        "يمكنك سؤالي بطريقتين:\n"
        "1. بالعربية: 'كم سعر الدولار مقابل السوم الاوزبكي؟'\n"
        "2. بالإنجليزية: '1 USD TO UZS'\n\n"
        "🌐 لمعرفة الرموز أو البحث عن عملة، اضغط على:\n/currencies"
    )
    bot.reply_to(message, text)

# ==========================================
# 4. واجهة الأزرار التفاعلية
# ==========================================
@bot.message_handler(commands=['currencies'])
def show_currencies_menu(message):
    send_main_menu(message.chat.id)

def send_main_menu(chat_id, message_id=None):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🌍 أهم العملات", callback_data="cat_world")
    btn2 = types.InlineKeyboardButton("🦅 الدول العربية", callback_data="cat_arab")
    btn3 = types.InlineKeyboardButton("🌏 آسيا", callback_data="cat_asia")
    btn4 = types.InlineKeyboardButton("💶 أوروبا", callback_data="cat_europe")
    btn5 = types.InlineKeyboardButton("🌍 أفريقيا", callback_data="cat_africa")
    btn6 = types.InlineKeyboardButton("🌎 الأمريكيتين وأوقيانوسيا", callback_data="cat_americas")
    # الزر الجديد للبحث
    search_btn = types.InlineKeyboardButton("🔍 بحث عن دولة أو عملة", callback_data="search_currency")
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    markup.add(search_btn) # إضافته في سطر منفصل بالأسفل

    text = "📊 **دليل العملات الشامل:**\n\nالرجاء اختيار القارة، أو استخدام زر البحث:"
    
    if message_id:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

# ==========================================
# 5. معالجة الضغط على الأزرار ونظام البحث
# ==========================================
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # إذا ضغط المستخدم على زر البحث
    if call.data == "search_currency":
        msg = bot.send_message(call.message.chat.id, "🔍 **البحث نشط الآن:**\n\nالرجاء كتابة اسم الدولة (مثال: اليمن)، اسم العملة (مثال: Euro)، أو رمزها (مثال: USD):", parse_mode="Markdown")
        # البوت سينتظر رسالة المستخدم التالية ويمررها لدالة process_search
        bot.register_next_step_handler(msg, process_search)
        return

    markup = types.InlineKeyboardMarkup()
    back_btn = types.InlineKeyboardButton("⬅️ رجوع", callback_data="main_menu")
    markup.add(back_btn)
    
    if call.data == "cat_world":
        text = "🌍 **أهم العملات العالمية:**\n🇺🇸 أمريكا: USD\n🇪🇺 أوروبا: EUR\n🇬🇧 بريطانيا: GBP\n🇨🇭 سويسرا: CHF\n🇯🇵 اليابان: JPY\n🇨🇳 الصين: CNY\n🇷🇺 روسيا: RUB"
    elif call.data == "cat_arab":
        text = "🦅 **الدول العربية:**\n🇸🇦 السعودية: SAR\n🇦🇪 الإمارات: AED\n🇰🇼 الكويت: KWD\n🇶🇦 قطر: QAR\n🇴🇲 عُمان: OMR\n🇾🇪 اليمن: YER\n🇪🇬 مصر: EGP\n🇯🇴 الأردن: JOD\n🇮🇶 العراق: IQD\n🇸🇾 سوريا: SYP\n🇱🇧 لبنان: LBP\n🇲🇦 المغرب: MAD\n🇩🇿 الجزائر: DZD"
    elif call.data == "cat_asia":
        text = "🌏 **آسيا (تشمل الوسطى):**\n🇺🇿 أوزبكستان: UZS\n🇰🇿 كازاخستان: KZT\n🇹🇯 طاجيكستان: TJS\n🇮🇳 الهند: INR\n🇧🇩 بنغلاديش: BDT\n🇵🇰 باكستان: PKR\n🇹🇷 تركيا: TRY\n🇲🇾 ماليزيا: MYR\n🇮🇩 إندونيسيا: IDR"
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

# دالة البحث (تتفعل فقط بعد ضغط زر البحث)
def process_search(message):
    query = message.text.lower()
    
    # البحث داخل قاعدة البيانات عن أي تطابق
    results = [line for line in currency_search_db if query in line.lower()]
    
    if results:
        response_text = "✅ **نتائج البحث:**\n\n" + "\n\n".join(results) + "\n\n💡 _يمكنك الآن استخدام الرمز (مثال: USD) للتحويل._"
        bot.send_message(message.chat.id, response_text, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "❌ لم أتمكن من العثور على الدولة أو العملة. حاول كتابة الاسم بطريقة مختلفة (مثلاً 'امريكا' بدلاً من 'الولايات المتحدة').")

# ==========================================
# 6. معالجة رسائل التحويل
# ==========================================
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    text_upper = text.upper().split()
    
    if len(text_upper) == 4 and text_upper[2] == "TO":
        try:
            amount = float(text_upper[0])
            base_currency = text_upper[1]
            target_currency = text_upper[3]
            rate = get_exchange_rate(base_currency, target_currency)
            if rate:
                result = amount * rate
                bot.reply_to(message, f"✅ التحويل:\n{amount} {base_currency} = {result:.2f} {target_currency}")
            else:
                bot.reply_to(message, "❌ تأكد من رموز العملات. اضغط /currencies للبحث.")
            return
        except ValueError:
            pass 

    base_curr, target_curr = extract_currencies_from_arabic(text)
    if base_curr and target_curr:
        rate = get_exchange_rate(base_curr, target_curr)
        if rate:
            bot.reply_to(message, f"✅ السعر المباشر الآن:\n1 {base_curr} = {rate:.2f} {target_curr}")
        else:
            bot.reply_to(message, "❌ عذراً، لم أتمكن من جلب السعر حالياً.")
    else:
        bot.reply_to(message, "🤔 عذراً، لم أفهم. جرب: 'كم سعر الدولار مقابل السوم الاوزبكي؟' أو اضغط /currencies للبحث عن الرموز.")

print("🤖 البوت يعمل الآن (وميزة البحث مفعلة)... اضغط Ctrl+C لإيقافه.")
bot.polling(none_stop=True)
