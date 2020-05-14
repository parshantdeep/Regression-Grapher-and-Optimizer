import xlrd #Module used to read data from excel
import sys
from pylab import plot,show,scatter,legend,ylabel,xlabel,subplot,tight_layout # Part of Lib Matplotlib used to plot graph
from scipy.optimize import curve_fit # Module used for curve fitting
from scipy.interpolate import interp1d
import numpy as np #For Data Analysis
from math import log #Importing log function from Math
from tkinter import * #Tkinter, GUI Library for Python
from models import *
from tkinter import filedialog

# r = row
# c = column
# updatelistbx(fl): updates listbox with new genes from file fl or returns an error if invalid fl passed

#nextclicks = 0 #For Next Button in identwind function
datalist = []
# correspodence = {'xvals' : [[]....],
#                 'samples' : [[]...],
#                 'yvalues' : [[]....]
#                 'intrap'  : [[[sample1 for gene1]....]..[file 2]....]}
correspodence = {'xvals':[[0.00015241579, 0.00045724737, 0.00137174211, 0.00411522633, 0.01234567901, 0.03703703703, 0.11111111111, 0.333333333, 1.0]],
                 'samples': [],
                 'yvalues': []}
firstrow = 0
intens10_rn: int = 39 #Intensity reporter 10 row number in sheet
intens1_rn: int = 30 #Intensity reporter 1 row number in sheet
models = {'Quadratic':quad, 'Cubic':cubic,'5PL':fivepl} # Dictional to relate relevant strings to their corresponding
                                                        # functions

def selectfile():
    global nextclicks
    nextclicks = 0
    fl = filedialog.askopenfilename(initialdir = "C:/Users/parsh/Desktop/Protien Data", title = "Select a file",
                                    filetypes= (("Excel Files", "*.xlsx"),("CSV Files", "*.csv")))
    extractdata(fl)

def extractdata(fl):
    try:
        wb = xlrd.open_workbook(fl) ## Load the excel workbook
        global sheet
        sheet = wb.sheet_by_index(0) # Load the First sheet in the workbook -- probably want to be user defined
        data = [[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)] # List of lists --
        # with first list corresponding to first row
        datalist.append(data)
        identwind()
    except:
        messagebox.showerror(title="Error", message="Invalid or No File Selected!")

## ********************** Top Level Windows for Choosing Ident, X/Y Points *************
# identwind() creates a toplevel window to select an identifier
def identwind():
    top = Toplevel(root)
    top.title("Select an identifier")
    newframe = Frame(top)
    chooseidentlab = Label(newframe, text = "Choose Identifier: ")
    identlist = []
    for c in range(len(datalist[0][firstrow])):
        identlist.append(str(c) + ". " + datalist[0][firstrow][c])
    global chosen
    chosen = StringVar()
    chosen.set(identlist[0])
    identifiers = OptionMenu(newframe,chosen,*identlist)
    nextbt = Button(newframe,text = "Next",command = lambda: choosesamples(top))
    chooseidentlab.pack()
    identifiers.pack()
    nextbt.pack()
    newframe.pack()
    # global nextclicks
    # while(nextclicks == 0): #nextclicks traces the user's first Next Click
    #                         # As soon as the user makes the click, the top is destroyed
    #     top.update() # updates to keep waiting till the user makes the click event
    # nextclicks = 0

def addyvals(listbox,lst):
    selected = listbox.curselection()
    for item in selected:
        lst.append(int(listbox.get(item).split(".")[0]))
    for item in selected:
        listbox.delete(item)

def addsamples(listbox, lst):
    selected = listbox.curselection()
    for item in selected:
        lst.append(int(listbox.get(item).split(".")[0]))
    for item in selected:
        listbox.delete(item)


def choosesamples(oldtop):
    # global nextclicks
    # nextclicks += 1
    oldtop.destroy()
    top2 = Toplevel(root)
    top2.title("Select Samples")
    frame2 = Frame(top2)
    allyvalslab = Label(frame2, text = "All Values: ")
    allyvals = Listbox(frame2, selectmode=SINGLE)
    for col in range(intens1_rn,intens10_rn+1):
        allyvals.insert(END, str(col) + ". " + datalist[-1][firstrow][col])
    allyvals.pack(side=LEFT)
    yvalues = []
    samples = []
    addtoselectedbt = Button(frame2,text = "Add to Y Values", command = lambda: addyvals(allyvals,yvalues))
    addtosamplesbt = Button(frame2, text = "Add to Samples", command = lambda: addsamples(allyvals,samples))
    addtosamplesbt.pack()
    addtoselectedbt.pack()
    frame2.pack()
    while (len(allyvals.get(0,END)) != 0):
        top2.update()
    correspodence['yvalues'].append(yvalues)
    correspodence['samples'].append(samples)
    #choosexvals(top2)
    updatelistbx()
    print(correspodence)

def addx(lst, clicks, corx):
    lst.append(corx.get())
    clicks[0] += 1

