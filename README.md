# Calibration-Curve-Grapher-and-Optimizer
Introduction:
The Calibration Curve Graphing and Interpolater software allows the user to load/upload a .txt or .xl.. file with the proteomics-based data from the experiments performed using mass-spectometry, and input all the experimentally decided parameters. This software helps with efficient browsing, sorting, optimizing, and interpolating of the required data.

Installion:
This Python 3.7 script makes use of 7 Modules, which are required to be installed along with Python 3.7 on the system before running the program.

	Steps:
	1. Open cmd in Windows
	2. Pass these commands seperately:
    pip install scikit-learn
    pip install pandas
		pip install xlrd
		pip install matplotlib
		pip install scipy
		pip install numpy
		pip install tkinter
		pip install xlsxwriter
		pip install PILLOW  
    
	3. Run the main.py


Software's Usage:
This section will look into the all the items present on the software
As of now, this software has three main tabs:
	1. Welcome! :-
		Shortcut to the readme file
		Load a new file
	2. Graphing :-
		Use preffered model for Curve-fitting:
			1. Quadratic
			2. Cubic
			3. 4PL
			4. 5PL
		MAXFEV:
			Maximum number of attemps to exhaust before program reaches optimum
			parameters for the model chosen for Curve-fitting
			
			Greater number of MAXFEV will likely take more time for the 
			the program to optimize for the parameters but ensures greater coverage.
		
		Search/Filter Tab:
			Search:
				Case Sensitive
				
				Type the keywords needed to be searched and click Search to find the highlight the first search result
				
				For next search results to be highlighted, Click Next
				
				If all the search results get exhausted, press Search again to search for new keywords or same keywords 
			Filter:
				Minumum no of Calibrator Values:
					Enter your desired number of minimum values and press update to update to listbox
					It removes all the protiens/identifiers with less than that number of calibrator values
				Remove Identifiers Missing All Sample Values (Includes NIR):
					This function works on the current list of protiens and removes the identifiers which doesn't
					have any sample values in any of the files or all of them in all of the files are NIR
		
		Enable Ln(Log base e):
			Applies Ln to all the Calibrator values

		Identifiers List Box :
			This listbox containes all the identifiers from the data file(s) uploaded. Identifiers present in multiple files will
			be listed down only once in the listbox. All the objects from Identifier columns selected in CIC* will be merged and then
			listed in the Identifier Column.

		Available Files List Box:
			This listbox gets affected by the selection of each identifier. It basically displays the row no of that identifier in all files
			If the identifier is not available in a certain file, it says 'NA' - Not Available. First item represents the row no of identifier
			in first file, and second item represents identifier's row no in second file, and so on.
		
		Infoview Tree:
			This widget displays all the corresponding information for the identifier in the selected file
	
		Sort Identifiers:
			Sorts all the identifiers in the listbox besides alphabetically

		Interpolate:
			Interpolates values for a single identifier in all the files(if available) and displays the results above the button

		Show Graph:
			Builds the graph using the model chosen and shows the interpolated values(if available) visually on the graph

		Export:
			Exports all the interpolated values onto an excel spreadsheet and saves it in the same folder as the file

	
	3. Files Uploaded :-
		The listbox displays all the files loaded on the program named with all the sample names merged
		
		Show Path:
			Prints out the location of the file selected on the computer

		Change:
			Opens the Corresponding Information Checkboard* and enables user to change any corresponding information

	4. Corresponding Information Checkboard(CIC)* (Not Directly Visible as a tab but pops us after a valid file is loaded or changed):-
		
		Identifier Column:-
			
			Column of checkbuttons 
			
			Checking the button makes that column an identifier and all of them get merged together

		Sample Column:-

			Column of checkbuttons

			Checking the button makes that column a sample column used to interpolate the value from calibrator values

		Y Value Column:-

			Column of checkbuttons

			Checking the button makes that column a calibrator column used to make a graph

		Sample Name:-
			
			Enables when the sample column is checked
			
			Names that specific name which is used to name the whole file

 


 
		









