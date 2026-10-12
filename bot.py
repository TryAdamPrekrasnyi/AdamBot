import telebot
from telebot import types
import os

API_TOKEN = '8987263887:AAFcoPeMM0TWj53P8DVUCdAHU7wuvyYfezA'
ADMIN_ID = 6481109309
CARD_NUMBER = '2200 7021 2852 6402'
SBP_PHONE = 'СБП не подключён'
TG_CONTACT_1 = '@adamWyou'
REVIEWS_CHAT = 'https://t.me/otzvadamstuduo'
STUDIO_CHANNEL = 'https://t.me/+UjOv-DWM79xkYzRi'
COUNTER_FILE = 'counter.txt'
ALL_USERS_FILE = 'users.txt'
ADMINS_FILE = 'admins.txt'
APPEALS_FILE = 'appeals.txt'
BANNED_FILE = 'banned.txt'
PROJECTS_FILE = 'projects.txt'
MODS_FILE = 'mods.txt'

def read_file(name):
    if not os.path.exists(name): return []
    with open(name, 'r') as f:
        return [l.strip() for l in f if l.strip()]

def write_file(name, lines):
    with open(name, 'w') as f:
        f.write('\n'.join(lines))

def append_file(name, line):
    with open(name, 'a') as f:
        f.write(line + '\n')

def get_counter():
    c = read_file(COUNTER_FILE)
    return int(c[0]) if c else 0

def save_counter(n):
    write_file(COUNTER_FILE, [str(n)])

def gen_order_id():
    n = get_counter() + 1
    save_counter(n)
    return str(n)

def save_user(uid):
    users = set(read_file(ALL_USERS_FILE))
    users.add(str(uid))
    write_file(ALL_USERS_FILE, list(users))

def get_users():
    return read_file(ALL_USERS_FILE)

def get_admins():
    a = [str(ADMIN_ID)]
    a.extend(read_file(ADMINS_FILE))
    return list(set(a))

def is_admin(uid):
    return str(uid) in get_admins()

def add_admin(uid):
    a = read_file(ADMINS_FILE)
    if str(uid) not in a:
        a.append(str(uid))
        write_file(ADMINS_FILE, a)

def is_banned(uid):
    return str(uid) in read_file(BANNED_FILE)

def ban_user(uid):
    b = read_file(BANNED_FILE)
    if str(uid) not in b:
        b.append(str(uid))
        write_file(BANNED_FILE, b)

def get_projects():
    base = [
        "ULTIMATE 2.5 (BR) AMX|699|BQACAgIAAxkBAAPgasoAARkbQ57qHP1FJuQPkbRuvNl-AAIquAACKMxRSqzXI1ECpAMMPQQ",
        "ULTIMATE 2.5 (BR) AMX+PWN|899|BQACAgIAAxkBAAPeasn_sigbh5wKqoyjdCyobWcV45AAAia4AAIozFFKiq9G4-A3kKU9BA",
    ]
    return base + read_file(PROJECTS_FILE)

def get_mods():
    base = [
        "ULTIMATE 2.5 (BR) AMX|599|BQACAgIAAxkBAAPgasoAARkbQ57qHP1FJuQPkbRuvNl-AAIquAACKMxRSqzXI1ECpAMMPQQ",
        "ULTIMATE 2.5 (BR) AMX+PWN|799|BQACAgIAAxkBAAPeasn_sigbh5wKqoyjdCyobWcV45AAAia4AAIozFFKiq9G4-A3kKU9BA",
    ]
    return base + read_file(MODS_FILE)

bot = telebot.TeleBot(API_TOKEN)
user_data = {}
pending_orders = {}
pending_files = {}
send_file_to = {}
support_waiting = {}
broadcast_waiting = {}
admin_waiting = {}
reply_waiting = {}
ban_waiting = {}

WELCOME_TEXT = (
    '🎩 Добро пожаловать в Adam Studio!\n\n'
    '📁 Проекты — готовые сборки под ключ.\n'
    '🔧 Моды — готовые файлы.\n'
    '💬 Создание форума — скоро.\n\n'
    'Выбери, что тебе нужно 👇'
)

