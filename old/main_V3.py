
######################################
#### basic plotting of dataframe #####
######################################

'''
Tkinter application that will be able to read a file type and produce a general dataframe.

The file type will start as a csv, but hopefully we can get into other types with newly created functions for cleanign

will have a simple drop down for file path and file type; the file type will be csv or defined

then a process button, which will read in the file and produce a dataframe that we can do plotting on

the dataframe will be "taken" to a new area/tab/region of the application for plotting and analysis basically

it can be basic one page, or potentially tabbed..


'''




#####################################
###### Libraries... ##############
##############################

# import the gui framework library, tk
import tkinter as tk
# import the drop down boxes in tkinter - need END for the insert method
from tkinter import ttk, Text, END
# dialog box for files on local machine
from tkinter import filedialog #<-- 
#from tkinter import tkFileDialog
# for message box / alerts
from tkinter import messagebox
## for the auto complete combobox - may need to import before tkinter, but we shall see
from ttkwidgets.autocomplete import AutocompleteCombobox as ACcombobox
# add the notebook so i can use tabs
from tkinter.ttk import Notebook
# import the (O)perating (S)ystem library for listings directories and other functionality
import os
# for file listings
import glob

# import for data analysis and dataframes
import pandas as pd
# import numpy for some numerical analyses..
import numpy as np







##################################################


## main ui code

class MainUI(tk.Tk):

# inherit from tk.Tk class
	def __init__(self):
		super().__init__()

		### the main Tk Window
		self.title(" Dataframe plotting - V2020-07.4.1")
		# give it a favicon/icon - the image seen in the top left
		self.iconbitmap("./favicon.ico")
		# grab width and height of man screen and make that the geometry of the window pop up...
		# self.ws=self.winfo_screenwidth()
		# self.hs=self.winfo_screenheight()
		# self.x=0.98*self.ws
		# self.y=self.hs
		# self.geometry('%dx%d+0+0'%(self.x,self.y))
		self.configure(bg='white')

		self.df = pd.DataFrame()

###		####-- Main UI build up --##

###		### Add a file menu, just in case we want it later...
		## create a main menu bar
		self.menuBar = tk.Menu(self, bg='lightgrey', fg='black')

		## add a "File" menu to put into main menu bar (tearoff=1 allows u to pop out the menu dropdown)
		self.fileMenu = tk.Menu(self.menuBar, tearoff=0, bg='white', fg='black')
		self.fileMenu.add_command(label="file 1", command=self.label1)
		self.fileMenu.add_command(label="Quit", command=self.quit)

		## add an "Edit" drop down
		self.editMenu = tk.Menu(self.menuBar, tearoff=0, bg='white', fg='black')
		self.editMenu.add_command(label="edit 1", command=self.edit1)

		## add the menus to the main menu on the UI
		self.menuBar.add_cascade(label='File', menu=self.fileMenu)
		self.menuBar.add_cascade(label='Edit', menu=self.editMenu)

		## add the main menu bar to the UI
		self.config(menu=self.menuBar, borderwidth=5,)


##		## add the notebook, to add tabs to the top
		self.notebook = Notebook(self)

		## create a frame inside the notebook object for both tabs to be
		inputDataTab = tk.Frame(self.notebook, bg="white")
		plotTab = tk.Frame(self.notebook)

		## create a canvas within the Frame objects that are now under notebook
		self.inputDataTab = tk.Canvas(inputDataTab)
		self.inputDataTab.grid()
		## now add the inputdataUI object into the canvas object above
		
		self.inputDF = InputDataUI(self.inputDataTab)#inputDataTab)




		## create the canvas for plot taking in the
		self.plotTab = tk.Canvas(plotTab)
		self.plotTab.grid()

		self.plotTab.df = self.inputDF.df

		plotting(self.plotTab)


		## explicitly add the tabs to the notebook
		self.notebook.add(inputDataTab, text="Input File")
		self.notebook.add(plotTab, text="Plotting")


		self.notebook.grid()


##		## required for the gui to continually loop and "run"
		self.mainloop()



	def label1(self):
		''' function for menu item '''
		## since our data is in the inputDataTab canvas/object
		print(self.notebook.children[self.notebook.select().split(".")[2]])
		print(self.notebook.tabs()[0])

	def edit1(self):
		print(self.df)
		print('--')
		print(self.inputDF.df)
		return self.df


#### First Class/Tab in Main...

class InputDataUI():
# this will inherit parent, which inherits tk.Tk(), so we don't need to inherit that again here
# so the parent is the object that is calling this window and thus we will set the widgets in that object, not self
	
	
	def __init__(self, parent):
		super(InputDataUI, self).__init__()

		# initialize to have the self object and the parent
		# parent.configure(bg='white')

		## empty df to be filled
		self.df  = pd.DataFrame()

		####-- Input Data File UI build up --##

##		## Main input file area... refer to all the objects/functions to self, theyre just in the parent object/frame
		self.inputFile_label = tk.Label(parent, text="Input File:", font=("Helvetica",10), bg="white")
		self.inputFile_label.grid(column=1,row=2,padx=5,pady=5,sticky="WNES") # sticky helps push away from borders here

		## input file combo box - default values are the files in current directory
		self.inputFile_combo = ttk.Combobox(parent, width=50, values=glob.glob("./*") )
		self.inputFile_combo.grid(column=2,row=2,padx=5,pady=5,sticky="WNES")

		## browse button to search for files outside current directory - calls browseFiles functions
		self.inputFile_browseButton = tk.Button(parent, text="Browse for File...", command=self.browseFiles)
		self.inputFile_browseButton.bind('<Return>', self.browseFiles) # allows to be exectued on enter key, function needs event=None
		self.inputFile_browseButton.grid(column=3,row=2,padx=5,pady=5,stick="nesw")

		## button to clear the input file field box
		self.inputFile_clearButton = tk.Button(parent, text="Clear File", width=25, command=self.clearFilename)
		self.inputFile_clearButton.grid(column=4,row=2,padx=5,pady=5,stick="nesw")

