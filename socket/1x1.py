# imports
from threading import Thread
from random import randint
import socket
import time
# from memory_profiler import profile

# variáveis de condição de parada do servidor
threads_atendidas = 0
num_threads = 1
conectado = False
# controle de tempo
tempo = 0


# linha de execução da thread server
# @profile
def server(id):
    global threads_atendidas
    global tempo
    global conectado
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5000))
    server.listen(1)
    while(threads_atendidas < num_threads):
        connect, client = server.accept()
        conectado = True
        print('Cliente', client, 'conectado')
        while(True):
            msg = connect.recv(50)
            if(not msg):
                break
            print('O cliente', client, 'enviou a mensagem:', msg.decode())
        print('O cliente', client, 'finalizou sua conexão.')
        connect.close()
        tempo = time.time() - tempo
        print('Tempo de comunicação: {}ms'.format((tempo * 1000)))
        threads_atendidas += 1


# linha de execução da thread client
# @profile
def client(id):
    global tempo
    tempo = time.time()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = ('localhost', 5000)
    while(not conectado):
        try:
            client.connect(dest)
        except Exception:
            time.sleep(0.001)
    msg = str(randint(0, 100))
    print('Thread', id, 'enviou:', msg)
    client.send(msg.encode())
    client.close()


# criação das threads
tserver = Thread(target=server, args=(0, ))
tclient = Thread(target=client, args=(1, ))

# inicialização da thread server
tserver.start()
tclient.start()
