import telebot  # импортируем telebot
from config import token  # из файла config.py забираем нашу переменную с токеном
from telebot import types  # импортируем types для работы с кнопками
import sqlite3  # импортируем sqlite3 для работы с базой данных

# создаем экземпляр бота
bot = telebot.TeleBot(token)


# Создаем базу данных: id, user_name1, user_surname1, user_birthdate1, user_address1, user_mob1, user_email1
@bot.message_handler(commands=["start"])
def start(message):
    conn = sqlite3.connect('db1.sql')
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS db1 (id int auto_increment primary key, user_name1 TEXT, user_surname1 TEXT, '
        'user_birthdate1 TEXT, user_address1 TEXT, user_mob1 TEXT, user_email1 TEXT)')
    conn.commit()
    cur.close()
    conn.close()

    # прописываем приветствие, после которого пойдет анкетирование из шести вопросов
    bot.send_message(message.chat.id, 'СПАСИБО, ЧТО ОБРАТИЛИСЬ К НАМ!'
                                      ' \n Инжиниринговая компания ElectricProfi Gbr \n предлагает возможность трудоустройства'
                                      ' \n для электриков-профессионалов в Германии.'
                                      ' \n Электромонтажные работы. Официальное трудоустройство.'
                                      ' \n Комфортные условия проживания, \n достойная и своевременная оплата труда \n от 3000EUR,'
                                      ' \n возможность получения авансов 1 раз в неделю.'
                                      ' \n Приветствуются навыки общения на немецком языке.'
                                      ' \n Если вы готовы к работе, пожалуйста, напишите ваши данные.'
                                      ' \n Наш менеджер свяжется с вами. \n '
                                      ' \n ИТАК:')

    # отправляем пользователю сообщение для ввода имени
    bot.send_message(message.chat.id, 'Введите ваше имя: ')
    # переход к функции user_name1
    bot.register_next_step_handler(message, user_name1)


def user_name1(message):
    # переменные делаем глобальными, так как будем использовать их вне конкретной одной функции
    global name1
    name1 = message.text.strip()  # strip - позволяет убрать лишние введенные пользователем пробелы
    # отправляем пользователю сообщение для ввода фамилии
    bot.send_message(message.chat.id, 'Введите вашу фамилию: ')
    # переход к функции user_surname1
    bot.register_next_step_handler(message, user_surname1)


def user_surname1(message):
    global surname1
    surname1 = message.text.strip()
    # отправляем пользователю сообщение для ввода даты рождения
    bot.send_message(message.chat.id, 'Введите вашу дату, месяц, год рождения: ')
    # переход к функции user_birthdate1
    bot.register_next_step_handler(message, user_birthdate1)


def user_birthdate1(message):
    global birthdate1
    birthdate1 = message.text.strip()
    # отправляем пользователю сообщение для ввода адреса
    bot.send_message(message.chat.id, 'Введите ваш адрес проживания: ')
    # переход к функции user_address1
    bot.register_next_step_handler(message, user_address1)


def user_address1(message):
    global address1
    address1 = message.text.strip()
    # отправляем пользователю сообщение для ввода номера телефона
    bot.send_message(message.chat.id, 'Введите ваш номер телефона: ')
    # переход к функции user_mob1
    bot.register_next_step_handler(message, user_mob1)


def user_mob1(message):
    global mob1
    mob1 = message.text.strip()
    # отправляем пользователю сообщение для ввода e-mail
    bot.send_message(message.chat.id, 'Введите ваш e-mail: ')
    # переход к функции user_email1
    bot.register_next_step_handler(message, user_email1)


def user_email1(message):
    global email1
    email1 = message.text.strip()
    # высылаем пользователю после регистрации сообщение
    bot.send_message(message.chat.id,
                     'Вы зарегистрированы в нашей системе. \n Наш менеджер свяжется с вами в ближайшее время.'
                     ' \n СПАСИБО ЗА РЕГИСТРАЦИЮ И ГОТОВНОСТЬ К РАБОТЕ!')

    conn = sqlite3.connect('db1.sql')
    cur = conn.cursor()

    #  заносим данные, введенные пользователем в базу данных
    cur.execute(
        f"INSERT INTO db1 (user_name1, user_surname1, user_birthdate1, user_address1, user_mob1, user_email1) "
        f"VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (
            name1, surname1, birthdate1, address1, mob1, email1))

    conn.commit()
    cur.close()
    conn.close()


# Вывод данных по логину и паролю в чате для администратора
@bot.message_handler(commands=["abrakadabra"])
def abrakadabra(message):
    bot.send_message(message.chat.id, 'Введите пароль: ')


@bot.message_handler(commands=["password"])
def password(message):
    # создание кнопки LIST OF EMPLOYEES при правильно введенном пароле: /password
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('LIST OF EMPLOYEES', callback_data='db1'))
    # callback_data срабатывает при нажатии на кнопку
    bot.send_message(message.chat.id, 'LIST OF EMPLOYEES', reply_markup=markup)

    # reply_markup указывает, что кнопка выводится вместе с сообщением


    # вывод данных в чат
    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        conn = sqlite3.connect('db1.sql')
        cur = conn.cursor()

        cur.execute('SELECT * FROM db1')
        db1 = cur.fetchall()

        # для вывода данных в чат проходим циклом по базе данных и заносим все данные в переменную info
        info = ''
        for el in db1:
            info += f' \n Имя: {el[1]}, \n Фамилия: {el[2]},  \n Дата рождения: {el[3]},  \n Адрес: {el[4]},  ' \
                    f'\n Телефон: {el[5]},  \n E-mail: {el[6]} \n'

        cur.close()
        conn.close()

        # отправляем данные в переменной info в чат пользователю с правами администратора
        bot.send_message(call.message.chat.id, info)

# Запускаем бота
bot.polling(none_stop=True)
