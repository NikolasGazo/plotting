
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

import matplotlib.pyplot as plt

# 
## potentially for plotting
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
## https://matplotlib.org/examples/user_interfaces/embedding_in_tk.html


from matplotlib.widgets import Slider, Button, RadioButtons






## main ui code

class MainUI(tk.Frame):
# inherit from tk.Tk class
	def __init__(self, master, *args, **kwargs):
		super().__init__(master, *args, **kwargs)

		### the main Tk Window
		master.title(" Dataframe plotting - V2020-08.01.01")
		# give it a favicon/icon - the image seen in the top left
		master.iconbitmap("./favicon.ico")
##		# grab width and height of main screen and make that the geometry of the window pop up...
		master.ws=master.winfo_screenwidth()
		master.hs=master.winfo_screenheight()
		master.x=0.95*master.ws
		master.y=master.hs
		master.geometry('%dx%d+0+0'%(master.x,master.y))
		master.configure(bg='white')

###		####-- Main UI build up --##

###		### Add a file menu, just in case we want it later...
		## create a main menu bar
		self.menuBar = tk.Menu(master, bg='lightgrey', fg='black')

		## add a "File" menu to put into main menu bar (tearoff=1 allows u to pop out the menu dropdown)
		self.fileMenu = tk.Menu(self.menuBar, tearoff=0, bg='white', fg='black')
		self.fileMenu.add_command(label="file 1", command=self.label1)
		self.fileMenu.add_command(label="Quit", command=self.quit)

		## add an "Edit" drop down
		self.editMenu = tk.Menu(self.menuBar, tearoff=0, bg='white', fg='black')
		self.editMenu.add_command(label="edit 1", command=self.label1)

		## add the menus to the main menu on the UI
		self.menuBar.add_cascade(label='File', menu=self.fileMenu)
		self.menuBar.add_cascade(label='Edit', menu=self.editMenu)

		## add the main menu bar to the UI
		master.config(menu=self.menuBar, borderwidth=5,)

##		## add the notebook, to add tabs to the top
		self.notebook = ttk.Notebook(self.master)

##		## add the tabs to out notebook, objects will inherit from tk.Frame
		self.inputTab = InputDataUI(self.notebook)
		self.plotTab = PlottingUI(self.notebook)

		# v = tk.Scrollbar(self.inputTab, orient=tk.VERTICAL).grid()


##		## give each tab a reference to the other tab 
		## 
		self.inputTab.plotTab = self.plotTab
		self.plotTab.inputTab = self.inputTab

##		## add the tabs into the notebook of the frame, ie create actual tabs
		self.notebook.add(self.inputTab, text = ' Input Data ')
		self.notebook.add(self.plotTab, text = ' Plotting ')

##		## set the notebook into the main frame/window of the UI
		self.notebook.pack()#grid(row=0,column=0,pady=10)

##		## required for the gui to continually loop and "run"
		# self.mainloop()

	def label1(self):
			''' function for menu item '''
			print(self.tab_1.df)


##########################################
##########################################
## the data input tab ##

class InputDataUI(tk.Frame):
# this will inherit parent, which inherits tk.Tk(), so we dont need to inherit that again here
# so the parent is the object that is calling this window and thus we will set the widgets in that object, not self

	def __init__(self, master, *args, **kwargs):
		super().__init__(master, *args, **kwargs)

		# initialize to have the self object and the parent
		self.configure(bg='white')
		self.plotTab = None # default value at the start

		## make an empty DataFrame
		self.df = pd.DataFrame()
		self.df.name = "Empty Dataframe!"

		####-- Input Data File UI build up --##
