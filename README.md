# Strong PUF Security Metrics: Sensitivity of Responses to Single Challenge Bit Flips

This repository provides the code used to run the simulations and create the plots presented in our paper 
* [**Strong PUF Security Metrics: Sensitivity of Responses to Single Challenge Bit Flips**](), [[]()].

It belongs to a series of papers for generic an easy-to-apply security metrics for Strong Physical Unclonable Functions (PUFs). The further manuscripts in this sequence are [as of 20th Sep 23]:

* [](), [[]()]


## Python Environment and Version

These instructions require a UNIX/MacOS operating system with [pyenv](https://github.com/pyenv/pyenv) installed. If you want to use Windows cf. the pyenv install instructions.

To create a suitable virtual environment called _Single_Bit_Flip_Env_ and then activate it, run the following commands in Bash/Zsh:
```bash
pyenv install 3.8.13
pyenv virtualenv 3.8.13 Single_Bit_Flip_Env
pyenv activate Single_Bit_Flip_Env
```

The [pypuf](https://github.com/nils-wisiol/pypuf) package in version 3.2.1, which is used for the simulations, does also contain implementations of various attacks. One of these requires tensorflow 2.4.x which is incompatible with python 3.8.13. Since the attacks are not required for the simulations, pypuf is installed without tensorflow.
This is achieved by first installing all packages from _requirements_no_pypuf.txt_ (which include all pypuf dependencies except tensorflow) and then pypuf without dependencies:
```bash
pip install -r requirements_no_pypuf.txt
pip install pypuf==3.2.1 --no-deps
```

## Running Simulations and Creating the Plots

### Simulations

The simulations can be run executing the _run_simulations.py_ script:
```bash
python run_simulations.py
```

This will perform the simulations and store the results as pickel files in the folder _./simulations/_.

Please note:
* This may, depending on your system, take considerable runtime.
* The first three files will be produced much faster than the second three, since the latter contain much more extensive simulations.
* The code is set to use all avaliable CPU cores and 10<sup>5</sup> challenges.

To adapt the number of cores and challenges, the arguments --cpus and --challenges can be used. To select 5 CPU cores and 10<sup>4</sup> challenges for instance, pass the following arguments to the script:
```bash
python run_simulations.py --cpus 5 --challenges 10000
```

### Plots and I2O<sub>1</sub> Scores

The plots and I2O<sub>1</sub> scores can be created from the stored simulation files by running the _create_plots.py script:
```bash
python create_plots.py
```

This will produce:

* The plots and store them as .png files in the folder _./plots/_.
* The I2O<sub>1</sub> values displayed in the tables, stored as .txt files in the folder _./plots/_.