##		## set the input file type - this will be of types "we" know, so csv, specific data files, etc
		self.fileType_label = tk.Label(parent, text="File Type:", font=("Helvetica",10), bg="white")
		self.fileType_label.grid(column=1,row=3,padx=5,pady=5,sticky="WNEW")

		## combo box to select one of the to-be predefined file types, currently csv
		self.fileType_combo = ttk.Combobox(parent, width=25, values=['csv','other types to come...'])
		self.fileType_combo.current(0) # default vales = first in values list
		self.fileType_combo.grid(column=2, row=3, padx=5, pady=5, sticky="WNES")

##		## button to actually read in the file and do the processing
		self.processFile_button = tk.Button(parent, text="Process File", font=("Helvetica",14), width=40, height=1, command=lambda: self.processFile(parent))
		self.processFile_button.grid(column=1, row=4, padx=10, pady=10, columnspan=2, rowspan=2, stick="WNES")


##		## add in a text frame to print some info on data file?
		self.processedFile_info = Text(parent, width=150, height=25, font=("Courier",8), borderwidth=2)
		self.processedFile_info.grid(row=6,column=2, columnspan=3)
		self.processedFile_info.grid_remove() # use this to hide until it is needed.



	# event=None needs to be in to be used by <Return> key
	def browseFiles(self,event=None):
		""" search for files on local machine """
		filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file")  
		self.inputFile_combo.set(filename)


	def clearFilename(self):
		self.inputFile_combo.set('')


	def processFile(self, parent, fileType="csv"):

		# need to check if a file has been given to process
		if self.inputFile_combo.get() == '':
			messagebox.showerror(title="Missing File", message="No input file selected...")
			return

		# remove any text within box if it exists...
		self.processedFile_info.delete('1.0',END)
		# un hide the text box
		# self.processedFile_info.grid()

		# read the data file into a dataframe
		if fileType == "csv":
			self.df = pd.read_csv(self.inputFile_combo.get())
			parent.df = self.df
			len_of_row = len(self.df.loc[0].to_string())

			# self.processedFile_info = Text(self, width=int(0.8*len_of_row), height=25, font=("Courier",8), borderwidth=2)
			# un hide the textbox... although originally this was earlier. may resort to that
			self.processedFile_info.grid()


			# self.processedFile_info.width=int(0.8*len_of_row)

			InfoString = \
			f'''The dataframe has {self.df.shape[0]} rows and {self.df.shape[1]} columns.\nThe column headers are:
			{self.list2VerticalString(self.df.columns.to_list())}\nBelow is a snippet of the date imported\n===========\n'''

			self.processedFile_info.insert(END, "Processed: " + self.inputFile_combo.get() +"\n")
			self.processedFile_info.insert(END, InfoString)
			self.processedFile_info.insert(END, self.df.head().to_string(index=False))


		## assign this df to the parent class...
		parent.df = self.df
		return parent.df


	def list2VerticalString(self,oldList):
		''' bring in a list of strings and return vertical string '''
		newString = '\n'
		for ind, val in enumerate(oldList):
			newString += str(ind+1)+": "+val+'\n'
		return newString


##################################################
##################################################


#### second Tab/class #####

class plotting():
# this will inherit parent, which inherits tk.Tk(), so we dont need to inherit that again here
# so the parent is the object that is calling this window and thus we will set the widgets in that object, not self
	
	
	def __init__(self, parent):
		super(plotting, self).__init__()

		# initialize to have the self object and the parent
		parent.configure(bg='white')

		####-- Input Data File UI build up --##

##		## Main input file area... refer to all the objects/functions to self, theyre just in the parent object/frame
		self.inputDF_label = tk.Label(parent, text="Input DataFrame:", font=("Helvetica",10), bg="white")
		self.inputDF_label.grid(column=1,row=2,padx=5,pady=5,sticky="WNES") # sticky helps push away from borders here

		## input file combo box - default values are the files in current directory
		self.inputDF_combo = ttk.Combobox(parent, width=25, values=list(parent.df))
		self.inputDF_combo.grid(column=2,row=2,padx=5,pady=5,sticky="WNES")


		## browse button to search for files outside current directory - calls browseFiles functions
		self.inputDF_Button = tk.Button(parent, text="Browse for File...", command= lambda: self.listDFs(parent))
		self.inputDF_Button.grid(column=3,row=2,padx=5,pady=5,stick="nesw")





	def listDFs(self, parent):
		print([cls.__name__ for cls in MainUI.__subclasses__() ] ) #	MainUI.label1(parent)
		print(parent.children)
		# print([cls.__name__ for cls in parent.__subclasses__()])





##################################################






if __name__ == "__main__":
	# root = tk.Tk()
	# mygui = InputDataUI(root)
	# root.mainloop()
	mygui = MainUI()
	
	

''' 

next steps...
-	take df into the plotting tab and plot!

'''