##		## Main input file area... refer to all the objects/functions to self, theyre just in the parent object/frame
		self.inputFile_label = tk.Label(self, text="Input File:", font=("Helvetica",10), bg="white")
		self.inputFile_label.grid(column=1,row=2,padx=5,pady=5,sticky="WNES") # sticky helps push away from borders here

		## input file combo box - default values are the files in current directory
		self.inputFile_combo = ttk.Combobox(self, width=50, values=glob.glob("./*") )
		self.inputFile_combo.current(3)
		self.inputFile_combo.grid(column=2,row=2,padx=5,pady=5,sticky="WNES")

		## browse buttong to search for files outside current directory - calls browseFiles functions
		self.inputFile_browseButton = tk.Button(self, text="Browse for File...", command=self.browseFiles)
		self.inputFile_browseButton.bind('<Return>', self.browseFiles) # allows to be exectued on enter key, function needs event=None
		self.inputFile_browseButton.grid(column=3,row=2,padx=5,pady=5,stick="nesw")

		## button to clear the input file field box
		self.inputFile_clearButton = tk.Button(self, text="Clear File", width=25, command=self.clearFilename)
		self.inputFile_clearButton.grid(column=4,row=2,padx=5,pady=5,stick="nesw")

##		## set the input file type - this will be of types "we" know, so csv, specific data files, etc
		self.fileType_label = tk.Label(self, text="File Type:", font=("Helvetica",10), bg="white")
		self.fileType_label.grid(column=1,row=3,padx=5,pady=5,sticky="WNEW")

		## combo box to select one of the to-be predefined file types, currently csv
		self.fileType_combo = ttk.Combobox(self, width=25, values=['csv','other types to come...'])
		self.fileType_combo.current(0) # default vales = first in values list
		self.fileType_combo.grid(column=2, row=3, padx=5, pady=5, sticky="WNES")

##		## button to actually read in the file and do the processing
		self.processFile_button = tk.Button(self, text="Process File", font=("Helvetica",14), width=40, height=1, command=self.processFile)
		self.processFile_button.grid(column=1, row=4, padx=10, pady=10, columnspan=2, rowspan=2, stick="WNES")

##		## add in a text frame to show the log, ie initial column types and then converted
		## plotting is a mess if the column type is object (ie string)
		self.processedFile_log = Text(self, width=60, height=30, font=("Courier",8), borderwidth=2, padx=2, pady=2)
		self.processedFile_log.grid(row=6,column=1, columnspan=2, sticky='nw', pady =2)
		self.processedFile_log.grid_remove() # use this to hide until it is needed.

##		## add in a text frame to print some info on data file?
		self.processedFile_info = Text(self, width=80, height=30, font=("Courier",8), borderwidth=2, padx=2)
		self.processedFile_info.grid(row=6,column=3, columnspan=3)
		self.processedFile_info.grid_remove() # use this to hide until it is needed.




	# event=None needs to be in to be used by <Return> key
	def browseFiles(self,event=None):
		""" search for files on local machine """
		filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file")  
		self.inputFile_combo.set(filename)

	def cleanDF(self,df):
		"""  This will be function that will clean the DF, may do it in-class, or may write own function """
		return df


	def clearFilename(self):
		self.inputFile_combo.set('')




	def processFile(self, fileType="csv"): 

		# need to check if a file has been given to process
		if self.inputFile_combo.get() == '':
			self.inputFile_label.config(bg='green')
			messagebox.showerror(title="Missing File", message="No input file selected...")
			self.inputFile_label.config(bg='white')
			return

		# remove any text within box if it exists...
		self.processedFile_info.delete('1.0',END)
		## under the assumption that the processing worked; want to decipher the columns.
		if self.processedFile_log.index("end") != 0:
			self.processedFile_log.delete('1.0', END)

		# un hide the text box
		self.processedFile_info.grid()
		self.processedFile_log.grid()

		# read the data file into a dataframe
		if fileType == "csv":
			self.df = pd.read_csv(self.inputFile_combo.get())
			# print the initial dataframe column types...
			self.processedFile_log.insert(END, "Initial DataFrame column types (must convert 'object'):\n\n")
			self.processedFile_log.insert(END, f'{self.df.dtypes}')
			self.processedFile_log.insert(END, "\n\n-----------------------------------------------\n")

			self.df = DataCleaning.cleanDF(self.df)
			self.df.name = 'Input Data DF' # may change this to be more personal to the casE?

			self.processedFile_log.insert(END, "\nAfter clean - DataFrame column types:\n\n")
			self.processedFile_log.insert(END, f'{self.df.dtypes}')

			InfoString = \
			f'''The dataframe has {self.df.shape[0]} rows and {self.df.shape[1]} columns.\nThe column headers are:
			{self.list2VerticalString(self.df.columns.to_list())}\nBelow is a snippet of the date imported\n===========\n'''

			self.processedFile_info.insert(END, "Processed: " + self.inputFile_combo.get() +"\n")
			self.processedFile_info.insert(END, InfoString)
			self.processedFile_info.insert(END, self.df.head().to_string(index=False) +"\n\n")
			self.processedFile_info.insert(END, self.df.tail().to_string(index=False))




	def list2VerticalString(self,oldList):
		''' bring in a list of strings and return vertical string '''
		newString = '\n'
		for ind, val in enumerate(oldList):
			newString += str(ind+1)+": "+val+'\n'
		return newString


