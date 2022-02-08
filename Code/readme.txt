Prerequisites:
	Packages: numpy,matplotlib,umt,math,random
         To install use command "pip install <package_name>

	Package: pymobility
         To install type following commands in command line.
	   $git clone git://github.com/panisson/pymobility.git
	   $cd pymobility
	   $python setup.py install (run as admin/root)

For more on mobility models go to : https://github.com/panisson/pymobility


Execution:
    Data Module:
	Contains csv file of dataset comprising of latitudes and longitudes of server locations.

    SimUtils Module:
	mobility : scales servers on a 2d co ordinate system. generates users trajectory co-ordinates according to random-way-point model. assigns all the parameter values to users and servers.
	params : contains parameters requires for mobility 
    
    TaskAcceptance Module:
	TaskAcceptance vs Task Deadline : $python runE1.py
	dcemto,localExecution,randomAllocation : returns an array of no of tasks accepted for the corresponding deadline using respective algorithm.

    Energy Consumption Module:
	No of users vs Energy Consumption : $python runE2.py
	No of users vs Avg Energy Consumption : $python runE3.py
	Task size vs Avg Energy Consumption : $python runE4.py
	Server Capacity vs Avg Energy Consumption : $python runE5.py
	dcemto,localExecution,randomAllocation : returns respective energy cosumption value by using that algorithm.
	
	
	