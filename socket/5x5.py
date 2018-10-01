# imports
from threading import Thread
from random import randint
import socket
import time
# from memory_profiler import profile

# quantidade de threads cliente / servidor
num_threads = 5
# tempos
# servidor[i] = [cliente, tempo]
servidor = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
tempos = [servidor, servidor, servidor, servidor, servidor]


# linha de execução do servidor
# @profile
def server(id):
    global tempos
    # criação da porta
    port = 5000 + id
    # contador de mensagens recebidas
    mensagens_recebidas = 0
    # criação do socket
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', port))
        server.listen(5)
        print("Servidor {} iniciado - Porta: {}".format(id, port))

        # inicio da execução
        try:
            while(mensagens_recebidas < num_threads):
                connect, client = server.accept()
                print("Cliente conectado")
                msg = connect.recv(128)
                msg = msg.decode()
                if(not msg):
                    continue

                print("Servidor {} recebeu: {}".format(id, msg))
                mensagens_recebidas += 1
                connect.close()
        except Exception as e:
            print("Falha de conexão na porta {}".format(port))
        finally:
            connect.close()
    except Exception as e:
        print("Não foi possível inicializar o servidor {}".format(port))
    finally:
        connect.close()
        for i in range(len(tempos[id])):
            tempos[id][i][1] = time.time() - tempos[id][i][1]
        print("++++ Servidor {} concluído ++++".format(id))


# linha de execução do cliente
# @profile
def client(id):
    global tempos
    # mensagem que será enviada
    msg = str(randint(0, 100))
    # contador de mensagens enviadas
    mensagens_enviadas = 0
    # criação dos sockets
    sockets = []
    for i in range(num_threads):
        tempos[i][id % 5][1] = time.time()
        sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        tempos[i][id % 5][0] = sockets[-1].getsockname()[1]

    # inicio da execução
    print("Cliente {} iniciou".format(id))
    while(mensagens_enviadas < num_threads):
        # configura a porta
        port = 5000 + mensagens_enviadas
        # tenta enviar a mensagem
        try:
            sockets[mensagens_enviadas].connect(('localhost', port))
            sockets[mensagens_enviadas].send(msg.encode())
            print("Cliente {} enviou {} na porta {}".format(id, msg, port))
            mensagens_enviadas += 1
        except Exception:
            pass

    print("Cliente {} concluído".format(id))


# criação e inicialização da thread servidor
for i in range(num_threads):
    tserver = Thread(target=server, args=(i, ))
    tserver.start()


# criação e inicialização das threads cliente
for i in range(num_threads, 10):
    tclient = Thread(target=client, args=(i, ))
    tclient.start()
    tclient.join()

# cálculo da média do tempo
media = 0
for servidor in tempos:
    for cliente in servidor:
        media += cliente[1]

media *= 1000
media /= 25
print('Tempo médio de comunicação: {}ms'.format(media))
