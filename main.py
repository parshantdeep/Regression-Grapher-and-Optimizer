import xlrd #Module used to read data from excel
import sys
from random import random,uniform
from matplotlib.pylab import plot,show,scatter,legend,ylabel,xlabel,subplot,tight_layout,text,annotate # Part of Lib Matplotlib used to plot graph
from scipy.optimize import curve_fit # Module used for curve fitting
from scipy.interpolate import interp1d
import numpy as np #For Data Analysis
from math import log #Importing log function from Math
from tkinter import * #Tkinter, GUI Library for Python
from tkinter import filedialog
from tkinter import ttk
import xlsxwriter
from PIL import ImageTk, Image
#pip install PILLOW
root = Tk()

# Curve-fitting model
def cubic(x, a, b, c, d):
    return a*x**3 + b*x**2 + c*x + d

def quad(x,a,b,c):
    return a*x**2 + b*x + c

def fivepl(x,a,b,c,d,m):
    return d + (a - d)/((1+(x/c)**b)**m)

def fourpl(x,a,b,c,d):
    return d + (a-d)/(1 + (x/c)**b)

# r = row
# c = column
# updatelistbx(fl): updates listbox with new genes from file fl or returns an error if invalid fl passed
datalist = []
correspodence = {'xvals':[],
                 'samples': [],
                 'yvalues': [],
                 'samplename': [],
                 'identcols' : [],
                 'filedirs' : [],
                 'filenames' : []}
firstrow = 0
models = {'Quadratic':quad, 'Cubic':cubic,'5PL':fivepl, '4PL': fourpl} # Dictionary to relate relevant strings to their corresponding
                                                        # functions

def selectfile():
    fl = filedialog.askopenfilename(title = "Select a file",
                                    filetypes= (("Excel Files", "*.xlsx"),("CSV Files", "*.csv"),("TXT File", "*.txt")))
    extractdata(fl)

def extractdata(fl):
    try:
        wb = xlrd.open_workbook(fl) ## Load the excel workbook
        global sheet
        sheet = wb.sheet_by_index(0) # Load the First sheet in the workbook -- probably want to be user defined
        data = [[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)] # List of lists --
        # with first list corresponding to first row
        datalist.append(data)
        correspodence['filedirs'].append(fl)
        print(data)
        Checkgrid()
        return 0
    except:
        pass
    
    try:
        textfile = open(fl,'r')
        data = textfile.readlines()
        for row in enumerate(data):
            data[row[0]] = (row[1].split('\n'))[0].split('\t')
            for each in enumerate(data[row[0]]):
                try:
                    data[row[0]][each[0]] = float(each[1])
                except:
                    pass
        datalist.append(data)
        correspodence['filedirs'].append(fl)
        Checkgrid()
    
    except:
        messagebox.showerror(title="Error", message="Invalid or No File Selected!")

