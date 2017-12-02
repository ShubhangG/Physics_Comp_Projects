#include <iostream>
#include <fstream>
#include <ctime>
#include <time.h>
#include <stdlib.h>
#include <math.h>
#include <vector>
#include <numeric>
#include <algorithm>

class hopnet{
	std::vector<int> states;
	std::vector<double> bias;
	std::vector<std::vector<double>> weights;
public:
	hopnet(); 												  //default constructor
	hopnet(int);											  //constructor with size	
	hopnet(std::vector<int>);								  //constructor with states
	hopnet(const hopnet&);								      //copy constructor
	void set_memweight(std::vector<std::vector<int>>&);       //set weights from out
	//void set_inpstates(std::vector<int>);
	void initialize(int);									  //initialize states/weights
	void flip_state(int);									  //flip spin
	float get_E();											  //get energy
	float Ediff(int);										  //get energy difference
	void transition(float); 				  				  //Metropolis update
	std::vector<std::vector<double>> get_w() const; 		  //get weights of net
	std::vector<int> get_states() const;					  //get states of net
	std::vector<double> get_bias() const;						  //get biases of net
};

void printstates(std::vector<int>);							  //print all states
void printweights(std::vector<std::vector<double>>);		  //print all weights
void part1page1();											  //first part of proj, get graph
std::vector<int> readstate(std::string);					  //read states from file
void dump2file(hopnet&, std::string);						  //dump network to file
void statecorruptor(hopnet&,int);					  		  //corrupt at k spots
void runMC(hopnet&);										  //Runs Metropolis
void hammingdist(std::vector<std::vector<int>>&);
void part2page1(std::vector<std::vector<int>>&);
int calc_dist(std::vector<int>&, std::vector<int>&);
std::vector<int> mkrandvec(int);