EXENAME = hippityhop
RM=rm -f
OBJS = main.o
CC = g++-5 -std=c++14
DEBUG = -g
CFLAGS = -Wall -Wpedantic -Wextra -c -fopenmp $(DEBUG)
LFLAGS = -Wall -fopenmp $(DEBUG) 
OMP_NUM_THREADS=4
export OMP_NUM_THREADS

all : $(EXENAME)

$(EXENAME) : $(OBJS)
	$(CC) $(LFLAGS) $(OBJS) -o $(EXENAME)

main.o : main.cpp hopnet.h
	$(CC) $(CFLAGS) main.cpp

clean:
	$(RM) *.o $(EXENAME)
