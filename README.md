
##  Install and setup 

### Create a conda environment and install rdkit 


Open up your terminal and copy paste the following line: 
```bash
conda create -c rdkit -n my-rdkit-env rdkit
```

This created the conda environment. Now activate it.

For Mac and Linux users:
```bash
source activate my-rdkit-env
```

For Windows Users: 
```
activate my-rdkit-env
```

### Install necessary dependencies into the conda environment
Activate your conda environment first 
#### Numpy
```bash 
 pip install numpy
```

#### Django
```bash 
 pip install django
```

### Pubchempy 
```bash 
 pip install pubchempy
```


## Running the program 

### Activate the conda wnvironemnt
For Mac and Linux users:
```bash
source activate my-rdkit-env
```

For Windows Users: 
```
activate my-rdkit-env
```

### Run Program on Terminal 
Open up the terminal and navigate to the Directory you have the project folder in.

```bash
cd surfSiteProj
```
```bash
source activate my-rdkit-env
```

### Open Program on browser

Once the program is running on your Terminal you willl see the following output 

```
Django version 2.0.7, using settings 'surfSiteProj.settings'
Starting development server at http://127.0.0.1:XXXX/
Quit the server with CONTROL-C.
```

The XXXX above will be 4 numbers, typically 8000. Open your browser and type in
localhost:XXXX/search

## Contact

Email: aespino@caltech.edu
# surfProject
