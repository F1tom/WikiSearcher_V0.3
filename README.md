# WikiSearcher_V0.3
This Telegram bot allows users to search for information on Wikipedia directly through Telegram. The bot supports both private chats and group conversations, with built-in user management and administration features.

Features
- Wikipedia article search with direct links
- Support for both private and group chats
- User management system
- Administrative commands
- Russian Wikipedia as default source

Setup
1. Create a bot token through [@BotFather](https://t.me/BotFather)
2. Set environment variables:
   - `TOKEN`: Your Telegram bot token
   - `ADMIN_US`: Your Telegram username (without @) for admin access

Commands
- `/start` - Start the bot
- `/help` - Show available commands
- `/wiki [query]` - Search Wikipedia for information

Admin Commands
- `/bot @username add` - Add/unblock user
- `/bot @username kill` - Block user
- `/bot @username admin` - Grant admin rights
- `/bot @username unadmin` - Remove admin rights
- `/users` - Show user list and permissions


Описание
Этот Telegram бот позволяет пользователям искать информацию в Википедии прямо через Telegram. Бот поддерживает как личные чаты, так и групповые беседы, имеет встроенную систему управления пользователями и администрирования.

Возможности
- Поиск статей в Википедии с прямыми ссылками
- Поддержка личных и групповых чатов
- Система управления пользователями
- Административные команды
- Русская Википедия как источник по умолчанию

Установка
1. Создайте токен бота через [@BotFather](https://t.me/BotFather)
2. Установите переменные окружения:
   - `TOKEN`: Ваш токен Telegram бота
   - `ADMIN_US`: Ваш username в Telegram (без @) для доступа администратора

Команды
- `/start` - Запуск бота
- `/help` - Показать доступные команды
- `/wiki [запрос]` - Поиск информации в Википедии

Команды администратора
- `/bot @username add` - Добавить/разблокировать пользователя
- `/bot @username kill` - Заблокировать пользователя
- `/bot @username admin` - Назначить администратором
- `/bot @username unadmin` - Снять права администратора
- `/users` - Показать список пользователей и их разрешения
