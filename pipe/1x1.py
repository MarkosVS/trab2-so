# imports
from random import randint
import multiprocessing as mp
import time
# from memory_profiler import profile

# pipe
r, w = mp.Pipe()
# controle de tempo
tempo = mp.Value('d', 0.0)
# controle
num_mensagens = mp.Value('i', 0)


# linha de execução da thread que envia
# @profile
def writer(id):
    global tempo
    global num_mensagens
    n = randint(0, 100)
    tempo.value = time.time()
    w.send(n)
    print('Processo', id, 'escreveu:', n)
    num_mensagens.value += 1


# linha de execução da thread que recebe
# @profile
def reader(id):
    while(num_mensagens.value != 1):
        pass

    global tempo
    n = r.recv()
    tempo.value = time.time() - tempo.value
    print('Processo', id, 'leu o valor:', n)
    print('Tempo de comunicação: {}ms'.format((tempo.value * 1000)))


# criação dos processos
p1 = mp.Process(target=writer, args=(1, ))
p2 = mp.Process(target=reader, args=(2, ))

# inicialização do processo p1
p1.start()

# inicialização do processo p2
p2.start()
