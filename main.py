import os
import sys
import json
import logging
import uuid
import telebot

# Принудительное отключение прокси-переменных для обхода сетевых багов Windows
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

# Настройка вывода логов в консоль Visual Studio
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

USER_DATA_FILE = 'user_data.json'
DEALS_FILE = 'deals.json'
IMAGE_PATH = 'image.jpg'
VIDEO_PATH = 'animation.mp4'

# Безопасная работа с файлами баз данных
def load_json(filepath, default_val):
    if not os.path.exists(filepath):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(default_val, f, ensure_ascii=False, indent=4)
        except Exception: pass
        return default_val
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default_val

def save_json(filepath, data):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Ошибка сохранения файла {filepath}: {e}")

# Инициализируем словари базы данных
user_data = load_json(USER_DATA_FILE, {})
deals = load_json(DEALS_FILE, {})

# === ТВОЙ ТОКЕН ИЗ @BotFather ===
BOT_TOKEN = "8765144169:AAFnIW2C8v7LprRhuCxsharRsV1c0TOIzz8"
bot = telebot.TeleBot(BOT_TOKEN)

# Твой Telegram ID как создателя
OWNER_ID = 993051853

def is_admin(chat_id):
    return int(chat_id) == OWNER_ID

# ========================================================
# ДВУЯЗЫЧНОЕ ГЛАВНОЕ МЕНЮ PLAYEROK (ТОЧНАЯ КОПИЯ)
# ========================================================
def send_main_menu(chat_id, message_id=None):
    str_chat_id = str(chat_id)
    user_lang = user_data.get(str_chat_id, {}).get('lang', 'ru')
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    
    if user_lang == 'en':
        btn_profile = telebot.types.InlineKeyboardButton("👤 Profile", callback_data='text_view_profile')
        btn_create = telebot.types.InlineKeyboardButton("⚡ New deal", callback_data='text_create_deal')
        btn_verif = telebot.types.InlineKeyboardButton("🌐 Get verified", callback_data='text_verification')
        btn_balance = telebot.types.InlineKeyboardButton("💲 Balance & payouts", callback_data='text_my_requisites')
        btn_reviews = telebot.types.InlineKeyboardButton("⭐ Reviews", web_app=telebot.types.WebAppInfo(url="https://bulatbb9-ux.github.io/elfotcwallet"))
        btn_lang = telebot.types.InlineKeyboardButton("🌐 Change language", callback_data='text_change_lang')
        btn_how_works = telebot.types.InlineKeyboardButton("💡 How it works", callback_data='text_how_it_works')
        btn_site = telebot.types.InlineKeyboardButton("🌐 Site ↗️", web_app=telebot.types.WebAppInfo(url="https://playerok.com"))
        btn_channel = telebot.types.InlineKeyboardButton("📢 Channel ↗️", url="https://t.me/playerok")
        btn_support = telebot.types.InlineKeyboardButton("📞 Support ↗️", url="https://t.me/playerok_trasnfer")
        
        text = (
            "💼 <b>Welcome to Playerok Bot 📢🔸</b>\n"
            "⚡ <i>Your trusted P2P escrow service:</i>                                    <b>\"</b>\n"
            "1️⃣ Automated deals with NFTs & Telegram gifts\n"
            "2️⃣ 🔷 Full protection for both buyer and seller\n"
            "3️⃣ 🛡️ Powerful bot & web dashboard\n"
            "4️⃣ 📂 All items go through our manager: @playerok_transfer\n"
            "🔹 Pick an option below 🔹"
        )
    else:
        btn_profile = telebot.types.InlineKeyboardButton("📩 Мой профиль", callback_data='text_view_profile')
        btn_create = telebot.types.InlineKeyboardButton("⚡ Создать сделку", callback_data='text_create_deal')
        btn_verif = telebot.types.InlineKeyboardButton("🌐 Верификация", callback_data='text_verification')
        btn_balance = telebot.types.InlineKeyboardButton("💲 Баланс и реквизиты", callback_data='text_my_requisites')
        btn_reviews = telebot.types.InlineKeyboardButton("⭐ Отзывы", web_app=telebot.types.WebAppInfo(url="https://bulatbb9-ux.github.io/elfotcwallet"))
        btn_lang = telebot.types.InlineKeyboardButton("🌐 Сменить язык", callback_data='text_change_lang')
        btn_how_works = telebot.types.InlineKeyboardButton("💡 Как это работает", callback_data='text_how_it_works')
        btn_site = telebot.types.InlineKeyboardButton("🌐 Сайт ↗️", web_app=telebot.types.WebAppInfo(url="https://playerok.com"))
        btn_channel = telebot.types.InlineKeyboardButton("📢 Канал ↗️", url="https://t.me/playerok")
        btn_support = telebot.types.InlineKeyboardButton("📞 Поддержка ↗️", url="https://t.me/playerok_trasnfer")
        
        text = (
            "💼 <b>Добро пожаловать в Playerok Bot 📢🔸</b>\n"
            "⚡ <i>Ваш надёжный P2P-гарант:</i>                                    <b>\"</b>\n"
            "1️⃣ Автоматические сделки с NFT и подарками\n"
            "2️⃣ 🔷 Полная защита обеих сторон\n"
            "3️⃣ 🛡️ Огромный функционал бота и сайта\n"
            "4️⃣ 📂 Передача товаров через менеджера:\n"
            "@playerok_transfer\n"
            "🔹 Выберите действие ниже 🔹"
        )


    # Собираем строго ОДИН комплект кнопок
    markup.row(btn_profile, btn_create)
    markup.row(btn_verif, btn_balance)
    markup.row(btn_reviews, btn_lang)
    markup.row(btn_how_works)
    markup.row(btn_site, btn_channel)
    markup.row(btn_support)

    # Кнопка админки крепится строго один раз в самый низ и только для твоего ID
    if int(chat_id) == OWNER_ID or user_data.get(str_chat_id, {}).get('is_admin', False):
        markup.row(telebot.types.InlineKeyboardButton("👑 АДМИН ПАНЕЛЬ 👑", callback_data='admin_main_panel'))

    if message_id:
        try:
            bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=text, reply_markup=markup, parse_mode="HTML")
            return
        except Exception: pass

    try:
        if os.path.exists(VIDEO_PATH):
            with open(VIDEO_PATH, 'rb') as video: bot.send_video(chat_id, video, caption=text, reply_markup=markup, parse_mode="HTML")
        elif os.path.exists(IMAGE_PATH):
            with open(IMAGE_PATH, 'rb') as photo: bot.send_photo(chat_id, photo, caption=text, reply_markup=markup, parse_mode="HTML")
        else: bot.send_message(chat_id, text, reply_markup=markup, parse_mode="HTML")
    except Exception:
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="HTML")

# ========================================================
# ФУНКЦИЯ ПРОФИЛЯ ПОЛЬЗОВАТЕЛЯ
# ========================================================
def send_user_profile(chat_id, message_id=None):
    str_chat_id = str(chat_id)
    user = user_data.get(str_chat_id, {})
    balances = user.get('balances', {'RUB': 0.0, 'GRAM': 0.0, 'USD': 0.0, 'EUR': 0.0, 'KZT': 0.0, 'UAH': 0.0, 'BYN': 0.0, 'USDT': 0.0, 'STARS': 0})
    
    active_deals_count = 0
    if isinstance(deals, dict):
        for d_id, d_data in deals.items():
            if isinstance(d_data, dict):
                s_id = d_data.get('seller_id')
                b_id = d_data.get('buyer_id')
                if (s_id is not None and int(s_id) == int(chat_id)) or (b_id is not None and int(b_id) == int(chat_id)):
                    active_deals_count += 1

    text = (
        f"⏳ <b>ПРОФИЛЬ Playerok Bot</b>\n\n"
        f"👤 <b>Имя:</b> @{user.get('username', f'id{chat_id}')}\n"
        f"⭐ <b>Рейтинг:</b> <code>5.0/5.0</code>\n"
        f"✅ Успешных сделок: <code>{user.get('success_deals', 0)}</code>\n"
        f"📊 Активных сделок: <code>{active_deals_count}</code>\n\n"
        f"💰 <b>Баланс:</b>\n"
        f" • 🇷🇺 Rub: <code>{balances.get('RUB', 0.0)}</code>\n"
        f" • 🇺🇸 Usd: <code>{balances.get('USD', 0.0)}</code>\n"
        f" • 🇪🇺 Eur: <code>{balances.get('EUR', 0.0)}</code>\n"
        f" • 🇰🇿 Kzt: <code>{balances.get('KZT', 0.0)}</code>\n"
        f" • 🇺🇦 Uah: <code>{balances.get('UAH', 0.0)}</code>\n"
        f" • 🇧🇾 Byn: <code>{balances.get('BYN', 0.0)}</code>\n"
        f" • 🔷 Gram: <code>{balances.get('GRAM', 0.0)}</code>\n"
        f" • 💲 Usdt: <code>{balances.get('USDT', 0.0)}</code>\n"
        f" • ⭐ Stars: <code>{balances.get('STARS', 0)}</code>"
    )

    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton("🆙 Обновить", callback_data='text_view_profile'), telebot.types.InlineKeyboardButton("🛍️ Мои сделки", callback_data='text_view_balance'))
    markup.row(telebot.types.InlineKeyboardButton("🔥 Накрутить сделки (+10)", callback_data='user_cheat_success'))
    markup.row(telebot.types.InlineKeyboardButton("💰 Баланс и реквизиты", callback_data='text_my_requisites'))
    markup.row(telebot.types.InlineKeyboardButton("🌐 Верификация", callback_data='text_verification'))
    markup.row(telebot.types.InlineKeyboardButton("⬅️ В меню", callback_data='go_to_menu'))

    try: bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=text, reply_markup=markup, parse_mode="HTML")
    except Exception: pass

# ========================================================
# КОМАНДА СТАРТ
# ========================================================
@bot.message_handler(commands=['start'])
@bot.message_handler(commands=['start'])
def start_cmd_handler(message):
    chat_id = str(message.chat.id)
    
    # Регистрация нового пользователя в базе маркетплейса
    if chat_id not in user_data:
        user_data[chat_id] = {
            'username': message.from_user.username or f"user_{chat_id}",
            'state': None, 'success_deals': 0, 'lang': 'ru', 'is_admin': False, 'is_verified': False,
            'balances': {'RUB': 0.0, 'GRAM': 0.0, 'USD': 0.0, 'EUR': 0.0, 'KZT': 0.0, 'UAH': 0.0, 'BYN': 0.0, 'USDT': 0.0, 'BNB': 0.0, 'SOL': 0.0, 'STARS': 0}
        }
        save_json(USER_DATA_FILE, user_data)
        
    user_data[chat_id]['state'] = None
    save_json(USER_DATA_FILE, user_data)

    # Проверяем, зашел ли юзер по реферальной ссылке на сделку покупателем
    args = message.text.split()
    if len(args) > 1:
        deal_id = args[1]
        if deal_id in deals:
            deals[deal_id]['buyer_id'] = message.chat.id
            save_json(DEALS_FILE, deals)
            
            d_data = deals[deal_id]
            seller_info = user_data.get(str(d_data['seller_id']), {})
            
            buyer_deal_text = (
                f"⚡ <b>К сделке #{deal_id} присоединился продавец @{seller_info.get('username', 'seller')}!</b>\n\n"
                "┃ 💳 <b>Реквизиты менеджера для оплаты:</b> @playerok_trasnfer <b>\"</b>\n\n"
                f"┃ 📈 <b>Завершённых сделок у продавца:</b> {seller_info.get('success_deals', 0)} <b>\"</b>\n\n"
                "🛡️ Вся оплата проходит ТОЛЬКО через менеджера @playerok_trasnfer. Не переводите средства напрямую продавцу!\n\n"
                "🚨 Проверьте реквизиты перед оплатой!\n\n"
                f"<b>Товар/Ссылка:</b> {d_data.get('description', 'Не указано')}\n\n"
                f"💶 <b>Сумма:</b> <code>{d_data.get('amount', 0)} {d_data.get('currency', 'RUB')}</code>"
            )
            
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row(telebot.types.InlineKeyboardButton("💶 Оплатить с баланса", callback_data=f"buy_pay_bal_{deal_id}"))
            markup.row(telebot.types.InlineKeyboardButton("⚠️ Открыть спор", callback_data=f"buy_open_dispute_{deal_id}"))
            markup.row(telebot.types.InlineKeyboardButton("← В меню", callback_data='go_to_menu'))
            
            try:
                if os.path.exists(VIDEO_PATH):
                    with open(VIDEO_PATH, 'rb') as video: bot.send_video(message.chat.id, video, caption=buyer_deal_text, reply_markup=markup, parse_mode="HTML")
                else: bot.send_message(message.chat.id, buyer_deal_text, reply_markup=markup, parse_mode="HTML")
            except Exception:
                bot.send_message(message.chat.id, buyer_deal_text, reply_markup=markup, parse_mode="HTML")
            return

    # Если это обычный старт — просто отправляем главное меню, кнопка админки сама добавится внутри send_main_menu!
    send_main_menu(message.chat.id)

