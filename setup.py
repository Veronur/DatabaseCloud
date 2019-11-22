import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client.tarefas
collection = db.tarefas


def adicionaTarefas(nome):
    tarefa={"Nome": "{}".format(nome)}
    #print(tarefa)
    try:
        collection.insert_one(tarefa)
    except:
        print('Falha ao adicionar')
    
def buscaTarefa(nome):
    ret=[]
    try:
        cursor = collection.find_one({"Nome": "{}".format(nome)})
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

print(buscaTarefa('asdsad'))
adicionaTarefas('asdsad')
print(buscaTarefa('asdsad'))
removeTarefas('asdsad')
print(buscaTarefa('asdsad'))