##################################################
##################################################

class PlottingUI(tk.Frame):
# so the parent is the object that is calling this window and thus we will set the widgets in that object,

	def __init__(self, master, *args, **kwargs):
		super().__init__(master, *args, **kwargs)

		# initialize to have the self object and the parent
		self.configure(bg='white')
		self.inputTab = None # default value at the start

		####-- Input Data File UI build up --###

##		## Main input file area... refer to all the objects/functions to self, theyre just in the parent object/frame
		self.inputDF_label = tk.Label(self, text="Input DataFrame", font=("Helvetica",10), bg="white")
		self.inputDF_label.grid(column=1,row=2,padx=5,pady=5,sticky="WNES") # sticky helps push away from borders here

		## input file combo box - default values are the files in current directory
		self.inputDF_entry = tk.Entry(self, width=50, borderwidth=3)
		self.inputDF_entry.insert(END, 'NULL')
		self.inputDF_entry.grid(column=2,row=2,padx=5,pady=5,sticky="WNES")

		## browse buttong to search for files outside current directory - calls browseFiles functions
		self.inputDF_importButton = tk.Button(self, text="Import DF", bg='yellow', command=self.importDF)
		self.inputDF_importButton.bind('<Return>', self.plotDF) # allows to be exectued on enter key, function needs event=None
		self.inputDF_importButton.grid(column=3,row=2,padx=5,pady=5,stick="nesw")

		##  plot the dataframe to search for files outside current directory - calls browseFiles functions
		self.inputDF_plotButton = tk.Button(self, text="Plot DF", bg='red',command=self.plotDF)
		self.inputDF_plotButton.bind('<Return>', self.plotDF) # allows to be exectued on enter key, function needs event=None
		self.inputDF_plotButton.grid(column=4,row=2,padx=5,pady=5,stick="nesw")


		frameHeight=650
##		## figure axes info, will be left side
		self.figureAxes = tk.Frame(self, borderwidth=2, width=100, height=frameHeight, bg='#ADD8E6')
		self.figureAxes.grid(column=1, row=3)
##		## figure frame, will host the figure
		self.figureFrame = tk.Frame(self,bg='gray', width=1600, height=frameHeight+150)
		self.figureFrame.grid(column=2, row=3,columnspan=5,)
##		## figure actions, buttons etc, will be on right side 
		self.figureActions = tk.Frame(self, borderwidth=2, width=100, height=frameHeight, bg='#3EA99F')
		self.figureActions.grid(column=12, row=3,padx=10)

##		## drop downdowns for the left side column - this is for the axes on each plot
		## these will go into the left side frame object
		self.topPlot_YVales_label = tk.Label(self.figureAxes, text="Top Plot \n Y-axes: ")
		self.topPlot_YVales_label.grid(row=0,column=0)
		self.topPlot_YVales_combo = ttk.Combobox(self.figureAxes,)
		self.topPlot_YVales_combo.grid(row=1,column=0)
		## the shared X-axis between the two plot
		self.sharedX_label = tk.Label(self.figureAxes, text="Shared X axes variable ")
		self.sharedX_label.grid(row=4, column=0)
		self.sharedX_combo = ttk.Combobox(self.figureAxes,)
		self.sharedX_combo.grid(row=5,column=0)
