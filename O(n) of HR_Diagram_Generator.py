from HR_Diagram_Generator import HR_Diagram_Generator
from scipy.stats import linregress
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
Magnitude_Range = [-4.0,14.0,0.5]
Color_Range = [-0.5,4.0,0.5]

Sector_Generator = HR_Diagram_Generator()
Sector_Generator.add_Sectors_Stars(r"D:\44730\Documents\Projects\URSS Exoplanet Research\HR-Diagram PositionData\Sector GAIA DR2 Data\Southern_Ecliptic_Hemisphere_Gaia_DR2_Data.csv")
Sector_Generator.add_Candidate_Stars(r"D:\44730\Documents\Projects\URSS Exoplanet Research\CandidateData\Heir_To_Candidate_Data_v3.csv")

maximum_index = Sector_Generator.get_length_Of_Sector_DataSet() 
filters = np.linspace(1,maximum_index-1000,50)
times = np.array([])
bin_resolutions = np.array([])
print(filters)
x_values = np.array([])
for filter in filters:
    x_values = np.append(x_values,maximum_index-int(filter))
    time,bin_resolution = Sector_Generator.Plot_HR_Diagram_Using_Heatmap(['parallax','parallax'],'phot_g_mean_mag','bp_rp','Default',[-4.0,14.0,2.0],[-0.5,4.0,0.5],plot_candidates= True, plot_sectors= True, filter = [0], image_resolution= 400, filter_choice = int(filter))
    times = np.append(times,time)
    bin_resolutions = np.append(bin_resolutions,bin_resolution)

Figure_1 = plt.Figure()
ax = sns.scatterplot(x = x_values, y = times)
ax.invert_xaxis()
ax.set_xlabel("Number of Stars in Simulation")
ax.set_ylabel("Time taken to complete")
ax.set_title("Time to completion vs n:")
x = x_values
y = times
m,c,r_value,p_value,std_error = linregress(x,y)
print(f"A linear fit has been fit to the data. The gradient is {m}, the intercept is {c}.")
print(f"The r_value is {r_value}, the p_value is {p_value}, the standard error is {std_error}.")
plt.plot(x,m*x+c)
ax.invert_xaxis()
Figure_1.savefig("HR_Diagram_Time_to_plot_1", bbox_inches = 'tight', dpi = 1000, facecolor = 'w')

plt.show()

Figure_2 = plt.Figure()
ax = sns.scatterplot(x = bin_resolutions, y = times)
ax.invert_xaxis()
ax.set_xlabel("Bin_resolution")
ax.set_ylabel("Time taken to complete")
ax.set_title("Time to completion vs n:")
x = bin_resolutions
y = times
m,c,r_value,p_value,std_error = linregress(x,y)
print(f"A linear fit has been fit to the data. The gradient is {m}, the intercept is {c}.")
print(f"The r_value is {r_value}, the p_value is {p_value}, the standard error is {std_error}.")
plt.plot(x,m*x+c)
ax.invert_xaxis()
Figure_2.savefig("HR_Diagram_Time_to_plot_2", bbox_inches = 'tight', dpi = 1000, facecolor = 'w')
plt.show()