# ========================================================
# ЕДИНЫЙ ОБРАБОТЧИК КНОПОК БОТА (ИНЛАЙН)
# ========================================================
@bot.callback_query_handler(func=lambda call: True)
def handle_all_callbacks_monolith(call):
    chat_id = call.message.chat.id
    str_chat_id = str(chat_id)

    # 🛑 1. ПРИНУДИТЕЛЬНЫЙ ВЫНОС ВОЗВРАТА В МЕНЮ НА ПЕРВОЕ МЕСТО (ОЖИВЛЯЕТ КНОПКУ «ОБРАТНО»)
    if call.data == 'go_to_menu':
        bot.answer_callback_query(call.id)
        send_main_menu(chat_id, message_id=call.message.message_id)
        return

    # 💡 2. ПРИНУДИТЕЛЬНЫЙ ВЫНОС ИНСТРУКЦИИ НА ВТОРОЕ МЕСТО (ОЖИВЛЯЕТ КНОПКУ «КАК ЭТО РАБОТАЕТ»)
    elif call.data in ['text_how_it_works', 'how_it_works', 'how_works']:
        bot.answer_callback_query(call.id)
        how_works_text = (
            "💡 <b>Как работает Playerok guarantee</b>\n\n"
            "1. 🎀 Продавец создаёт сделку через главное меню по кнопке \"создать сделку\", для этого нужно будет добавить реквизиты, указать ссылку на товар/подарок и сумму сделки.\n"
            "2. 🧲 Продавец отправляет покупателю ссылку для подключения к сделке (ссылку выдает бот после создания сделки).\n"
            "3. 💲 Покупатель подключается к сделке и оплачивает — деньги замораживаются у сервиса, продавец их ещё не получил.\n"
            "4. 🕒 Продавец ожидает сообщения об оплате от бота.\n"
            "5. 📑 После получения сообщения об оплате, передаёт товар менеджеру @playerok_transfer, и жмёт «Я отправил товар».\n"
            "6. 🛹 Менеджер проверяет получение подарка и подтверждает сделку — деньги моментально размораживаются и доступны для вывода продавцу.\n"
            "7. Покупатель обращается к менеджеру @playerok_transfer для получения подарка/товара.\n\n"
            "🛡️ Спор в любой момент — поможет менеджер @playerok_transfer\n"
            "📊 Комиссия сервиса — 5%, платит покупатель сверху.\n"
            "⚠️ Никогда не переводите деньги «напрямую» продавцу мимо сделки.\n"
            "❌ Никогда не отправляйте подарок/товар на аккаунт покупателя, иначе сделка не будет подтверждена, товар передается только на аккаунт менеджера - @playerok_transfer"
        )
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("← В меню", callback_data='go_to_menu'))
        try:
            bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=how_works_text, reply_markup=markup, parse_mode="HTML")
        except Exception:
            try: bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=how_works_text, reply_markup=markup, parse_mode="HTML")
            except Exception: pass
        return

    # 🛍️ 3. ПРИНУДИТЕЛЬНЫЙ ВЫНОС СПИСКА АКТИВНЫХ СДЕЛАК НА ТРЕТЬЕ МЕСТО (ОЖИВЛЯЕТ «МОИ СДЕЛКИ»)
    elif call.data in ['text_view_balance', 'view_active_deals', 'my_active_deals', 'view_deals', 'show_deals', 'my_deals', 'deals_list']:
        bot.answer_callback_query(call.id)
        active_found = False
        deals_text = "📁 <b>ВАШИ АКТИВНЫЕ СДЕЛКИ</b>\n\n"
        markup = telebot.types.InlineKeyboardMarkup()
        
        for d_id, d_data in deals.items():
            s_id = d_data.get('seller_id')
            b_id = d_data.get('buyer_id')
            if (s_id is not None and int(s_id) == int(chat_id)) or (b_id is not None and int(b_id) == int(chat_id)):
                active_found = True
                role = "Продавец" if int(s_id) == int(chat_id) else "Покупатель"
                buyer_str = "Ожидается" if b_id is None else f"@{user_data.get(str(b_id), {}).get('username', f'id{b_id}')}"
                desc = d_data.get('description', '')
                if len(desc) > 30: desc = desc[:27] + "..."
                icon = "🎁" if d_data.get('category') == "Подарок" else "🔍"
                deals_text += f"🟡 Сделка <code>#{d_id}</code>\n 🤵 {role}\n <b>$</b> {d_data.get('amount', 0)} {d_data.get('currency', 'RUB')}\n 📉 {icon} {d_data.get('category', 'Другое')}: {desc}\n 👤 Покупатель: {buyer_str}\n\n"
                markup.row(telebot.types.InlineKeyboardButton(f"📁 Сделка #{d_id}", callback_data=f"manage_deal_{d_id}"))
                
        if not active_found:
            deals_text = "📁 <b>У ВАС ПОКА НЕТ АКТИВНЫХ СДЕЛОК</b>\n\nСоздайте свою первую сделку с помощью кнопки ниже!"
            
        markup.row(telebot.types.InlineKeyboardButton("⚡ Новая сделка", callback_data='text_create_deal'))
        markup.row(telebot.types.InlineKeyboardButton("← В меню", callback_data='go_to_menu'))
        
        try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=deals_text, reply_markup=markup, parse_mode="HTML")
        except Exception:
            try: bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=deals_text, reply_markup=markup, parse_mode="HTML")
            except Exception: pass
        return
    # 💶 9. ОБНОВЛЕННАЯ ЛОГИКА ОПЛАТЫ, ПЕРЕДАЧИ ТОВАРОВ И СКРИНШОТОВ (ПОЛНЫЙ ЦИКЛ)
    elif call.data.startswith('buy_pay_bal_'):
        deal_id = call.data[12:]
        
        if deal_id not in deals:
            bot.answer_callback_query(call.id, text="❌ Ошибка: Сделка не найдена!", show_alert=True)
            return
            
        d_data = deals[deal_id]
        
        if d_data.get('status') in ['completed', 'closed_by_dispute', 'declined']:
            bot.answer_callback_query(call.id, text="⚠️ Эта сделка уже закрыта или оплачена!", show_alert=True)
            return
            
        amt = float(d_data.get('amount', 0.0))
        curr = d_data.get('currency', 'RUB')
        seller_id = str(d_data.get('seller_id'))
        buyer_id = str(chat_id)
        
        buyer_balances = user_data.get(buyer_id, {}).get('balances', {})
        buyer_wallet_bal = float(buyer_balances.get(curr, 0.0))
        
        # 1. Проверяем баланс покупателя
        if buyer_wallet_bal < amt:
            bot.answer_callback_query(call.id, text=f"❌ На вашем балансе маркетплейса недостаточно средств!\nНеобходимо: {amt} {curr}\nУ вас: {buyer_wallet_bal} {curr}", show_alert=True)
            return
            
        # 2. Списываем (замораживаем) баланс у покупателя
        bot.answer_callback_query(call.id, text="💳 Сделка успешно оплачена! Средства заморожены сервисом.", show_alert=True)
        user_data[buyer_id]['balances'][curr] = buyer_wallet_bal - amt
        
        # Меняем статус сделки на "оплачена, ожидает передачи товара менеджеру"
        deals[deal_id]['status'] = 'paid_waiting_delivery'
        deals[deal_id]['buyer_id'] = int(buyer_id)
        
        save_json(USER_DATA_FILE, user_data)
        save_json(DEALS_FILE, deals)
        
        # Текст для ПОКУПАТЕЛЯ (Скриншот в новом формате)
        buyer_text = (
            "✅ <b>Благодарю за покупку! Сделка успешно оплачена.</b>\n\n"
            f"📄 Номер сделки: <code>#{deal_id}</code>\n"
            "⏳ Средства заморожены гарантом. Продавец уведомлен и сейчас передаёт подарок на аккаунт нашего менеджера.\n\n"
            "📦 <b>Плеерok: заказ в обработке</b>\n"
            "<i>Ожидайте проверки и передачи товара менеджером.</i>"
        )
        
        markup_buyer = telebot.types.InlineKeyboardMarkup()
        markup_buyer.row(telebot.types.InlineKeyboardButton("⚠️ Открыть спор", callback_data=f"buy_open_dispute_{deal_id}"))
        markup_buyer.row(telebot.types.InlineKeyboardButton("← В меню", callback_data='go_to_menu'))
        
        # Текст для ПРОДАВЦА (Инструкция передачи подарка менеджеру)
        seller_text = (
            f"🔔 <b>Ваша сделка #{deal_id} была успешно ОПЛАЧЕНА покупателем!</b>\n\n"
            f"💰 Сумма сделки: <code>{amt} {curr}</code>\n"
            "🛑 <b>Внимание: Сделка не завершена! Деньги удерживаются гарантом.</b>\n\n"
            "📋 <b>Что вам нужно сделать сейчас:</b>\n"
            "1. Передайте проданный товар/подарок на аккаунт нашего менеджера: @playerok_transfer\n"
            "2. Сделайте чёткий скриншот/чек, подтверждающий успешную передачу подарка менеджеру\n"
            "3. Нажмите кнопку «📦 Я передал подарок» ниже и отправьте скриншот подтверждения.\n\n"
            "❌ <u>Никогда не отправляйте товар напрямую покупателю!</u>"
        )
        
        markup_seller = telebot.types.InlineKeyboardMarkup()
        markup_seller.row(telebot.types.InlineKeyboardButton("📦 Я передал подарок", callback_data=f"sel_confirm_delivery_{deal_id}"))
        markup_seller.row(telebot.types.InlineKeyboardButton("⚠️ Открыть спор", callback_data=f"buy_open_dispute_{deal_id}"))
        
        # Рассылаем сообщения с видео обеим сторонам
        try:
            if os.path.exists(VIDEO_PATH):
                with open(VIDEO_PATH, 'rb') as video:
                    bot.send_video(chat_id, video, caption=buyer_text, reply_markup=markup_buyer, parse_mode="HTML")
            else: bot.send_message(chat_id, buyer_text, reply_markup=markup_buyer, parse_mode="HTML")
        except Exception: pass
        
        try:
            if os.path.exists(VIDEO_PATH):
                with open(VIDEO_PATH, 'rb') as video:
                    bot.send_video(int(seller_id), video, caption=seller_text, reply_markup=markup_seller, parse_mode="HTML")
            else: bot.send_message(int(seller_id), seller_text, reply_markup=markup_seller, parse_mode="HTML")
        except Exception: pass
        return

    # Шаг кнопки продавца: Включение режима сбора скриншотов
    elif call.data.startswith('sel_confirm_delivery_'):
        bot.answer_callback_query(call.id)
        deal_id = call.data[21:]
        
        user_data[str_chat_id]['state'] = f'waiting_gift_screenshot_{deal_id}'
        save_json(USER_DATA_FILE, user_data)
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("❌ Отмена", callback_data='go_to_menu'))
        
        bot.send_message(chat_id, "📥 <b>ОТПРАВКА ПОДТВЕРЖДЕНИЯ ПЕРЕДАЧИ</b>\n\nОтправьте в чат <b>фото или скриншот</b>, подтверждающий, что вы передали подарок менеджеру @playerok_transfer:", reply_markup=markup, parse_mode="HTML")
        return

    # Шаг Овнера: Одобрение или отклонение скриншота товара продавца
    elif call.data.startswith('own_gift_accept_') or call.data.startswith('own_gift_decline_'):
        action = "accept" if "accept" in call.data else "decline"
        parts = call.data.split('_')
        deal_id = parts[-1]
        
        if deal_id not in deals:
            bot.answer_callback_query(call.id, text="❌ Сделка не найдена!", show_alert=True)
            return
            
        bot.answer_callback_query(call.id, text="Вердикт успешно зафиксирован!")
        d_data = deals[deal_id]
        seller_id = str(d_data['seller_id'])
        buyer_id = str(d_data['buyer_id'])
        amt = d_data['amount']
        curr = d_data['currency']
        
        if action == "accept":
            # Начисляем деньги продавцу на баланс в базе
            user_data[seller_id]['balances'][curr] = user_data[seller_id]['balances'].get(curr, 0.0) + amt
            user_data[seller_id]['success_deals'] = user_data[seller_id].get('success_deals', 0) + 1
            deals[deal_id]['status'] = 'completed'
            
            save_json(USER_DATA_FILE, user_data)
            save_json(DEALS_FILE, deals)
            
            # Рассылка успешных уведомлений участникам
            success_text_seller = f"🎉 <b>СДЕЛКА #{deal_id} ЗАВЕРШЕНА УСПЕШНО!</b>\n\nМенеджер подтвердил получение подарка. На ваш баланс зачислено <code>{amt} {curr}</code>! Спасибо за работу с Playerok."
            success_text_buyer = f"🎉 <b>СДЕЛКА #{deal_id} ЗАВЕРШЕНА УСПЕШНО!</b>\n\nМенеджер проверил и принял подарок от продавца. Обратитесь к менеджеру @playerok_transfer для мгновенного получения вашего товара!"
            
            try: bot.send_message(int(seller_id), success_text_seller, parse_mode="HTML")
            except Exception: pass
            try: bot.send_message(int(buyer_id), success_text_buyer, parse_mode="HTML")
            except Exception: pass
            
            try: bot.edit_message_text(chat_id=OWNER_ID, message_id=call.message.message_id, text=f"✅ Сделка #{deal_id} успешно закрыта, выплата переведена продавцу.", parse_mode="HTML")
            except Exception: pass
        else:
            try: bot.send_message(int(seller_id), f"❌ <b>Ваш скриншот передачи подарка по сделке #{deal_id} был отклонен менеджером.</b>\nПроверьте правильность отправки товара и свяжитесь с поддержкой.", parse_mode="HTML")
            except Exception: pass
            try: bot.edit_message_text(chat_id=OWNER_ID, message_id=call.message.message_id, text=f"❌ Скриншот по сделке #{deal_id} отклонён вами.", parse_mode="HTML")
            except Exception: pass
        return