## ********************** Top Level Windows for Choosing Ident, X/Y Points *************
cgobjects = []
class Checkgrid(object):
    def __init__(self):
        self.newwind = Toplevel(root)
        self.newwind.geometry("1000x1000")
        self.canvas = Canvas(self.newwind)
        self.frame = Frame(self.canvas)
        self.vsb = Scrollbar(self.newwind, orient= "vertical", command = self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side = "right", fill = "y")
        self.canvas.pack(side = "left", fill= "both",expand = True)
        self.canvas.create_window((4,4),window = self.frame, anchor = "nw", tags = "self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.clmcol,self.identcol, self.samplecol, self.yvalcol, self.xvalcol, self.samnamecol = 0,1,2,3,4,5
        cgobjects.append(self)
        finalizefn = lambda: self.finalize() 
        finalizebt = Button(self.frame, text = 'Finalize', command = finalizefn)
        finalizebt.grid(row = 0, column = self.samnamecol + 1)
        rowcurtlyat = 0
        #creating first row labels
        collab = Label(self.frame,text = 'Columns').grid(row = rowcurtlyat, column = self.clmcol)
        identlab = Label(self.frame, text = 'Identifier?').grid(row = rowcurtlyat, column = self.identcol)
        samlab = Label(self.frame, text = 'Sample?').grid(row = rowcurtlyat, column = self.samplecol)
        yvallab = Label(self.frame, text = 'Y Value?').grid(row = rowcurtlyat, column = self.yvalcol)
        xvallab = Label(self.frame, text = 'X Value: ').grid(row = rowcurtlyat, column = self.xvalcol)
        samname = Label(self.frame, text = "Sample's Name: ").grid(row = rowcurtlyat, column = self.samnamecol)
        self.grid = []
        self.fileno = len(datalist) - 1
        frstrowdata = datalist[-1][0]
        for eachcol in range(len(frstrowdata)):
            row = []
            rowcurtlyat += 1
            itemlab = Label(self.frame,text = frstrowdata[eachcol])
            itemlab.grid(row = rowcurtlyat, column = self.clmcol)
            row.append(itemlab)
            #Adding sample and y val check boxes for that row 
            for bt in range(3):
                b = Checkbutton(self.frame)
                b.pos = (bt+1,eachcol)
                b.var = IntVar()
                func = lambda w=b: self.check_cb(w)
                b.config(variable=b.var, command = func)
                b.grid(row = rowcurtlyat,column = bt+1)
                row.append(b)
            ##############################################################
            xvalent = Entry(self.frame)
            samnament = Entry(self.frame)
            xvalent.var = DoubleVar()
            samnament.var = StringVar()
            xvalent.config(textvariable=xvalent.var, state = DISABLED)
            samnament.config(textvariable=samnament.var, state = DISABLED)
            xvalent.grid(row = rowcurtlyat, column = self.xvalcol)
            samnament.grid(row = rowcurtlyat, column = self.samnamecol)
            row.extend([xvalent,samnament])
            self.grid.append(row) 
        print(self.grid)
        self.newwind.protocol("WM_DELETE_WINDOW", self.finalize)
        self.frame.mainloop()
    
    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def check_state(self,button):
        state = button.var.get()
        print(state)    
    def check_cb(self, button):
        x,y = button.pos
        state = button.var.get()
        row = self.grid[y]
        print(state)
        if state == 1:
            if x == self.samplecol:
                row[self.yvalcol].config(state = DISABLED)
                row[self.identcol].config(state = DISABLED)
                row[self.samnamecol].config(state = NORMAL)
            elif x == self.yvalcol :
                row[self.samplecol].config(state = DISABLED)
                row[self.identcol].config(state = DISABLED)
                row[self.xvalcol].config(state = NORMAL)
            else:
                row[self.samplecol].config(state = DISABLED)
                row[self.yvalcol].config(state = DISABLED)
                row[self.xvalcol].config(state = DISABLED)
                row[self.samnamecol].config(state = DISABLED)
        elif state == 0:
            if x == self.samplecol:
                row[self.yvalcol].config(state = NORMAL)
                row[self.identcol].config(state = NORMAL)
                row[self.samnamecol].config(state = DISABLED)
            elif x == self.yvalcol:
                row[self.identcol].config(state = NORMAL)
                row[self.samplecol].config(state = NORMAL)
                row[self.xvalcol].config(state = DISABLED)
            else:
                row[self.samplecol].config(state = NORMAL)
                row[self.yvalcol].config(state = NORMAL)
    # finalize(self) is gonna append selected samples and selected y values to correspodence and append xvals and sample names to correspodence too 
    def finalize(self):
        self.identcols,self.samplecols,self.yvalcols,samplenames,xvalues = [],[],[],[],[]
        filename = ''
        for rowno in range(len(self.grid)):
            if self.grid[rowno][self.samplecol].var.get() :
                self.samplecols.append(rowno)
                samplenames.append(self.grid[rowno][self.samnamecol].var.get())
                filename += self.grid[rowno][self.samnamecol].var.get()
                filename += ' '
            elif self.grid[rowno][self.yvalcol].var.get() :
                self.yvalcols.append(rowno)
                xvalues.append(self.grid[rowno][self.xvalcol].var.get())
            elif self.grid[rowno][self.identcol].var.get() :
                self.identcols.append(rowno)
        global correspodence
        try:
            del correspodence['xvals'][self.fileno]
            del correspodence['samples'][self.fileno]
            del correspodence['yvalues'][self.fileno]
            del correspodence['samplename'][self.fileno]
            del correspodence['identcols'][self.fileno]
            del correspodence['filenames'][self.fileno]
            filelistbox.delete(self.fileno)
        except:
            pass
        correspodence['xvals'].append(xvalues)
        correspodence['samples'].append(self.samplecols)
        correspodence['yvalues'].append(self.yvalcols)
        correspodence['samplename'].append(samplenames)
        correspodence['identcols'].append(self.identcols)
        correspodence['filenames'].append(filename)
        filelistbox.insert(self.fileno,filename)
        updatelistbx()
        self.newwind.withdraw()
        tabcontrol.select(1)
    
    def openback(self):
        self.newwind.deiconify()
        
def changesetting():
    cgobjects[filelistbox.curselection()[0]].openback()

def showdir():
    messagebox.showinfo("File Path",correspodence['filedirs'][filelistbox.curselection()[0]])

sortval = False
# When resetting the program:
#       * Make nextclicks = 0
def updatelistbx():
    listbox.delete(0,END)
    #global identifier_coln  # putting 0 because first letter is a number corresponding
    #identifier_coln = int((chosen.get())[0])   # to chosen identifier's column
    genelistcreator(datalist)
    global allgenes
    print(allgenes)
    for row in range(0,len(allgenes)):
        listbox.insert(END, str(row) + ". " + str(allgenes[row]))

    # for row in range(1, sheet.nrows): #Ignoring zero because first row is just titles
    #     listbox.insert(END, str(row) + ". " + str(data[row][identifier_coln]))

# Filter identifiers by no of calibrators
# Component:
# Filter idents with atleast 4 calib vals in either file:

# allgenes is the list of all the identifiers created
# in the genelistcreator function
def genelistcreator(datalist):
    global calibfiltval
    global allgenes
    global samplefilterbool
    allgenes = []
    for datano in range(len(datalist)):
        for row in enumerate(datalist[datano]):
            if row[0] == 0: #Skip the first row in data which is just the titles
                continue
            if calibfiltval.get()> 0 or samplefilterbool.get():
                xlist,ylist = [],[]
                xycreate(datano,row[0],xlist,ylist)
                if len(ylist)<calibfiltval.get():
                    continue
                if samplefilterbool.get() and len(ylist) != 0:
                    samplevals = []
                    samplevalcreate(datano,row[0],samplevals)
                    inrange = [] #List containing NIR for every sample not in range
                    miny,maxy = min(ylist),max(ylist) #wouldn't work if len(ylist) == 0
                    for samval in samplevals:
                        if samval < miny or samval > maxy:
                            inrange.append('NIR')
                    if len(inrange) == len(samplevals):
                        continue
            
            identname = ""
            for ident in correspodence['identcols'][datano]:
                identname+= str(row[1][ident])
                identname += "-"
            allgenes.append(identname)
    allgenes = list(dict.fromkeys(allgenes)) #removes duplicates by converting all the elements of list to keys of dictionary which have to be unique
    if sortval:
     allgenes.sort()


# selected_genes returns the identifier selected from the listbox
def select_genes():
    clicked_items = listbox.curselection()
    r = clicked_items[0] #adding 1 because the row seleced corresponds to row+1 in allgenes
    print(r)
    return allgenes[r]

# searchwhatrow(identifier) returns a list of row numbers corresponding to the identifier  in each
#                           data (if it exists) in datalist else if it doesn't exist, it says NA(means Not available)
def searchwhatrow(identifier):
    rows = []
    for datano in range(len(datalist)):
        rows.append('NA')
        for row in range(1,len(datalist[datano])):
            identname = ""
            for ident in correspodence['identcols'][datano]:
                identname+= str(datalist[datano][row][ident])
                identname += "-"
            
            if (identname == identifier):
                rows[datano] = int(row)
                break

    return rows

# Appends into xlst and ylst
#Takes in the fileno(datano), rowno, xlst, ylst
def xycreate(datano,rowno,xlst,ylst):
    row = datalist[datano][rowno]
    for calibcolumn in enumerate(correspodence['yvalues'][datano]):
        calibval = row[calibcolumn[1]]
        if calibval>0 :
            ylst.append(calibval)
            xlst.append(correspodence['xvals'][datano][calibcolumn[0]]) 


def xycreator(improws,xlst,ylst):
    #correspodent['xvals'][datano] gives x vals defined by the user for that specific data
    for datano in range(len(datalist)):
        x = [] #list of x vals for that certain gene in that certain file to be plotted
        y = [] #list of y vals for that certain gene in that certain file to be plotted 
        #datalist[datano][improws[datano]] is actaully the data we are going to be playing with - this corresponds to the gene selected 
        # by user to be graphed ---- only if improws[datano] is not 'NA'
        #datalist[datano] gives the whole data
        #correspodence['yvalues'][datano] contains all the colnos required for y vals
        if (improws[datano] != 'NA'): #if the identifier exists in that file
            xycreate(datano,improws[datano],x,y)
        
        xlst.append(x)
        ylst.append(y)
    print(xlst)
    print(ylst)
def samplevalcreate(datano,rowno,samplevalforeach):
    samplecols = correspodence['samples'][datano]
    data = datalist[datano][rowno]
    for samplecol in samplecols:
        samplevalforeach.append(data[samplecol])

def samplevalcreator(improws,samplevals):
    for datano in range(len(datalist)):
        samplevalforfile = []
        if (improws[datano] != 'NA'):
            samplevalcreate(datano,improws[datano],samplevalforfile)
        # if (onoff.get() == 1):
        #     samplevalforfile = list(map(log, samplevalforfile))
        samplevals.append(samplevalforfile)

def show_graph():
    ident = select_genes()
    intravals = inter(ident,resultlabel)
    samplevals = []
    improws = searchwhatrow(ident) #important rows contains row numbers for the certain identifier selected in each data file
                                            # so 1st item in improws corresponds to row number in first file for that identifier
    listofxvals,listofyvals = [],[]
    samplevalcreator(improws,samplevals)
    #Adding all the intensities greater than zero to the y list - This ensures that zero intensities are not counted
    xycreator(improws,listofxvals,listofyvals)
    for index in range(len(listofxvals)):
        if len(listofxvals[index]) == 0:
            messagebox.showerror(title = 'Warning', message = "The item selected doesn't exist in File no. {} or all of the Y values are 0".format(index + 1))
        else:
            xfit = np.arange(min(listofxvals[index]),max(listofxvals[index]),0.01)
            if (onoff.get() == 1):
                listofyvals[index] = list(map(log,listofyvals[index]))
            try:
                popt,pcov = curve_fit(models[clicked.get()],listofxvals[index],listofyvals[index], maxfev = maxfevvar.get())
            except:
                messagebox.showerror(title = 'Error', message = "Insufficient non-zero Y points for the curvefitting! ")
                continue
            sp = subplot(1, len(listofxvals), index+1)
            sp.title.set_text(correspodence['filenames'][index])
            if (onoff.get() == 1):
                ylabel('Log of Intensities')
            else:
                ylabel('Intensity')
            xlabel('Absolute Values')
            identname = ""
            for ident in correspodence['identcols'][index]:
                identname+= str(datalist[index][improws[index]][ident])
                identname += "-"
            plot(xfit, models[clicked.get()](xfit, *popt),label= identname + ' ' + clicked.get())
            scatter(listofxvals[index], listofyvals[index])
            sampleno = 0
            for i_x, i_y in zip(intravals[index],samplevals[index]):
                if (i_x != 'NA' and i_x != 'NIR' and i_x != 'MNC'):
                    if onoff.get() == 1:
                            i_y = log(i_y)
                    scatter(i_x,i_y)
                    label_x = uniform(min(listofxvals[index]),max(listofxvals[index]))
                    label_y = uniform(min(listofyvals[index]),max(listofyvals[index]))
                    arrow_prop = dict(facecolor = "black", width = 2, headwidth = 4, shrink = 0.1)
                    annotate("Sample: "+correspodence['samplename'][index][sampleno] + " ({} , {})".format(i_x,i_y), xy = (i_x,i_y),xytext = (label_x,label_y),arrowprops=arrow_prop)
                
                sampleno+=1
            print(popt)
    legend()
    tight_layout()
    show()
            #messagebox.showerror(title = "Error", message = "Insufficient non-zero Y points for the curvefitting! ")
# intrap(ident,label) returns a list of lists of intrapolated values of each sample in each datafile so returned value 
def inter(ident,label):
    improws = searchwhatrow(ident)
    listofxvals,listofyvals = [],[]
    xycreator(improws,listofxvals,listofyvals)
    global finalresult
    finalresult = []
    for datano in range(len(datalist)):
        interlistforfile = []
        if len(listofyvals[datano]) != 0:
            xfit = np.arange(min(listofxvals[datano]),max(listofxvals[datano]),0.01)
            if (onoff.get() == 1):
                listofyvals[datano] = list(map(log,listofyvals[datano]))
            try:
                popt,pcov = curve_fit(models[clicked.get()],listofxvals[datano],listofyvals[datano], maxfev = maxfevvar.get())
                fittedyvals = models[clicked.get()](xfit, *popt)
                interfunc = interp1d(fittedyvals,xfit)
            except:
                for samplecol in correspodence['samples'][datano]:
                    interlistforfile.append('MNC') #Model not compatible
                finalresult.append(interlistforfile)
                continue
            impdata = datalist[datano][improws[datano]]
            for samplecol in correspodence['samples'][datano]:
                tobeintrapolated = impdata[samplecol]
                if onoff.get() == 1:   
                    if tobeintrapolated > 0:                    
                        tobeintrapolated = log(tobeintrapolated)
                    else:
                        interlistforfile.append('NIR')
                        continue 
                if tobeintrapolated >= min(listofyvals[datano]):
                    try:
                        interlistforfile.append(float(interfunc(tobeintrapolated)))
                    except:
                        interlistforfile.append('NIR') #NIR means not in range
                else:
                    interlistforfile.append('NIR')
        else: 
            for samplecol in correspodence['samples'][datano]:
                interlistforfile.append('NA') #NA means not available
        
        finalresult.append(interlistforfile)
    label['text'] = (str(finalresult))
    print(finalresult)
    return finalresult



def spreadcreate():
    outworkbook = xlsxwriter.Workbook("{}.xlsx".format(clicked.get()))
    outsheet = outworkbook.add_worksheet()
    #Write headers first
    # first is going to be ident names, all other are going to be sam1 file1.. samn file1.....sam1 filen....samn file n  
    xcurrentlyat = 0
    ycurrentlyat = 0 
    outsheet.write(ycurrentlyat,xcurrentlyat,'Identifier Names: ')
    xcurrentlyat += 1
    for datano in range(len(datalist)):
        for sampleno in range(len(correspodence['samples'][datano])):
            outsheet.write(ycurrentlyat,xcurrentlyat,'Sample {} - File {}'.format(str(sampleno + 1)+correspodence['samplename'][datano][sampleno],datano + 1))
            xcurrentlyat += 1
    
    for eachident in allgenes:
        ycurrentlyat += 1
        xcurrentlyat = 0
        intradataeach = inter(eachident,resultlabel)
        outsheet.write(ycurrentlyat,xcurrentlyat,eachident)
        xcurrentlyat += 1
        for file in intradataeach:
            for eachsample in file:
                outsheet.write(ycurrentlyat,xcurrentlyat,eachsample)
                xcurrentlyat += 1
        xcurrentlyat += 1

    outworkbook.close()

def alphsort():
    global sortval
    sortval = True
    updatelistbx()
    sortval = False      
"""
searchitem(loi,item) returns a list of indexes of items in loi having same chars
                     as in item in same order
"""
def searchfn(loi,item):
    return([element for element in enumerate(loi) if item in element[1]])

global searchresult
searchresult = []

def createresults():
    global allgenes
    global searchresult
    searchresult = searchfn(allgenes,searchtext.get())
    nextsearch()
    
def nextsearch(*Event):
    global searchresult
    if searchresult != []:
        listbox.selection_clear(0,END)
        popped = searchresult.pop(0)
        listbox.selection_set(popped[0])
        listbox.activate(popped[0])
        listbox.see(popped[0])
    else:
        messagebox.showerror(title = "ERROR!", message = "NO MORE RESULTS! Press Search Again")

def updateinfotreeview(*event):
    if len(availableinlstbx.curselection())>0:
        fileno = availableinlstbx.curselection()[0]
        rowno = availableinlstbx.get(fileno)
        Remove = infoviewtree.get_children()
        for child in Remove:
            infoviewtree.delete(child) 
        if availableinlstbx.get(fileno)!= 'NA': 
            file = datalist[fileno]
            for field in enumerate(file[firstrow]):
                data = file[int(rowno)][field[0]]
                infoviewtree.insert("","end",text = "",values = (field[1],data))
            infoviewtree.focus()


def initiateinfoviewtree(event):
    if len(listbox.curselection())>0 :
        identifier = select_genes()
        whatrows = searchwhatrow(identifier)
        # Delete all in the availableinlstbx
        availableinlstbx.delete(0,END)
        #Delete all in the tree
        Remove = infoviewtree.get_children()
        for child in Remove:
            infoviewtree.delete(child)    
        #Put new stuff in the availableinlstbx
        for row in whatrows:
            availableinlstbx.insert(END,str(row))

## GUI STUFF ##
class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom


app=FullScreenApp(root)
root.title('Protien Graphing Software')
tabcontrol = ttk.Notebook(root)
uploadtab = Frame(tabcontrol, height = 400, width = 500)
uploadfilebt = Button(uploadtab,text = "Load File", command = selectfile, height = 15, width = 40)
uploadfilebt.pack(side = TOP)
canvas = Canvas(uploadtab)
canvas2 = Canvas(uploadtab)
#canvas3 = Canvas(uploadtab)
canvas.pack(side = LEFT, expand = YES, fill = BOTH)
canvas2.pack(side = RIGHT,expand = YES, fill = BOTH)
#canvas3.pack(side = BOTTOM, expand = YES, fill = BOTH)
img = Image.open('trchr-logo.png') #Both images are '350 by 88 pixels'
img2 = Image.open('uoft.png')
#img3 = Image.open('enter dir here.ex') #Image location can be entered in here
canvas.image = ImageTk.PhotoImage(img)
canvas2.image = ImageTk.PhotoImage(img2)
#canvas3.image = ImageTk.PhotoImage(img3)
canvas.create_image(250,200, image = canvas.image, anchor = 'nw')
canvas2.create_image(250,200,image = canvas2.image,anchor = 'nw')
#canvas3.create_image(250,200,image = canvas3.image, anchor = 'nw')
frame = Frame(root, height=400, width=500)
tabcontrol.add(uploadtab, text = "Welcome!")
tabcontrol.add(frame, text = "Graphing")
#************DROPDOWN BOX FOR MODEL************
clicked = StringVar()
clicked.set("Quadratic")
droplabel = Label(frame, text="Choose Model for Curve-fitting: ").pack()
drop = OptionMenu(frame, clicked, "Quadratic", "Cubic", "5PL", "4PL")
drop.pack()
#***********************************************
maxfevlb = Label(frame,text = "MAXFEV(Max number of attempts before the algorithm stops trying): ").pack()
maxfevvar = IntVar()
maxfevvar.set(100000)
maxfevinp = Entry(frame,textvariable = maxfevvar)
maxfevinp.pack()
#****************Scrollbar and Listbox**********
searchtabcontrol = ttk.Notebook(frame)
searchframe = Frame(frame,height = 20, width = 100)
searchtabcontrol.add(searchframe, text = 'Search')
searchtext = StringVar()
searchbar = Entry(searchframe,textvariable = searchtext)
searchbar.bind("<Return>",nextsearch)
searchbar.pack(side = LEFT,fill = BOTH, expand = TRUE, ipadx = 100)
searchbt = Button(searchframe, text = "Search", command = createresults)
nextbt = Button(searchframe,text = "Next", command = nextsearch)
nextbt.pack(side = RIGHT)
searchbt.pack(side = RIGHT)
filterframe = Frame(frame,height = 20, width = 100)
searchtabcontrol.add(filterframe, text = 'Filter')
calibvallab = Label(filterframe, text = "Minimum no of Calibrator Values: ").grid(row = 0, column = 0)
calibfiltval =  IntVar()
calibfiltval.set(0)
calibfilentry = Entry(filterframe,textvariable = calibfiltval).grid(row = 0, column = 1)
samplefilterbool = BooleanVar()
samplefilterchk = Checkbutton(filterframe, text = "Remove Identifiers Missing All Sample Values (Includes NIR)",variable = samplefilterbool).grid(row = 0, column = 2)
filterbt = Button(filterframe, text = "Update", command = updatelistbx).grid(row=0, column = 100)
searchtabcontrol.pack(expan = 1, fill = "both")

#####Identifier Listbox and Scroll
scroll = Scrollbar(frame)
listbox = Listbox(frame, yscrollcommand=scroll.set, selectmode=SINGLE, width = 50, height = 50)
listbox.bind('<<ListboxSelect>>',initiateinfoviewtree)
listbox.pack(side=LEFT)
scroll.pack(side=LEFT, fill=Y)
scroll.config(command=listbox.yview)

## Identifier Info Gui ##
infoframe = Frame(frame,height = 200, width = 300)
filelistboxscroll = Scrollbar(infoframe)
availableinlstbx = Listbox(infoframe,yscrollcommand = filelistboxscroll.set, selectmode = SINGLE, width = 20, height = 50)
availableinlstbx.bind('<<ListboxSelect>>',updateinfotreeview)
availableinlstbx.pack(side = LEFT)
filelistboxscroll.pack(side = LEFT)
filelistboxscroll.config(command = availableinlstbx.yview)
infoviewtree = ttk.Treeview(infoframe)
infoviewtree['columns'] = ("field","data")
infoviewtree.heading("#0",text = "",anchor = "w")
infoviewtree.column("#0",anchor="center",width=5,stretch = NO)
infoviewtree.heading("field",text = "Field",anchor = "w")
infoviewtree.column("field",anchor="center",width=80)
infoviewtree.heading("data",text = "Data",anchor = "w")
infoviewtree.column("field",anchor="center",width=80)
infoviewtree.pack(side=RIGHT,expand = TRUE,fill = BOTH)
infoframe.pack(side = LEFT,expand = TRUE, fill = BOTH)

bottomframe = Frame(frame)
showgraphbt = Button(bottomframe, text="Show Graph", command=show_graph).grid(row=0,column=0)
interpolatebt = Button(bottomframe, text = "Interpolate", command = lambda: inter(select_genes(),resultlabel)).grid(row=1,column=0)
sortbt = Button(bottomframe,text = "Sort Identifiers",command = alphsort).grid(row=2,column=0)
Exportbt = Button(bottomframe, text = "Export", command = spreadcreate).grid(row=3,column=0)
bottomframe.pack(side = BOTTOM,expand = TRUE, fill = BOTH)
rlab = Label(bottomframe)
rlab['text'] = "Result from Interpolation: "
rlab.grid(row=0,column=1)
t = StringVar()
resultlabel = Label(frame, text = t)
resultlabel['text'] = ""
resultlabel.pack(side = BOTTOM)

#***********************************************
fileframe = Frame(root, height = 200, width = 500)
filelabel = Label(fileframe, text = "Files Uploaded: ")
filelabel.pack(side = TOP)
scroll2 = Scrollbar(fileframe)
scroll2.pack(side = RIGHT, fill = Y)
filelistbox = Listbox(fileframe, yscrollcommand = scroll2.set, selectmode = SINGLE, width = 50, height = 30)
filelistbox.pack()
scroll2.config(command = filelistbox.yview)
changebt = Button(fileframe,text = "Change", command = changesetting)
changebt.pack(side = BOTTOM)
showdirbt = Button(fileframe, text = "Show Path", command = showdir)
showdirbt.pack(side = BOTTOM)
tabcontrol.add(fileframe,text = "Files Uploaded")
#***************Log Transform Checkbutton*******
onoff = IntVar()
logtrans = Checkbutton(frame,text = "Enable Ln (Log base e) Transform", variable = onoff)
logtrans.deselect()
logtrans.pack()
tabcontrol.pack(expan = 1, fill = "both")
root.mainloop()