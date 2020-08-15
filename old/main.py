
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
# import the drop down boxes in tkinter
from tkinter import ttk
# dialog box for files on local machine
from tkinter import filedialog
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









def main_window():
	### the main Tk Window
	# make the main tk window object
	root = tk.Tk()
	# give it a title
	root.title(" Dataframe plotting - V2020-07.4")
	# give it a favicon/icon - the image seen in the top left
	root.iconbitmap("./favicon.ico")
	# grab width and height of man screen and make that the geometry of the window pop up...
	ws=root.winfo_screenwidth()
	hs=root.winfo_screenheight()
	x=ws
	y=hs
	root.geometry('%dx%d+0+0'%(x,y))
	root.configure(bg='white')



	####-- Main UI build up --##

	## Main input file area...
	inputFile_label = tk.Label(root, text="Input File:", font=("Helvetica",10),bg="white")
	inputFile_label.grid(column=1,row=2,padx=5,pady=5,sticky="nsew") # sticky helps push away from borders here

	inputFile_combo = ttk.Combobox(root, width=25, values=glob.glob("./*") )
	inputFile_combo.grid(column=2,row=2,padx=5,pady=5,sticky="nesw")

	inputFile_browseButton = tk.Button(root, text="Browse for File...", command=browseFiles)
	inputFile_browseButton.grid(column=3,row=2,padx=5,pady=5,stick="nesw")


	# root.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=[("Text Files", "*.txt"),("CSV","*.csv")])
	root.mainloop()



def browseFiles():
	messagebox.showinfo("You are browsing files!", "OK, just testing the alerts")
	filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=[("All File types","*.*")])  #[("Text Files", "*.txt"),("CSV","*.csv")])
	print(filename)






if __name__ == "__main__":
	main_window()
	
	