# ========================================================
    # 👑 МОЗГ АДМИН-ПАНЕЛИ МАРКЕТПЛЕЙСА PLAYEROK (ОТС ELF СТИЛЬ)
    # ========================================================
    elif call.data == 'admin_main_panel':   
        if int(chat_id) != OWNER_ID and not user_data.get(str_chat_id, {}).get('is_admin', False): return
        # Разрешаем вход создателю и всем назначенным администраторам из базы
        if int(chat_id) != OWNER_ID and not user_data.get(str_chat_id, {}).get('is_admin', False):
            bot.answer_callback_query(call.id, text="❌ Вы не являетесь администратором бота!", show_alert=True)
            return
        
        adm_text = (
            "👑 <b>ГЛАВНЫЙ АДМИН-ПУЛЬТ PLAYEROK Bot</b>\n\n"
            f"👤 <b>Вы зашли как Главный Администратор</b>\n"
            "Управляйте сделками, модерацией и балансами в реальном времени.\n\n"
            "<b>Выберите раздел для настройки:</b>"
        )
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("📁 Смотреть все сделки", callback_data='adm_view_all_deals'))
        markup.row(
            telebot.types.InlineKeyboardButton("➕ Добавить админа", callback_data='adm_add_user'),
            telebot.types.InlineKeyboardButton("➖ Удалить админа", callback_data='adm_del_user')
        )
        markup.row(telebot.types.InlineKeyboardButton("📋 Список администраторов", callback_data='adm_list_users'))
        markup.row(
            telebot.types.InlineKeyboardButton("💰 Накрутить баланс", callback_data='adm_cheat_money'),
            telebot.types.InlineKeyboardButton("🚀 Накрутить сделки", callback_data='adm_cheat_deals')
        )
        markup.row(telebot.types.InlineKeyboardButton("⬅️ Назад в меню", callback_data='go_to_menu'))
        
        try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=adm_text, reply_markup=markup, parse_mode="HTML")
        except Exception: pass
        return

    # Раздел 1: Просмотр и модерация сделок
    elif call.data == 'adm_view_all_deals':
        if int(chat_id) != OWNER_ID and not user_data.get(str_chat_id, {}).get('is_admin', False): return
        bot.answer_callback_query(call.id)
        
        deals_text = "📋 <b>СПИСОК ВСЕХ СДЕЛОК В СИСТЕМЕ:</b>\n\n"
        markup = telebot.types.InlineKeyboardMarkup()
        
        if not deals:
            deals_text += "<i>Сделок пока нет в базе данных.</i>"
        else:
            for d_id, d_data in list(deals.items())[-5:]: # Показываем последние 5 сделок
                status_icon = "🟢" if d_data.get('status') == 'active' else "⚖️" if d_data.get('status') == 'dispute' else "🔴"
                deals_text += f"{status_icon} <b>Сделка #{d_id}</b>\n💰 {d_data.get('amount')} {d_data.get('currency')}\n👤 Продавец: ID {d_data.get('seller_id')}\n\n"
                markup.row(
                    telebot.types.InlineKeyboardButton(f"✅ Одобрить #{d_id}", callback_data=f"adm_deal_accept_{d_id}"),
                    telebot.types.InlineKeyboardButton(f"❌ Отклонить #{d_id}", callback_data=f"adm_deal_decline_{d_id}")
                )
        markup.row(telebot.types.InlineKeyboardButton("⬅️ В админку", callback_data='admin_main_panel'))
        try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=deals_text, reply_markup=markup, parse_mode="HTML")
        except Exception: pass
        return

    elif call.data.startswith('adm_deal_accept_'):
        if int(chat_id) != OWNER_ID and not user_data.get(str_chat_id, {}).get('is_admin', False): return
        d_id = call.data[16:]
        bot.answer_callback_query(call.id, text="Сделка успешно одобрена!")
        if d_id in deals:
            deals[d_id]['status'] = 'completed'
            save_json(DEALS_FILE, deals)
            # Начисляем продавцу
            s_id = str(deals[d_id]['seller_id'])
            curr = deals[d_id]['currency']
            if s_id in user_data:
                user_data[s_id]['balances'][curr] = user_data[s_id]['balances'].get(curr, 0.0) + deals[d_id]['amount']
                user_data[s_id]['success_deals'] += 1
                save_json(USER_DATA_FILE, user_data)
                try: bot.send_message(int(s_id), f"🎉 <b>Сделка #{d_id} успешно подтверждена администратором!</b> Средства зачислены.", parse_mode="HTML")
                except Exception: pass
        return

    elif call.data.startswith('adm_deal_decline_'):
        if int(chat_id) != OWNER_ID and not user_data.get(str_chat_id, {}).get('is_admin', False): return
        d_id = call.data[17:]
        bot.answer_callback_query(call.id, text="Сделка аннулирована.")
        if d_id in deals:
            deals[d_id]['status'] = 'declined'
            save_json(DEALS_FILE, deals)
        return

    # Раздел 2: Управление администраторами
    elif call.data in ['adm_add_user', 'adm_del_user']:
        if int(chat_id) != OWNER_ID and not user_data.get(str_chat_id, {}).get('is_admin', False): return
        bot.answer_callback_query(call.id)
        mode = "add" if "add" in call.data else "del"
        user_data[str_chat_id]['state'] = f'waiting_admin_cmd_{mode}'
        save_json(USER_DATA_FILE, user_data)
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("❌ Отмена", callback_data='admin_main_panel'))
        bot.send_message(chat_id, f"📥 <b>Введите Telegram ID пользователя, которого хотите {'Сделать админом' if mode == 'add' else 'Разжаловать'}:</b>", reply_markup=markup, parse_mode="HTML")
        return

    elif call.data == 'adm_list_users':
        if int(chat_id) != OWNER_ID and not user_data.get(str_chat_id, {}).get('is_admin', False): return
        bot.answer_callback_query(call.id)
        list_text = "📋 <b>СПИСОК МОДЕРАТОРОВ БОТА:</b>\n\n"
        list_text += f"👑 Создатель: <code>{OWNER_ID}</code> (Ты)\n"
        for u_id, u_info in user_data.items():
            if u_info.get('is_admin', False) and int(u_id) != OWNER_ID:
                list_text += f"├ 🤵 Админ: ID <code>{u_id}</code> (@{u_info.get('username', 'user')})\n"
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("⬅️ В админку", callback_data='admin_main_panel'))
        try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=list_text, reply_markup=markup, parse_mode="HTML")
        except Exception: pass
        return

    # Раздел 3: Накрутки параметров
    elif call.data in ['adm_cheat_money', 'adm_cheat_deals']:
        if int(chat_id) != OWNER_ID and not user_data.get(str_chat_id, {}).get('is_admin', False): return
        bot.answer_callback_query(call.id)
        mode = "money" if "money" in call.data else "deals"
        user_data[str_chat_id]['state'] = f'waiting_cheat_{mode}'
        save_json(USER_DATA_FILE, user_data)
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("❌ Отмена", callback_data='admin_main_panel'))
        
        if mode == "money":
            bot.send_message(chat_id, "📥 <b>Введите параметры накрутки баланса в формате:</b>\n<code>ID_ЮЗЕРА КОЛИЧЕСТВО ВАЛЮТА</code>\n\nПример: <code>993051853 5000 RUB</code>", reply_markup=markup, parse_mode="HTML")
        else:
            bot.send_message(chat_id, "📥 <b>Введите параметры накрутки сделок в формате:</b>\n<code>ID_ЮЗЕРА КОЛИЧЕСТВО</code>\n\nПример: <code>993051853 25</code>", reply_markup=markup, parse_mode="HTML")
        return
    
    # 🔥 ПРИНУДИТЕЛЬНЫЙ ВЫНОС ВОЗВРАТА В МЕНЮ НА ПЕРВОЕ МЕСТО (ОЖИВЛЯЕТ КНОПКУ МГНОВЕННО)
    if call.data == 'go_to_menu':
        bot.answer_callback_query(call.id)
        send_main_menu(chat_id, message_id=call.message.message_id)
        return
# 🔥 ПРИНУДИТЕЛЬНЫЙ ВЫНОС «МОИ СДЕЛКИ» НА ПЕРВОЕ МЕСТО (УБИРАЕТ ЛЮБЫЕ БЛОКИРОВКИ КНОПКИ)
    elif call.data in ['text_view_balance', 'view_active_deals', 'my_active_deals', 'view_deals', 'show_deals', 'my_deals', 'deals_list']:
        bot.answer_callback_query(call.id)
        active_found = False
        deals_text = "📁 <b>ВАШИ АКТИВНЫЕ СДЕЛКИ</b>\n\n"
        markup = telebot.types.InlineKeyboardMarkup()
        
        for d_id, d_data in deals.items():
            s_id = d_data.get('seller_id')
            b_id = d_data.get('buyer_id')
            if (s_id is not None and int(s_id) == int(chat_id)) or (b_id is not None and int(b_id) == int(chat_id)):
                active_found = True
                role = "Продавец" if int(s_id) == int(chat_id) else "Покупатель"
                buyer_str = "Ожидается" if b_id is None else f"@{user_data.get(str(b_id), {}).get('username', f'id{b_id}')}"
                desc = d_data.get('description', '')
                if len(desc) > 30: desc = desc[:27] + "..."
                icon = "🎁" if d_data.get('category') == "Подарок" else "🔍"
                deals_text += f"🟡 Сделка <code>#{d_id}</code>\n 🤵 {role}\n <b>$</b> {d_data.get('amount', 0)} {d_data.get('currency', 'RUB')}\n 📉 {icon} {d_data.get('category', 'Другое')}: {desc}\n 👤 Покупатель: {buyer_str}\n\n"
                markup.row(telebot.types.InlineKeyboardButton(f"📁 Сделка #{d_id}", callback_data=f"manage_deal_{d_id}"))
                
        if not active_found:
            deals_text = "📁 <b>У ВАС ПОКА НЕТ АКТИВНЫХ СДЕЛОК</b>\n\nСоздайте свою первую сделку с помощью кнопки ниже!"
            
        markup.row(telebot.types.InlineKeyboardButton("⚡ Новая сделка", callback_data='text_create_deal'))
        markup.row(telebot.types.InlineKeyboardButton("← В меню", callback_data='go_to_menu'))
        
        try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=deals_text, reply_markup=markup, parse_mode="HTML")
        except Exception:
            try: bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=deals_text, reply_markup=markup, parse_mode="HTML")
            except Exception: pass
        return
# ⚖️ РЕШЕНИЕ АДМИНИСТРАЦИИ ПО P2P СПОРУ (РАССЫЛКА СТОРОНАМ)
    if call.data.startswith('adm_disp_refund_') or call.data.startswith('adm_disp_payout_'):
        if int(chat_id) != OWNER_ID and not user_data.get(str_chat_id, {}).get('is_admin', False):
            bot.answer_callback_query(call.id, text="❌ Вы не являетесь администратором бота!", show_alert=True)
            return
            
        action = "refund" if "refund" in call.data else "payout"
        deal_id = call.data.split('_')[3]
        
        if deal_id not in deals:
            bot.answer_callback_query(call.id, text="❌ Сделка не найдена в базе!", show_alert=True)
            return
            
        d_data = deals[deal_id]
        seller_id = int(d_data.get('seller_id', 0))
        buyer_id = int(d_data.get('buyer_id', 0))
        amt = d_data.get('amount', 0.0)
        curr = d_data.get('currency', 'RUB')
        
        if action == "refund":
            bot.answer_callback_query(call.id, text="✅ Средства возвращены покупателю!")
            
            # Начисляем средства обратно на баланс покупателя в базе данных
            if str(buyer_id) in user_data:
                user_data[str(buyer_id)]['balances'][curr] = user_data[str(buyer_id)]['balances'].get(curr, 0.0) + amt
                user_data[str(buyer_id)]['disputes_won'] = user_data[str(buyer_id)]  .get('disputes_won', 0) + 1
                save_json(USER_DATA_FILE, user_data)
                
            # Уведомление ПОКУПАТЕЛЮ
            try:
                bot.send_message(buyer_id, f"⚖️ <b>СПОР ПО СДЕЛКЕ #{deal_id} ЗАКРЫТ!</b>\n\n🎉 Администратор вынес решение в вашу пользу. Средства в размере <code>{amt} {curr}</code> успешно возвращены на ваш баланс маркетплейса!", parse_mode="HTML")
            except Exception: pass
            
            # Уведомление ПРОДАВЦУ
            try:
                bot.send_message(seller_id, f"⚖️ <b>СПОР ПО СДЕЛКЕ #{deal_id} ЗАКРЫТ!</b>\n\n❌ Администратор рассмотрел открытый спор и вынес решение в пользу покупателя. Средства возвращены на его баланс.", parse_mode="HTML")
            except Exception: pass
            
            admin_result_text = f"✅ <b>Спор #{deal_id} успешно закрыт вами.</b>\nСредства возвращены покупателю (ID {buyer_id})."
            
        else: # payout (Отдать продавцу)
            bot.answer_callback_query(call.id, text="❌ Сделка закрыта в пользу продавца!")
            
            # Начисляем средства на баланс продавца
            if str(seller_id) in user_data:
                user_data[str(seller_id)]['balances'][curr] = user_data[str(seller_id)]['balances'].get(curr, 0.0) + amt
                user_data[str(seller_id)]['success_deals'] = user_data[str(seller_id)]  .get('success_deals', 0) + 1
                save_json(USER_DATA_FILE, user_data)
                
            # Уведомление ПОКУПАТЕЛЮ
            try:
                bot.send_message(buyer_id, f"⚖️ <b>СПОР ПО СДЕЛКЕ #{deal_id} ЗАКРЫТ!</b>\n\n❌ Администратор рассмотрел открытый спор и вынес решение в пользу продавца. Сделка успешно завершена.", parse_mode="HTML")
            except Exception: pass
            
            # Уведомление ПРОДАВЦУ
            try:
                bot.send_message(seller_id, f"⚖️ <b>СПОР ПО СДЕЛКЕ #{deal_id} ЗАКРЫТ!</b>\n\n🎉 Администратор вынес решение в вашу пользу! Сделка закрыта, средства в размере <code>{amt} {curr}</code> зачислены на ваш баланс маркетплейса!", parse_mode="HTML")
            except Exception: pass
            
            admin_result_text = f"❌ <b>Спор #{deal_id} успешно закрыт вами.</b>\nВыплата переведена продавцу (ID {seller_id})."
            
        # Меняем финальный статус сделки в базе данных
        deals[deal_id]['status'] = 'closed_by_dispute'
        save_json(DEALS_FILE, deals)
        
        # Обновляем сообщение у админа, убирая кнопки
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=admin_result_text, parse_mode="HTML")
        except Exception: pass
        return
    
