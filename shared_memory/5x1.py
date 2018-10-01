# imports
from threading import Thread
from random import randint
import time
# from memory_profiler import profile

# variável compartilhada
a = []
# controle de tempo
tempos = []


# linha de execução da thread que envia
# @profile
def writer(id):
    global a
    global tempos
    tempos.append(time.time())
    a.append(randint(0, 100))
    print('Thread', id, 'escreveu:', a[-1])


# linha de execução da thread que recebe
# @profile
def reader(id):
    while(len(a) != 5):
        pass

    for i in range(len(a)):
        print('Thread', id, 'leu da Thread', i, 'o valor:', a[i])
        tempos[i] = time.time() - tempos[i]


# criação e inicialização das threads escritoras
for n in range(5):
    t = Thread(target=writer, args=(n, ))
    t.start()

# criação da thread leitora (tr)
tr = Thread(target=reader, args=(5, ))

# inicialização da thread tr
tr.start()
tr.join()

media = 0
for i in range(len(tempos)):
    media += tempos[i]

media *= 1000
media /= len(tempos)
print('Tempo médio de comunicação: {}ms'.format(media))
