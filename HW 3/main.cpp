#include "ising.h"


double get_m(std::vector<int> &grid)
{	double m=0.0;
	for(auto const& value: grid)
		m+=double(value)/grid.size();
	return m;	
}

int get_E(std::vector<int> &grid)
{	int Ea=0;
	int Eb=0;
	int boxlen = pow(grid.size(),0.5);
	//#pragma omp parallel for
	for(int coord=0;coord<(int)grid.size();coord+=1)
	{	if((coord+1)%boxlen==0) //right edge
        	{//E+=grid[coord]*grid[coord-boxlen+1]; //periodic boundary right
        	        if(coord!=boxlen-1) Ea+=grid[coord]*grid[coord-boxlen]; //look up
        	//      else m=m+grid[boxlen*boxlen-1]; //periodic boundary up
        	}
        else if(coord<boxlen) //top edge
   		{	Ea+=grid[coord]*grid[coord+1]; //look right 
		}
		else
		{	Ea+=grid[coord]*grid[coord+1]; //look right
			Ea+=grid[coord]*grid[coord-boxlen]; //look up
		}
	}
	//#pragma omp barrier
	
	// #pragma omp parallel for
	// for(int coord=1;coord<(int)grid.size();coord+=2)
	// {	if((coord+1)%boxlen==0) //right edge
 //        	{//E+=grid[coord]*grid[coord-boxlen+1]; //periodic boundary right
 //        	        if(coord!=boxlen-1) Eb+=grid[coord]*grid[coord-boxlen]; //look up
 //        	//      else m=m+grid[boxlen*boxlen-1]; //periodic boundary up
 //        	}
 //        	else if(coord<boxlen) //top edge
 //   		{	Eb+=grid[coord]*grid[coord+1]; //look right 
	// 	}
	// 	else
	// 	{	Eb+=grid[coord]*grid[coord+1]; //look right
	// 		Eb+=grid[coord]*grid[coord-boxlen]; //look up
	// 	}
	// }
	// int Eout = Ea+Eb;
	return Ea;
}
int calc_Ediff(std::vector<int>& grid,int coord,int boxlen)
{
	int ediff=0.0;
	// if((rcoord+1)%lx==0) //right edge
	// {	
	// 	ediff+=grid[rcoord]*grid[rcoord-1]; //look left
 //       		if(rcoord!=lx-1){ 
	// 		ediff+=grid[rcoord]*grid[rcoord-lx]; //look up
	// 	}
	// 	if(rcoord!=grid.size()-1){
	// 		ediff+=grid[rcoord]*grid[rcoord+lx]; //look down
	// 	}
	// }
	// else if(rcoord%lx==0) //left edge
	// {	ediff+=grid[rcoord]*grid[rcoord+1];//look right
		
	// 	if(rcoord!=0) ediff+=grid[rcoord]*grid[rcoord-lx]; //look up
	// 	if(rcoord!=grid.size()-lx) ediff+=grid[rcoord]*grid[rcoord+lx]; //look down
	// }
	
	// else{
	// ediff+=grid[rcoord]*grid[rcoord+1]; //look right
	// ediff+=grid[rcoord]*grid[rcoord-1]; //look left
	// if(rcoord>=lx) ediff+=grid[rcoord]*grid[rcoord-lx]; //look up
	// if(rcoord<grid.size()-lx) ediff+=grid[rcoord]*grid[rcoord+lx]; //look down
	// }
	if((coord+1)%boxlen==0) //right edge
        	{//E+=grid[coord]*grid[coord-boxlen+1]; //periodic boundary right
        	        if(coord!=boxlen-1) ediff+=grid[coord]*grid[coord-boxlen]; //look up
        	//      else m=m+grid[boxlen*boxlen-1]; //periodic boundary up
        	}
        	else if(coord<boxlen) //top edge
   		{	ediff+=grid[coord]*grid[coord+1]; //look right 
		}
		else
		{	ediff+=grid[coord]*grid[coord+1]; //look right
			ediff+=grid[coord]*grid[coord-boxlen]; //look up
		}

	return ediff;

}