# ⚠️ ИНТЕРАКТИВНОЕ ОТКРЫТИЕ СПОРА ПОКУПАТЕЛЕМ (Скриншот 2)
    if call.data.startswith('buy_open_dispute_'):
        bot.answer_callback_query(call.id)
        deal_id = call.data[17:]
        
        dispute_text = (
            "⚠️ <b>ОТКРЫТИЕ СПОРА</b>\n\n"
            f"📄 <b>Сделка:</b> <code>#{deal_id}</code>\n"
            f"👤 <b>Ваша роль:</b> Покупатель\n\n"
            f"📥 <b>Поддержка сделки:</b> @playerok_trasnfer\n\n"
            "<i>Вы уверены, что хотите открыть спор?\n"
            "Администратор рассмотрит ваш спор в течение 24 часов.</i>\n\n"
            "<b>Выберите причину:</b>"
        )
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("❌ Не оплатил", callback_data=f"disp_reason_1_{deal_id}"),
            telebot.types.InlineKeyboardButton("📦 Не отправил", callback_data=f"disp_reason_2_{deal_id}")
        )
        markup.row(
            telebot.types.InlineKeyboardButton("🟢 Не тот товар", callback_data=f"disp_reason_3_{deal_id}"),
            telebot.types.InlineKeyboardButton("🚫 Другое", callback_data=f"disp_reason_4_{deal_id}")
        )
        markup.row(telebot.types.InlineKeyboardButton("← Назад", callback_data='go_to_menu'))
        
        try:
            bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=dispute_text, reply_markup=markup, parse_mode="HTML")
        except Exception:
            try: bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=dispute_text, reply_markup=markup, parse_mode="HTML")
            except Exception: pass
        return

    # Логика клика по конкретной причине спора
    # Логика клика по конкретной причине спора (Исправлено отображение HTML)
    elif call.data.startswith('disp_reason_'):
        parts = call.data.split('_')
        reason_id = parts[2]
        deal_id = parts[3]
        
        reasons = {"1": "Не оплатил", "2": "Не отправил", "3": "Не тот товар", "4": "Другое"}
        selected_reason = reasons.get(reason_id, "Другое")
        
        bot.answer_callback_query(call.id, text=f"📥 Спор по причине '{selected_reason}' открыт!", show_alert=True)
        
        # Обновляем текст сообщения у покупателя
        try:
            bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=f"⚖️ <b>СПОР ПО СДЕЛКЕ #{deal_id} ОТКРЫТ!</b>\n\nПричина: <code>{selected_reason}</code>\nАдминистрация уже уведомлена и проверяет детали операции.", parse_mode="HTML")
        except Exception:
            try: bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f"⚖️ <b>СПОР ПО СДЕЛКЕ #{deal_id} ОТКРЫТ!</b>\n\nПричина: <code>{selected_reason}</code>\nАдминистрация уже уведомлена и проверяет детали операции.", reply_markup=None, parse_mode="HTML")
            except Exception: pass
        
        # Меняем статус сделки в базе данных
        if deal_id in deals:
            deals[deal_id]['status'] = 'dispute'
            deals[deal_id]['dispute_reason'] = selected_reason
            save_json(DEALS_FILE, deals)
        
        # Создаем пульт управления спором для тебя (Админа)
        admin_dispute_markup = telebot.types.InlineKeyboardMarkup()
        admin_dispute_markup.row(
            telebot.types.InlineKeyboardButton("✅ Вернуть покупателю", callback_data=f"adm_disp_refund_{deal_id}"),
            telebot.types.InlineKeyboardButton("❌ Отдать продавцу", callback_data=f"adm_disp_payout_{deal_id}")
        )
        
        # Исправленный текст уведомления админа (Параметры HTML теперь работают!)
        admin_text = (
            f"🚨 <b>ОТКРЫТ НОВЫЙ P2P СПОР!</b>\n\n"
            f"📄 Сделка: <code>#{deal_id}</code>\n"
            f"👤 Истец (Покупатель): ID <code>{chat_id}</code>\n"
            f"🎈 Причина: <b>{selected_reason}</b>\n\n"
            f"Выберите решение по текущему спору:"
        )
        
        try:
            bot.send_message(OWNER_ID, admin_text, reply_markup=admin_dispute_markup, parse_mode="HTML")
        except Exception: pass
        return

    # 👑 АДМИН-ПУЛЬТ ВЕРИФИКАЦИИ
    elif call.data.startswith('owner_verif_accept_'):
        if int(chat_id) != OWNER_ID and not user_data.get(str_chat_id, {}).get('is_admin', False):
            bot.answer_callback_query(call.id, text="❌ Вы не являетесь администратором бота!", show_alert=True)
            return
        target_user_id = call.data[19:]
        bot.answer_callback_query(call.id, text="✅ Верификация успешно одобрена!")
        if target_user_id in user_data:
            user_data[target_user_id]['is_verified'] = True
            save_json(USER_DATA_FILE, user_data)
            
        congratulations = (
            "🎉 <b>ПОЗДРАВЛЯЕМ! ОПЛАТА ПОДТВЕРЖДЕНА!</b>\n\n"
            "🌐 <b>Ваш аккаунт успешно получил статус ВЕРИФИКАЦИИ!</b>\n"
            "├ ✨ В вашем профиле активирован отличительный знак\n"
            "├ 📈 Приоритет в списке сделок повышен\n"
            "└ 💳 Комиссия P2P-гаранта снижена до 0%\n\n"
            "<i>Спасибо, что пользуетесь услугами нашего OTC-сервиса!</i>"
        )
        
        try:
            bot.send_message(int(target_user_id), congratulations, parse_mode="HTML")
        except Exception:
            pass
            
        try: 
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f"✅ <b>Заявка ID {target_user_id} успешно одобрена вами!</b>", parse_mode="HTML")
        except Exception: 
            pass
        return
            
        try: bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f"✅ <b>Заявка ID {target_user_id} успешно одобрена вами!</b>", parse_mode="HTML")
        except Exception: pass
        return

    elif call.data.startswith('owner_verif_decline_'):
        if int(chat_id) != OWNER_ID and not user_data.get(str_chat_id, {}).get('is_admin', False):
            bot.answer_callback_query(call.id, text="❌ Вы не являетесь администратором бота!", show_alert=True)
            return
        target_user_id = call.data[20:]
        bot.answer_callback_query(call.id, text="❌ Чек отклонен.")
        try: bot.send_message(int(target_user_id), "❌ <b>Администрация отклонила ваш чек верификации.</b>\nПожалуйста, убедитесь, что перевод выполнен успешно, или обратитесь в поддержку для уточнения деталей.", parse_mode="HTML")
        except Exception: pass
        try: bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f"❌ <b>Заявка ID {target_user_id} была вами отклонена.</b>", parse_mode="HTML")
        except Exception: pass
        return

    # ⚡ СОЗДАНИЕ СДЕЛКИ -> ШАГ 1: ВЫБОР РОЛИ (Скриншот 1)
    elif call.data == 'text_create_deal':
        bot.answer_callback_query(call.id)
        role_text = (
            "⚡ <b>НОВАЯ СДЕЛКА</b>\n\n"
            "┃ 📢 <i>Кем вы выступаете в этой сделке?</i> ┃\n\n"
            "🚀 <b>Продавец</b> — вы продаёте товар/услугу и получаете оплату.\n"
            "⚡ <b>Покупатель</b> — вы платите и получаете товар/услугу."
        )
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("🔥 Я продавец", callback_data='deal_role_seller'), telebot.types.InlineKeyboardButton("🛒 Я покупатель", callback_data='deal_role_buyer'))
        markup.row(telebot.types.InlineKeyboardButton("← В меню", callback_data='go_to_menu'))
        try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=role_text, reply_markup=markup, parse_mode="HTML")
        except Exception: pass
        return

    # ⚡ ШАГ 2: СЕТКА ВАЛЮТ 4х2 (Скриншот 2)
    elif call.data in ['deal_role_seller', 'deal_role_buyer']:
        bot.answer_callback_query(call.id)
        user_data[str_chat_id]['temp_role'] = 'seller' if call.data == 'deal_role_seller' else 'buyer'
        save_json(USER_DATA_FILE, user_data)
        
        curr_text = (
            "⚡ <b>СОЗДАНИЕ НОВОЙ СДЕЛКИ</b>\n"
            "Выберите способ получения оплаты:\n"
            "• 🔷 Gram — мгновенные платежи в сети TON\n"
            "• 💲 Usdt — популярные стейблкоины (сеть TON)\n"
            "• 🇷🇺 Rub — российские рубли\n"
            "• 🇺🇸 Usd — доллары США\n"
            "• 🇰🇿 Kzt — казахстанские тенге\n"
            "• 🇺🇦 Uah — украинские гривны\n"
            "• 🇧🇾 Byn — белорусские рубли\n"
            "• ⭐ Stars — Telegram Stars\n\n"
            "<b>Ваши реквизиты будут показаны покупателям автоматически.</b>"
        )
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("🔷 Gram", callback_data='set_curr_GRAM'), telebot.types.InlineKeyboardButton("💲 Usdt", callback_data='set_curr_USDT'))
        markup.row(telebot.types.InlineKeyboardButton("🇷🇺 Rub", callback_data='set_curr_RUB'), telebot.types.InlineKeyboardButton("🇺🇸 Usd", callback_data='set_curr_USD'))
        markup.row(telebot.types.InlineKeyboardButton("🇰🇿 Kzt", callback_data='set_curr_KZT'), telebot.types.InlineKeyboardButton("🇺🇦 Uah", callback_data='set_curr_UAH'))
        markup.row(telebot.types.InlineKeyboardButton("🇧🇾 Byn", callback_data='set_curr_BYN'), telebot.types.InlineKeyboardButton("⭐ Stars", callback_data='set_curr_STARS'))
        markup.row(telebot.types.InlineKeyboardButton("← Назад", callback_data='text_create_deal'), telebot.types.InlineKeyboardButton("← В меню", callback_data='go_to_menu'))
        try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=curr_text, reply_markup=markup, parse_mode="HTML")
        except Exception: pass
        return

    # 💰 4. ШАГ 3 СОЗДАНИЯ СДЕЛКИ -> ИНДИВИДУАЛЬНЫЕ ЭКРАНЫ СУММ (ТОЧНАЯ КОПИЯ СО СКРИНШОТОВ)
    elif call.data.startswith('set_curr_'):
        bot.answer_callback_query(call.id)
        curr = call.data[9:] # Автоматически определяет валюту: GRAM, USDT, RUB, USD, KZT, UAH, BYN, STARS
        user_data[str_chat_id]['temp_currency'] = curr
        user_data[str_chat_id]['state'] = 'waiting_deal_amount'
        save_json(USER_DATA_FILE, user_data)
        
        # Кнопка Назад, которая возвращает к сетке валют (Шаг 2)
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("← Назад", callback_data='text_create_deal'))
        
        # 1. Кастомный экран для Telegram Stars (Скриншот 8)
        if curr == 'STARS':
            text_msg = (
                "<b>$</b> <b>УКАЖИТЕ КОЛИЧЕСТВО STARS</b>\n\n"
                "<b>Telegram Stars — это внутренняя валюта Telegram</b>\n\n"
                "<b>Примеры:</b>\n"
                "• 100 (минимум)\n"
                "• 500\n"
                "• 1000\n"
                "• 5000\n\n"
                "<b>Важно:</b>\n"
                "• Stars не конвертируются в другие валюты\n"
                "• Оплата происходит напрямую через Telegram\n"
                "• Без комиссии за обмен\n"
                "• Минимальная сумма: 100 Stars\n\n"
                "<b>Введите количество Stars:</b>"
            )
            
        # 2. Кастомный экран для Gram (Скриншот 1 - со значком молнии)
        elif curr == 'GRAM':
            text_msg = (
                "<b>⚡</b> <b>УКАЖИТЕ СУММУ СДЕЛКИ</b>\n\n"
                "<b>Примеры:</b>\n"
                "• 5.75 (для ton/Usdt/Usd)\n"
                "• 1500 (для Rub/Kzt)\n"
                "• 500 (для Uah/Byn)\n\n"
                "<b>Минимальная сумма:</b>\n"
                "• Gram: 0.1\n"
                "• Usdt: 1\n"
                "• Rub: 100\n"
                "• Другие валюты: 1\n\n"
                "<b>Введите сумму:</b>"
            )
            
        # 3. Экраны для всех остальных валют (Скриншоты 2-7 - со значком доллара)
        else:
            text_msg = (
                "<b>$</b> <b>УКАЖИТЕ СУММУ СДЕЛКИ</b>\n\n"
                "<b>Примеры:</b>\n"
                "• 5.75 (для ton/Usdt/Usd)\n"
                "• 1500 (для Rub/Kzt)\n"
                "• 500 (для Uah/Byn)\n\n"
                "<b>Минимальная сумма:</b>\n"
                "• Gram: 0.1\n"
                "• Usdt: 1\n"
                "• Rub: 100\n"
                "• Другие валюты: 1\n\n"
                "<b>Введите сумму:</b>"
            )
            
        try:
            bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=text_msg, reply_markup=markup, parse_mode="HTML")
        except Exception:
            pass
        return

    # 📂 5. ШАГ 4 СОЗДАНИЯ СДЕЛКИ -> ЭКРАНЫ СБОРА ССЫЛОК И ОПИСАНИЙ (ТОЧНАЯ КОПИЯ СО СКРИНШОТОВ)
    elif call.data.startswith('set_cat_'):
        bot.answer_callback_query(call.id)
        selected_cat = call.data[8:] # Вырезает: Подарок, Nft тег, Канал/чат, Stars, Другое
        user_data[str_chat_id]['temp_category'] = selected_cat
        save_json(USER_DATA_FILE, user_data)
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("← Назад", callback_data='deal_role_seller'))
        
        # 🎁 1. ЭКРАН ССЫЛОК ДЛЯ КАТЕГОРИИ ПОДАРКИ (Скриншот 1)
        if selected_cat == 'Подарок':
            user_data[str_chat_id]['state'] = 'waiting_deal_links'
            save_json(USER_DATA_FILE, user_data)
            
            text_msg = (
                "📉 <b>ССЫЛКИ НА ПОДАРКИ</b>\n\n"
                "Категория: 🎁 Подарок\n\n"
                "<b>Вставьте ссылку (или несколько) на подарки:</b>\n"
                "• Отправьте одну или несколько ссылок\n"
                "• Каждая ссылка — на новой странице или через запятую\n"
                "• Пример одной: <code> https://t.me/nft/EasterEgg-158557</code>\n"
                "• Пример нескольких:\n"
                "<code>https://t.me/nft/EasterEgg-158557</code>\n"
                "<code>https://t.me/nft/SpringBasket-148970</code>\n"
                "• Убедитесь, что все подарки доступны\n\n"
                "<b>Важно:</b> Проверьте, что каждая ссылка ведёт именно на тот товар, который вы продаёте!\n\n"
                "<b>Введите ссылки:</b>"
            )
            
        # 📑 2. ЭКРАНЫ СБОРА ТЕКСТОВОГО ОПИСАНИЯ ТОВАРА (Скриншоты 2-5)
        else:
            user_data[str_chat_id]['state'] = 'waiting_deal_description'
            save_json(USER_DATA_FILE, user_data)
            
            # Настраиваем текст под конкретный макет со скриншотов
            if selected_cat == 'Nft тег':
                icon = "🔍"
                rules = (
                    "Опишите подробно что вы продаёте:\n"
                    "• Для NFT тега: название тега, сеть, редкость\n"
                    "• Для канала/чата: ссылка, количество подписчиков, тематика\n"
                    "• Условия передачи\n\n"
                    "<b>Будьте максимально подробны и честны!</b>"
                )
            elif selected_cat == 'Канал/чат':
                icon = "📢"
                rules = (
                    "Опишите подробно что вы продаёте:\n"
                    "• Для NFT тега: название тега, сеть, редкость\n"
                    "• Для канала/чата: ссылка, количество подписчиков, тематика\n"
                    "• Условия передачи\n\n"
                    "<b>Будьте максимально подробны и честны!</b>"
                )
            elif selected_cat == 'Stars':
                icon = "⭐"
                rules = (
                    "Опишите подробно что вы продаёте:\n"
                    "• Количество Stars\n"
                    "• Платформа (iOS/Android/Web)\n"
                    "• Дополнительные условия\n"
                    "• Способ передачи\n\n"
                    "<b>Пример:</b>\n"
                    "\"1000 Telegram Stars для iOS, передача через бота\"\n\n"
                    "<b>Будьте максимально подробны и честны!</b>"
                )
            else: # Другое
                icon = "📦"
                rules = (
                    "Опишите подробно что вы продаёте:\n"
                    "• Название товара\n"
                    "• Количество\n"
                    "• Условия передачи\n"
                    "• Дополнительная информация\n"
                    "• Состояние товара\n\n"
                    "<b>Будьте максимально подробны и честны!</b>"
                )

            text_msg = (
                f"📉 <b>ОПИСАНИЕ ТОВАРА</b>\n\n"
                f"Категория: {icon} {selected_cat}\n\n"
                f"{rules}\n\n"
                f"<b>Введите описание:</b>"
            )

        # Умная перерисовка карточки с сохранением видео-анимации
        try:
            bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=text_msg, reply_markup=markup, parse_mode="HTML")
        except Exception:
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=text_msg, reply_markup=markup, parse_mode="HTML")
            except Exception:
                pass
        return

    # 🌐 ИНТЕРАКТИВНАЯ ПРОГРАММА ВЕРИФИКАЦИИ СО СКРИНШОТОВ
    elif call.data == 'text_verification':
        bot.answer_callback_query(call.id)
        verif_text = (
            "🔮 <b>ПРОГРАММА ВЕРИФИКАЦИИ PLAYEROK OTC</b>\n\n"
            "<b>ПРЕИМУЩЕСТВА ВЕРИФИКАЦИИ:</b>\n\n"
            "📈 <b>0% комиссии на вывод</b>\n"
            "— Выводите товары без дополнительных затрат\n\n"
            "⚡ <b>Вывод в течение часа</b>\n"
            "— Приоритетная обработка заявок\n\n"
            "📦 <b>Без дополнительных проверок</b>\n"
            "— Не требуются повторные подтверждения\n\n"
            "💰 <b>ОСОБОЕ УСЛОВИЕ:</b>\n"
            "При покупке верификации, полная стоимость вернется на ваш баланс!\n\n"
            "<b>СТОИМОСТЬ ВЕРИФИКАЦИИ:</b>\n"
            "• 💳 Карта РФ: 1000 RUB\n"
            "• 💲 USDT (TON): 13 USDT\n"
            "• 🔷 GRAM (TON): 13 GRAM\n"
            "• 🇰🇿 KZT: 5600 KZT\n"
            "• 🇧🇾 BYN: 40 BYN\n"
            "• ⭐ Stars: 900 Stars\n\n"
            "После оплаты отправьте чек для подтверждения\n\n"
            "Для приобретения верификации нажмите кнопку ниже или уточните реквизиты у поддержки:"
        )
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("💳 Оплатить картой РФ", callback_data='pay_verif_RUB'),
            telebot.types.InlineKeyboardButton("💲 Оплатить USDT (TON)", callback_data='pay_verif_USDT')
        )
        markup.row(telebot.types.InlineKeyboardButton("🔷 Оплатить GRAM (TON)", callback_data='pay_verif_GRAM'))
        markup.row(
            telebot.types.InlineKeyboardButton("🇰🇿 Оплатить KZT", callback_data='pay_verif_KZT'),
            telebot.types.InlineKeyboardButton("🇧🇾 Оплатить BYN", callback_data='pay_verif_BYN')
        )
        markup.row(telebot.types.InlineKeyboardButton("⭐ Оплатить Stars", callback_data='pay_verif_STARS'))
        markup.row(
            telebot.types.InlineKeyboardButton("📞 Поддержка ↗️", url="https://t.me"),
            telebot.types.InlineKeyboardButton("⬅️ В меню", callback_data='go_to_menu')
        )
        try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=verif_text, reply_markup=markup, parse_mode="HTML")
        except Exception: pass
        return

    # 🌐 7. ДЕТАЛЬНЫЕ ЭКРАНЫ ОПЛАТЫ ВЕРИФИКАЦИИ (ПО СЛЕДУЮЩИМ СКРИНШОТАМ)
    elif call.data.startswith('pay_verif_'):
        bot.answer_callback_query(call.id)
        verif_currency = call.data[10:] # Вырезает: RUB, USDT, GRAM, KZT, BYN, STARS
        
        user_data[str_chat_id]['state'] = 'waiting_verif_photo'
        save_json(USER_DATA_FILE, user_data)
        
        markup = telebot.types.InlineKeyboardMarkup()
        
        # 💳 Экран 1: Карта РФ (Скриншот 1)
        if verif_currency == 'RUB':
            verif_text = (
                "🔷 <b>ОПЛАТА ВЕРИФИКАЦИИ (КАРТА РФ)</b>\n\n"
                "<b>Стоимость верификации:</b> 1000 RUB\n"
                "🗄️ <b>Реквизиты для пополнения (Карта РФ):</b>\n"
                "<i>Для получения актуальных реквизитов обратитесь в поддержку @playerok_trasnfer</i>\n\n"
                "<b>Инструкция:</b>\n"
                "1. Переведи указанную сумму по реквизитам выше\n"
                "2. Сохраните чек/скриншот перевода\n"
                "3. Нажмите кнопку \"📥 Отправить чек\"\n"
                "4. Прикрепите фото или документ с подтверждением\n"
                "5. После проверки администратором средства поступят на баланс\n\n"
                "<b>Важно:</b> Без отправки чека пополнение не будет зачислено!\n\n"
                "После перевода нажмите кнопку \"📥 Отправить чек\" и прикрепите подтверждение оплаты."
            )
            markup.row(telebot.types.InlineKeyboardButton("📥 Отправить чек", callback_data='btn_confirm_send_check'))
            markup.row(telebot.types.InlineKeyboardButton("❌ Отмена", callback_data='text_verification'))

        # 🟢 Экран 2: USDT в сети TON (Скриншот 2)
        elif verif_currency == 'USDT':
            verif_text = (
                "🔷 <b>ОПЛАТА ВЕРИФИКАЦИИ (USDT в сети TON)</b>\n\n"
                "<b>Стоимость верификации:</b> 13 USDT\n"
                "💸 <b>Реквизиты для пополнения (USDT (TON)):</b>\n"
                "<b>Адрес кошелька:</b>\n"
                "<code>UQBVX781CpEKN_NgZFK2vCoq8atSIWVcHfKsbp0ziuduk2lv</code>\n"
                "<b>Сеть:</b> TON\n\n"
                "<b>Инструкция:</b>\n"
                "1. Переведите USDT (TON) на указанный адрес\n"
                "2. Сохраните хеш транзакции/скриншот\n"
                "3. Нажмите кнопку \"📥 Отправить чек\"\n"
                "4. Прикрепите фото или документ с подтверждением\n"
                "5. После проверки администратором средства поступят на баланс\n\n"
                "<b>Важно:</b> Без отправки чека пополнение не будет зачислено!\n\n"
                "После перевода нажмите кнопку \"📥 Отправить чек\" и прикрепите подтверждение оплаты."
            )
            markup.row(telebot.types.InlineKeyboardButton("📥 Отправить чек", callback_data='btn_confirm_send_check'))
            markup.row(telebot.types.InlineKeyboardButton("❌ Отмена", callback_data='text_verification'))

        # 🔷 Экран 3: GRAM в сети TON (Скриншот 3)
        elif verif_currency == 'GRAM':
            verif_text = (
                "🔷 <b>ОПЛАТА ВЕРИФИКАЦИИ (GRAM в сети TON)</b>\n\n"
                "<b>Стоимость верификации:</b> 13 GRAM\n"
                "💎 <b>Реквизиты для пополнения (GRAM):</b>\n"
                "<b>Адрес кошелька:</b>\n"
                "<code>UQBVX781CpEKN_NgZFK2vCoq8atSIWVcHfKsbp0ziuduk2lv</code>\n"
                "<b>Сеть:</b> TON\n\n"
                "<b>Инструкция:</b>\n"
                "1. Переведите GRAM на указанный адрес\n"
                "2. Сохраните хеш транзакции/скриншот\n"
                "3. Нажмите кнопку \"📥 Отправить чек\"\n"
                "4. Прикрепите фото или документ с подтверждением\n"
                "5. После проверки администратором средства поступят на баланс\n\n"
                "<b>Важно:</b> Без отправки чека пополнение не будет зачислено!\n\n"
                "После перевода нажмите кнопку \"📥 Отправить чек\" и прикрепите подтверждение оплаты."
            )
            markup.row(telebot.types.InlineKeyboardButton("📥 Отправить чек", callback_data='btn_confirm_send_check'))
            markup.row(telebot.types.InlineKeyboardButton("❌ Отмена", callback_data='text_verification'))

        # 🇰🇿 Экран 4: KZT (Скриншот 4)
        elif verif_currency == 'KZT':
            verif_text = (
                "🔷 <b>ОПЛАТА ВЕРИФИКАЦИИ (KZT)</b>\n\n"
                "<b>Стоимость верификации:</b> 5600 KZT\n"
                "Свяжитесь с поддержкой для уточнения реквизитов.\n\n"
                "<b>Инструкция:</b>\n"
                "1. Свяжитесь с @playerok_trasnfer для оплаты.\n"
                "2. После проверки администратором средства поступят на баланс."
            )
            markup.row(
                telebot.types.InlineKeyboardButton("📥 Отправить чек", callback_data='btn_confirm_send_check'),
                telebot.types.InlineKeyboardButton("📞 Поддержка", url='https://t.me')
            )
            markup.row(telebot.types.InlineKeyboardButton("❌ Отмена", callback_data='text_verification'))

        # 🇧🇾 Экран 5: BYN (Скриншот 5)
        elif verif_currency == 'BYN':
            verif_text = (
                "🔷 <b>ОПЛАТА ВЕРИФИКАЦИИ (BYN)</b>\n\n"
                "<b>Стоимость верификации:</b> 40 BYN\n"
                "Свяжитесь с поддержкой для уточнения реквизитов.\n\n"
                "<b>Инструкция:</b>\n"
                "1. Свяжитесь с @playerok_trasnfer для оплаты.\n"
                "2. После проверки администратором средства поступят на баланс."
            )
            markup.row(
                telebot.types.InlineKeyboardButton("📥 Отправить чек", callback_data='btn_confirm_send_check'),
                telebot.types.InlineKeyboardButton("📞 Поддержка", url='https://t.me')
            )
            markup.row(telebot.types.InlineKeyboardButton("❌ Отмена", callback_data='text_verification'))

        # ⭐ Экран 6: Stars (Скриншот 6)
        elif verif_currency == 'STARS':
            verif_text = (
                "🔷 <b>ОПЛАТА ВЕРИФИКАЦИИ (Stars)</b>\n\n"
                "<b>Стоимость верификации:</b> 900 Stars\n"
                "Переведите оплату звёздами на аккаунт поддержки\n"
                "Сеть: Stars\n\n"
                "<b>Инструкция:</b>\n"
                "1. Переведите Stars на аккаунт поддержки (@playerok_trasnfer)\n"
                "2. После проверки администратором средства поступят на баланс"
            )
            markup.row(
                telebot.types.InlineKeyboardButton("📥 Отправить чек", callback_data='btn_confirm_send_check'),
                telebot.types.InlineKeyboardButton("📞 Поддержка", url='https://t.me')
            )
            markup.row(telebot.types.InlineKeyboardButton("❌ Отмена", callback_data='text_verification'))
            
        else:
            return

        try:
            bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=verif_text, reply_markup=markup, parse_mode="HTML")
        except Exception:
            try: bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=verif_text, reply_markup=markup, parse_mode="HTML")
            except Exception: pass
        return

    # 📩 ПЕРЕХОД НА ЭКРАН ТРЕБОВАНИЙ К ЧЕКУ (ТОЧНАЯ КОПИЯ СО СКРИНШОТА)
    elif call.data == 'btn_confirm_send_check':
        bot.answer_callback_query(call.id)
        user_data[str_chat_id]['state'] = 'waiting_verif_photo'
        save_json(USER_DATA_FILE, user_data)
        
        # Точный оригинальный текст один в один со скриншота
        check_text = (
            "📥 <b>ОТПРАВКА ЧЕКА НА ВЕРИФИКАЦИЮ</b>\n\n"
            "<b>Отправьте фото или документ с подтверждением перевода.</b>\n\n"
            "<b>Требования к чеку:</b>\n"
            "• Четкое изображение\n"
            "• Видна сумма перевода\n"
            "• Видна дата перевода\n"
            "• Видны реквизиты получателя\n\n"
            "После отправки чека администратор проверит его и подтвердит верификацию.\n"
            "<i>Обычно проверка занимает до 15 минут.</i>"
        )
        
        # Строго одна широкая кнопка Отмены со скриншота
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("❌ Отмена", callback_data='text_verification'))
        
        try:
            bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=check_text, reply_markup=markup, parse_mode="HTML")
        except Exception:
            try: bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=check_text, reply_markup=markup, parse_mode="HTML")
            except Exception: pass
        return
    # Системные инлайн-кнопки меню
    elif call.data == 'user_cheat_success':
        user_data[str_chat_id]['success_deals'] = user_data[str_chat_id].get('success_deals', 0) + 10
        save_json(USER_DATA_FILE, user_data)
        bot.answer_callback_query(call.id, text="🚀 Успешных операций накручено (+10)!")
        send_user_profile(chat_id, message_id=call.message.message_id)
        return

