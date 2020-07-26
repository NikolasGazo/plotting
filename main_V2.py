
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
from tkinter import filedialog #<-- this one is shit; crashing the program
#from tkinter import tkFileDialog
# for message box / alerts
from tkinter import messagebox
## for the auto complete combobox - may need to import before tkinter, but we shall see
from ttkwidgets.autocomplete import AutocompleteCombobox as ACcombobox
# import the (O)perating (S)ystem library for listings directories and other functionality
import os
# for file listings
import glob

# import for data analysis and dataframes
import pandas as pd
# import numpy for some numerical analyses..
import numpy as np








class MainUI(tk.Tk):

	def __init__(self):
		super().__init__()
		### the main Tk Window
		self.title(" Dataframe plotting - V2020-07.4")
		# give it a favicon/icon - the image seen in the top left
		self.iconbitmap("./favicon.ico")
		# grab width and height of man screen and make that the geometry of the window pop up...
		self.ws=self.winfo_screenwidth()
		self.hs=self.winfo_screenheight()
		self.x=0.98*self.ws
		self.y=self.hs
		self.geometry('%dx%d+0+0'%(self.x,self.y))
		self.configure(bg='white')

		####-- Main UI build up --##

##		## Main input file area...
		self.inputFile_label = tk.Label(self, text="Input File:", font=("Helvetica",10), bg="white")
		self.inputFile_label.grid(column=1,row=2,padx=5,pady=5,sticky="WNES") # sticky helps push away from borders here

		self.inputFile_combo = ttk.Combobox(self, width=50, values=glob.glob("./*") )
		self.inputFile_combo.grid(column=2,row=2,padx=5,pady=5,sticky="WNES")

		self.inputFile_browseButton = tk.Button(self, text="Browse for File...", command=self.browseFiles)
		self.inputFile_browseButton.bind('<Return>', self.browseFiles) # allows to be exectued on enter key, function needs event=None
		self.inputFile_browseButton.grid(column=3,row=2,padx=5,pady=5,stick="nesw")

		self.inputFile_clearButton = tk.Button(self, text="Clear File", width=25, command=self.clearFilename)
		self.inputFile_clearButton.grid(column=4,row=2,padx=5,pady=5,stick="nesw")


##		## set the input file type - this will be of types "we" know, so csv, specific data files, etc
		self.fileType_label = tk.Label(self, text="File Type:", font=("Helvetica",10), bg="white")
		self.fileType_label.grid(column=1,row=3,padx=5,pady=5,sticky="WNEW")

		self.fileType_combo = ttk.Combobox(self, width=25, values=['csv','other types to come...'])
		self.fileType_combo.current(0) # default vales = first in values list
		self.fileType_combo.grid(column=2, row=3, padx=5, pady=5, sticky="WNES")



##		## button to actually read in the file and do the processing
		self.processFile_button = tk.Button(self, text="Process File", font=("Helvetica",14), width=40, height=1, command=self.processFile)
		self.processFile_button.grid(column=1, row=4, padx=10, pady=10, columnspan=2, rowspan=2, stick="WNES")



##		## add in a text frame to print some info on data file?
		self.processedFile_info = Text(self, width=80, height=25, font=("Courier",8), borderwidth=2)
		self.processedFile_info.grid(row=6,column=2, columnspan=3)
		self.processedFile_info.grid_remove() # use this to hide until it is needed.

		# need this to run the mainloop and keep window open
		self.mainloop()


	# event=None needs to be in to be used by <Return> key
	def browseFiles(self,event=None):
		""" search for files on local machine """
		filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file")  
		self.inputFile_combo.set(filename)


	def clearFilename(self):
		self.inputFile_combo.set('')


	def processFile(self, fileType="csv"):

		# need to check if a file has been given to check
		if self.inputFile_combo.get() == '':
			messagebox.showerror(title="Missing File", message="No input file selected...")
			return

		# remove any text within box if it exists...
		self.processedFile_info.delete('1.0',END)
		# un hide the text box
		self.processedFile_info.grid()

		# read the datefile into a dataframe
		if fileType == "csv":
			df = pd.read_csv(self.inputFile_combo.get())

			InfoString = \
			f'''The dataframe has {df.shape[0]} rows and {df.shape[1]} columns.\nThe column headers are:
			{self.list2VerticalString(df.columns.to_list())}\nBelow is a snippet of the date imported\n===========\n'''

			self.processedFile_info.insert(END, "Processed: " + self.inputFile_combo.get() +"\n")
			self.processedFile_info.insert(END, InfoString)
			self.processedFile_info.insert(END, df.head().to_string(index=False))




	def list2VerticalString(self,oldList):
		''' bring in a list of strings and return vertical string '''
		newString = '\n'
		for ind, val in enumerate(oldList):
			newString += str(ind+1)+": "+val+'\n'
		return newString







if __name__ == "__main__":
	mygui = MainUI()

	
	