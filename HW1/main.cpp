#include "cellstructs.h"

cell::cell(int x, int y, state r): posx(x), posy(y), curr(r){} 	//Create cell at position (x,y)

cell::cell():posx(-1), posy(-2), curr(none) {}

cell& cell::operator=(const cell &rhs)
{	if (this == &rhs)
		return *this;
	int* posit= rhs.pos();
	this->update_pos(posit[0],posit[1]);
	this->update_state(rhs.stout());
	delete[] posit;
	return *this;	
	 
}
std::ostream& operator<<(std::ostream& out, const cell& rhs)
{	int* posit = rhs.pos();
	out<<posit[0]<<" "<<posit[1]<<" "<<rhs.stout()<<std::endl;
	delete[] posit;
	return out;
}
  
void cell::update_pos(int x, int y)
{	posx = x;
	posy = y; 
}

void cell::update_state(state r)
{	curr = r;
}

int* cell::pos() const
{	int* positions = new int[2];
	positions[0] = posx;
	positions[1] = posy;
	return positions;
}

state cell::stout() const
{	return curr;
}

std::vector<cell> setup_initial(int boxlen)
{	std::vector<cell> grid(boxlen*boxlen);
	for(int i=0;i<boxlen;i++)
	{	for(int j=0;j<boxlen;j++)
		{	grid[i+j*boxlen].update_pos(i,j);
			if(i<boxlen/2)
				grid[i+j*boxlen].update_state(cream);
			else
				grid[i+j*boxlen].update_state(coffee);

		}
	}

	return grid;
}

void swap(cell &cell1, cell &cell2)
{
	state tmp = cell1.stout();
	cell1.update_state(cell2.stout());
	cell2.update_state(tmp);

}

bool neighbour(std::vector<cell> &grid, int coord, int boxlen)
{	
	state curstate = grid[coord].stout();
	//corner cases
	if(coord%boxlen==0) //left edge
	{ 	switch(rand()%3)
		{		
			//look right
			case(0): if(grid[coord+1].stout()!=curstate)
				{	swap(grid[coord],grid[coord+1]);
					return true;	
				}
				break;
			case(1): if(coord==0){} //topleft corner
				//look up
				else
				{
					if(grid[coord-boxlen].stout()!=curstate)
					{	swap(grid[coord-boxlen],grid[coord]);
						return true;
					}	
				}
				break;
			case(2): if(coord==boxlen*(boxlen-1)){} //bottom left corner
			//look down
				else
				{	
					if(grid[coord+boxlen].stout()!=curstate)
					{	swap(grid[coord+boxlen],grid[coord]);
						return true;
					}
				
				}
				break;
		}	
		return false;
	}
	else if((coord+1)%boxlen==0)	//right edge
	{ 	//look left
	
		switch(rand()%3)
		{	case 0: if(grid[coord-1].stout()!=curstate)
				{	swap(grid[coord-1],grid[coord]);
					return true;
				}	
				break;

		 	case 1: if(coord==boxlen-1){} //top right corner
		 		else
		 		//look up
			 	{	
			 	       	if(grid[coord-boxlen].stout()!=curstate)
			 	       	{	swap(grid[coord-boxlen],grid[coord]);
			 	       		return true;
			 	       	}
			 	}
				break;

			case 2: if(coord==boxlen*boxlen-1){} //bottom right corner
				else
				//look down
				{
				
						if(grid[coord+boxlen].stout()!=curstate)
						{	swap(grid[coord+boxlen],grid[coord]);
							return true;
						}
				}
				break;
		}
		return false;
	}
	else if(coord<boxlen) //top edge
	{	switch(rand()%3)
		{
				//look down
			case 0:	if(grid[coord+boxlen].stout()!=curstate)
				{	swap(grid[coord+boxlen],grid[coord]);
					return true;
				}
				break;
				//look left	
				//We are not doing corner edge cases because handled before
			case 1:	if(grid[coord-1].stout()!=curstate)
				{	swap(grid[coord-1],grid[coord]);
					return true;
				}
				break;
				//look right
			case 2:	if(grid[coord+1].stout()!=curstate)
				{	swap(grid[coord+1],grid[coord]);
					return true;
				}
				break;
		}
		return false;
	}
	else if(coord>=boxlen*(boxlen-1))	//bottom edge
	{	switch(rand()%3)
		{		//look up
			case 0: 	if(grid[coord-boxlen].stout()!=curstate)
					{	swap(grid[coord-boxlen],grid[coord]);
						return true;
					}
				 	break;
			case 1:	//look left
					if(grid[coord-1].stout()!=curstate)
					{	swap(grid[coord-1],grid[coord]);
						return true;
					}
				 	break;
			case 2:	//look right
					if(grid[coord+1].stout()!=curstate)
					{	swap(grid[coord+1],grid[coord]);
						return true;
					}
					break;
		}
		return false;
		
	}
	else
	{	switch(rand()%4)
		{
				//look right
			case 0:	if(grid[coord+1].stout()!=curstate)
				{	swap(grid[coord],grid[coord+1]);
					return true;
				}
				break;
				//look left
			case 1:	if(grid[coord-1].stout()!=curstate)
				{	swap(grid[coord-1],grid[coord]);
					return true;
				}
				break;
				//look up
			case 2:	if(grid[coord-boxlen].stout()!=curstate)
				{	swap(grid[coord-boxlen],grid[coord]);
					return true;
				}
				break;
				//look down
			case 3:	if(grid[coord+boxlen].stout()!=curstate)
				{	swap(grid[coord+boxlen],grid[coord]);
					return true;
				}
				break;
		}
	}
	return false;
}

void automate(std::vector<cell> &grid)
{	
	int coord;
	int len = grid.size();		//get array length
	int i=0;
	while(i<100000)
	{	
		coord = rand()%len;
		if(neighbour(grid,coord,sqrt(len)))
			i++;
	
		 
	}

}



int main()
{	srand(time(NULL)); 		//set time seed			
	int boxlen;
	std::cout<<"Enter the size of the square box: \n";
	std::cin>>boxlen;
	std::ofstream snapshot;
	std::vector<cell> grid = setup_initial(boxlen);
	snapshot.open("snap_0.txt");
	for(int p=0;p<boxlen*boxlen;p++)
	{	snapshot<<grid[p];
	}
	snapshot.close();
	snapshot.clear();
	for(int i=1;i<=200;i++)
	{	std::string str="snap_"+std::to_string(i)+".txt";
		automate(grid);
		snapshot.open(str);
		for(int j=0;j<boxlen*boxlen;j++)
		{	snapshot<<grid[j];
			
		}
		snapshot.close();
		snapshot.clear();
	}
	return 0;
	
}
