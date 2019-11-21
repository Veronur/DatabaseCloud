import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 5000)
db = client.tarefas
collection = db.tarefas


def adicionaTarefas(nome):
    tarefa={"Nome": "{}".format(nome)}
    print(tarefa)
    try:
        collection.insert_one(tarefa).inserted_id
    except:
        print('Falha ao adicionar')
    
def listaTarefas():
    ret=[]
    try:
        cursor = collection.find({})
        for document in cursor:
            ret.append(document)    
        return ret
    except:
        print('Falha na listagem')

def removeTarefas(nome):
    try:
        collection.remove({"Nome": "{}".format(nome)})
    except:
        print('Falha na delecao')

print(listaTarefas())
adicionaTarefas('asdsad')
print(listaTarefas())
removeTarefas('asdsad')
print(listaTarefas())