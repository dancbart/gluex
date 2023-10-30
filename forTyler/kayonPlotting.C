// From Vitalli Baturin, JLab. 10/3/2023
 Double_t  myfun(Double_t *x, Double_t *par) 
{
   //TRandom3 * generator = new TRandom3();
   //double x1 = generator->Uniform(0,1);
   //double y1 = generator->Uniform(0,1);
   //double w1 = x1 + y1;
   //if (w1>=0.&& w1<=1.){
   //   return w1;
   //} else if (w1>1.&& w1<=2.) {
   //   return (2.-w1);
   //} else {
        double_t KLm=0.4976;	// KL beam  mass
	double_t Km =0.4976;    //0.4937;	// K+ mass secondary
	double_t Nm =0.939;	// Neutron mass recoil
	double_t Pm =0.939;      // Proton mass target
	double_t Ka;		// K+ ang(Xp) , to return  function of the variable 
	double_t Xp=x[0];	// K+ momentum, variable
	double_t KLp=par[0];	//par[0] = KLong momentum in  LabSys
	double KLe=sqrt(KLp*KLp+KLm*KLm);	// KL beam  energy
	double Xe2=(Xp*Xp+Km*Km);		//K+ energy**2
	double Xe=sqrt(Xe2);	//K+ energy
        double W=Pm+KLe;	//W energy
	double W2=W*W;		//W**2 energy



   //        Ka=  ;
   //  if (w1>=0.&& w1<=1.){
   //   return w1;
   //} 
	double_t coter=(KLp*KLp+Nm*Nm-W*W-Km*Km) ;
	//Ka= (KLp*KLp+Nm*Nm-W*W+2*W*sqrt(Xp*Xp+Km*Km)-Km*Km)/(2*KLp*Xp);
    	Ka= (coter+2*W*Xe)/(2*KLp*Xp);
        if (Ka >=-1. && Ka <=1.)
		{
Ka=(180./3.14)*acos(Ka);
	return Ka;}
	else 
		{return -0.;}

//	ret=p[2]/ret;

//	return (Ka);

   // };
}

int formoscov4(double beg=0.3, double end=1.0)
        {
	std::cout<<"formoscov4.C message ::  started ! " << std::endl;
        Double_t xx=3.;
	Double_t par[3] = {0., 0., 0.};
	Double_t momeK[5]={0.6, 0.7, 0.8, 0.9, 1.0};
        std::cout << "moskov p=" << ",   Hist. begins =" <<beg<< ", ends =" <<end<< std::endl;
        std::cout << "Requested momentas starts from : " << *momeK << std::endl;

//	TH2F *h1 = new TH2F("h1","Moskov",1,0,600,100,-1,1);
//	TF1 *f1 = new TF1("f1","sin(1*x)",0.,end);

        TF1 *f1 = new TF1("Ks Pol.Ang. vs Momentum 0",myfun,0.,end,3);
	TF1 *f2 = new TF1("Ks Pol.Ang. vs Momentum 1",myfun,0.,end,3);
        TF1 *f3 = new TF1("Ks Pol.Ang. vs Momentum 2",myfun,0.,end,3);
        TF1 *f4 = new TF1("Ks Pol.Ang. vs Momentum 3",myfun,0.,end,3);
        TF1 *f5 = new TF1("Ks Pol.Ang. vs Momentum 4",myfun,0.,end,3);

        TCanvas *c1  = new TCanvas("c1", " Angular distributions   ", 800, 400);
      
        //c1->Divide(2,2,0,0);
	//h1->Draw();

        f1->SetParameter(0,momeK[0]);
	f1->Draw();

        f2->SetParameter(0,momeK[1]);
        f2->Draw("same");

	f3->SetParameter(0,momeK[2]);
        //f2->SetParameter(1,0.001);
        f3->Draw("same");

	f4->SetParameter(0,momeK[3]); //set momentum
        //f5->SetParameter(1,0.001);
        f4->Draw("same");


	f5->SetParameter(0,momeK[4]); //set momentum
        //f5->SetParameter(1,0.001);
        f5->Draw("same");

        return 0;       
	}

int  kayonPlotting()
//#include <iostream.h>
{
std::cout<<"Hello Vitaly N. Baturin=id "<<std::endl;
formoscov4();
std::cout<<"Hello Vitaly N. Baturin=id "<<std::endl;
        return 0;
}

