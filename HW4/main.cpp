#include "hopnet.h"

hopnet::hopnet()
{}

hopnet::hopnet(std::vector<int> v)
{	
	states=std::move(v);
	for(uint i=0;i<states.size();++i)
	{	double rf =std::rand()/RAND_MAX;
		bias.push_back(rf);
	}
}

void hopnet::set_memweight(std::vector<std::vector<int>>& imgs)
{
	weights.resize(imgs[0].size());
	for(uint l=0;l<imgs[0].size();l++)
		weights[l].resize(imgs[0].size());
	
	for(uint i=0;i<imgs[0].size();i++)
	{	
		for(uint j=i;j<imgs[0].size();j++)
		{	double weighsum= 0;
			for(auto& n: imgs)
				weighsum+=n[i]*n[j];

			weights[i][j]=weights[j][i]=weighsum/imgs.size();
			//(img1[i]*img1[j]+img2[i]*img2[j])/2.0;
		}

		weights[i][i] = 0;
	}

} 

void hopnet::initialize(int size)
{   for(int i=0;i<size;i++)
	{	int r = std::rand()%2;
		double rf = std::rand()/RAND_MAX;
		if(r==0) r= -1;
		states.push_back(r);	//-1 is spin down,1 is up
		bias.push_back(rf);
	}
	weights.resize(size);
	for(int l=0;l<size;l++)
		weights[l].resize(size);

	for(int k=0;k<size;k++)
	{	for(int j=k;j<size;j++)
		{	weights[k][j]=weights[j][k]=(double)std::rand()/RAND_MAX;
			
		}	
		weights[k][k] = 0;
	}

}

hopnet::hopnet(int s)
{
	initialize(s);
}

hopnet::hopnet(const hopnet &obj)
{
	states = obj.get_states();
	weights = obj.get_w();
	bias = obj.get_bias();
}

void hopnet::flip_state(int i)
{
	if(states[i]==1) states[i] = -1;
	else states[i] = 1;
}

float hopnet::get_E()
{	float E=0;
	for(uint i=0;i<states.size();i++)
	{	for(uint j=i+1;j<states.size();j++)
			E+=-0.5*weights[i][j]*states[i]*states[j];
		E+=bias[i]*states[i];
	}
	return E;
}

void hopnet::transition(float beta)
{	int rcoord = std::rand()%(int)states.size();
	float ediff = Ediff(rcoord);
	double A = std::min(1.0,(double)exp(-1.0*beta*ediff));
	if(A>double(std::rand())/RAND_MAX){
		flip_state(rcoord);
	}
}

float hopnet::Ediff(int state)
{	float Ediff=0;	
	for(uint j=0;j<states.size();j++)
		{	if((int)j==state) Ediff+=states[state]*bias[j];
			else Ediff+= -0.5*weights[state][j]*states[j]*states[state];

		}
	return -2.0*Ediff;
}

std::vector<std::vector<double>> hopnet::get_w() const
{	return weights;
}
std::vector<int> hopnet::get_states() const
{
	return states;
}
std::vector<double> hopnet::get_bias() const
{
	return bias;
}

void printstates(std::vector<int> states)
{
	for(auto s:states)
		std::cout<<s<<" ";
}

void printweights(std::vector<std::vector<double>> w)
{
	for(uint i=0;i<w[0].size();i++)
	{	for(uint j=0;j<w[0].size();j++)
			std::cout<<w[i][j]<<" ";
		std::cout<<"\n";
	}
}	
std::vector<int> readstate(std::string infile)
{	
	std::ifstream inf;
	inf.open(infile);
	if(!inf)
	{
		std::cout<<"Unable to open file "<<infile<<"\n";
		exit(1);
	}
	std::vector<int> redvec;
	char x;
	while(inf >> x)
	{	if(x=='1')
			redvec.push_back(1);
		else
			redvec.push_back(-1);
	}
	inf.close();
	return redvec;

}

void part1page1()
{	int size;
	std::cout<<"Enter the size of the grid"<<'\n';
	std::cin>>size;
	for(int cnfg=1;cnfg<=10;cnfg++){
		hopnet hnet(size);
		std::ofstream outfile;
		outfile.open("outputs/out_"+std::to_string(cnfg));
		for(int i=0;i<10000;i++)
		{	if(i%100)
				outfile<< i << " "<< hnet.get_E()<<"\n";
			hnet.transition(100);
		}
		outfile.close();
	}
}

void dump2file(hopnet& net, std::string filename)
{
	std::vector<int> states = net.get_states();
	std::vector<std::vector<double>> weights = net.get_w();
	std::ofstream out;
	out.open(filename);
	for(uint i=0;i<states.size();i++)
	{	out<< states[i]<<" ";
		for (uint j = 0; j < states.size(); ++j)
		{
			out<< weights[i][j]<< " ";
		}
		out<<"\n";
	}
	out.close(); 
}

