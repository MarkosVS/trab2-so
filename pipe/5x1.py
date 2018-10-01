# imports
from random import randint
import multiprocessing as mp
import time
# from memory_profiler import profile

# pipes
# r, w = mp.Pipe()
# pipe[0] = r; pipe[1] = w
pipes = []
# controle dos tempos
tempos = []
for i in range(5):
    pipe = mp.Pipe()
    pipes.append(pipe)
    tempos.append(mp.Value('d', 0.0))

# controle
num_mensagens = mp.Value('i', 0)


# linha de execução da thread que envia
# @profile
def writer(id):
    global tempos
    global num_mensagens
    n = randint(0, 100)
    pipe = pipes[id]
    w = pipe[1]
    tempos[id].value = time.time()
    w.send(n)
    print('Processo', id, 'escreveu:', n)
    num_mensagens.value += 1


# linha de execução da thread que recebe
# @profile
def reader(id):
    while(num_mensagens.value != 5):
        pass

    global tempos
    for i in range(len(pipes)):
        pipe = pipes[i]
        r = pipe[0]
        n = r.recv()
        tempos[i].value = 1000 * (time.time() - tempos[i].value)
        print('Processo {} leu do Processo {} o valor: {}'.format(id, i, n))


for i in range(5):
    p = mp.Process(target=writer, args=(i, ))
    p.start()

pr = mp.Process(target=reader, args=(5, ))
pr.start()
pr.join()

media = 0
for i in range(len(tempos)):
    media += tempos[i].value

media /= len(tempos)
print('Tempo médio de comunicação: {}ms'.format(media))
