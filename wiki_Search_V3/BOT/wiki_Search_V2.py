import wikipedia
import telebot
import time
import os
import sys

TOKEN = ''
wikipedia.set_lang('ru')
bot = telebot.TeleBot(TOKEN)

is_processing = False
ADMIN_USERNAME = ''# @username

script_dir = os.path.dirname(os.path.abspath(__file__))
user_file_path = os.path.join(script_dir, '..', 'REQ', 'User_wiki.txt')  

def load_users():
    users = {}
    try:
        with open(user_file_path, 'r') as file:
            for line in file:
                try:
                    username, active, role = line.strip().split(', ')
                    username = username.lstrip('@')
                    users[username] = {
                        'active': active == 'True',
                        'admin': role == 'Admin'
                    }
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return users

def save_users(users):
    with open(user_file_path, 'w') as file:
        for username, data in users.items():
            role = 'Admin' if data['admin'] else 'User'
            file.write(f"@{username}, {data['active']}, {role}\n")

users = load_users()

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type in ['group', 'supergroup']:
        sending_mess = "<b>Привет!</b> Я бот для поиска информации на Wikipedia. Используйте команду /wiki [запрос] для поиска статей.\nДля просмотра всех доступных команд введите /help"
    else:
        sending_mess = "<b>Привет!</b> Это Ваш бот для поиска информации на Wikipedia, напишите тему по которой хотели бы найти статью...\nДля просмотра всех доступных команд введите /help"
    bot.send_message(message.chat.id, sending_mess, parse_mode='html')

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
Список доступных команд:
/start - Начать работу с ботом
/wiki [запрос] - Поиск информации в Wikipedia по вашему запросу

Для администраторов:
/bot *имя пользователя* add - Добавить пользователя
/bot *имя пользователя* kill - Заблокировать пользователя
/bot *имя пользователя* admin - Назначить пользователя администратором
/bot *имя пользователя* unadmin - Снять права администратора
/users - Показать список пользователей и их разрешения
"""
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['users'])
def list_users(message):
    sender = message.from_user.username
    if sender != ADMIN_USERNAME and (sender not in users or not users[sender].get('admin', False)):
        bot.send_message(message.chat.id, "У Вас нет прав для просмотра списка пользователей.")
        return
        
    user_list = "Список пользователей:\n\n"
    for username, data in users.items():
        status = "Активен" if data['active'] else "Заблокирован"
        admin_status = "Администратор" if data.get('admin', False) else "Пользователь"
        user_list += f"@{username} - {status} - {admin_status}\n"
    
    bot.send_message(message.chat.id, user_list)

@bot.message_handler(commands=['wiki'])
def wiki_command(message):
    global is_processing
    if is_processing:
        bot.send_message(message.chat.id, "Бот сейчас занят обработкой другого запроса...")
        return

    username = message.from_user.username
    if username not in users:
        bot.send_message(message.chat.id, "У Вас нет разрешения на использование этого бота.")
        return
    if not users[username]['active']:
        bot.send_message(message.chat.id, "Вы заблокированы ")
        return

    query = message.text[len('/wiki '):].strip()
    if not query:
        bot.send_message(message.chat.id, "Пожалуйста, укажите поисковый запрос после команды /wiki")
        return
        
    busy_message = bot.send_message(message.chat.id, "Поиск на Wikipedia...")
    
    is_processing = True 
    try:
        summary = wikipedia.summary(query)
        if message.chat.type in ['group', 'supergroup']:
            response = f"@{message.from_user.username}, вот что я нашел:\n\n{summary}\n\nСсылка на статью: {wikipedia.page(query).url}"
        else:
            response = f"{summary}\n\nСсылка на статью: {wikipedia.page(query).url}"
    except Exception as e:
        if message.chat.type in ['group', 'supergroup']:
            response = f"@{message.from_user.username}, произошла ошибка: {str(e)}"
        else:
            response = f"Произошла ошибка: {str(e)}"
    finally:
        is_processing = False
    
    bot.send_message(message.chat.id, response, parse_mode='html')
    bot.delete_message(message.chat.id, busy_message.message_id)

@bot.message_handler(commands=['bot'])
def admin_command(message):
    args = message.text.split()
    if len(args) < 3:
        bot.send_message(message.chat.id, "Использование: /bot @username команда")
        return
        
    username = args[1].lstrip('@')
    command = args[2]

    sender = message.from_user.username
    if sender != ADMIN_USERNAME and (sender not in users or not users[sender].get('admin', False)):
        bot.send_message(message.chat.id, "У Вас нет прав для выполнения этой команды.")
        return

    if command == 'add':
        if username in users:
            if users[username]['active']:
                bot.send_message(message.chat.id, "Пользователь уже получил разрешение.")
            else:
                users[username]['active'] = True
                save_users(users)
                bot.send_message(message.chat.id, f"Пользователь @{username} разблокирован.")
        else:
            users[username] = {'active': True, 'admin': False}
            save_users(users)
            bot.send_message(message.chat.id, f"Пользователь @{username} добавлен")
    
    elif command == 'kill':
        if username in users:
            users[username]['active'] = False
            save_users(users)
            bot.send_message(message.chat.id, f"Пользователь @{username} заблокирован.")
        else:
            bot.send_message(message.chat.id, "Пользователь не найден.")
    
    elif command == 'admin' and message.from_user.username == ADMIN_USERNAME:
        if username in users:
            users[username]['admin'] = True
            save_users(users)
            bot.send_message(message.chat.id, f"Пользователь @{username} назначен администратором.")
        else:
            users[username] = {'active': True, 'admin': True}
            save_users(users)
            bot.send_message(message.chat.id, f"Пользователь @{username} добавлен и назначен администратором.")
    
    elif command == 'unadmin' and message.from_user.username == ADMIN_USERNAME:
        if username in users:
            users[username]['admin'] = False
            save_users(users)
            bot.send_message(message.chat.id, f"У пользователя @{username} сняты права администратора.")
        else:
            bot.send_message(message.chat.id, "Пользователь не найден.")

bot.polling(non_stop=True)