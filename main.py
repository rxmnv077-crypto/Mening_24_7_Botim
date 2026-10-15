import telebot
from telebot import types
from telebot import apihelper
import time
import random
import os
import threading
import sqlite3
from datetime import datetime

TOKEN = "8679268036:AAGk-f5t4c77wFb_qLHLTrx2wRQfeQJUiKg"
KANAL_USER = "@eskidaftar"
ADMIN_USER = "jizzaxlioka"

# --- KITOB KODLARI BAZASI (001 dan 999 gacha) ---
KITOB_001_ID = "BQACAgIAAxkBAAIBSGqaxbrxg4of4cKgYhRHx8kmIGeDAAKBqAAC58fZSKAPz52d4t1rPQQ"
KITOB_002_ID = "BQACAgIAAxkBAAICPGqa4Zbs5tn0hLOHTzuzgoxGOX32AAKxqQAC58fZSBUqVpAUmKSjPQQ"
KITOB_003_ID = "BQACAgIAAxkBAAICn2qa-0_jTqpZ_YxDvLBGagvGN7clAAIjqwAC58fZSKVFr34lAR3MPQQ"
KITOB_004_ID = "BQACAgIAAxkBAAICqGqa_Wzdlzbf2VQCyRJ1UKJOVzmjAAJCqwAC58fZSNav9hsiRay8PQQ"
KITOB_005_ID = "BQACAgIAAxkBAAICrGqa_5xS14hR8Ybay1ujSzplF7cFAAJcqwAC58fZSKQeXd8zT7bnPQQ"
KITOB_006_ID = "BQACAgIAAxkBAAIGN2qdQ3DttKW3m2axplgGYJSxhZP4AAKbqwACBnroSD5ZDQ1q0_YuPQQ"
KITOB_007_ID = "BQACAgIAAxkBAAIGOWqdREJFSXj1PQtFZsIZzIvyVtqdAAKnqwACBnroSKn53JVHPc3xPQQ"
KITOB_008_ID = "BQACAgIAAxkBAAIHV2qdczExZZOGvCdzjt1Vsa9SZt1MAALdnQACBnrwSIsx_mleMpKpPQQ"
KITOB_009_ID = "BQACAgEAAxkBAAIHWWqdc0AFUvjhqsisp4nDbqw3GxjaAAK6CAACGY3ZRFZv84i9x-5OPQQ"
KITOB_010_ID = "BQACAgIAAxkBAAIHW2qdc3McuVjOdozHQNmBd0Ip2x_7AALjnQACBnrwSEDFMWIT6jrOPQQ"
KITOB_011_ID = "BQACAgIAAxkBAAIHXWqdc8eIgrXzBjoE-FPF6C-6xR4wAAIfgwACjygQSiGjPbs6mZ1gPQQ"
KITOB_012_ID = "BQACAgEAAxkBAAIHX2qdc-ZwEK1xsgzZJHX9k7rguZeRAAL5BgACLqjoRA6o_vIUpYyMPQQ"
KITOB_013_ID = "BQACAgEAAxkBAAIHYWqdc_veuT2jchESu8_8RXFTEQv4AALlBgACV3kpRvxvDdcK8I0sPQQ"
KITOB_014_ID = "BQACAgEAAxkBAAIJ22qejoRpn7Lq8xZjScx3jOcTWV9ZAAJbCAACZbHgRbWyIzU5zKHxPQQ"
KITOB_015_ID = "BQACAgEAAxkBAAIJ3WqejutNlfZ-iaCSyThv3-l8g4BPAAKNBwACIQbIRA3Wx-HlYszCPQQ"
KITOB_016_ID = "BU YERGA KITOB IDSI YOZILADI"
KITOB_017_ID = "BU YERGA KITOB IDSI YOZILADI"
KITOB_018_ID = "BU YERGA KITOB IDSI YOZILADI"
KITOB_019_ID = "BU YERGA KITOB IDSI YOZILADI"

