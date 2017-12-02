#include<iostream>
#include<ctime>
#include<math.h>
#include<vector>
#include<fstream>
#include<bitset>
#include<algorithm>
#include "input.h"

int get_E(std::vector<int>&);//Get Energy of ising configuration
double get_m(std::vector<int>&);//Get m of ising configuration
void transition(std::vector<int>&,float,int);//does a random spin flip
std::vector<int> initialize(int,int,bool=1);//initializes a random ising grid bool=1 or all spin ups bool=0
void snapshot(std::vector<int>& ,int ,std::string);//produces a snapshot of ising grid
long int bin2dec(std::vector<int>); //converts binary ising grid to decimal value
void probdistributions(int, int, double); //produces prob distribution
void Eallconfigs(int,int,double); //produces all 2^N configurations and computes E
int calc_Ediff(std::vector<int>&,int,int); //calculate E without looping over grid
void m_calculation(int, int,double,std::string,int=1000); //Writes all m values to file for each MCMC run
void sim_anneal(int lx, int ly,double beta,int count);  //Simulated annealing