void transition(std::vector<int>& grid,float beta,int lx)
{	auto newgrid = grid;  
	int rcoord = std::rand()%(int)grid.size();
	if(grid[rcoord]==-1) newgrid[rcoord]=1;
	else newgrid[rcoord]=-1;
	//int ediff = calc_Ediff(grid,rcoord,lx); 
	int En = get_E(grid);
	int E = get_E(newgrid);
	double A = std::min(1.0,(double)exp(-2*beta*(En-E)));
	if(A>double(std::rand())/RAND_MAX){
		// if(grid[rcoord]==-1) grid[rcoord]=1;
		// else grid[rcoord]=-1;
		grid=newgrid;
	}
}

std::vector<int> turn2vec(std::bitset<9> bitvec)
{	std::vector<int> config;
	for(int i=0;i<(int)bitvec.size();i++)
		if(!(int)bitvec[i]) config.push_back(-1);
		else config.push_back((int)bitvec[i]);
	
	return config;
}
long int bin2dec(std::vector<int> isinggrid)
{	long int decimal = 0;
	std::replace(isinggrid.begin(), isinggrid.end(), -1,0);
	for(int i=0;i<(int)isinggrid.size();i++)
		decimal = decimal*2 + isinggrid[i];
	return decimal;
} 

std::vector<int> initialize(int lx,int ly,bool randflag) //flag to tell me whether we initialize the grid to be random or not
{	std::vector<int> grid;
	grid.reserve(lx*ly);

	// if(randflag){
	// //#pragma omp parallel
	//  {
	// 	std::vector<int> priv_grid;
	// 	//#pragma omp for schedule(static) nowait
	// 	for(int i=0;i<lx*ly;i++)
	// 	{	int r = std::rand()%2;
	// 		if(r==0) r= -1;
	// 		priv_grid.push_back(r);	//-1 is spin down,1 is up
	// 	}
	// 	//#pragma omp critical
	// 	grid.insert(grid.end(),priv_grid.begin(),priv_grid.end());
	// }
	
	// return grid;
	// }

	//#pragma omp declare reduction(merge: std::vector<int> : omp_out.insert(omp_out.end(),omp_in.begin(),omp_in.end()))
// Parallel code help for vector insertion taken from https://stackoverflow.com/questions/18669296/c-openmp-parallel-for-loop-alternatives-to-stdvector
	
	//#pragma omp parallel for reduction(merge: grid)
	for(int i=0;i<lx*ly;i++)
		grid.push_back(1);
	
	return grid;
	
	
}

void probdistributions(int lx, int ly, double beta)
{        
	std::ofstream numcfig;
	std::vector<int> spins;
	spins.reserve(lx*ly);
	numcfig.open("outputs/Whichconfig_5.dat");
        for(int t=0; t<10000; t++)       
        {	spins = initialize(lx,ly,0);
		for(int tau=0;tau<5;tau++) transition(spins,beta,lx);
                numcfig <<t<<" "<<bin2dec(spins)<<" "<<get_E(spins)<<"\n";
		

	}
	
	numcfig.close();
	numcfig.clear();
	numcfig.open("outputs/Whichconfig_50.dat");
        for(int t=0; t<10000; t++)       
        {	spins = initialize(lx,ly,0);
		for(int tau=0;tau<50;tau++) transition(spins,beta,lx);
                numcfig <<t<<" "<<bin2dec(spins)<<"\n";

	}

	numcfig.close();
	numcfig.clear();
	numcfig.open("outputs/Whichconfig_500.dat");
        for(int t=0; t<10000; t++)       
        {	spins = initialize(lx,ly,0);
		for(int tau=0;tau<500;tau++) transition(spins,beta,lx);
		
                numcfig <<t<<" "<<bin2dec(spins)<<"\n";

	}

	numcfig.close();
	
}

void Eallconfigs(int lx,int ly,double beta)
{	
	std::bitset<9> A;
	std::vector<int> config;
	config.reserve(lx*ly);
	std::ofstream vecadd;
	vecadd.open("outputs/vec_"+std::to_string(beta));
	for(int k=0;k<pow(2,lx*ly);k++)
	{	A=k;
		config = turn2vec(A);
		auto l = get_E(config);
		vecadd<< k<<" "<<l<<"\n";
	}
	vecadd.close();	

}