TERMS_TEXT = (
    '📜 ПОЛЬЗОВАТЕЛЬСКОЕ СОГЛАШЕНИЕ\n\n'
    '1. Общие положения\n1.1. Используя бота, вы соглашаетесь с условиями.\n'
    '1.2. Бот продаёт моды и проекты для CRMP.\n1.3. Услуги «как есть».\n\n'
    '2. Оплата\n2.1. Оплата переводом на карту.\n2.2. В комментарии укажи НОМЕР ЗАКАЗА.\n\n'
    '3. Возврат\n3.1. До передачи файла.\n3.2. После — нет.\n\n'
    '4. Ответственность\n4.1. Администрация не отвечает за действия пользователя.\n\n'
    '5. Конфиденциальность\n5.1. Данные только для заказа.\n\n'
    f'📩 {TG_CONTACT_1}'
)

@bot.message_handler(content_types=['document'])
def handle_doc(message):
    uid = message.from_user.id
    if is_banned(uid): return
    if uid == ADMIN_ID and uid in send_file_to:
        d = send_file_to.pop(uid)
        try:
            bot.send_document(d['target'], message.document.file_id, caption=f'📦 Заказ {d["order_id"]}. Спасибо!\n⭐ {REVIEWS_CHAT}')
            bot.send_message(ADMIN_ID, f'✅ Отправлено {d["target"]}')
        except Exception as e:
            bot.send_message(ADMIN_ID, f'❌ {e}')
        return
    if uid == ADMIN_ID:
        bot.send_message(ADMIN_ID, f'📎 file_id:\n\n{message.document.file_id}')

@bot.message_handler(commands=['start'])
def start(message):
    if is_banned(message.from_user.id):
        bot.send_message(message.chat.id, '❌ Вы забанены.')
        return
    save_user(message.from_user.id)
    m = types.InlineKeyboardMarkup(row_width=1)
    m.add(
        types.InlineKeyboardButton('📁 Проекты', callback_data='projects'),
        types.InlineKeyboardButton('🔧 Моды', callback_data='mods'),
        types.InlineKeyboardButton('⭐ Отзывы', callback_data='reviews'),
        types.InlineKeyboardButton('🆘 Поддержка', callback_data='support'),
        types.InlineKeyboardButton('✉️ Свяжись с нами', callback_data='contact'),
    )
    bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=m)

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if not is_admin(message.from_user.id): return
    m = types.InlineKeyboardMarkup(row_width=1)
    m.add(
        types.InlineKeyboardButton('📢 Рассылка', callback_data='broadcast'),
        types.InlineKeyboardButton('📩 Обращения', callback_data='appeals'),
        types.InlineKeyboardButton('👑 Выдать админку', callback_data='give_admin'),
        types.InlineKeyboardButton('🚫 Забанить', callback_data='ban'),
        types.InlineKeyboardButton('✅ Разбанить', callback_data='unban'),
        types.InlineKeyboardButton('➕ Добавить проект', callback_data='add_proj'),
        types.InlineKeyboardButton('➕ Добавить мод', callback_data='add_mod'),
        types.InlineKeyboardButton('📊 Статистика', callback_data='stats'),
    )
    bot.send_message(message.chat.id, '👑 Админ-панель:', reply_markup=m)

