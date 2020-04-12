import sys
import string
import random
import copy
import math


class Job:
    pass
    
class Cola:
    def __init__(self):
        self.items = []
    
    def IsEmpty(self):
        return self.items == []
    
    def Enqueue(self, item):
        self.items.insert(0, item)

    def Dequeue(self):
        self.items.pop()

    def Peek(self):
        return self.items[len(self.items) - 1]

    def Count(self):
        return len(self.items)


def total_avg(l:[]):
    suma_turnaround = 0
    suma_response = 0
    for item in l:
        suma_turnaround += item[0]
        suma_response += item[1]
    return round( (suma_turnaround / len(l)) ,2), round( (suma_response / len(l)),2)

def check_blocks(jobs:[], quantum_size):
    for job in jobs:
        if(job.isblock):
            aux0 = job.blocks.items[job.blocks.Count() -1 ][0]
            aux1 = job.blocks.items[job.blocks.Count() -1 ][1]
            aux1 -= quantum_size
            job.blocks.items[job.blocks.Count() -1 ] = (aux0, aux1)

            if(job.blocks.items[job.blocks.Count() -1 ][1] <= 0):
                job.isblock = False
                job.blocks.Dequeue()
        

def turnaround(completion,arrival):
    return completion - arrival
    

def response(firstrun, arrival):
    return firstrun - arrival

def FIFO(jobs:[], quantum_size):
    time = 0
    queue = []
  
    for job in jobs:
        queue.append((job.arrival,job.id))
    queue = sorted(queue)

    for t in queue:
        job = jobs[t[1] - 1]
        
        if(time < job.arrival):
            time = job.arrival
        
        job.firstrun = time

        while(not job.blocks.IsEmpty):
            block = job.blocks.Dequeue()
            job.duration += (float)(block[1])

        
        count_quantum = math.ceil((job.duration / quantum_size))
        time += (count_quantum * quantum_size)
        job.fifo_turnaround = time - job.arrival
        job.fifo_response = job.firstrun - job.arrival

  
    return time


def STC(jobs:[], quantum_size):
    time = 0
    need_check_block = False
    

    count = 0
    while(count < len(jobs)):

        if(need_check_block):
            check_blocks(jobs,quantum_size)

        ready = []
        for job in jobs:
            if(job.arrival <= time and job.left > 0 and not job.isblock):
                ready.append((job.duration,job.id))
        ready = sorted(ready)

        if(len(ready) == 0):
            time += quantum_size
            need_check_block = True
            continue
            
        job = jobs[ready[0][1] - 1]

        if(not job.isfirstrun):
            job.isfirstrun = True
            job.firstrun = time
 
        if(not job.blocks.IsEmpty()):
            if((job.blocks.Peek()[0]) == time):
                job.isblock = True
                need_check_block = False
                continue


        job.left -= quantum_size
        time += quantum_size
        need_check_block = True

        if job.left <= 0:
            job.stc_turnaround = time - job.arrival
            job.stc_response = job.firstrun - job.arrival
            count += 1

    return time



def STCF(jobs:[], quantum_size):
    time = 0
    need_check_block = False
    

    count = 0
    while(count < len(jobs)):

        if(need_check_block):
            check_blocks(jobs,quantum_size)

        ready = []
        for job in jobs:
            if(job.arrival <= time and job.left > 0 and not job.isblock):
                ready.append((job.left,job.id))
        ready = sorted(ready)

        if(len(ready) == 0):
            time += quantum_size
            need_check_block = True
            continue
            
        job = jobs[ready[0][1] - 1]

        if(not job.isfirstrun):
            job.isfirstrun = True
            job.firstrun = time
 
        if(not job.blocks.IsEmpty()):
            if((job.blocks.Peek()[0]) == time):
                job.isblock = True
                need_check_block = False
                continue


        job.left -= quantum_size
        time += quantum_size
        need_check_block = True

        if job.left <= 0:
            job.stcf_turnaround = time - job.arrival
            job.stcf_response = job.firstrun - job.arrival
            count += 1

    return time