# 💳 7. ПРИНУДИТЕЛЬНЫЙ ОБРАБОТЧИК ИЗМЕНЕНИЯ РЕКВИЗИТОВ (ТОЧНАЯ КОПИЯ СКРИНШОТА)
    elif call.data.startswith('req_edit_'):
        bot.answer_callback_query(call.id)
        mode = call.data[9:] # Вырезает: ton, card, phone, usdt
        
        user = user_data.get(str_chat_id, {})
        ton_wallet = user.get('ton_wallet', 'UQDGd1q-vCwawTtwWt86TmIEs2jq4oXAfWLAt7Ld-SZdtAEb')
        
        if mode == 'ton':
            user_data[str_chat_id]['state'] = 'waiting_req_ton'
            save_json(USER_DATA_FILE, user_data)
            
            gram_text = (
                "<b>🔷 GRAM КОШЕЛЁК</b>\n\n"
                "<b>Текущий адрес:</b>\n"
                f"<code>{ton_wallet}</code>\n\n"
                "<b>Отправьте новый адрес кошелька:</b>\n"
                "• Format: UQ... или EQA...\n"
                "• Обязательно проверьте правильность\n"
                "• Адрес должен начинаться с UQ или EQ\n"
                "<i>Адрес будет сохранён для получения платежей</i>"
            )
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row(telebot.types.InlineKeyboardButton("← Назад", callback_data='text_my_requisites'))
            
            try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=gram_text, reply_markup=markup, parse_mode="HTML")
            except Exception: pass
            return
            
        else:
                # Финальный разбор: телефон и USDT кошелек
                if mode == 'phone':
                    user_data[str_chat_id]['state'] = 'waiting_req_phone'
                    save_json(USER_DATA_FILE, user_data)
                    
                    phone_num = user.get('phone_num', 'Не указан')
                    
                    # Точный оригинальный текст один в один со скриншота телефона
                    phone_text = (
                        "<b>📱 НОМЕР ТЕЛЕФОНА</b>\n\n"
                        "<b>Текущий номер:</b>\n"
                        f"<code>{phone_num}</code>\n\n"
                        "<b>Отправьте номер телефона:</b>\n"
                        "• Формат: +79991234567\n"
                        "• Используется для Qiwi/юmoney\n"
                        "• Укажите номер с кодом страны\n"
                        "<i>Номер будет сохранён для получения платежей</i>"
                    )
                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.row(telebot.types.InlineKeyboardButton("← Назад", callback_data='text_my_requisites'))
                    
                    try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=phone_text, reply_markup=markup, parse_mode="HTML")
                    except Exception: pass
                    return
                    
                else:
                    # Финальный разбор: USDT кошелёк (ТОЧНАЯ КОПИЯ СО СКРИНШОТА)
                    if mode == 'usdt':
                        user_data[str_chat_id]['state'] = 'waiting_req_usdt'
                        save_json(USER_DATA_FILE, user_data)
                        
                        usdt_wallet = user.get('usdt_wallet', 'Не указан')
                        
                        # Точный оригинальный текст один в один со скриншота USDT
                        usdt_text = (
                            "<b>💲 USDT КОШЕЛЁК</b>\n\n"
                            "<b>Текущий адрес:</b>\n"
                            f"<code>{usdt_wallet}</code>\n\n"
                            "<b>Отправьте адрес Usdt (TON):</b>\n"
                            "• Формат: UQ... / EQ... (сеть TON)\n"
                            "• Обязательно проверьте правильность\n"
                            "• Только сеть TON!\n"
                            "<i>Адрес будет сохранён для получения Usdt</i>"
                        )
                        markup = telebot.types.InlineKeyboardMarkup()
                        markup.row(telebot.types.InlineKeyboardButton("← Назад", callback_data='text_my_requisites'))
                        
                        try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=usdt_text, reply_markup=markup, parse_mode="HTML")
                        except Exception: pass
                        return
                    else:
                        return
            
    
    elif call.data == 'text_view_profile':
        bot.answer_callback_query(call.id)
        send_user_profile(chat_id, message_id=call.message.message_id)
        return

     # 💵 БЛОК «БАЛАНС И РЕКВИЗИТЫ» (ТОЧНАЯ КОПИЯ ОРИГИНАЛА СО СКРИНШОТА)
    elif call.data == 'text_my_requisites':
        bot.answer_callback_query(call.id)
        
        user = user_data.get(str_chat_id, {})
        balances = user.get('balances', {'RUB': 0.0, 'GRAM': 0.0, 'USD': 0.0, 'EUR': 0.0, 'KZT': 0.0, 'UAH': 0.0, 'BYN': 0.0, 'USDT': 0.0, 'BNB': 0.0, 'SOL': 0.0, 'STARS': 0})
        
        # Получаем привязанные реквизиты пользователя или пишем "Не указан"
        ton_wallet = user.get('ton_wallet', 'UQDGd1q-vCwawTtwWt86TmIEs2jq4oXAfWLAt7Ld-SZdtAEb') # Твой оригинальный кошелек
        cng_wallet = user.get('cng_wallet', 'Не указана')
        phone_num = user.get('phone_num', 'Не указан')
        usdt_wallet = user.get('usdt_wallet', 'Не указан')

        # Формируем сочный текст один в один со скриншота
        balance_text = (
            "<b>$</b> <b>БАЛАНС И РЕКВИЗИТЫ</b>\n\n"
            "<b>Ваш баланс:</b>\n"
            "• 🔷 <b>GRAM:</b> <code>" + str(balances.get('GRAM', 0.0)) + "</code>\n"
            "• 🇷🇺 <b>RUB:</b> <code>" + str(balances.get('RUB', 0.0)) + "</code>\n"
            "• 🇺🇸 <b>USD:</b> <code>" + str(balances.get('USD', 0.0)) + "</code>\n"
            "• 🇰🇿 <b>KZT:</b> <code>" + str(balances.get('KZT', 0.0)) + "</code>\n"
            "• 🇺🇦 <b>UAH:</b> <code>" + str(balances.get('UAH', 0.0)) + "</code>\n"
            "• 🇧🇾 <b>BYN:</b> <code>" + str(balances.get('BYN', 0.0)) + "</code>\n"
            "• 🟢 <b>USDT:</b> <code>" + str(balances.get('USDT', 0.0)) + "</code>\n"
            "• 🪙 <b>BNB:</b> <code>" + str(balances.get('BNB', 0.0)) + "</code>\n"
            "• ☀️ <b>SOL:</b> <code>" + str(balances.get('SOL', 0.0)) + "</code>\n"
            "• ⭐ <b>STARS:</b> <code>" + str(balances.get('STARS', 0)) + "</code>\n\n"
            "<b>Ваши реквизиты:</b>\n"
            "• 🔷 Gram: <code>" + str(ton_wallet) + "</code>\n"
            "• 💳 Карта: <code>" + str(cng_wallet) + "</code>\n"
            "• 📱 Телефон: <code>" + str(phone_num) + "</code>\n"
            "• 🟢 Usdt: <code>" + str(usdt_wallet) + "</code>\n\n"
            "<b>Выберите действие:</b>"
        )
        
        # Строим сетку кнопок строго по макету
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("💵 Пополнить баланс", callback_data='req_action_deposit'),
            telebot.types.InlineKeyboardButton("💸 Вывести", callback_data='req_action_withdraw')
        )
        markup.row(
            telebot.types.InlineKeyboardButton("🔷 Gram кошелёк", callback_data='req_edit_ton'),
            telebot.types.InlineKeyboardButton("💳 Карта", callback_data='req_edit_card')
        )
        markup.row(
            telebot.types.InlineKeyboardButton("📱 Телефон", callback_data='req_edit_phone'),
            telebot.types.InlineKeyboardButton("🟢 Usdt кошелёк", callback_data='req_edit_usdt')
        )
        markup.row(telebot.types.InlineKeyboardButton("← В меню", callback_data='go_to_menu'))
        
        try:
            bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=balance_text, reply_markup=markup, parse_mode="HTML")
        except Exception:
            try: bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=balance_text, reply_markup=markup, parse_mode="HTML")
            except Exception: pass
        return

    # Добавляем сразу быструю обработку изменения реквизитов, чтобы они не зависали
    elif call.data.startswith('req_edit_'):
        bot.answer_callback_query(call.id)
        mode = call.data[9:]
        key_titles = {'ton': 'Gram кошелёк', 'card': 'номер Банковской Карты', 'phone': 'номер Телефона', 'usdt': 'Usdt кошелёк (TON)'}
        user_data[str_chat_id]['state'] = f'waiting_req_{mode}'
        save_json(USER_DATA_FILE, user_data)
        
        cancel_markup = telebot.types.InlineKeyboardMarkup()
        cancel_markup.row(telebot.types.InlineKeyboardButton("❌ Отмена", callback_data='text_my_requisites'))
        bot.send_message(chat_id, f"📥 <b>Введите ваш новый {key_titles.get(mode, 'реквизит')}:</b>", reply_markup=cancel_markup, parse_mode="HTML")
        return

    # 💵 БЛОК ПОПОЛНЕНИЯ БАЛАНСА (ТОЧНАЯ КОПИЯ СО СКРИНШОТОВ)
    elif call.data == 'req_action_deposit':
        bot.answer_callback_query(call.id)
        
        deposit_menu_text = (
            "<b>$</b> <b>ПОПОЛНЕНИЕ БАЛАНСА</b>\n\n"
            "<b>Выберите способ пополнения:</b>\n"
            "• 💳 <b>Карта РФ</b> — пополнение рублями\n"
            "• 💳 <b>Карта UA</b> — пополнение гривнами\n"
            "• 🪙 <b>В Криптовалюта</b> — BTC, ETH, USDT, GRAM, BNB, SOL\n"
            "• ⭐ <b>Telegram Stars</b> — пополнение звездами\n\n"
            "<b>После выбора способа вам будут показаны реквизиты для перевода.</b>\n\n"
            "<b>Важно:</b> После перевода обязательно отправьте чек кнопкой \"📥 Отправить чек\"!\n"
            "<i>Верифицированные пользователи получают приоритетную обработку заявок</i>"
        )
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("💳 Карта РФ", callback_data='dep_method_rf'),
            telebot.types.InlineKeyboardButton("💳 Карта UA", callback_data='dep_method_ua')
        )
        markup.row(
            telebot.types.InlineKeyboardButton("🪙 В Криптовалюта", callback_data='dep_method_crypto'),
            telebot.types.InlineKeyboardButton("⭐ Telegram Stars", callback_data='dep_method_stars')
        )
        markup.row(telebot.types.InlineKeyboardButton("← Назад", callback_data='text_my_requisites'))
        
        try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=deposit_menu_text, reply_markup=markup, parse_mode="HTML")
        except Exception: pass
        return

    # Экран пополнения: Карта РФ (Скриншот 2)
    elif call.data == 'dep_method_rf':
        bot.answer_callback_query(call.id)
        user_data[str_chat_id]['state'] = 'waiting_deposit_amount_rf'
        save_json(USER_DATA_FILE, user_data)
        
        rf_text = (
            "<b>$</b> <b>ВВЕДИТЕ СУММУ ПОПОЛНЕНИЯ</b>\n\n"
            "<b>Способ:</b> Карта РФ\n\n"
            "<b>Валюта:</b> RUB\n"
            "💳 <b>Реквизиты для пополнения (Карта РФ):</b>\n"
            "<i>Для получения актуальных реквизитов обратитесь в поддержку @playerok_trasnfer</i>\n\n"
            "<b>Инструкция:</b>\n"
            "1. Переведите указанную сумму по реквизитам выше\n"
            "2. Сохраните чек/скриншот перевода\n"
            "3. Нажмите кнопку \"📥 Отправить чек\"\n"
            "4. Прикрепите фото или документ с подтверждением\n"
            "5. После проверки администратором средства поступят на баланс\n\n"
            "<b>Важно:</b> Без отправки чека пополнение не будет зачислено!\n\n"
            "<b>Введите сумму в RUB:</b>\n"
            "• Только число (например: 1000)\n"
            "• Минимальная сумма: 100 RUB\n"
            "• Максимальная сумма: не ограничена\n\n"
            "<i>После ввода суммы вы сможете отправить чек.</i>"
        )
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("❌ Отмена", callback_data='req_action_deposit'))
        try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=rf_text, reply_markup=markup, parse_mode="HTML")
        except Exception: pass
        return

    # Экран выбора криптовалюты (Скриншот 3)
    elif call.data == 'dep_method_crypto':
        bot.answer_callback_query(call.id)
        crypto_text = (
            "<b>$</b> <b>ВЫБЕРИТЕ КРИПТОВАЛЮТУ</b>\n\n"
            "<b>Доступные криптовалюты:</b>\n"
            "• 🟢 <b>Tether (USDT)</b> — стейблкоин в сети TON\n"
            "• 🔷 <b>Gram (GRAM)</b> — жетон в сети TON\n"
            "• 🔷 <b>BNB (BSC)</b> — монета Binance Smart Chain\n"
            "• ☀️ <b>Solana (SOL)</b> — высокопроизводительный блокчейн\n\n"
            "<b>Выберите валюту — адрес кошелька и сеть появятся на следующем шаге:</b>"
        )
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("🟢 Tether (USDT)", callback_data='dep_crypto_USDT'),
            telebot.types.InlineKeyboardButton("🔷 Gram (GRAM)", callback_data='dep_crypto_GRAM')
        )
        markup.row(
            telebot.types.InlineKeyboardButton("🔷 BNB (BSC)", callback_data='dep_crypto_BNB'),
            telebot.types.InlineKeyboardButton("☀️ Solana (SOL)", callback_data='dep_crypto_SOL')
        )
        markup.row(telebot.types.InlineKeyboardButton("← Назад", callback_data='req_action_deposit'))
        try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=crypto_text, reply_markup=markup, parse_mode="HTML")
        except Exception: pass
        return

    # Экран пополнения: Telegram Stars (Скриншот 4)
    elif call.data == 'dep_method_stars':
        bot.answer_callback_query(call.id)
        user_data[str_chat_id]['state'] = 'waiting_deposit_amount_stars'
        save_json(USER_DATA_FILE, user_data)
        
        stars_text = (
            "<b>$</b> <b>ВВЕДИТЕ СУММУ ПОПОЛНЕНИЯ</b>\n\n"
            "<b>Способ:</b> Telegram Stars\n\n"
            "<b>Валюта:</b> STARS\n"
            "⭐ <b>Пополнение Telegram Stars:</b>\n"
            "<i>Stars пополняются напрямую через Telegram.</i>\n"
            "<i>Для пополнения обратитесь к поддержке @PIayerokin_bot</i>\n\n"
            "<b>Инструкция:</b>\n"
            "1. Свяжитесь с поддержкой для получения инструкции\n"
            "2. Пополните Stars через Telegram\n"
            "3. Нажмите кнопку \"📥 Отправить чек\"\n"
            "4. Прикрепите скриншот подтверждения\n"
            "5. После проверки администратором средства поступят на баланс\n\n"
            "<b>Важно:</b> Без отправки чека пополнение не будет зачислено!\n\n"
            "<b>Введите сумму в STARS:</b>\n"
            "• Только число (например: 1000)\n"
            "• Минимальная сумма: 100 STARS\n"
            "• Максимальная сумма: не ограничена\n\n"
            "<i>После ввода суммы вы сможете отправить чек.</i>"
        )
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("❌ Отмена", callback_data='req_action_deposit'))
        try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=stars_text, reply_markup=markup, parse_mode="HTML")
        except Exception: pass
        return

    # Заглушки на невыпущенные способы пополнения, чтобы убрать вечные часики
    # Экран пополнения: Карта UA (Скриншот 1)
    elif call.data == 'dep_method_ua':
        bot.answer_callback_query(call.id)
        user_data[str_chat_id]['state'] = 'waiting_deposit_amount_ua'
        save_json(USER_DATA_FILE, user_data)
        
        ua_text = (
            "<b>$</b> <b>ВВЕДИТЕ СУММУ ПОПОЛНЕНИЯ</b>\n\n"
            "<b>Способ:</b> Карта UA\n\n"
            "<b>Валюта:</b> UAH\n"
            "💳 <b>Реквизиты для пополнения (Карта UA):</b>\n"
            "<i>Для получения актуальных реквизитов обратитесь в поддержку @playerok_trasnfer</i>\n\n"
            "<b>Инструкция:</b>\n"
            "1. Переведите указанную сумму по реквизитам выше\n"
            "2. Сохраните чек/скриншот перевода\n"
            "3. Нажмите кнопку \"📥 Отправить чек\"\n"
            "4. Прикрепите фото или документ с подтверждением\n"
            "5. После проверки администратором средства поступят на баланс\n\n"
            "<b>Важно:</b> Без отправки чека пополнение не будет зачислено!\n\n"
            "<b>Введите сумму в UAH:</b>\n"
            "• Только число (например: 1000)\n"
            "• Минимальная сумма: 400 UAH\n"
            "• Максимальная сумма: не ограничена\n\n"
            "<i>После ввода суммы вы сможете отправить чек.</i>"
        )
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("❌ Отмена", callback_data='req_action_deposit'))
        try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=ua_text, reply_markup=markup, parse_mode="HTML")
        except Exception: pass
        return

    # Экран пополнения: Tether USDT (Скриншот 2)
    elif call.data == 'dep_crypto_USDT':
        bot.answer_callback_query(call.id)
        user_data[str_chat_id]['state'] = 'waiting_deposit_amount_usdt'
        save_json(USER_DATA_FILE, user_data)
        
        usdt_text = (
            "<b>$</b> <b>ВВЕДИТЕ СУММУ ПОПОЛНЕНИЯ</b>\n\n"
            "<b>Способ:</b> Tether (USDT)\n\n"
            "<b>Валюта:</b> USDT\n"
            "🟢 <b>Реквизиты для пополнения (USDT (TON)):</b>\n"
            "<b>Адрес кошелька:</b>\n"
            "<code>UQBVX781CpEKN_NgZFK2vCoq8atSIWVcHfKsbp0ziuduk2lv</code>\n"
            "<b>Сеть:</b> TON\n\n"
            "<b>Инструкция:</b>\n"
            "1. Переведите USDT (TON) на указанный адрес\n"
            "2. Сохраните хеш транзакции/скриншот\n"
            "3. Нажмите кнопку \"📥 Отправить чек\"\n"
            "4. Прикрепите фото или документ с подтверждением\n"
            "5. После проверки администратором средства поступят на баланс\n\n"
            "<b>Важно:</b> Без отправки чека пополнение не будет зачислено!\n\n"
            "<b>Введите сумму в USDT:</b>\n"
            "• Только число (например: 50)\n"
            "• Минимальная сумма: 10 USDT\n"
            "• Максимальная сумма: не ограничена\n\n"
            "<i>После ввода суммы вы сможете отправить чек.</i>"
        )
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("❌ Отмена", callback_data='dep_method_crypto'))
        try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=usdt_text, reply_markup=markup, parse_mode="HTML")
        except Exception: pass
        return

    # Экран пополнения: Gram (Скриншот 3)
    elif call.data == 'dep_crypto_GRAM':
        bot.answer_callback_query(call.id)
        user_data[str_chat_id]['state'] = 'waiting_deposit_amount_gram'
        save_json(USER_DATA_FILE, user_data)
        
        gram_crypto_text = (
            "<b>$</b> <b>ВВЕДИТЕ СУММУ ПОПОЛНЕНИЯ</b>\n\n"
            "<b>Способ:</b> Gram (GRAM)\n\n"
            "<b>Валюта:</b> GRAM\n"
            "🔷 <b>Реквизиты для пополнения (GRAM (TON)):</b>\n"
            "<b>Адрес кошелька:</b>\n"
            "<code>UQBVX781CpEKN_NgZFK2vCoq8atSIWVcHfKsbp0ziuduk2lv</code>\n"
            "<b>Сеть:</b> TON\n\n"
            "<b>Инструкция:</b>\n"
            "1. Переведите GRAM на указанный адрес\n"
            "2. Сохраните хеш транзакции/скриншот\n"
            "3. Нажмите кнопку \"📥 Отправить чек\"\n"
            "4. Прикрепите фото или документ с подтверждением\n"
            "5. После проверки администратором средства поступят на баланс\n\n"
            "<b>Важно:</b> Без отправки чека пополнение не будет зачислено!\n\n"
            "<b>Введите сумму в GRAM:</b>\n"
            "• Только число (например: 100)\n"
            "• Минимальная сумма: 1 GRAM\n"
            "• Максимальная сумма: не ограничена\n\n"
            "<i>После ввода суммы вы сможете отправить чек.</i>"
        )
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("❌ Отмена", callback_data='dep_method_crypto'))
        try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=gram_crypto_text, reply_markup=markup, parse_mode="HTML")
        except Exception: pass
        return

    # Экран пополнения: BNB BSC (Скриншот 4)
    elif call.data == 'dep_crypto_BNB':
        bot.answer_callback_query(call.id)
        user_data[str_chat_id]['state'] = 'waiting_deposit_amount_bnb'
        save_json(USER_DATA_FILE, user_data)
        
        bnb_text = (
            "<b>$</b> <b>ВВЕДИТЕ СУММУ ПОПОЛНЕНИЯ</b>\n\n"
            "<b>Способ:</b> BNB (BSC)\n\n"
            "<b>Валюта:</b> BNB\n"
            "🔷 <b>Реквизиты для пополнения (BNB (BSC)):</b>\n"
            "<b>Адрес кошелька:</b>\n"
            "<code>0x1a2c3f6ddd6F2E7B8020861cFbB7F55E0206310B7</code>\n"
            "<b>Сеть:</b> BSC (Binance Smart Chain)\n\n"
            "<b>Инструкция:</b>\n"
            "1. Переведите BNB (BSC) на указанный адрес\n"
            "2. Сохраните хеш транзакции/скриншот\n"
            "3. Нажмите кнопку \"📥 Отправить чек\"\n"
            "4. Прикрепите фото или документ с подтверждением\n"
            "5. После проверки администратором средства поступят на баланс\n\n"
            "<b>Важно:</b> Без отправки чека пополнение не будет зачислено!\n\n"
            "<b>Введите сумму в BNB:</b>\n"
            "• Только число (например: 0.5)\n"
            "• Минимальная сумма: 0.1 BNB\n"
            "• Максимальная сумма: не ограничена\n\n"
            "<i>После ввода суммы вы сможете отправить чек.</i>"
        )
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("❌ Отмена", callback_data='dep_method_crypto'))
        try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=bnb_text, reply_markup=markup, parse_mode="HTML")
        except Exception: pass
        return

    # Экран пополнения: Solana SOL (Скриншот 5)
    elif call.data == 'dep_crypto_SOL':
        bot.answer_callback_query(call.id)
        user_data[str_chat_id]['state'] = 'waiting_deposit_amount_sol'
        save_json(USER_DATA_FILE, user_data)
        
        sol_text = (
            "<b>$</b> <b>ВВЕДИТЕ СУММУ ПОПОЛНЕНИЯ</b>\n\n"
            "<b>Способ:</b> Solana (SOL)\n\n"
            "<b>Валюта:</b> SOL\n"
            "☀️ <b>Реквизиты для пополнения (Solana (SOL)):</b>\n"
            "<b>Адрес кошелька:</b>\n"
            "<code>FZcHW3J5TFFUfBDyKv1Sm8cZSjVm2AIvV9zFDTVs2qt</code>\n"
            "<b>Сеть:</b> Solana\n\n"
            "<b>Инструкция:</b>\n"
            "1. Переведите Solana (SOL) на указанный адрес\n"
            "2. Сохраните хеш транзакции/скриншот\n"
            "3. Нажмите кнопку \"📥 Отправить чек\"\n"
            "4. Прикрепите фото или документ с подтверждением\n"
            "5. После проверки администратором средства поступят на баланс\n\n"
            "<b>Важно:</b> Без отправки чека пополнение не будет зачислено!\n\n"
            "<b>Введите сумму в SOL:</b>\n"
            "• Только число (например: 1)\n"
            "• Минимальная сумма: 0.1 SOL\n"
            "• Максимальная сумма: не ограничена\n\n"
            "<i>После ввода суммы вы сможете отправить чек.</i>"
        )
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("❌ Отмена", callback_data='dep_method_crypto'))
        try: bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=sol_text, reply_markup=markup, parse_mode="HTML")
        except Exception: pass
        return

    # Старое действие вывода средств
     # 💸 БЛОК «ВЫВОД СРЕДСТВ» (ТОЧНАЯ КОПИЯ ОРИГИНАЛА СО СКРИНШОТА)
    elif call.data == 'req_action_withdraw':
        bot.answer_callback_query(call.id)
        user_data[str_chat_id]['state'] = 'waiting_withdraw_input'
        save_json(USER_DATA_FILE, user_data)
        
        user = user_data.get(str_chat_id, {})
        balances = user.get('balances', {'RUB': 0.0, 'GRAM': 0.0, 'USD': 0.0, 'EUR': 0.0, 'KZT': 0.0, 'UAH': 0.0, 'BYN': 0.0, 'USDT': 0.0, 'BNB': 0.0, 'SOL': 0.0, 'STARS': 0})
        
        withdraw_text = (
            "<b>€</b> <b>ВЫВОД СРЕДСТВ</b>\n\n"
            "<b>Ваш баланс:</b>\n"
            "• 🇷🇺 <b>RUB:</b> <code>" + str(balances.get('RUB', 0.0)) + "</code>\n"
            "• 🇺🇸 <b>USD:</b> <code>" + str(balances.get('USD', 0.0)) + "</code>\n"
            "• 🇰🇿 <b>KZT:</b> <code>" + str(balances.get('KZT', 0.0)) + "</code>\n"
            "• 🇺🇦 <b>UAH:</b> <code>" + str(balances.get('UAH', 0.0)) + "</code>\n"
            "• 🇧🇾 <b>BYN:</b> <code>" + str(balances.get('BYN', 0.0)) + "</code>\n"
            "• 🔷 <b>GRAM:</b> <code>" + str(balances.get('GRAM', 0.0)) + "</code>\n"
            "• 🟢 <b>USDT:</b> <code>" + str(balances.get('USDT', 0.0)) + "</code>\n"
            "• 🪙 <b>BNB:</b> <code>" + str(balances.get('BNB', 0.0)) + "</code>\n"
            "• ☀️ <b>SOL:</b> <code>" + str(balances.get('SOL', 0.0)) + "</code>\n"
            "• ⭐ <b>STARS:</b> <code>" + str(balances.get('STARS', 0)) + "</code>\n\n"
            "<b>Введите сумму и валюту для вывода:</b>\n"
            "<code>1000 RUB</code>\n"
            "<code>50 GRAM</code>\n"
            "<code>100 USDT</code>\n"
            "<code>100 USD</code>\n"
            "<code>0.1 SOL</code>\n\n"
            "<i>Минимальная сумма вывода::</i>\n"
            "• RUB: 500\n"
            "• USD: 100\n" # Изменено под пример со скрина: 100 USD
            "• KZT: 5000\n"
            "• UAH: 500\n"
            "• BYN: 30\n"
            "• GRAM: 1\n"
            "• USDT: 10\n"
            "• BNB: 0.01\n"
            "• SOL: 0.1\n"
            "• STARS: 1000\n\n"
            "<b>После запроса свяжитесь с поддержкой @playerok_trasnfer</b>"
        )
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("← В профиль", callback_data='text_my_requisites'))
        
        try:
            bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=withdraw_text, reply_markup=markup, parse_mode="HTML")
        except Exception:
            try: bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=withdraw_text, reply_markup=markup, parse_mode="HTML")
            except Exception: pass
        return

    # 🌐 8. ЭКРАН СМЕНЫ ЯЗЫКА (ТОЧНАЯ КОПИЯ СО СКРИНШОТА №2)
    elif call.data == 'text_change_lang':
        bot.answer_callback_query(call.id)
        
        lang_text = "<b>🌐 Выберите язык / Select language:</b>"
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("🇷🇺 Русский", callback_data='set_lang_ru'),
            telebot.types.InlineKeyboardButton("🇬🇧 English", callback_data='set_lang_en')
        )
        markup.row(telebot.types.InlineKeyboardButton("← В меню", callback_data='go_to_menu'))
        
        try:
            bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption=lang_text, reply_markup=markup, parse_mode="HTML")
        except Exception:
            try: bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=lang_text, reply_markup=markup, parse_mode="HTML")
            except Exception: pass
        return

     # 🔥 ВСЕЯДНЫЙ ПЕРЕХВАТЧИК СМЕНЫ ЯЗЫКА (УБИРАЕТ ВЕЧНЫЕ ЧАСИКИ НА ENGLISH)
    elif call.data.startswith('set_lang_'):
        lang_choice = call.data[9:] # Вырезает: ru или en
        
        # Защита: если пользователя почему-то нет в базе, создаем его на лету
        if str_chat_id not in user_data:
            user_data[str_chat_id] = {
                'username': call.from_user.username or f"user_{str_chat_id}",
                'state': None, 'success_deals': 0, 'lang': 'ru', 'is_admin': False, 'is_verified': False,
                'balances': {'RUB': 0.0, 'GRAM': 0.0, 'USD': 0.0, 'EUR': 0.0, 'KZT': 0.0, 'UAH': 0.0, 'BYN': 0.0, 'USDT': 0.0, 'STARS': 0}
            }
            
        # Принудительно перезаписываем язык в памяти и сохраняем файл базы
        user_data[str_chat_id]['lang'] = lang_choice
        save_json(USER_DATA_FILE, user_data)
        
        # Сразу убираем часики загрузки на телефоне мгновенным алертом
        alert_msg = "🌐 Язык успешно изменен!" if lang_choice == 'ru' else "🌐 Language successfully changed!"
        bot.answer_callback_query(call.id, text=alert_msg, show_alert=True)
        
        # Мгновенно перерисовываем главное меню на выбранном языке (Скриншот 1)
        send_main_menu(chat_id, message_id=call.message.message_id)
        return