@bot.callback_query_handler(func=lambda c: True)
def cb(call):
    uid = call.from_user.id
    if is_banned(uid): return
    save_user(uid)

    if call.data == 'projects':
        m = types.InlineKeyboardMarkup(row_width=1)
        projects = get_projects()
        for i, p in enumerate(projects):
            name, price, fid = p.split('|')
            m.add(types.InlineKeyboardButton(f'🔥 {name} — {price}₽', callback_data=f'buy_proj|{i}'))
        m.add(types.InlineKeyboardButton('⬅️ Назад', callback_data='back'))
        bot.edit_message_text('📁 Выбери проект:', call.message.chat.id, call.message.message_id, reply_markup=m)

    elif call.data == 'mods':
        m = types.InlineKeyboardMarkup(row_width=1)
        mods = get_mods()
        for i, mod in enumerate(mods):
            name, price, fid = mod.split('|')
            m.add(types.InlineKeyboardButton(f'🔧 {name} — {price}₽', callback_data=f'buy_mod|{i}'))
        m.add(types.InlineKeyboardButton('⬅️ Назад', callback_data='back'))
        bot.edit_message_text('🔧 Выбери мод:', call.message.chat.id, call.message.message_id, reply_markup=m)

    elif call.data == 'reviews':
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(types.InlineKeyboardButton('⭐ Перейти', url=REVIEWS_CHAT), types.InlineKeyboardButton('⬅️ Назад', callback_data='back'))
        bot.edit_message_text('⭐ Отзывы', call.message.chat.id, call.message.message_id, reply_markup=m)

    elif call.data == 'support':
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton('📜 Соглашение', callback_data='terms'),
            types.InlineKeyboardButton('💬 Написать в поддержку', url=f'https://t.me/{TG_CONTACT_1[1:]}'),
            types.InlineKeyboardButton('⬅️ Назад', callback_data='back'),
        )
        bot.edit_message_text('🆘 Поддержка:', call.message.chat.id, call.message.message_id, reply_markup=m)

    elif call.data == 'terms':
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(types.InlineKeyboardButton('⬅️ Назад', callback_data='support'))
        bot.edit_message_text(TERMS_TEXT, call.message.chat.id, call.message.message_id, reply_markup=m)

    elif call.data == 'contact':
        support_waiting[uid] = True
        bot.edit_message_text('✉️ Напиши обращение сюда.', call.message.chat.id, call.message.message_id)

    elif call.data.startswith('buy_proj|'):
        idx = int(call.data.split('|')[1])
        projects = get_projects()
        if idx >= len(projects): return
        name, price, fid = projects[idx].split('|')
        user_data[uid] = {'lot': name, 'price': int(price), 'fid': fid}
        bot.edit_message_text(
            '⚠️ Нужны данные:\n\n1. Логин/почта от аккаунта\n2. Пароль\n3. Название проекта\n4. Ссылка на хост\n\n'
            '🔒 Данные не утекут.\n\nОтправь одним сообщением, каждое с новой строки.',
            call.message.chat.id, call.message.message_id
        )
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, get_project_data)

    elif call.data.startswith('buy_mod|'):
        idx = int(call.data.split('|')[1])
        mods = get_mods()
        if idx >= len(mods): return
        name, price, fid = mods[idx].split('|')
        oid = gen_order_id()
        pending_files[uid] = {'id': oid, 'name': name, 'price': int(price), 'fid': fid}
        text = f'🧾 НОМЕР: {oid}\n💰 Сумма: {price}₽\n💳 Карта: {CARD_NUMBER}\n📱 СБП: {SBP_PHONE}\n\n⚠️ В комментарии укажи: {oid}'
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(types.InlineKeyboardButton('✅ Я оплатил', callback_data=f'modpaid|{oid}'))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=m)
        am = types.InlineKeyboardMarkup(row_width=1)
        am.add(types.InlineKeyboardButton('✅ Подтвердить', callback_data=f'modok|{oid}'))
        bot.send_message(ADMIN_ID, f'🔔 ЗАКАЗ\n🧾 {oid}\n📦 {name}\n💰 {price}₽\n👤 {uid}', reply_markup=am)

    elif call.data.startswith('modpaid|'):
        if uid not in pending_files: return
        bot.answer_callback_query(call.id, '✅ Жди подтверждения.')
        bot.send_message(call.message.chat.id, f'✅ Принято!\n🧾 {pending_files[uid]["id"]}')

    elif call.data.startswith('modok|'):
        oid = call.data.split('|')[1]
        for u, o in list(pending_files.items()):
            if str(o['id']) == str(oid):
                try:
                    bot.send_document(u, o['fid'], caption=f'📦 Заказ {oid}. Спасибо!\n⭐ {REVIEWS_CHAT}')
                    bot.send_message(ADMIN_ID, f'✅ Отправлено {u}')
                except Exception as e:
                    bot.send_message(ADMIN_ID, f'❌ {e}')
                bot.answer_callback_query(call.id, '✅ Отправлено.')
                return

    elif call.data.startswith('confirm_pay|'):
        if not is_admin(uid): return
        oid = call.data.split('|')[1]
        for u, o in list(pending_orders.items()):
            if o['id'] == oid:
                bot.send_message(u, f'✅ Заказ взят! Ожидайте, в течение 5 минут отправим проект.\n\n🧾 {oid}')
                am = types.InlineKeyboardMarkup(row_width=1)
                am.add(types.InlineKeyboardButton('📤 Отправить проект', callback_data=f'sendproj|{u}|{oid}'))
                bot.send_message(ADMIN_ID, f'✅ Подтверждено. Заказ {oid}.', reply_markup=am)
                pending_orders.pop(u, None)
                bot.answer_callback_query(call.id, '✅ Заказ взят.')
                return

    elif call.data.startswith('sendproj|'):
        if not is_admin(uid): return
        _, target, oid = call.data.split('|')
        send_file_to[ADMIN_ID] = {'target': int(target), 'order_id': oid}
        bot.answer_callback_query(call.id, '📎 Скинь файл.')
        bot.send_message(ADMIN_ID, f'📎 Скинь проект для {oid}.')

    elif call.data == 'broadcast':
        if not is_admin(uid): return
        broadcast_waiting[ADMIN_ID] = True
        bot.send_message(ADMIN_ID, '📢 Напиши сообщение.')

    elif call.data == 'appeals':
        if not is_admin(uid): return
        appeals = read_file(APPEALS_FILE)
        if not appeals:
            bot.send_message(ADMIN_ID, '📭 Обращений нет.')
            return
        for line in appeals:
            if '|' in line:
                u, text = line.split('|', 1)
                m = types.InlineKeyboardMarkup(row_width=1)
                m.add(types.InlineKeyboardButton('✉️ Ответить', callback_data=f'reply|{u}'))
                bot.send_message(ADMIN_ID, f'📩 От {u}:\n\n{text}', reply_markup=m)

    elif call.data.startswith('reply|'):
        if not is_admin(uid): return
        reply_waiting[ADMIN_ID] = call.data.split('|')[1]
        bot.send_message(ADMIN_ID, f'✉️ Напиши ответ.')

    elif call.data == 'give_admin':
        if uid != ADMIN_ID: return
        admin_waiting[ADMIN_ID] = True
        bot.send_message(ADMIN_ID, '👑 Отправь ID или @юзернейм.')

    elif call.data == 'ban':
        if not is_admin(uid): return
        ban_waiting[ADMIN_ID] = True
        bot.send_message(ADMIN_ID, '🚫 Отправь ID для бана.')

    elif call.data == 'unban':
        if not is_admin(uid): return
        bot.send_message(ADMIN_ID, '✅ Отправь ID для разбана.')
        bot.register_next_step_handler_by_chat_id(ADMIN_ID, do_unban)

    elif call.data == 'add_proj':
        if not is_admin(uid): return
        bot.send_message(ADMIN_ID, '➕ Отправь: Название | Цена | file_id')
        bot.register_next_step_handler_by_chat_id(ADMIN_ID, do_add_project)

    elif call.data == 'add_mod':
        if not is_admin(uid): return
        bot.send_message(ADMIN_ID, '➕ Отправь: Название | Цена | file_id')
        bot.register_next_step_handler_by_chat_id(ADMIN_ID, do_add_mod)

    elif call.data == 'stats':
        if not is_admin(uid): return
        bot.send_message(ADMIN_ID, f'📊 Юзеров: {len(get_users())}\nЗаказов: {get_counter()}\nПроектов: {len(get_projects())}\nМодов: {len(get_mods())}')

    elif call.data == 'back':
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton('📁 Проекты', callback_data='projects'),
            types.InlineKeyboardButton('🔧 Моды', callback_data='mods'),
            types.InlineKeyboardButton('⭐ Отзывы', callback_data='reviews'),
            types.InlineKeyboardButton('🆘 Поддержка', callback_data='support'),
            types.InlineKeyboardButton('✉️ Свяжись с нами', callback_data='contact'),
        )
        bot.edit_message_text(WELCOME_TEXT, call.message.chat.id, call.message.message_id, reply_markup=m)