#		# button to refresh
		self.refreshPlot_Button = tk.Button(self.figureAxes, text="Refresh", command=self.refreshPlot)
		self.refreshPlot_Button.grid(row=3,column=1,padx=2,ipadx=2,ipady=2, pady=3)

		# the bottom plot Y values
		self.bottomPlot_YVales_label = tk.Label(self.figureAxes, text="Bottom Plot \n Y-axes: ")
		self.bottomPlot_YVales_label.grid(row=8, column=0)
		self.bottomPlot_YVales_combo = ttk.Combobox(self.figureAxes,)
		self.bottomPlot_YVales_combo.grid(row=9, column=0)


##		## buttons on right side to perform certain actions/functions
## 		## these buttons will go into the right frame
		self.topPlot_Button1 = tk.Button(self.figureActions, text="Button 1", command=self.button1).pack(padx=2,ipadx=2,ipady=2, pady=3)
		self.topPlot_Button2 = tk.Button(self.figureActions, text="Button 2", command=self.button2).pack(padx=2,ipadx=2,ipady=2, pady=3)
		self.topPlot_Button3 = tk.Button(self.figureActions, text="Button 3").pack(padx=2,ipadx=2,ipady=2, pady=3)
		self.topPlot_Button4 = tk.Button(self.figureActions, text="Button 4").pack(padx=2,ipadx=2,ipady=2, pady=3)
		self.topPlot_Button5 = tk.Button(self.figureActions, text="Button 5").pack(padx=2,ipadx=2,ipady=2, pady=3)
		self.topPlot_Button6 = tk.Button(self.figureActions, text="Button 6").pack(padx=2,ipadx=2,ipady=2, pady=3)
		self.topPlot_Button7 = tk.Button(self.figureActions, text="Button 7").pack(padx=2,ipadx=2,ipady=2, pady=3)
		self.topPlot_Button8 = tk.Button(self.figureActions, text="Button 8").pack(padx=2,ipadx=2,ipady=2, pady=3)
		self.topPlot_Button9 = tk.Button(self.figureActions, text="Button 9").pack(padx=2,ipadx=2,ipady=2, pady=3)



##		## figure aspect to the whole thing... had to make its own class...
		# create the Figure object and make an attribute of this current class
		self.fig = Figure(figsize=(12,8))

		# graph object which ties the figure into the tk.Frame -> figureFrame
		plot = FigureCanvasTkAgg(self.fig, self.figureFrame)
		# this packs the graph widget into the frame - without it the "graph" doesnt show up
		plot.get_tk_widget().pack(side='top', fill='both', expand=True)

		# take the Figure object into the plot class, probably cleanest this way
		# # add this object as an attribute to this current class to use functions and drop downs...
		self.MainPlot = MainPlotWindow(self.fig)


		# toolbar = NavigationToolbar2Tk(plot, self.figureFrame)
		# toolbar.update()
		# plot.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


		# def on_key_press(event):
		#     print("you pressed {}".format(event.key))
		#     key_press_handler(event, plot, toolbar)

		# plot.mpl_connect("key_press_event", on_key_press)
