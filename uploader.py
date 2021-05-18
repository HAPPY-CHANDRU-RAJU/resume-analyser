import tkinter as tk
from tkinter import *
from tkinter import filedialog
import shutil, os

SuccessFull = False

def Uploader():
	SuccessFull = False
	filename = filedialog.askopenfilename(initialdir = os.getcwd() ,title = "Select your resume file (*.pdf)")
	uploaderName = str(name.get()).strip()
	if(uploaderName):
		listSplit = filename.split("/")
		OfileName = listSplit[-1]
		if not os.path.exists(os.getcwd()+"/data/"+OfileName):
			shutil.copy(filename, os.getcwd()+"/data/")
		else:  
			ii = 1
			NfileName = "{}{}{}".format(OfileName[:-4],ii,OfileName[-4:])
			while True:
				if not os.path.exists(os.getcwd()+"/data/"+NfileName):
					shutil.copy(filename, os.getcwd()+"/data/"+NfileName)
					SuccessFull = True
					break 
				else:
					NfileName = "{}{}{}".format(OfileName[:-4],ii,NfileName[-4:])
					ii += 1

		label_file_explorer.config(text="Uploaded", fg = "green")
	else:
		label_file_explorer.config(text="Enter Name", width=10, fg = "red")
	
	
def submit():
	if(SuccessFull):
		label_file_explorer.config(text="Resume not yet ", width=10, fg = "red")
	else:
		label_file_explorer.config(text="App Submit", fg = "green")
		print("{} Your Application Submitted Successfully ".format(str(name.get()).strip()))

root=tk.Tk()
root.title("Resume Analysis - Uploader")
root.geometry("500x500")
root.resizable(height=False,width=False)

headingLabel=Label(root,text="\n\nData-driven HR Resume Analysis Based on \n NLP using Tkinter",font=('Helvetics',12,'bold'))
headingLabel.place(relx=.5,y=15,anchor='center')

Label(root,text="Enter Applicant Name").place(x=120,y=80)
name=StringVar()
nameBox=Entry(root,textvariable=name).place(x=220,y=80)

button_explore = Button(root,text = "Browse Files", command = Uploader).place(relx=.39,y=120)
label_file_explorer = Label(root,text = "Resume not yet !!", height = 4,fg = "red")
label_file_explorer.place(x=190,y=150)

tk.Button(root,text="Upload Resume",command=submit).place(relx=.5,y=300,anchor="center")

root.mainloop()