bot = telebot.TeleBot(TOKEN)
USER_STATES = {}
CLICK_COUNTS = {}
TEXT_COUNTS = {}
DB_FILE = "kutubxona.db"
# --- MA'LUMOTLAR BAZASI TIZIMI ---
def db_yaratish():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT,
            phone TEXT,
            donat INT DEFAULT 0,
            sana TEXT
        )
    ''')
    conn.commit()
    conn.close()

def foydalanuvchi_saqlash(user_id, username):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (str(user_id),))
        if not cursor.fetchone():
            bugun = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("INSERT INTO users (user_id, username, sana) VALUES (?, ?, ?)",
                           (str(user_id), str(username), bugun))
            conn.commit()
        conn.close()
    except Exception: pass

def jami_odamlar():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(user_id) FROM users")
        soni = cursor.fetchone()[0]
        conn.close()
        return soni
    except Exception: return 0

db_yaratish()

def tekshirish(user_id):
    try:
        holat = bot.get_chat_member(KANAL_USER, user_id).status
        if holat in ['member', 'administrator', 'creator']: return True
        return False
    except Exception: return False

def majburiy_obuna_menyusi():
    klaviatura = types.InlineKeyboardMarkup(row_width=1)
    kanal_tugma = types.InlineKeyboardButton(text="📢 Yaxshilar kanaliga qo'shilish", url=f"tg://resolve?domain={KANAL_USER.replace('@', '')}")
    tekshir_tugma = types.InlineKeyboardButton(text="✅ Tekshirish", callback_data="tekshir_obuna")
    klaviatura.add(kanal_tugma, tekshir_tugma)
    return klaviatura
@bot.message_handler(commands=['start', 'boshlash'])
def start_xabari(message):
    try:
        user_id = message.from_user.id
        username = message.from_user.username or "yo'q"
        foydalanuvchi_saqlash(user_id, username)
        USER_STATES[user_id] = "kitob"
        CLICK_COUNTS[user_id] = 0
        TEXT_COUNTS[user_id] = 0

        if tekshirish(user_id):
            matn = "📚 **Yaxshilar Kutubxonasiga xush kelibsiz!**\n\nQidirayotgan kitobingiz raqamini chatga yozib yuboring:\n\n*( Yaxshilar Kutubxonachi Ai tizimi bilan gaplashish uchun /suhbatlashish: Hisob va profil ma'lumotlarini ko'rish uchun /profil: Yaqin oradagi do'konlar topish uchun /lokatsiya buyrug'ini bosing )*"
            bot.send_message(message.chat.id, matn, parse_mode="Markdown")
        else:
            matn = "✨ **Assalamu Alaykum!**\n\nBotdan foydalanish va kitoblarni bepul yuklab olish uchun birinchi navbatda rasmiy kanalimizga a'zo bo'lishingiz shart."
            bot.send_message(message.chat.id, matn, reply_markup=majburiy_obuna_menyusi(), parse_mode="Markdown")
    except Exception: pass

@bot.callback_query_handler(func=lambda call: call.data == "tekshir_obuna")
def callback_tekshir(call):
    try:
        user_id = call.from_user.id
        username = call.from_user.username or "yo'q"
        foydalanuvchi_saqlash(user_id, username)

        if tekshirish(user_id):
            CLICK_COUNTS[user_id] = 0
            TEXT_COUNTS[user_id] = 0
            matn = (
                "🎉 **Siz kanalimizga muvaffaqiyatli qo'shildingiz!**\n\n"
                "Marhamat, qidirayotgan kitobingiz raqamini yozing:\n\n"
                "*( Yaxshilar Kutubxonachi Ai tizimi bilan gaplashish uchun /suhbatlashish: Hisob va profil ma'lumotlarini ko'rish uchun /profil: Yaqin oradagi do'konlar topish uchun /lokatsiya buyrug'ini bosing )*"
            )
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=matn, parse_mode="Markdown")
        else:
            CLICK_COUNTS[user_id] = CLICK_COUNTS.get(user_id, 0) + 1
            count = CLICK_COUNTS[user_id]
            if count == 1:
                bot.answer_callback_query(call.id, text="❌ Siz hali kanalga a'zo bo'lmadingiz! Iltimos, avval kanalga qo'shiling.", show_alert=True)
            elif count == 2:
                matn = "⚠️ **Kechirasiz, siz hali kanalimizga obuna bo'lmagansiz!**\n\nIltimos, pastdagi ko'k tugma orqali kanalga qo'shiling va keyin 'Tekshirish' tugmasini qayta bosing."
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=matn, reply_markup=majburiy_obuna_menyusi(), parse_mode="Markdown")
            else:
                matn = "❌ **Muammoga duch kelgan bo'lsangiz, adminga murojaat qiling!**"
                klaviatura = types.InlineKeyboardMarkup(row_width=1)
                kanal_tugma = types.InlineKeyboardButton(text="📢 Yaxshilar kanaliga qo'shilish", url=f"tg://resolve?domain={KANAL_USER.replace('@', '')}")
                admin_tugma = types.InlineKeyboardButton(text="👨‍💻 Admin bilan bog'lanish", url=f"tg://resolve?domain={ADMIN_USER}")
                tekshir_tugma = types.InlineKeyboardButton(text="✅ Qayta tekshirish", callback_data="tekshir_obuna")
                klaviatura.add(kanal_tugma, admin_tugma, tekshir_tugma)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=matn, reply_markup=klaviatura, parse_mode="Markdown")
    except Exception: pass

@bot.message_handler(commands=['statistika'])
def statistika_bo_limi(message):
    try:
        if message.from_user.username == ADMIN_USER:
            soni = jami_odamlar()
            matn = f"📊 **Yaxshilar Kutubxonasi statistikasi:**\n\nBotga kirib start bosgan jami foydalanuvchilar soni: **{soni} ta**"
            bot.send_message(message.chat.id, matn, parse_mode="Markdown")
    except Exception: pass

@bot.message_handler(commands=['donat'])
def donat_bo_limi(message):
    try:
        user_id = message.from_user.id
        if not tekshirish(user_id): return
        matn = (
            "✨ **Yaxshilar Kutubxonasi — mutlaqo bepul va reklamasiz loyihadir.**\n\n"
            "Biz har kuni siz uchun eng sara, eng trenddagi kitoblarni qidirib topamiz va botga joylaymiz. "
            "Agar loyihamiz sizga yoqqan bo‘lsa va uning rivojiga hissa qo‘shishni istasangiz, ixtiyoriy miqdorda donat ( ko‘mak ) qilishingiz mumkin: Admin sizdan minnatdor bo‘ladi! 🌿❤️\n\n"
            "💳 **Istalgan plastik karta orqali:**\n"
            "`4916990366612676` *( Nusxalash uchun ustiga bosing! )*\n"
            "👤 Ega: **S.Rahmonqulov**\n\n"
            "👋 *Yaxshilik zanjirining bir qismi bo‘lganingiz uchun tashakkur!*"
        )
        bot.send_message(message.chat.id, matn, parse_mode="Markdown")
    except Exception: pass

@bot.message_handler(commands=['suhbatlashish'])
def suhbat_rejimi(message):
    try:
        user_id = message.from_user.id
        if not tekshirish(user_id): return
        USER_STATES[user_id] = "ai"
        matn = "✨ **Assalamu alaykum! Bugun nima haqida gaplashamiz?**\n\n*( Kitob qidirish bo'limiga qaytish uchun istalgan vaqtda /boshlash buyrug'ini bosing )*"
        bot.send_message(message.chat.id, matn, parse_mode="Markdown")
    except Exception: pass

@bot.message_handler(commands=['lokatsiya'])
def lokatsiya_so_rash(message):
    try:
        user_id = message.from_user.id
        if not tekshirish(user_id): return

        klaviatura = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        tugma = types.KeyboardButton(text="Joylashuvni yuborish", request_location=True)
        klaviatura.add(tugma)

        matn = "**Iltimos: Joylashuv ma'lumotingizni yuborish uchun pastdagi ( Joylashuvni yuborish ) tugmasini bosing:**"
        bot.send_message(message.chat.id, matn, reply_markup=klaviatura, parse_mode="Markdown")
    except Exception: pass

@bot.message_handler(content_types=['location'])
def lokatsiya_qabul_qilindi(message):
    try:
        user_id = message.from_user.id
        if not tekshirish(user_id): return

        inline_klaviatura = types.InlineKeyboardMarkup(row_width=2)

        andijon = types.InlineKeyboardButton(text="Andijon", callback_data="vil_andijon")
        buxoro = types.InlineKeyboardButton(text="Buxoro", callback_data="vil_buxoro")
        fargona = types.InlineKeyboardButton(text="Farg'ona", callback_data="vil_fargona")
        jizzax = types.InlineKeyboardButton(text="Jizzax", callback_data="vil_jizzax")
        xorazm = types.InlineKeyboardButton(text="Xorazm", callback_data="vil_xorazm")
        namangan = types.InlineKeyboardButton(text="Namangan", callback_data="vil_namangan")
        navoiy = types.InlineKeyboardButton(text="Navoiy", callback_data="vil_navoiy")
        qashqadaryo = types.InlineKeyboardButton(text="Qashqadaryo", callback_data="vil_qashqadaryo")
        samarqand = types.InlineKeyboardButton(text="Samarqand", callback_data="vil_samarqand")
        sirdaryo = types.InlineKeyboardButton(text="Sirdaryo", callback_data="vil_sirdaryo")
        surxondaryo = types.InlineKeyboardButton(text="Surxondaryo", callback_data="vil_surxondaryo")
        toshkent = types.InlineKeyboardButton(text="Toshkent", callback_data="vil_toshkent")

        inline_klaviatura.add(
            andijon, buxoro,
            fargona, jizzax,
            xorazm, namangan,
            navoiy, qashqadaryo,
            samarqand, sirdaryo,
            surxondaryo, toshkent
        )

        matn = "✅ **Joylashuvingiz qabul qilindi!**\n\nMarhamat, o'z viloyatingizni tanlang:"

        yopish_klaviatura = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, matn, reply_markup=inline_klaviatura, parse_mode="Markdown")
    except Exception: pass

# --- VILOYATLAR BO'YICHA 3 TAdan KITOB MASKANLARI MA'LUMOTLARI ---
KITOB_MASKANLARI = {
    "vil_andijon": (
        "🍏 **Andijon viloyati bo'yicha kitob maskanlari:**\n\n"
        "1. **Andijon viloyat 'Kitob Olami' markazi**\n"
        "📍 Manzil: Andijon sh., Muqimiy ko'chasi, 1-uy\n\n"
        "2. **Zahiriddin Muhammad Bobur nomidagi viloyat kutubxonasi**\n"
        "📍 Manzil: Andijon sh., Navoiy shoh ko'chasi, 15\n\n"
        "3. **Asaxiy Books Andijon filiali**\n"
        "📍 Manzil: Andijon sh., Bobur shoh ko'chasi, 12"
    ),
    "vil_buxoro": (
        "🐪 **Buxoro viloyati bo'yicha kitob maskanlari:**\n\n"
        "1. **Buxoro markaziy 'Kitob Olami' do'koni**\n"
        "📍 Manzil: Buxoro sh., M.Iqbol ko'chasi, 2-uy\n\n"
        "2. **Abu Ali ibn Sino nomidagi viloyat kutubxonasi**\n"
        "📍 Manzil: Buxoro sh., Navoiy shoh ko'chasi, 3\n\n"
        "3. **Hilol Nashr Buxoro do'koni**\n"
        "📍 Manzil: Buxoro sh., Ibn Sino ko'chasi, 15"
    ),
    "vil_fargona": (
        "🍇 **Farg'ona viloyati bo'yicha kitob maskanlari:**\n\n"
        "1. **Sarmoya Books Farg'ona markazi**\n"
        "📍 Manzil: Farg'ona sh., Al-Farg'oniy ko'chasi, 18\n\n"
        "2. **Al-Farg'oniy nomidagi viloyat kutubxonasi**\n"
        "📍 Manzil: Farg'ona sh., Marifat ko'chasi, 4\n\n"
        "3. **Kitob Olami Farg'ona filiali**\n"
        "📍 Manzil: Farg'ona sh., Mustaqillik ko'chasi, 22"
    ),
    "vil_jizzax": (
        "🏛️ **Jizzax viloyati bo'yicha kitob maskanlari:**\n\n"
        "1. **Sh.Rashidov nomidagi Jizzax viloyat kutubxonasi**\n"
        "📍 Manzil: Jizzax sh., Qassoblik mfy, Sh.Rashidov ko'chasi, 12\n\n"
        "2. **Gallaorol Markaziy Kitob Do'koni**\n"
        "📍 Manzil: G'allaorol tumani, Mustaqillik ko'chasi\n\n"
        "3. **Asaxiy Books Jizzax hamkor nuqtasi**\n"
        "📍 Manzil: Jizzax sh., Markaziy dehqon bozori yoni"
    ),
    "vil_xorazm": (
        "🏛️ **Xorazm viloyati bo'yicha kitob maskanlari:**\n\n"
        "1. **Urganch markaziy kitoblar dunyosi**\n"
        "📍 Manzil: Urganch sh., Al-Xorazmiy ko'chasi, 26\n\n"
        "2. **Isfandiyorxon nomidagi viloyat kutubxonasi**\n"
        "📍 Manzil: Urganch sh., Tinchlik ko'chasi, 11\n\n"
        "3. **Hilol Nashr Urganch do'koni**\n"
        "📍 Manzil: Urganch sh., Xonqa ko'chasi, 5"
    ),
    "vil_namangan": (
        "🌸 **Namangan viloyati bo'yicha kitob maskanlari:**\n\n"
        "1. **Baraket Bookstore Namangan**\n"
        "📍 Manzil: Namangan sh., Otamirzayev ko'chasi, 7\n\n"
        "2. **Mashrab nomidagi viloyat markaziy kutubxonasi**\n"
        "📍 Manzil: Namangan sh., Nodira ko'chasi, 14\n\n"
        "3. **Kitob Dunyosi Namangan do'koni**\n"
        "📍 Manzil: Namangan sh., Uychi ko'chasi, 45"
    ),
    "vil_navoiy": (
        "💎 **Navoiy viloyati bo'yicha kitob maskanlari:**\n\n"
        "1. **Navoiy viloyat markaziy kutubxonasi**\n"
        "📍 Manzil: Navoiy sh., Islom Karimov shoh ko'chasi, 5\n\n"
        "2. **Ziyo Kitoblar Dunyosi do'koni**\n"
        "📍 Manzil: Navoiy sh., G'alaba shoh ko'chasi, 24\n\n"
        "3. **Asaxiy Books Navoiy nuqtasi**\n"
        "📍 Manzil: Navoiy sh., Me'morlar ko'chasi, 10"
    ),
    "vil_qashqadaryo": (
        "🍉 **Qashqadaryo viloyati bo'yicha kitob maskanlari:**\n\n"
        "1. **Qarshi markaziy 'Kitob Dunyosi' do'koni**\n"
        "📍 Manzil: Qarshi sh., Mustaqillik maydoni, 4\n\n"
        "2. **Sadriddin Ayniy nomidagi viloyat kutubxonasi**\n"
        "📍 Manzil: Qarshi sh., O'zbekiston ko'chasi, 19\n\n"
        "3. **Hilol Nashr Qarshi filiali**\n"
        "📍 Manzil: Qarshi sh., Islom Karimov ko'chasi, 8"
    ),
    "vil_samarqand": (
        "🕌 **Samarqand viloyati bo'yicha kitob maskanlari:**\n\n"
        "1. **A.S.Pushkin nomidagi viloyat axborot-kutubxonasi**\n"
        "📍 Manzil: Samarqand sh., Universitet xiyoboni, 21\n\n"
        "2. **Sarmoya Books Samarqand do'koni**\n"
        "📍 Manzil: Samarqand sh., Shohrux Mirzo ko'chasi, 17\n\n"
        "3. **Hilol Nashr Samarqand filiali**\n"
        "📍 Manzil: Samarqand sh., Gagarin ko'chasi, 88"
    ),
    "vil_sirdaryo": (
        "🌾 **Sirdaryo viloyati bo'yicha kitob maskanlari:**\n\n"
        "1. **Guliston shahri 'Ziyo Olami' kitob do'koni**\n"
        "📍 Manzil: Guliston sh., Mustaqillik ko'chasi, 32\n\n"
        "2. **Sirdaryo viloyat markaziy kutubxonasi**\n"
        "📍 Manzil: Guliston sh., Beruniy ko'chasi, 4\n\n"
        "3. **Bilimdon kitoblar markazi**\n"
        "📍 Manzil: Yangiyer sh., Tinchlik ko'chasi, 12"
    ),
    "vil_surxondaryo": (
        "☀️ **Surxondaryo viloyati bo'yicha kitob maskanlari:**\n\n"
        "1. **Termiz markaziy kitob do'koni**\n"
        "📍 Manzil: Termiz sh., At-Termiziy ko'chasi, 11\n\n"
        "2. **Adib Sobir Termiziy nomidagi kutubxona**\n"
        "📍 Manzil: Termiz sh., Barkamol Avlod ko'chasi, 5\n\n"
        "3. **Ziyo Nur Kitoblar do'koni**\n"
        "📍 Manzil: Denov tumani, Sharaf Rashidov ko'chasi"
    ),
    "vil_toshkent": (
        "🏢 **Toshkent shahri va viloyati bo'yicha kitob maskanlari:**\n\n"
        "1. **Asaxiy Books - Kitob Olami markazi**\n"
        "📍 Manzil: Yunusobod tumani, Mustaqillik shoh ko'chasi, 6\n\n"
        "2. **Alisher Navoiy nomidagi O'zbekiston Milliy kutubxonasi**\n"
        "📍 Manzil: Yunusobod tumani, Alisher Navoiy ko'chasi, 1\n\n"
        "3. **«Kitob Olami» markaziy savdo majmuasi**\n"
        "📍 Manzil: Mirabod tumani, Islom Karimov ko'chasi, 17"
    )
}

@bot.callback_query_handler(func=lambda call: call.data.startswith("vil_"))
def viloyat_tanlandi(call):
    try:
        user_id = call.from_user.id
        if not tekshirish(user_id): return

        viloyat_kodi = call.data
        if viloyat_kodi in KITOB_MASKANLARI:
            javob_matni = KITOB_MASKANLARI[viloyat_kodi]

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=javob_matni,
                parse_mode="Markdown"
            )
        bot.answer_callback_query(call.id)
    except Exception: pass

@bot.message_handler(commands=['profil'])
def profil_bo_limi(message):
    try:
        user_id = message.from_user.id
        if not tekshirish(user_id): return

        # A) ADMIN BOSGANDA HAMMANING JADVALI CHIQADI (XATOLIK TUZATILDI!)
        if message.from_user.username == ADMIN_USER:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT username, phone, donat, sana FROM users WHERE phone IS NOT NULL")
            rows = cursor.fetchall()
            conn.close()

            matn = f"👑 **Yaxshilar Kutubxonasi — Bosh Admin paneli**\n\n👥 Jami ro'yxatdan o'tganlar: **{len(rows)} ta**\n\n"
            for r in rows[-15:]:
                matn += f"👤 `@{r[0]}` | 📱 `{r[1]}` | 💳 {r[2]} so'm | ⏳ {r[3]}\n"
            bot.send_message(message.chat.id, matn, parse_mode="Markdown")
            return

        # B) ODDID FOYDALANUVCHILAR BOSGANDA
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT phone, donat, sana FROM users WHERE user_id = ?", (str(user_id),))
        res = cursor.fetchone()
        conn.close()

        if res and res[0]:
            sana_dt = datetime.strptime(res[2], "%Y-%m-%d")
            kunlar = (datetime.now() - sana_dt).days + 1
            matn = (
                "👤 **Sizning shaxsiy hisobingiz:**\n\n"
                f"📱 Telefon raqam: `{res[0]}`\n"
                f"⏳ Botdagi faollik: **{kunlar} kun**\n"
                f"💳 Umumiy donatingiz: **{res[1]} so'm**\n\n"
                "🌿 *Yaxshilar safiga qo'shilganingiz uchun tashakkur!*"
            )
            bot.send_message(message.chat.id, matn, parse_mode="Markdown")
        else:
            klaviatura = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
            tugma = types.KeyboardButton(text="📱 Telefon raqamni ulashish", request_contact=True)
            klaviatura.add(tugma)
            matn = "🔑 **Bot ichida shaxsiy hisob yaratish va faollik tarixingizni ko'rish uchun pastdagi [ 📱 Telefon raqamni ulashish ] tugmasini bosing:**"
            bot.send_message(message.chat.id, matn, reply_markup=klaviatura, parse_mode="Markdown")
    except Exception: pass

@bot.message_handler(content_types=['contact'])
def telefon_raqam_saqlash(message):
    try:
        user_id = message.from_user.id
        if not tekshirish(user_id): return

        phone = message.contact.phone_number
        if not phone.startswith("+"): phone = "+" + phone

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET phone = ? WHERE user_id = ?", (str(phone), str(user_id)))
        conn.commit()

        cursor.execute("SELECT sana FROM users WHERE user_id = ?", (str(user_id),))
        sana = cursor.fetchone()[0]
        conn.close()

        sana_dt = datetime.strptime(sana, "%Y-%m-%d")
        kunlar = (datetime.now() - sana_dt).days + 1

        matn = (
            "🎉 **Tabriklaymiz! Shaxsiy hisobingiz muvaffaqiyatli yaratildi!**\n\n"
            f"📱 Telefon raqam: `{phone}`\n"
            f"⏳ Botdagi faollik: **{kunlar} kun**\n"
            "💳 Umumiy donatingiz: **0 so'm**\n\n"
            "📚 *Endi bot faoliyatingiz va qilgan ko'maklaringizni aniq hisoblanib boradi!*"
        )
        yopish_klaviatura = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, matn, reply_markup=yopish_klaviatura, parse_mode="Markdown")
    except Exception: pass

@bot.message_handler(commands=['yordam'])
def yordam_xabari(message):
    try:
        matn = "Agar botdan foydalanishda muammolarga duch kelasangiz yoki takliflaringiz bo'lsa, admin bilan bog'laning:"
        klaviatura = types.InlineKeyboardMarkup()
        admin_tugma = types.InlineKeyboardButton(text="👨‍💻 Yaxshilar admin", url=f"tg://resolve?domain={ADMIN_USER}")
        klaviatura.add(admin_tugma)
        bot.send_message(message.chat.id, matn, reply_markup=klaviatura)
    except Exception: pass

@bot.message_handler(content_types=['document'])
def admin_fayl_qabul_qilish(message):
    try:
        if message.from_user.username == ADMIN_USER:
            fayl_id = message.document.file_id
            fayl_nomi = message.document.file_name
            toza_nom = fayl_nomi.replace(".pdf", "").replace(".PDF", "").split("[")[0].strip()
            matn = f"📥 **Yaxshilar Kutubxonasi uchun yangi kitob aniqlandi!**\n\n📄 Tozalangan Nomi: **{toza_nom}**\n🔑 Maxfiy uzun kod (File ID):\n\n`{fayl_id}`\n\n*(Ushbu kodni ustiga bosing, nusxalanadi!)*"
            bot.reply_to(message, matn, parse_mode="Markdown")
    except Exception: pass

@bot.message_handler(content_types=['text'])
def kitob_va_ai_boshqaruv(message):
    try:
        user_id = message.from_user.id
        kod = message.text.strip()
        username = message.from_user.username or "yo'q"
        foydalanuvchi_saqlash(user_id, username)

        if not tekshirish(user_id):
            TEXT_COUNTS[user_id] = TEXT_COUNTS.get(user_id, 0) + 1
            if TEXT_COUNTS[user_id] == 1:
                matn = "⚠️ **Kechirasiz, siz hali kanalga obuna bo'lmadingiz!**\n\nObuna bo'lish uchun pastdagi bo'limni tanlang:"
                bot.send_message(message.chat.id, matn, reply_markup=majburiy_obuna_menyusi(), parse_mode="Markdown")
            else:
                matn = "❌ **Obuna bo'lishda muammoga duch kelsangiz, Adminga murojaat qiling!**"
                klaviatura = types.InlineKeyboardMarkup(row_width=1)
                kanal_tugma = types.InlineKeyboardButton(text="📢 Yaxshilar kanaliga qo'shilish", url=f"tg://resolve?domain={KANAL_USER.replace('@', '')}")
                admin_tugma = types.InlineKeyboardButton(text="👨‍💻 Yaxshilar admin", url=f"tg://resolve?domain={ADMIN_USER}")
                tekshir_tugma = types.InlineKeyboardButton(text="✅ Tekshirish", callback_data="tekshir_obuna")
                klaviatura.add(kanal_tugma, tekshir_tugma, admin_tugma)
                bot.send_message(message.chat.id, matn, reply_markup=klaviatura, parse_mode="Markdown")
            return

        if USER_STATES.get(user_id) == "ai" and not kod.startswith('/'):
            bot.send_chat_action(message.chat.id, 'typing')
            savol = kod.lower()
            if any(x in savol for x in ["salom", "assalom", "qalaysiz"]):
                javob = random.choice(["Vaalaykum assalom! Bugun qanday mavzuda gaplashamiz?", "Assalamu alaykum! Nima haqida suhbatlashamiz?"])
            elif "rahmat" in savol: javob = "Arziydi, do'stim! Mutolaadan aslo to'xtamang! ✨"
            else: javob = random.choice([f"Siz bergan '{kod}' savoli ustida chuqur o'ylayapman...", "Ajoyib mulohaza! Men eshityapman. ✨"])
            bot.reply_to(message, javob)
            return

        elif not kod.startswith('/'):
            if kod.isdigit() and len(kod) == 3 and "001" <= kod <= "999":
                if kod in ["001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015"]:
                    if kod == "001": c_matn = "📄 **Chingiz Aytmatov — Asrga tatigulik kun**"
                    elif kod == "002": c_matn = "📄 **Xudoyberdi To'xtaboyev — Qiz bolaga tosh otmang**"
                    elif kod == "003": c_matn = "📄 **Jeyn Ostin — G'urur va andisha**"
                    elif kod == "004": c_matn = "📄 **Jorj Oruell — Molxona**"
                    elif kod == "005": c_matn = "📄 **Mirach Chag'riy Oqtosh — To'siqlarga qaramay sevdik**"
                    elif kod == "006": c_matn = "📄 **Ba'zilar olisdan sevarlar**"
                    elif kod == "007": c_matn = "📄 **O'zinga xush kelding**"
                    elif kod == "008": c_matn = "📄 **Besh bolali yigitcha**"
                    elif kod == "009": c_matn = "📄 **Seni sevaman dema his ettir**"
                    elif kod == "010": c_matn = "📄 **Birinchi muhabbatim**"
                    elif kod == "011": c_matn = "📄 **Amina Shanliko'g'li - Vijdon azobi**"
                    elif kod == "012": c_matn = "📄 **Sen mening qalbimdasan**"
                    elif kod == "013": c_matn = "📄 **Choliqushi**"
                    elif kod == "014": c_matn = "📄 **Go'kan Kinsun — Seniki bo'lgan seni topadi**"
                    elif kod == "015": c_matn = "📄 **Atham Amin Nemutlu — Duo taqdirni o'zgartiradi**"
                    bot.send_document(message.chat.id, globals()[f"KITOB_{kod}_ID"], caption=c_matn + "\n\n*Yaxshilar kutubxonasi tomonidan taqdim etildi.*\n\n✨ **Maroqli hordiq tilaymiz!**", parse_mode="Markdown")
                else:
                    bot.send_message(message.chat.id, "Kechirasiz, asar tizimda mavjud emas yoki mualliflik huquqi bilan himoyalangan.")
            else:
                bot.send_message(message.chat.id, "[ Xato ]  Iltimos, kitob raqamini to'g'ri kiriting! ( Masalan: 001 )")
    except Exception: pass

def botni_uyg_otib_turish():
    while True:
        try:
            bot.get_me()
            print("[HEARTBEAT]: Server muvaffaqiyatli chalg'itildi, bot 100% uyg'oq!")
        except Exception: pass
        time.sleep(1800)

threading.Thread(target=botni_uyg_otib_turish, daemon=True).start()

while True:
    try:
        bot.delete_webhook()
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except Exception: time.sleep(3)
