from flask import Flask, render_template, request
from task5 import process

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_value = request.form['input_value']
        print(input_value)
        result = process(input_value)
        return render_template('output.html', input_value=input_value, result=result)
    else:
        return '''<html>
                    <head>
                        <title>Страница поиска</title>
                    </head>
                    <body>
                        <h1>Введите ваш запрос:</h1>
                        <form action="/" method="POST">
                            <input type="text" name="input_value">
                            <input type="submit" value="Отправить">
                        </form>
                    </body>
                </html>'''


if __name__ == '__main__':
    app.run()