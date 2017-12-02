#include <iostream>
#include <fstream>
#include <time.h>
#include <stdlib.h>
#include <math.h>
#include <vector>

enum state {coffee,cream,none};
class cell{
	int posx;
	int posy;
	state curr;
public:
	cell();
	cell(int, int, state); 	        //Create cell at position (x,y)
	void update_pos(int, int);	//Update position of cell
	void update_state(state);	//Update state of cell
	int* pos() const;		//returns pair of x and y value
	state stout() const;		//returns the output of the current state
	cell& operator=(const cell& rhs);	//To be able to use cell1=cell2
	
};

std::ostream& operator<<(std::ostream& out, const cell& rhs);	//for outputting to file
std::vector<cell> setup_initial(int boxlen);//Setup the initial state of coffee cup
void automate(std::vector<cell> &grid);	//Start the mixing
void swap(cell &cell1, cell&cell2);	//swapping two cells
bool neighbour(std::vector<cell> &grid, int coord, int boxlen); //checking if the neighbour is opposite state and swapping if needed



