import telebot
import datetime
from SQLTable import *
bot = telebot.TeleBot('1689403620:AAH3kI43vntgRqkMQhZobB7S_x-tZ_oofuQ')

db_config = {
    'user': 'j1007852',
    'password': 'el|N#2}-F8',
    'host': 'srv201-h-st.jino.ru',
    'database': 'j1007852_13423'
}


f = SQLTable(db_config, 'cites')
data = list(map(lambda x: x.lower(), list(f.select_where('', 'name')['name'])))

q = SQLTable(db_config, 'questions')


cites_for_game = {}
for i in data:
    if i[0] not in cites_for_game:
        cites_for_game[i[0]] = [i]
    else:
        cites_for_game[i[0]].append(i)

game = False
cites = cites_for_game.copy()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    question_data = {'text': message.text,
                     'time': datetime.datetime.now().time(),
                     'date': datetime.datetime.now().date()}
    with open('report.txt', 'a') as f:
        f.write(f'{datetime.datetime.now()}\n')
        f.write('User: ' + message.text + '\n')
        global game, cites
        if game:
            city = message.text.lower()
            if city == 'стоп':
                game = False
                cites = cites_for_game.copy()
            elif city in cites[city[0]]:
                del cites[city[0]][cites[city[0]].index(city)]
                if len(cites[city[-1]]) != 0:
                    bot.send_message(message.from_user.id, cites[city[-1]][0])
                    del cites[city[-1]][0]
                else:
                    question_data['ans'] = 'Сдаюсь, ты победил'
                    bot.send_message(message.from_user.id, "Сдаюсь, ты победил")
                    f.write("Bot: Сдаюсь, ты победил\n")
                    game = False
                    cites = cites_for_game.copy()
            else:
                question_data['ans'] = 'Этого города нет в нашей игре'
                bot.send_message(message.from_user.id, "Этого города нет в нашей игре")
                f.write("Bot: Этого города нет в нашей игре\n")
        elif message.text == "Города":
            game = True
            question_data['ans'] = 'Ничинай'
            bot.send_message(message.from_user.id, "Ничинай")
            f.write("Bot: Начинай\n")
        else:
            question_data['ans'] = "Для игры напиши 'Города'"
            bot.send_message(message.from_user.id, "Для игры напиши 'Города'")
            f.write("Bot: Для игры напиши 'Города'\n")
    q.insert_row(question_data)

bot.polling(none_stop=True, interval=0)