def choosexvals(oldtop):
    oldtop.destroy
    xvals = []
    for item in correspodence['yvalues'][-1]:
        newtop = Toplevel(root)
        corx = DoubleVar()
        inputlbl = Label(newtop, text = "Enter corresponding X value for : " + str(item))
        inputbx = Entry(newtop,textvariable = corx)
        clicks = [0]
        nextbt = Button(newtop, text = "Next", command = lambda: addx(xvals, clicks, corx))
        inputlbl.pack()
        inputbx.pack()
        nextbt.pack()
        while(clicks[0] == 0):
            newtop.update()
        newtop.destroy()
    correspodence['xvals'].append(xvals)
    updatelistbx()





    # Choose range for columns for y values:
    # newframe2 = Frame(top2)
    # choosestartlab = Label(newframe2,text = "Enter Starting Column: ")
    # startcoln = IntVar()
    # endcoln = IntVar()
    # startent = Entry(newframe2, textvariable = startcoln)
    # startent.delete(0,END)
    # startent.insert(0,intens1_rn)
    # choosestartlab.pack()
    # startent.pack()
    # chooseendlab = Label(newframe2, text="Enter Last Column: ")
    # endent = Entry(newframe2, textvariable=endcoln)
    # endent.delete(0, END)
    # endent.insert(0, intens1_rn)
    # chooseendlab.pack()
    # endent.pack()
    # newframe2.pack()






# When resetting the program:
#       * Make nextclicks = 0
def updatelistbx():
    listbox.delete(0,END)
    global identifier_coln  # putting 0 because first letter is a number corresponding
    identifier_coln = int((chosen.get())[0])   # to chosen identifier's column
    global allgenes
    allgenes = genelistcreator(datalist)
    for row in range(1,len(allgenes)):
        listbox.insert(END, str(row) + ". " + str(allgenes[row]))

    # for row in range(1, sheet.nrows): #Ignoring zero because first row is just titles
    #     listbox.insert(END, str(row) + ". " + str(data[row][identifier_coln]))

def genelistcreator(datalist):
    allident = []
    for data in datalist:
        for row in data:
            allident.append(row[identifier_coln])

    allident = list(dict.fromkeys(allident)) #a way of removing duplicates from the list
    return allident

# selected_genes returns the identifier selected from the listbox
def select_genes():
    clicked_items = listbox.curselection()
    r = clicked_items[0] + 1 #adding 1 because the row seleced corresponds to row+1 in allgenes
    return allgenes[r]

# searchwhatrow(identifier) returns a list of row numbers corresponding to the identifier  in each
#                           data (if it exists) in datalist else if it doesn't exist, it says NA(means Not available)
def searchwhatrow(identifier):
    rows = []
    for datano in range(len(datalist)):
        rows.append('NA')
        for row in range(1,len(datalist[datano])):
            if (datalist[datano][row][identifier_coln] == identifier):
                rows[datano] = int(row)
                break

    return rows

def xycreator(improws,xlst,ylst):
    #correspodent['xvals'][datano] gives x vals defined by the user for that specific data
    for datano in range(len(improws)):
        x = [] #list of x vals for that certain gene in that certain file to be plotted
        y = [] #list of y vals for that certain gene in that certain file to be plotted 
        #datalist[datano][improws[datano]] is actaully the data we are going to be playing with - this corresponds to the gene selected 
        # by user to be graphed ---- only if improws[datano] is not 'NA'
        #datalist[datano] gives the whole data
        #correspodence['yvalues'][datano] contains all the colnos required for y vals
        if (improws[datano] != 'NA'):
            ycols = correspodence['yvalues'][datano]
            xvalues = correspodence['xvals'][datano]
            for index in range(len(ycols)):
                yvalue = datalist[datano][improws[datano]][ycols[index]]
                xvalue = xvalues[index]
                if (yvalue > 0):
                    y.append(yvalue)
                    x.append(xvalue)
        
        xlst.append(x)
        ylst.append(y)
    print(xlst)
    print(ylst)




xfit = np.arange(0.0,1.01,0.01)
def show_graph():

    improws = searchwhatrow(select_genes()) #important rows contains row numbers for the certain identifier selected in each data file
                                            # so 1st item in improws corresponds to row number in first file for that identifier
    listofxvals,listofyvals = [],[]
    #Adding all the intensities greater than zero to the y list - This ensures that zero intensities are not counted
    
    xycreator(improws,listofxvals,listofyvals)
    # listofxvals = [] # Contains xvalues for all files in the form of lists
    # for index in range(len(datalist)):
    #     listofxvals.append(correspodence['xvals'][index])
    
    # for index in range(len(datalist)):
    #     y = []
    #     for c in correspodence['yvalues'][index]: #Needs to be changed when intensities become user defined
    #         yvalue = datalist[index][improws[index]][c]
    #         if yvalue > 0:
    #             y.append(yvalue)
    #         else:
    #             listofxvals[index].pop(len(y))
    #     listofyvals.append(y)
    
    # if onoff.get() == 1 :
    #     for index in range(len(listofyvals)):
    #         listofyvals[index] = list(map(log, listofyvals[index]))

    #         ylabel('Log of Recorder Intensities')
    # else:
    #      ylabel('Recorder Intensities')


    
    # What to do when a gene doesn't have any name in the excel sheet
    for index in range(len(listofxvals)):
        if len(listofxvals[index]) == 0:
            messagebox.showerror(title = 'Warning', message = "The item selected doesn't exist in File no. {} or all of the Y values are 0".format(index + 1))
        else:
            try:
                popt,pcov = curve_fit(models[clicked.get()],listofxvals[index],listofyvals[index], maxfev = 10000)
                subplot(1, len(listofxvals), index+1)
                xlabel('Absolute Values')
                plot(xfit, models[clicked.get()](xfit, *popt))
                #label=datalist[index][improws[index]][identifier_coln])
                scatter(listofxvals[index], listofyvals[index])
                print(popt)

            except:
                messagebox.showerror(title = 'Error', message = "Insufficient non-zero Y points for the curvefitting! ")

    tight_layout()
    show()

            #messagebox.showerror(title = "Error", message = "Insufficient non-zero Y points for the curvefitting! ")
