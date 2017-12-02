#include "NNets.h"

NN::NN(std::vector<double> input,int hidden_layers,int nodes_per_layer,activ_func fin)
{	
	fx=fin;
	initialize(input,hidden_layers,nodes_per_layer);
}

void NN::initialize(std::vector<double>& input,int hidden_layers,int nodes_per_layer)
{	
	//int num_states = input.size() + hidden_layers*nodes_per_layer;
	init_weights(input.size(),hidden_layers, nodes_per_layer);

	//init_biases(input.size(),hidden_layers, nodes_per_layer);
	// for(int i=0;i<num_states;i++)
	// {	double r1=std::rand()/RAND_MAX;
	// 	bias.push_back(r1);
	// }

	init_states(input,hidden_layers, nodes_per_layer);

}

void NN::init_weights(int inpsize, int hidden_layers, int nodes_per_layer)
{	weights.resize(hidden_layers+2);
	
	weights[0].resize(inpsize*nodes_per_layer);
	for(int i=0;i<inpsize*nodes_per_layer;i++)
		weights[0][i]=(double)std::rand()/RAND_MAX;
	
	for(int i=1;i<hidden_layers;i++)
	{	weights[i].resize(nodes_per_layer*nodes_per_layer);
		for(int j=0;j<nodes_per_layer*nodes_per_layer;j++)
			weights[i][j]=(double)std::rand()/RAND_MAX;
	}
	weights[hidden_layers].resize(nodes_per_layer);
	for(int i=0;i<nodes_per_layer;i++)
		weights[hidden_layers][i]=(double)std::rand()/RAND_MAX;

}

double NN::activ(double x)
{
	if(fx==activ_func::Sigmoid)
		return 1.0/(1.0+exp(-x));
	else
		return (exp(x)-exp(-x))/(exp(x)+exp(-x));
}

void NN::init_states(std::vector<double>& input, int hidden_layers, int nodes_per_layer)
{	
	int inpsize = input.size();
	states.resize(hidden_layers+2);
	states[0].resize(inpsize);
	states[0] = input;

	bias.resize(hidden_layers+1);
	bias[0].resize(inpsize);
	states[1].resize(nodes_per_layer);
	for(int i=0;i<nodes_per_layer;i++)
	{	bias[0][i] = double(std::rand())/RAND_MAX;
		double sum=0;
		for(int k=0;k<inpsize;k++)
			sum+=weights[0][i+k*nodes_per_layer]*states[0][k];
		states[1][i] = activ(bias[0][i]+sum);
	}
	for(int i=1;i<hidden_layers;i++)
	{	{	states[i+1].resize(nodes_per_layer);
			bias[i].resize(nodes_per_layer);
			for(int j=0;j<nodes_per_layer;j++)
				{	double sum=0;
					bias[i][j]=double(std::rand())/RAND_MAX;
					for(int k=0;k<nodes_per_layer;k++)
						sum+=weights[i][j+k*nodes_per_layer]*states[i][k];
					states[i+1][j] = activ(bias[i][j]+sum);
				}

		}
	}
	double sum =0;
	for(int i=0;i<nodes_per_layer;i++)
	{	bias[hidden_layers].push_back(double(std::rand())/RAND_MAX);
		sum+=weights[hidden_layers][i]*states[hidden_layers][i];
	}
	states[hidden_layers+1].push_back(activ(sum+bias[hidden_layers][0]));
}

void NN::feedfwd()
{	int nodes_per_layer = states[1].size();
	int hidden_layers = states.size()-2;
	int inpsize = states[0].size();
	

	for(int i=0;i<nodes_per_layer;i++)
	{
		double sum=0;
		for(int k=0;k<inpsize;k++)
			sum+=weights[0][i+k*nodes_per_layer]*states[0][k];
		states[1][i] = activ(bias[0][i]+sum);
	}
	for(int i=1;i<hidden_layers;i++)
	{	{	states[i+1].resize(nodes_per_layer);
			for(int j=0;j<nodes_per_layer;j++)
				{	double sum=0;
					for(int k=0;k<nodes_per_layer;k++)
						sum+=weights[i][j+k*nodes_per_layer]*states[i][k];
					states[i+1][j] = activ(bias[i][j]+sum);
				}

		}
	}
	double sum =0;
	for(int i=0;i<nodes_per_layer;i++)
	{	sum+=weights[hidden_layers][i]*states[hidden_layers][i];
	}
	states[hidden_layers+1].push_back(activ(sum+bias[hidden_layers][0]));
}


void NN::backprop(int layer, int state, double prop_err)
{	//edge case
	if(layer==-1)
		return;
	//int num_states_in_layer = states[layer].size();
	//int num_weights_in_layer = weights[layer].size();
	for (uint i = 0; i < states[layer].size(); ++i)
	{	weights[layer][state+i*states[layer+1].size()]-=diffofS(states[layer+1][state])*prop_err*states[layer][i];
		backprop(layer-1,i,diffofS(states[layer+1][state])*prop_err*weights[layer][state+i*states[layer].size()]);
	}

	return;

}

double NN::diffofS(double s)
{
	if(fx==activ_func::Sigmoid)
		return s*(1-s);
	else
		return 1-s*s;
}

double NN::get_output()
{	uint size = states.size();
	return states[size-1][0];
}

double errfuncdiff(double y, NN& net)
{
	return y/(net.get_output()+0.0000001) - (1-y)/((1-net.get_output())+0.0000001);
}


int main()
{
	std::vector<double> v {0,1,1,0};
	// for(int i=0;i<4;i++)
	// 	v.push_back(std::rand()%2);
	NN neunet(v,2,2);
	double error;
	double y=5.0/pow(2,4);
	for(int i=0;i<4;i++)
	{	error = errfuncdiff(y,neunet);
		neunet.backprop(2,0,error);
		neunet.feedfwd();
		std::cout<<error<<"\n";
	}

	return 0;
}