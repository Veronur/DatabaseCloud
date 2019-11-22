import pymysql.cursors
import flask


app = flask.Flask(__name__)


conn = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='Cloud',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

conn.autocommit(True)
@app.route('/Tarefa/', methods=["GET", "POST"])
def tarefas():
    if flask.request.method == 'POST':
        
        task = flask.request.form['data']
        print("oi")
        with conn.cursor() as cursor:
            try:
                cursor.execute('INSERT INTO Tarefas (Nome) VALUES(%s)', (task))
            except pymysql.err.IntegrityError as e:
                print(e)
                raise ValueError(f'Não posso inserir {task} na tabela')
    # elif flask.request.method == 'GET':

        with conn.cursor() as cursor:
            cursor.execute('SELECT * from Tarefas')
            res = cursor.fetchall()
            # print (res)
            # nomes = tuple(x[0] for x in res)
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