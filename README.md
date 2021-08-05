# Sup-SE2021-40
Supplementary code asset for article "Reflection tomography by depth warping: A case study across the Java trench" on Solid Earth (SE-2021-40) 
(Xia et al., 2021, doi.org/10.5194/se-2021-40).

The scripts and Jupyter Notebooks provide the mathematical implementations of the depth variant displacement correction, and the automatic residual move-out(RMO) tracking.

For both NRM and PWD displacement fields, a simple and a complex synthetic example are presented to document the capacity and the limitation of the warping method on RMO tracking. 

The IPython (Jupyter) notebook (*.ipynb) is an open-source web-based script that allows you to read the interactive sub-procedures (e.g., formulas, intermediate figures) of the source code (*.py) with PC browser without building the Python environment in your computer. Please read the script of the calculation by simply clicking the .ipynb file in this repository. However, executing the *.ipynb needs building the local Python environment on your PC. 

Python (3.7-3.8), OBSpy (1.2.1-1.2.2), Numpy, and Scipy are needed dependencies before executing the code. The input data directory ("inputdata_withavo") is needed to be placed at the same directory level as the scripts. 

We suggested to use the Anaconda to build the Python environment. 