##https://stackoverflow.com/questions/11551049/matplotlib-plot-zooming-with-scroll-wheel


	def button1(self):
		self.MainPlot.plot1.set_color('green')
		self.MainPlot.fig.canvas.draw_idle()


	def button2(self):
		self.MainPlot.newPlot()

	# event=None needs to be in to be used by <Return> key
	def importDF(self,event=None):
		""" make sure to read in the dataframe from the input data tab """
		if self.inputTab:
			print("recognizes other tab")
			if not self.inputTab.df.empty:
				print("df exists!")
				# empty the entry box and add df name from other tab
				self.inputDF_entry.delete(0,END)
				self.inputDF_entry.insert(END,self.inputTab.df.name)
				# change colors of the buttons used..
				self.inputDF_importButton.config(bg='Green')
				self.inputDF_plotButton.config(bg='yellow')
				print(self.inputTab.df)
				## add values the combo boxes
				self.topPlot_YVales_combo.config(value=list(self.inputTab.df.columns))
				self.topPlot_YVales_combo.current(1)
				self.sharedX_combo.config(value=list(self.inputTab.df.columns))
				self.sharedX_combo.current(0)
				self.bottomPlot_YVales_combo.config(value=list(self.inputTab.df.columns))
				self.bottomPlot_YVales_combo.current(1)

			elif self.inputTab.df.empty:
				print("Input data tab is empty")
				self.inputDF_entry.delete(0,END)
				self.inputDF_entry.insert(END, 'Input Data Tab DF is NULL')


	# event=None needs to be in to be used by <Return> key
	def plotDF(self,event=None):
		""" this will take the dataframe and plot, put column names into columns """

		if self.inputTab:
			print("recognizes other tab")
			if not self.inputTab.df.empty:
				print("df exists!")
				print(self.inputTab.df)
				self.inputDF_plotButton.config(bg='green')
			elif self.inputTab.df.empty:
				print("Input data tab is empty")
				return # i think..

		if self.inputTab:

			if self.topPlot_YVales_combo.get() != '' and self.sharedX_combo.get() != '' and self.bottomPlot_YVales_combo.get():
				print('in update plot area...')
				x = self.sharedX_combo.get()
				yTop = self.topPlot_YVales_combo.get()
				yBot = self.bottomPlot_YVales_combo.get()

				self.MainPlot.updatePlot(self.inputTab.df,x,yTop,yBot)

				print('done')


	def refreshPlot(self):
		if self.topPlot_YVales_combo.get() != '' and self.sharedX_combo.get() != '' and self.bottomPlot_YVales_combo.get():
			print('in update plot area...')
			x = self.sharedX_combo.get()
			yTop = self.topPlot_YVales_combo.get()
			yBot = self.bottomPlot_YVales_combo.get()

			self.MainPlot.updatePlot(self.inputTab.df,x,yTop,yBot)



class MainPlotWindow():

    #------------------------------------------------------
	def __init__(self,fig):
    	# initialize the MainPlotWindow instance self.fg to be the fig we're bringing in...
		self.fig = fig
		self.ax1, self.ax2 = self.fig.subplots(2,1, sharex=True)
		# add grid lines
		self.ax1.grid(True)
		self.ax2.grid(True)

		# add title
		self.ax1.set_title("Top Plot")
		self.ax2.set_title("Bottom Plot")
		self.t = np.arange(0.0, 3.0, 0.01)
		self.s1 = np.sin(2.0*np.pi*self.t) 
		self.s2 = np.cos(2.0*np.pi*self.t)


		self.t2 = np.arange(0.0,600.0, 0.01)
		self.s12 = np.sin(2.0*np.pi*self.t2)
		## need to make a reference to the lines of the plot... must be "self.plot,". without comma it is list
		self.plot1, = self.ax1.plot(self.t,self.s1)
		self.ax1.set_title('Top plot')
		self.plot2, = self.ax2.plot(self.t,self.s2)
		self.ax2.set_title("Bottom plot")

		print(type(self.plot1))


	def newPlot(self):
		self.ax1.clear()
		print(type(self.t2))
		self.ax1.plot(self.t2,self.s12)
		self.fig.canvas.draw_idle() # need this line to actually draw to the figure

		self.ax1.grid(True)
		self.ax2.grid(True)
	
	def updatePlot(self,df,x,yTop,yBot):
		self.ax1.clear()
		self.ax2.clear()


		xVals = df[x].values
		yTopVals = df[yTop].values
		yBotVals = df[yBot].values

		self.ax1.plot(xVals,yTopVals)
		self.ax2.plot(xVals,yBotVals)

		self.ax1.grid(True)
		self.ax2.grid(True)


		self.fig.canvas.draw_idle() # need this line to actually draw to the figure

#----------------------------------------------------------





## dataframe cleaning class... may move to own module/file
class DataCleaning():


	def cleanDF(df):
	    ## find the column types - if none are 'object' then money
	    colNames = df.columns.astype(str).tolist()
	    colTypes = df.dtypes.astype(str).tolist()
	    
	    
	    colsToInfer = [col for col in df.columns if df[col].dtype == 'object']
	    
	    for col in colsToInfer:
	        # temp = df[col]
	        try:
	            tempCol = pd.to_datetime(df[col])
	            df[col] = tempCol
	        except:
	            pass
	        finally:
	            pass


	    return df




##################################################
##################################################






if __name__ == "__main__":
	root = tk.Tk()
	main_window = MainUI(root)
	# main_window.grid(row=1,column=0)#(side='top', fill="both", expand=True)
	root.mainloop()

	
	

