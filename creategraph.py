from main import *

def show_graph():

    improws = searchwhatrow(select_genes())
    listofyvals = []
    #Adding all the intensities greater than zero to the y list - This ensures that zero intensities are not counted
    for index in range(len(improws)):
        y = []
        for c in range(intens10_rn,intens1_rn,-1): #Needs to be changed when intensities become user defined
            y.append(datalist[index][improws[index]][c])
        listofyvals.append(y)


    if onoff.get() == 1 :
         for y in listofyvals:
             y = list(map(log,y))

         ylabel('Log of Recorder Intensities')
    else:
         ylabel('Recorder Intensities')

    listofxvals = []
    for y in listofyvals:
        x= []
        count = 1
        dilfact = 1/3
        for item in y:
            x.append(count)
            count*=dilfact
        listofxvals.append(x)


    # What to do when a gene doesn't have any name in the excel sheet
    for index in range(len(listofxvals)):
        try:
            popt,pcov = curve_fit(models[clicked.get()],listofxvals[index],listofyvals[index], maxfev = 10000)
            plot(xfit, models[clicked.get()](xfit, *popt), label=data[r][identifier_coln])
            scatter(listofxvals[index], listofyvals[index])
            xlabel('Absolute Values')
            legend()
            show()
        except:
            messagebox.showerror(title = "Error", message = "Insufficient non-zero Y points for the curvefitting! ")

    else:
     messagebox.showerror(title = "Error", message = "No Y Points!")