def RR(jobs:[], time_slice):
    time = 0
    need_check_block = False
    choose = []

     
    count = 0
    while(count < len(jobs)):

        choose = random.sample(jobs,len(jobs))
        empty_time_slice = True
        for job in choose:

            if(need_check_block):
                check_blocks(jobs,time_slice)

            if(job.arrival <= time and job.left > 0 and not job.isblock):

                if(not job.isfirstrun):
                    job.isfirstrun = True
                    job.firstrun = time

                if(not job.blocks.IsEmpty()):
                    if((job.blocks.Peek()[0]) == time):
                        job.isblock = True
                        need_check_block = False
                        continue

                empty_time_slice = False
                job.left -= time_slice
                time += time_slice
                need_check_block = True

                if job.left <= 0:
                    job.rr_turnaround = time - job.arrival
                    job.rr_response = job.firstrun - job.arrival
                    count += 1

            else:
                need_check_block = False
                continue    

        if(empty_time_slice):
            time += time_slice
            need_check_block = True

    return time



f = open(sys.argv[1])
#f = open("prueba.txt")
aux1 = ''
for line in f:
    if(line[0] == '#' or line[0] == '\n'):
        continue

    aux_line = ''
    for i in line:
        if(i == '#' or i == '\n'):
            break
        else:
            aux_line += i

    aux_line += '\n'
    aux1 += aux_line


aux1 = aux1.split('\n')      

aux = []        
for line in aux1:
    empty = " " * len(line)
    if (line == empty):
        continue
    aux.append(line)




jobs_count = (int)(aux[0])
quantum_size = (float)(aux[1])
aux_Ei = aux[2]
aux_Ei1 = aux_Ei.split(" ")
Ei = []
for ei in aux_Ei1:
    Ei.append(int(ei))


job = Job()

jobs = []
count = 1 
while(count <= jobs_count):
    line = aux[2 + count]
    line = line.split(" ")
    job = Job()
    job.id = count
    job.arrival = (float)(line[0])
    job.duration = (float)(line[1])
    job.left = job.duration
    job.isfirstrun = False
    job.blocks = Cola()
    job.isblock = False

    for i in range(2,len(line)):
        temp = line[i].split("-")
        io,iot = (float)(temp[0]),(float)(temp[1])
        job.blocks.Enqueue((io,iot))

    count += 1
    jobs.append(job)


fifo_jobs = copy.deepcopy(jobs) 
stc_jobs = copy.deepcopy(jobs)
stcf_jobs = copy.deepcopy(jobs)
rr_jobs = copy.deepcopy(jobs)

fifo_list = []
stc_list = []
stcf_list = []
rr_list = []

time_fifo = FIFO(fifo_jobs, quantum_size)
time_stc = STC(stc_jobs,quantum_size)
time_stcf = STCF(stcf_jobs,quantum_size)
time_rr = RR(rr_jobs, quantum_size)

for i in range(0, jobs_count):
    print( fifo_jobs[i].fifo_turnaround, fifo_jobs[i].fifo_response,
           stc_jobs[i].stc_turnaround, stc_jobs[i].stc_response,
           stcf_jobs[i].stcf_turnaround, stcf_jobs[i].stcf_response,
           rr_jobs[i].rr_turnaround, rr_jobs[i].rr_response
           )
    fifo_list.append( (fifo_jobs[i].fifo_turnaround, fifo_jobs[i].fifo_response) )
    stc_list.append( (stc_jobs[i].stc_turnaround, stc_jobs[i].stc_response) )
    stcf_list.append( (stcf_jobs[i].stcf_turnaround, stcf_jobs[i].stcf_response) )
    rr_list.append( (rr_jobs[i].rr_turnaround, rr_jobs[i].rr_response) )

print() 

for ei in Ei:
    temp_jobs = copy.deepcopy(jobs)
    RR(temp_jobs,ei)
    for i in range(0,jobs_count):
        print(temp_jobs[i].rr_turnaround, temp_jobs[i].rr_response)
    

fifo_avg_ta, fifo_avg_r = total_avg(fifo_list)
stc_avg_ta, stc_avg_r = total_avg(stc_list)
stcf_avg_ta, stcf_avg_r = total_avg(stcf_list)
rr_avg_ta, rr_avg_r = total_avg(rr_list)

print()

print(fifo_avg_ta, fifo_avg_r, time_fifo)
print(stc_avg_ta, stc_avg_r, time_stc)
print(stcf_avg_ta, stcf_avg_r, time_stcf)
print(rr_avg_ta, rr_avg_r, time_stc)
