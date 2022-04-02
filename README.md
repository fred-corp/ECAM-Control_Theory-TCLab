# TCLab - Control Theory laboratory

This repo contains the code and report files for the Control Theory Lab from 3rd bachelor year at ECAM Brussels.

## Files explanation

The different files in this repo were created following the rules of the laboratory assignment assignment.  
Here's a short description of the structure of thie repo

### Data.md

This file contains the evaluated dynamics parameter for P(s) and D(s) using a Firs-Order plus delay and Second-Order plus delay model.

### Code folder

This folder contains the codes used to make the identifications and experiments of the laboratory.  
We're only going to explain the files we had to write (not the ones that were given by our teacher (```TCLab_test.ipynb```, ```TCLab_OLP.ipynb```, ```package_DBR.py```, ```package_DBR.ipynb```, ```Identification_FOPDT.ipynb```, ```Identification_SOPDT.ipynb```)).

#### ```package_LAB.py```

This Python script contains the nessessary methods and functions we had to write to simulate/run a real-time lead-lag system, a real-time PID controller, IMC Tuning and calculate gain and phase margins.

#### ```package_LAB.ipynb```

This JupyterLab notebook contains the code to test and explain the parameters of the methods & functions of ```package_LAB.py```, as well as the step response of the ```LeadLag_RT()``` and ```PID_RT()``` methods.

#### ```package_LAB_Margins.ipynb```

This JupyterLab notebook contains the code to test and explain the parameters of the ```Margins()``` method of the ```package_LAB.py``` file. It also contains the code to perform a gain and phase margins analysis of the loop with the identified parameters.

#### ```Simulation_CLP_PID_FF.ipynb```

This JupyterLab notebook contains the code to simulate the control loop depending on different simulation parameters (scenarios).  
You can choose a scenario to simulate the loop with by uncommenting it, or you can write yours based on the scenarios already present.

#### ```TCLab_CLP_PID_FF.ipynb```

This JupyterLab notebook contains the code to perform an experiment on the physical TCLab platform depending on different simulation parameters (scenarios).  
You can choose a scenario to simulate the loop with by uncommenting it, or you can write yours based on the scenarios already present.

## Licence

Made with ❤️, lots of ☕️, and lack of 🛌  
Published under CreativeCommons BY-NC-SA 4.0

[![Creative Commons License](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)  
This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).