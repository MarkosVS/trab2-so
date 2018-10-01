# -*- coding: utf-8 -*-
# imports
from threading import Thread
from random import randint
import time
# from memory_profiler import profile

# variável compartilhada
a = -1
# controle de tempo
tempo = 0


# linha de execução da thread que envia
# @profile
def writer(id):
    global a
    global tempo
    tempo = time.time()
    a = randint(0, 100)
    print('Thread', id, 'escreveu:', a)


# linha de execução da thread que recebe
# @profile
def reader(id):
    while(a == -1):
        pass

    global tempo
    print('Thread', id, 'leu:', a)
    tempo = time.time() - tempo
    print('Tempo de comunicação: {}ms'.format((tempo * 1000)))


# criação das threads
t1 = Thread(target=writer, args=(1, ))
t2 = Thread(target=reader, args=(2, ))

# inicialização da thread t1
t1.start()

# inicialização da thread t2
t2.start()