def get_project_data(message):
    uid = message.from_user.id
    if uid not in user_data: return
    lines = message.text.split('\n')
    if len(lines) < 4:
        bot.send_message(message.chat.id, '❌ Нужно 4 строки.')
        bot.register_next_step_handler_by_chat_id(message.chat.id, get_project_data)
        return
    host_login, host_pass, project_name, host_link = [l.strip() for l in lines[:4]]
    oid = gen_order_id()
    pending_orders[uid] = {
        'id': oid, 'lot': user_data[uid]['lot'], 'price': user_data[uid]['price'],
        'login': host_login, 'pass': host_pass, 'project': project_name, 'host': host_link,
    }
    text = f'🧾 НОМЕР: {oid}\n💰 Сумма: {user_data[uid]["price"]}₽\n💳 Карта: {CARD_NUMBER}\n📱 СБП: {SBP_PHONE}\n\n⚠️ В комментарии укажи: {oid}'
    m = types.InlineKeyboardMarkup(row_width=1)
    m.add(types.InlineKeyboardButton('✅ Я оплатил', callback_data=f'projpaid|{oid}'))
    bot.send_message(message.chat.id, text, reply_markup=m)
    am = types.InlineKeyboardMarkup(row_width=1)
    am.add(types.InlineKeyboardButton('✅ Подтвердить оплату', callback_data=f'confirm_pay|{oid}'))
    bot.send_message(ADMIN_ID, f'🔔 ЗАКАЗ\n🧾 {oid}\n📦 {user_data[uid]["lot"]}\n💰 {user_data[uid]["price"]}₽\n👤 {uid}\n🔑 {host_login}\n🔒 {host_pass}\n📁 {project_name}\n🌐 {host_link}', reply_markup=am)

