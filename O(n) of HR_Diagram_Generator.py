"""
The HR Diagram Generator can be used to produce HR diagrams for a wide range of star dataset sizes. To
test it's performance I have created a python file to run the HR diagram Generator multiple times at different star dataset sizes using 
the filter function of the HR diagram plot function to measure how run time evolves with increasing star count.
From the tests I have run the primary dependence on the number of bins used to plot the diagram not the number of stars themselves. 
However, increasing the number of stars increases the amount of detail that can be extracted from the diagram and so the HR diagram in the
'Default' setting will make a rough estimate for the ideal bin count for the diagram and plot accordingly. Under this setting the run time
increases linearly with bin count providing the the Magnitude and Colour Range are kept constant.
"""

# Import the relevant modules
from HR_Diagram_Generator import HR_Diagram_Generator
from scipy.stats import linregress
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Create the Magnitude and Colour Ranges for the plot
Magnitude_Range = [-4.0,14.0,0.5] # Lower, Upper and Interval value for the Magnitudes 
Color_Range = [-0.5,4.0,0.5] # Lower, Upper and Interval value for the Colours

Sector_Generator = HR_Diagram_Generator() # Initalise the HR diagram Generator object
Sector_Generator.add_Sectors_Stars(r"") # The empty quotations can be filled by the list of file paths containing the Sector data
Sector_Generator.add_Candidate_Stars(r"") # The empty quotations can be filled by the list of file paths containing the Candidate data

maximum_index = Sector_Generator.get_length_Of_Sector_DataSet() # Obtains the length of Sector DataFrame
filters = np.linspace(1,maximum_index-1000,50) # Generates a list of values to filter the Sector DataFrame.
#The filter will start with the removal of 1 star and then increase to the number of stars in the dataset minus 1
times = np.array([]) # Creates an array to store the times
bin_resolutions = np.array([]) # Creates an array to store the default bin resolutions generated by the HR diagram
print(filters) # Check for the filters
x_values = np.array([]) # Creates an array to store the number of stars filtered
for filter in filters: # Creates a for loop to run the HR diagram multiple times
    x_values = np.append(x_values,maximum_index-int(filter)) # Stores the filter value being used
    time,bin_resolution = Sector_Generator.Plot_HR_Diagram_Using_Heatmap(['parallax','parallax'],'phot_g_mean_mag','bp_rp','Default',[-4.0,14.0,2.0],[-0.5,4.0,0.5],plot_candidates= True, plot_sectors= True, filter = [0], image_resolution= 400, filter_choice = int(filter)) 
    # Above produces a HR diagram that is not displayed and returns the time taken and the bin resolution to plot. Turn plot candidates to false if you are not plotting candidates
    times = np.append(times,time) # stores the time taken
    bin_resolutions = np.append(bin_resolutions,bin_resolution)# stores the bin resolution

Figure_1 = plt.Figure() # Creates a figure for the plot 
ax = sns.scatterplot(x = x_values, y = times) # Plots the scatterplot of filtered stars vs time taken
ax.invert_xaxis()
ax.set_xlabel("Number of Stars in Simulation") 
ax.set_ylabel("Time taken to complete")
ax.set_title("Time to completion vs n:")
x = x_values
y = times
m,c,r_value,p_value,std_error = linregress(x,y) #Fits a linear fit to the data
print(f"A linear fit has been fit to the data. The gradient is {m}, the intercept is {c}.") # Displays the result
print(f"The r_value is {r_value}, the p_value is {p_value}, the standard error is {std_error}.")
plt.plot(x,m*x+c) #Plots the fit
ax.invert_xaxis()
Figure_1.savefig("HR_Diagram_Time_to_plot_1", bbox_inches = 'tight', dpi = 1000, facecolor = 'w')

plt.show()

Figure_2 = plt.Figure() # Creates a Second figure
ax = sns.scatterplot(x = bin_resolutions, y = times) # Plots the bin resolution vs the time taken
ax.invert_xaxis()
ax.set_xlabel("Bin_resolution")
ax.set_ylabel("Time taken to complete")
ax.set_title("Time to completion vs n:")
x = bin_resolutions
y = times
m,c,r_value,p_value,std_error = linregress(x,y) # Fits a linear fit to the data
print(f"A linear fit has been fit to the data. The gradient is {m}, the intercept is {c}.") # Displays the results
print(f"The r_value is {r_value}, the p_value is {p_value}, the standard error is {std_error}.")
plt.plot(x,m*x+c)
ax.invert_xaxis()
Figure_2.savefig("HR_Diagram_Time_to_plot_2", bbox_inches = 'tight', dpi = 1000, facecolor = 'w')
plt.show()