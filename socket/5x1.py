# imports
from threading import Thread
from random import randint
import socket
import time
# from memory_profiler import profile

# variáveis de condição de parada do servidor
threads_atendidas = 0
num_threads = 5
tempos = [0, 0, 0, 0, 0]
conectados = [[0, False], [0, False], [0, False], [0, False], [0, False]]


# linha de execução da thread servidor
# @profile
def server(id):
    global threads_atendidas
    global tempos
    global conectados
    cliente_id = -1
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5000))
    server.listen(5)
    while(threads_atendidas < num_threads):
        connect, client = server.accept()
        print('+ Cliente', client[1], 'conectado')
        flag = False
        while(not flag):
            for i in range(len(conectados)):
                if(conectados[i][0] == client[1]):
                    conectados[i][1] = True
                    cliente_id = i
                    flag = True

        while(True):
            msg = connect.recv(50)
            msg = msg.decode()
            if(not msg):
                break
            print('+ O cliente', client[1], 'enviou a mensagem:', msg)
        connect.close()
        tempos[cliente_id] = 1000 * (time.time() - tempos[cliente_id])
        print('+ O cliente', client[1], 'finalizou sua conexão.\n')
        threads_atendidas += 1


# linha de execução da thread cliente
# @profile
def client(id):
    global tempos
    global conectados
    tempos[id] = time.time()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = ('localhost', 5000)
    while(not conectados[id][1]):
        try:
            client.connect(dest)
            conectados[id][0] = client.getsockname()[1]
            print('- Thread {} conectada.'.format(id))
            print('- ID de cliente:', conectados[id][0])
        except Exception:
            time.sleep(0.001)

    msg = str(randint(0, 100))
    print('- Thread', id, 'enviou:', msg)
    client.send(msg.encode())
    client.close()


# criação e inicialização da thread servidor
tserver = Thread(target=server, args=(5000, ))
tserver.start()

# criação e inicialização das threads cliente
for i in range(num_threads):
    tclient = Thread(target=client, args=(i, ))
    tclient.start()
    tclient.join()
    time.sleep(0.5)

media = 0
for i in range(len(tempos)):
    media += tempos[i]

media /= len(tempos)
print('Tempo médio de comunicação: {}ms'.format(media))
