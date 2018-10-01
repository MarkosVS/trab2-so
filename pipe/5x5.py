# imports
from random import randint
import multiprocessing as mp
import time
# from memory_profiler import profile

# pipes
# r, w = mp.Pipe()
# pipe[0] = r; pipe[1] = w
pipes = []
tempos = []
for i in range(25):
    pipe = mp.Pipe()
    pipes.append(pipe)
    tempos.append(mp.Value('d', 0.0))


# linha de execução da thread que envia
# @profile
def writer(id):
    global tempos
    start = id * 5
    for i in range(start, start + 5):
        n = randint(0, 100)
        pipe = pipes[i]
        w = pipe[1]
        tempos[i].value = time.time()
        w.send(n)
        print('Processo', id, 'escreveu:', n)


# linha de execução da thread que recebe
# @profile
def reader(id):
    global tempos
    count = 0
    for i in range(len(pipes)):
        if((id % 5) == (i % 5)):
            pipe = pipes[i]
            r = pipe[0]
            n = r.recv()
            tempos[i].value = time.time() - tempos[i].value
            print('Processo', id, 'leu o valor:', n, 'do processo', count)
            count += 1

    print('Processo {} concluiu sua execução'.format(id))


# criação dos processos
for i in range(5):
    p = mp.Process(target=writer, args=(i, ))
    p.start()
    p.join()

for i in range(5, 10):
    pr = mp.Process(target=reader, args=(i, ))
    pr.start()
    pr.join()


media = 0
for i in range(len(tempos)):
    media += tempos[i].value

media *= (1000.0 / len(tempos))
print('Tempo médio de comunicação: {}ms'.format(media))