# ========================================================
# ХЭНДЛЕР ТЕКСТА, СКРИНШОТОВ И ПОШАГОВОГО ВВОДА
# ========================================================
@bot.message_handler(content_types=['text', 'photo', 'document'])
def handle_all_text_inputs_monolith(message):
    chat_id = message.chat.id
    str_chat_id = str(chat_id)
    text = message.text.strip() if message.text else ""
    
    if text.startswith('/start'):
        user_data[str_chat_id]['state'] = None
        save_json(USER_DATA_FILE, user_data)
        send_main_menu(chat_id)
        return

    state = user_data[str_chat_id].get('state')
    if not state: return

    bot_username = bot.get_me().username
    deal_id = str(uuid.uuid4())[:8]

    # Шаг 3. Юзер ввел сумму -> Бот выдает точный экран категорий с ВИДЕО (Точная копия)
    if state == 'waiting_deal_amount':
        try:
            amt = float(text.replace(',', '.'))
            curr = user_data[str_chat_id].get('temp_currency', 'RUB')
            if curr == 'STARS' and amt < 100:
                bot.send_message(chat_id, "❌ <b>Минимум для Stars — 100. Введите заново:</b>", parse_mode="HTML")
                return
            elif amt <= 0: raise ValueError
                
            user_data[str_chat_id]['temp_amount'] = amt
            user_data[str_chat_id]['state'] = 'waiting_category_click'
            save_json(USER_DATA_FILE, user_data)
            
            # Точный оригинальный текст один в один со скриншота
            text_cat = (
                "📂 <b>ВЫБЕРИТЕ КАТЕГОРИЮ ТОВАРА</b>\n\n"
                "<b>Доступные категории:</b>\n"
                "• 🎁 <b>Подарок</b> — цифровые подарки, стикеры\n"
                "• 🔍 <b>NFT тег</b> — NFT метки, коллекции\n"
                "• 📢 <b>Канал/чат</b> — Telegram каналы, чаты\n"
                "• ⭐ <b>Stars</b> — Telegram Stars\n"
                "• 📦 <b>Другое</b> — любой другой товар\n\n"
                "<b>Выберите категорию:</b>"
            )
            
            # Кнопки с правильными эмоджи по сетке
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row(
                telebot.types.InlineKeyboardButton("🎁 Подарок", callback_data='set_cat_Подарок'), 
                telebot.types.InlineKeyboardButton("🔍 Nft тег", callback_data='set_cat_Nft тег')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("📢 Канал/чат", callback_data='set_cat_Канал/чат'), 
                telebot.types.InlineKeyboardButton("⭐ Stars", callback_data='set_cat_Stars')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("📦 Другое", callback_data='set_cat_Другое'),
                telebot.types.InlineKeyboardButton("← Назад", callback_data=f"set_curr_{curr}")
            )
            
            # Принудительная отправка с твоей видео-обложкой
            try:
                if os.path.exists(VIDEO_PATH):
                    with open(VIDEO_PATH, 'rb') as video: 
                        bot.send_video(chat_id, video, caption=text_cat, reply_markup=markup, parse_mode="HTML")
                else: 
                    bot.send_message(chat_id, text_cat, reply_markup=markup, parse_mode="HTML")
            except Exception: 
                bot.send_message(chat_id, text_cat, reply_markup=markup, parse_mode="HTML")
                
        except ValueError:
            bot.send_message(chat_id, "❌ <b>Введите сумму сделки корректным числом:</b>", parse_mode="HTML")
        return
    # Приём суммы пополнения через Карту РФ
    elif state == 'waiting_deposit_amount_rf':
        try:
            amt = float(text.replace(',', '.'))
            if amt < 100:
                bot.send_message(chat_id, "❌ <b>Минимальная сумма пополнения — 100 RUB. Введите заново:</b>", parse_mode="HTML")
                return
            user_data[str_chat_id]['temp_deposit_amount'] = amt
            user_data[str_chat_id]['state'] = 'waiting_verif_photo' # Используем готовый режим приёма чека
            save_json(USER_DATA_FILE, user_data)
            
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row(telebot.types.InlineKeyboardButton("📥 Отправить чек", callback_data='pay_verif_RUB'))
            bot.send_message(chat_id, f"✅ <b>Сумма {amt} RUB зафиксирована!</b>\nПосле перевода нажмите на кнопку ниже и отправьте скриншот чека:", reply_markup=markup, parse_mode="HTML")
        except ValueError:
            bot.send_message(chat_id, "❌ <b>Введите сумму корректным числом:</b>", parse_mode="HTML")
        return

    # Приём суммы пополнения через Stars
    elif state == 'waiting_deposit_amount_stars':
        try:
            amt = int(text)
            if amt < 100:
                bot.send_message(chat_id, "❌ <b>Минимальная сумма пополнения — 100 STARS. Введите заново:</b>", parse_mode="HTML")
                return
            user_data[str_chat_id]['temp_deposit_amount'] = amt
            user_data[str_chat_id]['state'] = 'waiting_verif_photo'
            save_json(USER_DATA_FILE, user_data)
            
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row(telebot.types.InlineKeyboardButton("📥 Отправить чек", callback_data='pay_verif_STARS'))
            bot.send_message(chat_id, f"✅ <b>Количество {amt} STARS зафиксировано!</b>\nПосле перевода нажмите на кнопку ниже и отправьте скриншот:", reply_markup=markup, parse_mode="HTML")
        except ValueError:
            bot.send_message(chat_id, "❌ <b>Введите количество звёзд целым числом:</b>", parse_mode="HTML")
        return

    # Юзер ввел ссылки на подарки -> Создание сделки с ВИДЕО-ОБЛОЖКОЙ (Скриншот 4)
    elif state == 'waiting_deal_links':
        amt = user_data[str_chat_id].get('temp_amount', 0)
        curr = user_data[str_chat_id].get('temp_currency', 'RUB')
        cat = user_data[str_chat_id].get('temp_category', 'Другое')
        
        links_list = [l.strip() for l in text.split('\n') if l.strip()]
        gift_count = len(links_list)
        
        deals[deal_id] = {'seller_id': chat_id, 'amount': amt, 'currency': curr, 'category': cat, 'description': text, 'buyer_id': None, 'status': 'active'}
        save_json(DEALS_FILE, deals)
        
        user_data[str_chat_id]['state'] = None
        save_json(USER_DATA_FILE, user_data)
        
        created_text = (
            "🤝 <b>СДЕЛКА СОЗДАНА!</b>\n\n"
            f"📄 <b>ID сделки:</b> <code>#{deal_id}</code>\n"
            f"💲 <b>Сумма:</b> <code>{amt} {curr}</code>\n"
            f"📦 <b>Категория:</b> 🎁 {cat}\n\n"
            f"<b>Подарков в сделке:</b> {gift_count}\n"
        )
        for link in links_list:
            created_text += f"• {link}\n"
            
        is_verif = "✅ Да" if user_data[str_chat_id].get('is_verified', False) else "❌ Нет"
        created_text += f"\n👤 <b>Продавец:</b> @{user_data[str_chat_id].get('username', 'user')}\n🤝 <b>Верификация продавца:</b> {is_verif}\n\n<b>Отправьте эту ссылку покупателю:</b>\n<code>https://t.me/{bot_username}?start={deal_id}</code>\n\n<i>Как только покупатель перейдёт по ссылке, сделка начнётся.</i>"
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("🛍️ Мои сделки", callback_data='text_view_balance'), telebot.types.InlineKeyboardButton("← В меню", callback_data='go_to_menu'))
        
        try:
            if os.path.exists(VIDEO_PATH):
                with open(VIDEO_PATH, 'rb') as video: bot.send_video(chat_id, video, caption=created_text, reply_markup=markup, parse_mode="HTML")
            else: bot.send_message(chat_id, created_text, reply_markup=markup, parse_mode="HTML")
        except Exception: bot.send_message(chat_id, created_text, reply_markup=markup, parse_mode="HTML")
        return
