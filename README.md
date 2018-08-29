
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

### Activate the conda environemnt
If your conda enviroment is already activated, you will see (my_rdkit_env) in your terminal. If it is activated, skip this step.

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

##### How to navigate to a directory on Terminal 

Switching to a folder in your current directory
For example: 
```bash
cd Desktop 
```
this will put you into your Desktop directory. 

To navigate to directory with spaces in the name, put a backslash before each space.

For a folder with a the name "Folder Name", you would use the following command:
```bash
cd Folder\ Name
```

To see the contents of your current directory use the following command:
```bash
ls 
```
Tip: when entering the first couple letters of a directory, pressing tab will autocomplete the file name for you.
For example a directory named Folder typing in:
``` bash
cd Fol 
```
and pressing the tab key will autocomplete to Folder. As long, no older folders in your current directory also begin with "Fol".

##### Running the program

```bash
cd surfSiteProj
```
```bash
python manage.py runserver
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
