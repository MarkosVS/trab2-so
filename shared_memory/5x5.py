# imports
from threading import Thread
from random import randint
import time
# from memory_profiler import profile

# variável compartilhada
a = []
# controle de tempo
tempos = []
# leituras concluidas
threads_concluidas = 0


# linha de execução da thread que envia
# @profile
def writer(id):
    global a
    global tempos
    inicio = time.time()
    tempos.append([inicio, inicio, inicio, inicio, inicio])
    a.append(randint(0, 100))
    print('Thread', id, 'escreveu:', a[-1])


# linha de execução da thread que recebe
# @profile
def reader(id):
    global tempos
    global threads_concluidas
    while(len(a) != 5):
        pass

    for i in range(len(a)):
        print('Thread', id, 'leu da Thread', i, 'o valor:', a[i])
        tempos[i][id % 5] = time.time() - tempos[i][id % 5]

    threads_concluidas += 1


# criação e inicialização das threads escritoras
for n in range(5):
    t = Thread(target=writer, args=(n, ))
    t.start()

# criação e inicialização das threads leitoras
for n in range(5, 10):
    tr = Thread(target=reader, args=(n, ))
    tr.start()

while(threads_concluidas < 5):
    pass

media = 0
for i in range(len(tempos)):
    media += sum(tempos[i])

media *= (1000.0 / 25)
print('Tempo médio de comunicação: {}ms'.format(media))
