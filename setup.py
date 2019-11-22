import pymysql.cursors
import flask


app = flask.Flask(__name__)


conn = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='Cloud',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


@app.route('/Tarefa/<nome>', methods=["GET", "DELETE", "POST"])
def tarefas(nome):
    if flask.request.method == 'POST':
        with conn.cursor() as cursor:
            try:
                cursor.execute('INSERT INTO Tarefas (Nome) VALUES(%s)', (nome))
            except pymysql.err.IntegrityError as e:
                print(e)
                raise ValueError(f'Não posso inserir {nome} na tabela')
    elif flask.request.method == 'DELETE':            
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM Tarefas WHERE idUser=%s', (nome))
    elif flask.request.method == 'GET':

            with conn.cursor() as cursor:
                cursor.execute('SELECT * from Tarefas')
                res = cursor.fetchall()
                nomes = tuple(x[0] for x in res)
                return nomes

@app.route('/healthcheck/')
def healthcheck():
    return 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')