void m_calculation(int lx, int ly,double beta,std::string filename, int count)
{	
	for(beta=0.1;beta<=1.2;beta+=0.1)
	{	std::vector<int> grid = initialize(lx,ly,0);
		std::ofstream outfile;
		outfile.open("outputs/out_"+std::to_string((int)(round(100*beta)/10)));
		for(int t=0; t<1000000; t++)
		{	transition(grid,beta,lx);
			if(!(t%count)) {
				auto fname = "snap_dats/snap_"+std::to_string((int)(round(100*beta)/10))+"_"+std::to_string(t/10000)+".dat";
				snapshot(grid,lx,fname);
			}
			outfile << t<<" "<< pow(get_m(grid),2)<<" ";
			outfile << get_E(grid)<<"\n";
	                //outfile <<" "<<bin2dec(grid)<<"\n";
		}
		outfile.close();
	}
	

}

void sim_anneal(int lx, int ly,double beta,int count)
{
	std::vector<int> grid = initialize(lx,ly,false);
		std::ofstream outfile;
		outfile.open("outputs/simann_log_out_"+std::to_string((int)(round(100*beta)/10)));
		for(int t=0; t<1000000; t++)
		{	transition(grid,beta,lx);
			if(!(t%count)) {
				beta = 	log(t+0.2);
				//beta = 
				//beta = beta+0.1;
				auto fname = "snap_dats/sim_log"+std::to_string((int)(round(100*beta)/10))+".dat";
				snapshot(grid,lx,fname);
				outfile << t<<" "<< pow(get_m(grid),2)<<" ";
				outfile << get_E(grid)<<" ";
				outfile<< std::to_string((int)(round(100*beta)/10));
				outfile<<"\n";
			}

	                //outfile <<" "<<bin2dec(grid)<<"\n";
		}
		outfile.close();
}
void boltzmann(double beta)
{
	std::ofstream outfile;
	outfile.open("outputs/Boltzmann"+std::to_string(beta)+".dat");
	for(int i=0;i<512;i++)
	{	auto A = std::bitset<9>(i);
		auto spins = turn2vec(A);
		outfile<<i<<" "<<get_E(spins)<<"\n";
	}
	outfile.close();
}
void snapshot(std::vector<int>& grid,int lenx,std::string fname)
{
	std::ofstream snapshot;
	snapshot.open(fname);
	for(int p=0;p<(int)grid.size();p++)
	{	snapshot<<grid[p]<<" ";
		if((p+1)%lenx==0) snapshot<<"\n";
	}
	snapshot.close();
}
int main()
{	double beta;
	InputClass input; 
	std::ifstream infname("InputFile.txt");
	input.Read(infname);
	beta = input.toDouble(input.GetVariable("beta"));
	infname.close();	
	int lenx = input.toInteger(input.GetVariable("Lx"));
	int leny = input.toInteger(input.GetVariable("Ly")); 
	
	auto filename = input.GetVariable("outFile");
	std::srand(std::time(0));
	
	//sim_anneal(lenx,leny,beta,10000);
	//m_calculation(lenx,leny,beta,filename,10000);
	probdistributions(lenx,leny,beta);
	boltzmann(beta);
	return 0;
	 
}

/*


//int sizeofgrid = 0;

int get_m(std::vector<int> &grid, int coord)
{	int boxlen = pow(grid.size(),0.5);
	int m=0;
	//top
	if(coord%boxlen==0)//left edge
	{	  m=m+grid[coord+1]; //look right
		  if(coord!=0) m=m+grid[coord-boxlen]; //look up
	//	  else{ m=m+grid[boxlen*(boxlen-1)]; //periodic boundary up
	//	        }
		  if(coord!=boxlen*(boxlen-1)) m=m+grid[coord+boxlen]; //look down
		  
	}
	else if((coord+1)%boxlen==0) //right edge
	{ 	m=m+grid[coord-1];  //look left
	//	m=m+grid[coord-boxlen+1]; //periodic boundary right
		if(coord!=boxlen-1) m=m+grid[coord-boxlen]; //look up
	//	else m=m+grid[boxlen*boxlen-1]; //periodic boundary up
		if(coord!=boxlen*boxlen-1) m=m+grid[coord+boxlen]; //look down
	}
	else if(coord<boxlen) //top edge
	{	m=m+grid[boxlen];
		
	}
}
*/