# intrap(ident) performs intrap on 
def inter(ident,label):
    improws = searchwhatrow(ident)
    listofxvals,listofyvals = [],[]
    xycreator(improws,listofxvals,listofyvals)
    global finalresult
    finalresult = []
    for datano in range(len(datalist)):
        interlistforfile = []
        if len(listofyvals[datano]) != 0:
            try:
                popt,pcov = curve_fit(models[clicked.get()],listofxvals[datano],listofyvals[datano], maxfev = 10000)
                global xfit
                fittedyvals = models[clicked.get()](xfit, *popt)
                interfunc = interp1d(fittedyvals,xfit)
            except:
                for samplecol in correspodence['samples'][datano]:
                    interlistforfile.append('MNC') #Model not compatible
                continue
            impdata = datalist[datano][improws[datano]]
            for samplecol in correspodence['samples'][datano]:
                try:
                    interlistforfile.append(float(interfunc(impdata[samplecol])))
                except:
                    interlistforfile.append('NIR')
        else: 
            for samplecol in correspodence['samples'][datano]:
                interlistforfile.append('NA')
        finalresult.append(interlistforfile)
    label['text'] = (str(finalresult))
    print(finalresult)

        
        

# show_graph first calls the function select_genes to see what genes have been selected by user
#            and then this function loops through all the corresponding data and produces a graph
# def show_graph():
#     for r in select_genes():
#        r += 1 #Increment r(row no) by 1 because the least r is 0 which would correspond to row 1 in spreadsheet
#     y = [] # Initiating y to be an empty list
#
#     #Adding all the intensities greater than zero to the y list - This ensures that zero intensities are not counted
#     for c in range(intens10_rn,intens1_rn,-1):
#          if data[r][c] > 0:
#              y.append(data[r][c])
#
#     if onoff.get() == 1 :
#          y = list(map(log,y))
#          ylabel('Log of Recorder Intensities')
#     else:
#          ylabel('Recorder Intensities')
#     x = []
#     count = 1
#     dilfact = 1/3  # Dilution Factor
#     for i in y:
#          x.append(count)
#          count *= dilfact
#     # What to do when a gene doesn't have any name in the excel sheet
#     if len(y) > 0:
#         try:
#             popt,pcov = curve_fit(models[clicked.get()],x,y, maxfev = 10000)
#             plot(xfit, models[clicked.get()](xfit, *popt), label=data[r][identifier_coln])
#             scatter(x, y)
#             xlabel('Absolute Values')
#             legend()
#             show()
#         except:
#             messagebox.showerror(title = "Error", message = "Insufficient non-zero Y points for the curvefitting! ")
#
#     else:
#      messagebox.showerror(title = "Error", message = "No Y Points!")
## GUI STUFF ##

root = Tk()
root.title('Protien Graphing Software')
root.geometry("500x500")
uploadfilebt = Button(root,text = "Load File", command = selectfile).pack()
frame = Frame(root, height=500, width=500)
#************DROPDOWN BOX FOR MODEL************
clicked = StringVar()
clicked.set("Cubic")
droplabel = Label(root, text="Choose Model for Curve-fitting: ").pack()
drop = OptionMenu(root, clicked, "Quadratic", "Cubic", "5PL")
drop.pack()
#***********************************************
#****************Scrollbar and Listbox**********
scroll = Scrollbar(frame)
scroll.pack(side=RIGHT, fill=Y)
listbox = Listbox(frame, yscrollcommand=scroll.set, selectmode=SINGLE)
listbox.pack(side=LEFT)
scroll.config(command=listbox.yview)
showgraphbt = Button(frame, text="Show Graph", command=show_graph)
showgraphbt.pack(side=BOTTOM)
interpolatebt = Button(frame, text = "Interpolate", command = lambda: inter(select_genes(),resultlabel))
interpolatebt.pack(side = BOTTOM)
t = StringVar()
resultlabel = Label(frame, text = t)
resultlabel.pack(side = BOTTOM)
#***********************************************
#***************Log Transform Checkbutton*******
onoff = IntVar()
logtrans = Checkbutton(frame,text = "Enable Log Transform", variable = onoff)
logtrans.deselect()
logtrans.pack()
frame.pack(side=LEFT)
root.mainloop()