void statecorruptor(hopnet& net,int k)
{	uint nstate = (net.get_states()).size();
	std::vector<int> v(nstate);
	std::iota(v.begin(),v.end(), 0);
	// for(uint i=0;i<nstate/4;i++)
	// {	if(std::rand()%2) net.flip_state(i);
	// }

	// int i=0;
	// while(i<k)
	// {
	// 	int rcoord=std::rand()%nstate;
	// 	net.flip_state(rcoord);
	// 	++i;
	// }
	std::shuffle(v.begin(), v.end(), std::mt19937{std::random_device{}()});
	for(int i=0;i<k;i++)
		net.flip_state(v[i]);


}

void runMC(hopnet& net)
{	
	for(int i=0;i<100000;++i)
	{	if(i%10000==0)
		{
			dump2file(net, "snapshot/thumb_snap_"+std::to_string(i)+".dat");
		}
		net.transition(100);
	}
}

void part2page1(std::vector<std::vector<int>>& vimgs)
{
	hopnet hnet(vimgs[0]);
	// vimgs.push_back(im1);
	// vimgs.push_back(im2);
	hnet.set_memweight(vimgs);
	statecorruptor(hnet,29);
	dump2file(hnet, "snapshot/smilb4.dat");

	runMC(hnet);
	dump2file(hnet, "snapshot/smilafter.dat");
}

void thumbpage1(std::vector<std::vector<int>>& vimgs)
{
	hopnet hnet(vimgs[0]);
	// vimgs.push_back(im1);
	// vimgs.push_back(im2);
	hnet.set_memweight(vimgs);
	statecorruptor(hnet,10240);
	dump2file(hnet, "snapshot/thumbb4.dat");

	runMC(hnet);
	dump2file(hnet, "snapshot/thumbafter.dat");
}
// std::vector<int> runham1(std::vector<int>& img)
// {	std::vector<int> dist;
// 	hopnet hnet1();
// 	int k=0;
// 	while(k<=img.size())
// 	{	hnet1.initialize(img.size());
// 		hnet1.set_memweight(img);
// 		statecorruptor(hnet1,k);
// 		runMC(hnet1);
// 		dist.push_back(calc_dist(hnet1.get_states(),img));
// 		k=k+0.1*img1.size();
// 	}
// 	return dist;
// }

int calc_dist(std::vector<int> v1, std::vector<int> v2)
{	
	if(v1.size()!=v2.size())
	{	std::cout<<"The sizes of the vectors AREN'T the same!!\n";
		return 0;
	}
	float dist=0;
	for(uint i=0;i<v1.size();i++)
	{
		dist+=std::abs(v1[i]-v2[i])/2;
	}

	return dist;

}


void hammingdist(std::vector<std::vector<int>>& vimgs)
{	//std::vector<std::vector<int>> hamdist;
	std::ofstream out;
	out.open("hammingdistances.txt");
 	for(uint i=0;i<vimgs.size();i++)
	{	std::vector<std::vector<int>> A;
		for(uint j=0;j<=i;j++)
			A.push_back(vimgs[j]);
		
		//std::vector<int> dist;
		uint k=0;
		std::vector<int> img=A[0];
		while(k<=img.size())
		{	int D=0;
			for(int l=0;l<20;l++)
			{	hopnet hnet(img);
				hnet.set_memweight(A);
				statecorruptor(hnet,k);
				runMC(hnet);
				D+=calc_dist(hnet.get_states(),img);
			}
			out<<D/20<<" ";
			k=k+0.1*img.size();
		}
		out<<'\n';
		//hamdist.push_back(dist);
	}
	out.close();
	
}

std::vector<int> mkrandvec(int size)
{
	std::vector<int> vec;
	for(int j=0;j<size;j++)
	{
		int r= std::rand()%2;
		if(r==0)
			vec.push_back(-1);
		else
			vec.push_back(1);
	}
	return vec;
}

int main(int argc, char *argv[])
{	std::vector<std::vector<int>> vimgs;
	std::cout<<argc<<"\n";
	if(argc > 1)
		for(int i=1;i<argc;i++)
		{	vimgs.push_back(readstate(argv[i]));
			std::cout<<argv[i]<<"\n";
		}
	else
	{	
		// for(int j=0;j<50;j++)
		// 	vimgs.push_back(mkrandvec(100));
		// hammingdist(vimgs);
		//part1page1();
		
		exit(0);
	}
	// std::vector<int> im1 = readstate("inputFig1");
	// std::vector<int> im2 = readstate("inputFig2");
	// std::cout<<im1.size()<<"\n";
	// std::cout<<im2.size()<<"\n";
	// for(const int& u: im1)
	// 	std::cout<< u <<' ';
	//std::cout<<"\n";
	
	thumbpage1(vimgs);


	//printweights(hnet.get_w());
	return 0;
}

