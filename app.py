from flask import Flask, render_template, request, redirect, url_for, flash
from SQLTable import *
import matplotlib.pyplot as plt
import os

app = Flask(__name__)



class Unknow:
    def __init__(self):
        self.prova = []

    def get_prova(self):
        return self.prova
class Editor:
    def __init__(self):
        self.prova = ['/edit']

    def get_prova(self):
        return self.prova
class Administrator(Editor):
    def __init__(self):
        super().__init__()
        self.prova += ['/statistik']

class No_prova_error(Exception):
    pass

def cheak_prova(url, prova_list):
    if url not in prova_list:
        raise No_prova_error("У вас нет прав для просмотра данной страницы")


db_config = {
    'user': 'j1007852',
    'password': 'el|N#2}-F8',
    'host': 'srv201-h-st.jino.ru',
    'database': 'j1007852_13423'
}

f = SQLTable(db_config, 'cites')
q = SQLTable(db_config, 'questions')

user_tupes = {'editor': Editor(),
              'administrator': Administrator()}

users = {'1': ('123', user_tupes['editor']),
         '2': ('123', user_tupes['administrator'])}

user = Unknow()

@app.route('/edit', methods=['GET', 'POST'])
def editor():
    global user
    try:
        print(user.get_prova())
        cheak_prova('/edit', user.get_prova())
    except:
        return render_template('no_pravo_error.html')
    else:
        if request.method == 'POST':
            content = request.form.get('content')
            if content in list(f.select_rows_by_column_value('name', f'{content}')['name']):
                massage = 'Город с таким названием уже есть в базе'
            else:
                f.insert_row({'name': f'{content}'})
                massage = 'Город добавлен'

            # Здесь вы можете сохранить содержимое, если нужно
            return render_template('index.html', content=massage)
        return render_template('index.html', content='Введите город')

@app.route('/statistik', methods=['GET', 'POST'])
def statistik():
    global user
    try:
        cheak_prova('/statistik', user.prova)
    except:
        return render_template('no_pravo_error.html')
    else:
        # Получаем данные из БД

        # Подготовка данных для графика
        names = list(q.select_where('', 'text')['text'])
        values = list(q.select_where('', 'date')['date'])

        # Создание графика
        # plt.figure(figsize=(10, 5))
        plt.bar(names, values)
        plt.title('Пример графика')
        plt.xlabel('Категории')
        plt.ylabel('Значения')
        plt.tight_layout()

        # Сохранение графика
        graph_path = os.path.join('static', 'templates/graph.png')
        plt.savefig('statik\graph.png')
        plt.close()
        sp = [[names[i], values[i]] for i in range(len(names))]

        return render_template('statistik.html', data=sp, graph_image='graph.png')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global user
    user = Unknow()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username][0] == password:
            user = users[username][1]
            return redirect(url_for('editor'))
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)