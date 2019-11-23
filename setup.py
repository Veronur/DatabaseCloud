import pymysql.cursors
import flask
import os


app = flask.Flask(__name__)


conn = pymysql.connect(host=str(os.environ['IPDataBase']),
                             user='root',
                             password='root',
                             db='Cloud',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

conn.autocommit(True)
@app.route('/Tarefa/', methods=["GET", "POST"])
def tarefas():
    with conn.cursor() as cursor:
            cursor.execute('SELECT * from Tarefas')
            res = cursor.fetchall()
    if flask.request.method == 'POST':
        
        task = flask.request.form['data']
        print("oi")
        with conn.cursor() as cursor:
            try:
                cursor.execute('INSERT INTO Tarefas (Nome) VALUES(%s)', (task))
            except pymysql.err.IntegrityError as e:
                print(e)
                raise ValueError(f'Não posso inserir {task} na tabela')
        with conn.cursor() as cursor:
            cursor.execute('SELECT * from Tarefas')
            res = cursor.fetchall()        
    return {'res':res}

@app.route('/Tarefa/<nome>', methods=["DELETE"])
def del_tarefas(nome):         
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM Tarefas WHERE Nome=%s', (nome))
            return 'Deleted'
        return 'Falha na delecao'



@app.route('/healthcheck/')
def healthcheck():
    return 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

