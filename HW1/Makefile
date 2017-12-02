EXENAME = covfefe
RM=rm -f
OBJS = main.o
CC = g++-5 -std=c++14
DEBUG = -g
CFLAGS = -Wall -Wpedantic -Wextra -c $(DEBUG)
LFLAGS = -Wall $(DEBUG)

all : $(EXENAME)

$(EXENAME) : $(OBJS)
	$(CC) $(LFLAGS) $(OBJS) -o $(EXENAME)

main.o : main.cpp cellstructs.h
	$(CC) $(CFLAGS) main.cpp

clean:
	$(RM) *.o $(EXENAME) snap_* shot_* coarse_* *.gz