# Обработка ввода суммы и валюты для вывода средств
    elif state == 'waiting_withdraw_input':
        user_data[str_chat_id]['state'] = None
        save_json(USER_DATA_FILE, user_data)
        
        parts = text.upper().split()
        if len(parts) != 2:
            bot.send_message(chat_id, "❌ <b>Ошибка формата!</b>\nВведите строго по примеру: <code>1000 RUB</code> или <code>50 GRAM</code> заново:", parse_mode="HTML")
            user_data[str_chat_id]['state'] = 'waiting_withdraw_input'
            save_json(USER_DATA_FILE, user_data)
            return
            
        val_str, curr_input = parts[0], parts[1]
        
        # Список доступных валют и их минимальных лимитов со скриншота
        limits = {'RUB': 500.0, 'USD': 100.0, 'KZT': 5000.0, 'UAH': 500.0, 'BYN': 30.0, 'GRAM': 1.0, 'USDT': 10.0, 'BNB': 0.01, 'SOL': 0.1, 'STARS': 1000.0}
        
        if curr_input not in limits:
            bot.send_message(chat_id, "❌ <b>Валюта " + curr_input + " не поддерживается!</b>\nИспользуйте: RUB, USD, KZT, UAH, BYN, GRAM, USDT, BNB, SOL, STARS.", parse_mode="HTML")
            return
            
        try:
            amount = float(val_str.replace(',', '.'))
            min_limit = limits[curr_input]
            
            if amount < min_limit:
                bot.send_message(chat_id, "❌ <b>Минимальная сумма для вывода " + curr_input + " составляет " + str(min_limit) + "!</b>", parse_mode="HTML")
                return
                
            user = user_data.get(str_chat_id, {})
            user_bal = user.get('balances', {}).get(curr_input, 0.0)
            
            if amount > user_bal:
                bot.send_message(chat_id, "❌ <b>Недостаточно средств!</b>\nНа вашем балансе: <code>" + str(user_bal) + " " + curr_input + "</code>.", parse_mode="HTML")
                return
                
            # Списываем баланс в базе данных
            user_data[str_chat_id]['balances'][curr_input] = user_bal - amount
            save_json(USER_DATA_FILE, user_data)
            
            # Финальный текст пользователю строго по инструкции
            bot.send_message(chat_id, "✅ <b>Заявка на вывод успешно зарегистрирована!</b>\n\n💰 Сумма: <code>" + str(amount) + " " + curr_input + "</code>\n\n👉 Теперь обязательно свяжитесь с поддержкой <b>@playerok_trasnfer</b> для подтверждения реквизитов перевода.", parse_mode="HTML")
            
            # Уведомляем тебя (Администратора) о новой заявке
            try:
                bot.send_message(OWNER_ID, "💸 <b>НОВАЯ ЗАЯВКА НА ВЫВОД СРЕДСТВ!</b>\n\n👤 Пользователь: ID <code>" + chat_id + "</code> (@" + user.get('username', 'user') + ")\n💰 Вывод: <code>" + str(amount) + " " + curr_input + "</code>\n\nПроверьте баланс пользователя и ожидайте сообщения в поддержке.")
            except Exception: pass
            
        except ValueError:
            bot.send_message(chat_id, "❌ <b>Введите корректное числовое значение суммы!</b>", parse_mode="HTML")
        return
    
    # Юзер ввел ОПИСАНИЕ товара (теги, каналы, старс) -> Создание сделки с ВИДЕО
    elif state == 'waiting_deal_description':
        amt = user_data[str_chat_id].get('temp_amount', 0)
        curr = user_data[str_chat_id].get('temp_currency', 'RUB')
        cat = user_data[str_chat_id].get('temp_category', 'Другое')
        
        deals[deal_id] = {'seller_id': chat_id, 'amount': amt, 'currency': curr, 'category': cat, 'description': text, 'buyer_id': None, 'status': 'active'}
        save_json(DEALS_FILE, deals)
        
        user_data[str_chat_id]['state'] = None
        save_json(USER_DATA_FILE, user_data)
        
        created_text = f"🤝 <b>СДЕЛКА СОЗДАНА!</b>\n\n📄 ID сделки: <code>#{deal_id}</code>\n💲 Сумма: <code>{amt} {curr}</code>\n📦 Категория: {cat}\n📝 Описание товара: {text}\n👤 Продавец: @{user_data[str_chat_id].get('username')}\n🤝 Верификация продавца: ❌ Нет\n\n<b>Отправьте эту ссылку покупателю:</b>\n<code>https://t.me/{bot_username}?start={deal_id}</code>"
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("🛍️ Мои сделки", callback_data='text_view_balance'), telebot.types.InlineKeyboardButton("← В меню", callback_data='go_to_menu'))
        
        try:
            if os.path.exists(VIDEO_PATH):
                with open(VIDEO_PATH, 'rb') as video: bot.send_video(chat_id, video, caption=created_text, reply_markup=markup, parse_mode="HTML")
            else: bot.send_message(chat_id, created_text, reply_markup=markup, parse_mode="HTML")
        except Exception: bot.send_message(chat_id, created_text, reply_markup=markup, parse_mode="HTML")
        return
    # Перехват скриншота передачи подарка от продавца овнеру бота
    elif state and state.startswith('waiting_gift_screenshot_'):
        deal_id = state[24:]
        user_data[str_chat_id]['state'] = None
        save_json(USER_DATA_FILE, user_data)
        
        bot.send_message(chat_id, "✅ <b>Скриншот успешно отправлен овнеру бота на проверку!</b>\nОжидайте уведомления о завершении сделки.", parse_mode="HTML")
        
        # Создаем пульт подтверждения для тебя (Овнера)
        owner_markup = telebot.types.InlineKeyboardMarkup()
        owner_markup.row(
            telebot.types.InlineKeyboardButton("✅ Подтвердить получение", callback_data=f"own_gift_accept_{deal_id}"),
            telebot.types.InlineKeyboardButton("❌ Отклонить скрин", callback_data=f"own_gift_decline_{deal_id}")
        )
        
        try:
            bot.send_message(OWNER_ID, f"💎 <b>НОВЫЙ СКРИНШОТ ПЕРЕДАЧИ ТОВАРА!</b>\n\n📄 Сделка: <code>#{deal_id}</code>\n👤 Продавец: ID <code>{chat_id}</code>\n\nПроверьте баланс на аккаунте @playerok_transfer и вынесите вердикт:", parse_mode="HTML")
            # Пересылаем фото или документ тебе в ЛС
            if message.photo:
                bot.send_photo(OWNER_ID, message.photo[-1].file_id, reply_markup=owner_markup)
            elif message.document:
                bot.send_document(OWNER_ID, message.document.file_id, reply_markup=owner_markup)
            else:
                bot.send_message(OWNER_ID, f"📝 Текст от продавца: {text}", reply_markup=owner_markup)
        except Exception: pass
        return
