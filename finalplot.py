import tkinter as tk
import os, json

#importing result.json for ploting bar graph
infile = open(os.getcwd()+"/result.json")
temp = json.load(infile)

ids = []
score = []


print("\n")
print("Resume Scores : ")
print("------------------------------------------------------------------")
for _ ,j in temp.items():
	ids.append(j[0][4:])
	score.append(j[2]/5)
	print("\n Id : {}\tName : {}  \n Score:{}%\n Resume File : {}\n".format(j[0],j[1],j[2],"data/"+_))
	print("------------------------------------------------------------------")

root = tk.Tk()
root.title("Resume Analysis Report")
root.geometry("650x350")
root.resizable(height=False,width=False)
c_width = 650  
c_height = 350  
c = tk.Canvas(root, width=c_width, height=c_height, bg='black')
c.pack()

y_stretch = 15 
y_gap = 10  
x_stretch = 20  
x_width = 45  
x_gap = 10  

for x, y, name in zip(range(len(score)), score, ids):
    x0 = x * x_stretch + x * x_width + x_gap
    y0 = c_height - (y * y_stretch + y_gap)
    x1 = x * x_stretch + x * x_width + x_width + x_gap
    y1 = c_height - y_gap
    c.create_rectangle(x0, y0, x1, y1, fill="green")
    c.create_text(x0 + 2, y0, anchor=tk.SW, text=str(name), fill="yellow")
root.mainloop()