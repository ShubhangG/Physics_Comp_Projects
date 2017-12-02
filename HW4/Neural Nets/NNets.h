#include <iostream>
#include <fstream>
#include <ctime>
#include <time.h>
#include <stdlib.h>
#include <math.h>
#include <vector>
#include <numeric>
#include <algorithm>

enum activ_func {Sigmoid, Tanh};

class NN
{	std::vector<std::vector<double> > states;
	std::vector<std::vector<double> > bias;
	std::vector<std::vector<double> > weights;
	activ_func fx; 
public:
	NN();
	NN(std::vector<double>,int,int,activ_func=Sigmoid);
	void initialize(std::vector<double>&,int,int);
	void init_weights(int, int, int);
	double activ(double);
	void init_states(std::vector<double>&, int, int);
	void backprop(int, int, double);
	void feedfwd();
	double diffofS(double);
	double get_output();
};

double errfuncdiff(double, NN&);