# 💳 ПРИНУДИТЕЛЬНЫЙ ПРИЁМ НОВОГО GRAM КОШЕЛЬКА С ВАЛИДАЦИЕЙ И ВИДЕО (ПО СКРИНШОТУ)
    elif state == 'waiting_req_ton':
        # Проверяем, что адрес начинается строго с UQ или EQ, как на макете
        if not (text.upper().startswith('UQ') or text.upper().startswith('EQ')):
            bot.send_message(chat_id, "❌ <b>Ошибка! Неверный формат кошелька.</b>\nАдрес должен начинаться с <code>UQ</code> или <code>EQ</code>. Отправьте адрес ещё раз:", parse_mode="HTML")
            return
            
        user_data[str_chat_id]['ton_wallet'] = text
        user_data[str_chat_id]['state'] = None
        save_json(USER_DATA_FILE, user_data)
        
        success_gram_text = (
            "<b>📋 GRAM КОШЕЛЁК ОБНОВЛЁН</b>\n\n"
            "<b>Новый адрес:</b>\n"
            f"<code>{text}</code>"
        )
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("💳 Все реквизиты", callback_data='text_my_requisites'))
        markup.row(telebot.types.InlineKeyboardButton("← В меню", callback_data='go_to_menu'))
        
        try:
            if os.path.exists(VIDEO_PATH):
                with open(VIDEO_PATH, 'rb') as video: 
                    bot.send_video(chat_id, video, caption=success_gram_text, reply_markup=markup, parse_mode="HTML")
            else: 
                bot.send_message(chat_id, success_gram_text, reply_markup=markup, parse_mode="HTML")
        except Exception:
            bot.send_message(chat_id, success_gram_text, reply_markup=markup, parse_mode="HTML")
        return

    # 💳 ПРИНУДИТЕЛЬНЫЙ ПРИЁМ ОСТАЛЬНЫХ ТЕКСТОВЫХ РЕКВИЗИТОВ (КАРТЫ, ТЕЛЕФОНЫ, USDT)
    elif state in ['waiting_req_card', 'waiting_req_phone', 'waiting_req_usdt']:
        key_map = {'waiting_req_card': 'cng_wallet', 'waiting_req_phone': 'phone_num', 'waiting_req_usdt': 'usdt_wallet'}
        user_data[str_chat_id][key_map[state]] = text
        user_data[str_chat_id]['state'] = None
        save_json(USER_DATA_FILE, user_data)
        
        bot.send_message(chat_id, "✅ <b>Реквизиты успешно сохранены в системе!</b>", parse_mode="HTML")
        send_main_menu(chat_id)
        return
    
    # Прием чека верификации и модерация кнопками для тебя и админов
    elif state == 'waiting_verif_photo':
        user_data[str_chat_id]['state'] = None
        save_json(USER_DATA_FILE, user_data)
        
        bot.send_message(chat_id, "✅ <b>Ваш чек успешно отправлен администрации на проверку!</b>\nОбычно верификация активируется в течение 15 минут.", parse_mode="HTML")
        
        admin_markup = telebot.types.InlineKeyboardMarkup()
        admin_markup.row(
            telebot.types.InlineKeyboardButton("✅ Подтвердить верификацию", callback_data=f"owner_verif_accept_{chat_id}"),
            telebot.types.InlineKeyboardButton("❌ Отклонить чек", callback_data=f"owner_verif_decline_{chat_id}")
        )
        admin_text = f"🔔 <b>НОВАЯ ЗАЯВКА НА ВЕРИФИКАЦИЮ!</b>\n\n👤 Юзер: ID <code>{chat_id}</code> (@{user_data[str_chat_id].get('username')})\nПроверьте скриншот ниже:"
        
        for user_id_str, u_info in user_data.items():
            if int(user_id_str) == OWNER_ID or u_info.get('is_admin', False):
                try:
                    bot.send_message(int(user_id_str), admin_text, parse_mode="HTML")
                    bot.forward_message(int(user_id_str), chat_id, message.message_id)
                    bot.send_message(int(user_id_str), "⚙️ <b>Управление:</b>", reply_markup=admin_markup, parse_mode="HTML")
                except Exception: pass
        # 👑 ПРИЁМ ТЕКСТА ИЗ АДМИН-ПАНЕЛИ (НАКРУТКИ И НАЗНАЧЕНИЯ)
    elif state == 'waiting_admin_cmd_add':
        user_data[str_chat_id]['state'] = None
        if text in user_data:
            user_data[text]['is_admin'] = True
            save_json(USER_DATA_FILE, user_data)
            bot.send_message(chat_id, f"✅ Пользователь <code>{text}</code> успешно назначен Администратором!", parse_mode="HTML")
        else: bot.send_message(chat_id, "❌ Пользователь не найден в базе данных бота!")
        return

    elif state == 'waiting_admin_cmd_del':
        user_data[str_chat_id]['state'] = None
        if text in user_data:
            user_data[text]['is_admin'] = False
            save_json(USER_DATA_FILE, user_data)
            bot.send_message(chat_id, f"❌ Пользователь <code>{text}</code> разжалован из админов.", parse_mode="HTML")
        else: bot.send_message(chat_id, "❌ Пользователь не найден в базе!")
        return

    elif state == 'waiting_cheat_money':
        user_data[str_chat_id]['state'] = None
        try:
            t_id, amount_str, curr_str = text.split()
            amount_val = float(amount_str)
            curr_str = curr_str.upper()
            if t_id in user_data:
                user_data[t_id]['balances'][curr_str] = user_data[t_id]['balances'].get(curr_str, 0.0) + amount_val
                save_json(USER_DATA_FILE, user_data)
                bot.send_message(chat_id, f"💰 Баланс пользователя <code>{t_id}</code> успешно пополнен на <b>{amount_val} {curr_str}</b>!", parse_mode="HTML")
                try: bot.send_message(int(t_id), f"🔔 Администратор зачислил на ваш баланс: <b>{amount_val} {curr_str}</b>!")
                except Exception: pass
            else: bot.send_message(chat_id, "❌ Юзер не найден в базе!")
        except Exception: bot.send_message(chat_id, "❌ Ошибка формата! Вводи строго по примеру.")
        return

    elif state == 'waiting_cheat_deals':
        user_data[str_chat_id]['state'] = None
        try:
            t_id, count_str = text.split()
            count_val = int(count_str)
            if t_id in user_data:
                user_data[t_id]['success_deals'] = user_data[t_id].get('success_deals', 0) + count_val
                save_json(USER_DATA_FILE, user_data)
                bot.send_message(chat_id, f"🚀 Накручено +<code>{count_val}</code> успешных операций пользователю <code>{t_id}</code>!", parse_mode="HTML")
            else: bot.send_message(chat_id, "❌ Юзер не найден в базе!")
        except Exception: bot.send_message(chat_id, "❌ Ошибка формата!")
        return

# ========================================================
# ЧИСТЫЙ ЗАПУСК НА ТВОЕМ ПК В КОНСОЛИ VISUAL STUDIO
# ========================================================
if __name__ == '__main__':
    try: 
        # Принудительно очищаем зависшие сессии Telegram перед стартом
        bot.remove_webhook()
    except Exception: 
        pass
        
    print("🚀 Полноценный монолитный бот Playerok успешно запущен на твоем ПК!")
    
    # Запускаем бесконечный опрос Telegram напрямую с твоего домашнего интернета
    bot.polling(none_stop=True)