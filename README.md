## Impetus (TL;DR)
I wanted to have the ability to read in a data file (currently only csv) and do some preprocessing of the data. Convert it into a pandas dataframe. Then do some plotting, with the intention of adding specialized plot functions - see below for intended upgrades

### my Machine
## Windows 10 on Lenovo P53
## my Python setup is Anaconda (I also have Cygwin, although powershell should work assuming you haveyour PATH set appropriately)
## the default install of Anaconda had everything,
```
$ python --version
Python 3.7.7

$ ipython
Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
Type 'copyright', 'credits' or 'license' for more information
IPython 7.16.1 -- An enhanced Interactive Python. Type '?' for help.

In [1]:


```

## Except ttkwidgets - you may need to install
![ttkwidgets](https://pypi.org/project/ttkwidgets/)

### How to use
```
 $ git clone https://github.com/NikolasGazo/plotting.git
 Cloning into 'plotting'...
 remote: Enumerating objects: 36, done.
 remote: Counting objects: 100% (36/36), done.
 remote: Compressing objects: 100% (30/30), done.
 remote: Total 36 (delta 18), reused 18 (delta 6), pack-reused 0
 Unpacking objects: 100% (36/36), 137.40 KiB | 1019.00 KiB/s, done.
 $ cd plotting/
 $ python main.py
```
### The main window should pop up (assuming all pythong libraries are installed)
![Main Popup](/screenshots/V1_opening.PNG)

#### read in the default csv file (AEM.TO.csv) and click "Process File"
##### a couple text boxes will pop up with info of the DataFrame types and also a snippet (head and tail) of the file imported
![Read in file processed](/screenshots/V1_readInFile.PNG)

#### click "Plotting" tab and then "Import DF" and "Plot DF" with the two buttons
![df](/screenshots/V1_importDFandPlot.PNG)

#### Now, you can plot!

##### A more detailed breakdown:
## The basic premise/reason for the build was stated above. There are two sides to this project. The data input/cleaning and then the plotting/visualization.
## I effectively want to make the "Input Data" able to read in any type of data file, which I will specify. Currently it is just CSV since it is easy to read in, but I will want to have my own predefined file types. After the read in, I want a cleaning tool that will make sure the DataFrame is in good form (no bad types) and easily plotable with matplotlib, so need numpy arrays and datetimes. Once cleaned, I can then do some plotting
## For the "Plotting" tab, I will read in the DataFrame from the first tab. Once read in, I will then plot on the main plot frame, which is a subplot, 1 col x 2 row, with a shared x-axis. From there I will be build various plotting functions and tools for what I desire.

## It isn't overly complicated as is, but it is very lightweight and easily run. Please take and build on it if you'd like!