@bot.callback_query_handler(func=lambda c: c.data.startswith('projpaid|'))
def projpaid(call):
    uid = call.from_user.id
    if uid not in pending_orders: return
    bot.answer_callback_query(call.id, '✅ Жди подтверждения.')
    bot.send_message(call.message.chat.id, f'✅ Принято!\n🧾 {pending_orders[uid]["id"]}')

@bot.message_handler(func=lambda m: m.from_user.id in support_waiting)
def handle_support(message):
    uid = message.from_user.id
    support_waiting.pop(uid, None)
    append_file(APPEALS_FILE, f'{uid}|{message.text}')
    bot.send_message(ADMIN_ID, f'📩 От {uid}:\n\n{message.text}')
    bot.send_message(uid, '✅ Отправлено.')

@bot.message_handler(func=lambda m: m.from_user.id in broadcast_waiting)
def do_broadcast(message):
    broadcast_waiting.pop(message.from_user.id, None)
    ok = 0
    for u in get_users():
        try:
            bot.send_message(int(u), f'📢 {message.text}')
            ok += 1
        except: pass
    bot.send_message(ADMIN_ID, f'✅ Отправлено: {ok}')

@bot.message_handler(func=lambda m: m.from_user.id in reply_waiting)
def do_reply(message):
    target = reply_waiting.pop(message.from_user.id, None)
    if not target: return
    try:
        bot.send_message(int(target), f'📩 Ответ:\n\n{message.text}')
        bot.send_message(ADMIN_ID, '✅ Отправлено.')
    except Exception as e:
        bot.send_message(ADMIN_ID, f'❌ {e}')

@bot.message_handler(func=lambda m: m.from_user.id in admin_waiting)
def do_give_admin(message):
    admin_waiting.pop(message.from_user.id, None)
    try:
        new_admin = int(message.text.strip().replace('@', ''))
        add_admin(new_admin)
        bot.send_message(ADMIN_ID, f'✅ {new_admin} теперь админ.')
    except Exception as e:
        bot.send_message(ADMIN_ID, f'❌ {e}')

@bot.message_handler(func=lambda m: m.from_user.id in ban_waiting)
def do_ban(message):
    ban_waiting.pop(message.from_user.id, None)
    try:
        target = int(message.text.strip().replace('@', ''))
        ban_user(target)
        bot.send_message(ADMIN_ID, f'✅ {target} забанен.')
    except Exception as e:
        bot.send_message(ADMIN_ID, f'❌ {e}')

def do_unban(message):
    try:
        target = int(message.text.strip().replace('@', ''))
        banned = read_file(BANNED_FILE)
        if str(target) in banned:
            banned.remove(str(target))
            write_file(BANNED_FILE, banned)
            bot.send_message(ADMIN_ID, f'✅ {target} разбанен.')
        else:
            bot.send_message(ADMIN_ID, f'❌ {target} не в бане.')
    except Exception as e:
        bot.send_message(ADMIN_ID, f'❌ {e}')

def do_add_project(message):
    try:
        name, price, fid = message.text.split('|')
        append_file(PROJECTS_FILE, f'{name.strip()}|{price.strip()}|{fid.strip()}')
        bot.send_message(ADMIN_ID, f'✅ Проект «{name}» добавлен.')
    except Exception as e:
        bot.send_message(ADMIN_ID, f'❌ Ошибка: {e}')

def do_add_mod(message):
    try:
        name, price, fid = message.text.split('|')
        append_file(MODS_FILE, f'{name.strip()}|{price.strip()}|{fid.strip()}')
        bot.send_message(ADMIN_ID, f'✅ Мод «{name}» добавлен.')
    except Exception as e:
        bot.send_message(ADMIN_ID, f'❌ Ошибка: {e}')

bot.polling(none_stop=True)
