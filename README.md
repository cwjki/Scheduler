# Scheduler


## 1. Implementar un scheduler que tenga los 4 algoritmos vistos en clases
  - FIFO - first come, first serve
  - STF - shortest time first
  - STCF - shortest time to completoion first
  - RR - round robin

## 2. implementar ambas metricas
  - turnaround time
  - response time

## 3. el programa debe leer de la entrada standard e imprimir por la salida standard

## 4. el formato de entrada es

 - lineas que comienzan con simbolo # se ignoran
 - lineas en blanco o que solo contengan espacios tambien se ignoran
 - todo lo que venga despues del primer # de cada linea tambien se ignora
 - N # numero de jobs a ejecutar (N > 1 < 1000)
 - Q # quantum size, tiempo que dura cada time slice en sistema operativo, en milisegundos (interrupcion de reloj)
 - E1 E2 E3 ... # tiempos, multiplos de Q que significan el quantum de tiempo que el sistema operativo le va a dar a cada job
 - nota, tiene que haber una corrida completa para cada numero
 - a1 t1 io11-iot11 io12-iot12 
 - requerido: a1 = tiempo de arrival del job 1
 - requerido: t1 = tiempo de completamiento del job 1 (todo en milisegundos)
 - opcional: io11 = momento en el que va a ocurrir el 1er request IO (bloqueo) para el job 1
 - opcional: iot11 = tiempo que va a demorar el 1er bloqueso del job 1
...
an tn ion1 iotn1 ....

### a) el tiempo de duracion de un job (proceso) puede no ser multiplo de Q.

## 5. formato de salida

### a) las primeras N lineas deben tener 8 numeros cada una, separados por espacios
- turnaround time with fifo
- response time with fifo
- turnaround time with stf
- response time with stf
- turnaround time with stcf
- response time with stcf
- turnaround time with rr
- response time with rr

### b) luego una linea en blanco

### c) luego 4 lineas (fifo, stf, stcf, rr) con 3 numeros (en milisegundos, redondeando)
- average turnaround time
- average response time
- total time

## 6. si dos o mas jobs son iniciados a la misma vez, el scheduler debe escoger aleatoriamente cual de ellos se ejecuta primero. 
- el scheduler con una misma entrada, puede tener una salida diferente, en dependencia de la aleatoriedad mencionada anteriormente.

## 7. el programa debe terminar correctamente cuando termina de leer la entrada (y de imprimir la salida)