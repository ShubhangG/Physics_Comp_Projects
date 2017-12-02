EXENAME = neuralnuts
RM=rm -f
OBJS = NNmain.o
CC = g++-5 -std=c++14
DEBUG = -g
CFLAGS = -Wall -Wpedantic -Wextra -c -fopenmp $(DEBUG)
LFLAGS = -Wall $(DEBUG) 



all : $(EXENAME)

$(EXENAME) : $(OBJS)
	$(CC) $(LFLAGS) $(OBJS) -o $(EXENAME)

NNmain.o : NNmain.cpp NNets.h
	$(CC) $(CFLAGS) NNmain.cpp

clean:
	$(RM) *.o $(EXENAME)
