from HR_Diagram_Generator import HR_Diagram_Generator
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
Magnitude_Range = [-4.0,14.0,0.5]
Color_Range = [-0.5,4.0,0.5]

Sector_Generator = HR_Diagram_Generator(r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector1_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector2_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector3_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector4_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector5_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector6_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector7_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector8_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector9_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector10_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector11_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector12_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector13_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector27_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector28_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector29_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector30_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector32_Positions_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector32_Positions_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector33_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector34_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector35_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector36_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector37_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector38_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector39_Position_Data_v2.csv",)

maximum_index = Sector_Generator.get_length_Of_Sector_DataSet() 
filters = np.linspace(1,maximum_index-1000,50)
print(filters)
times = np.array([])
x_values = np.array([])
for filter in filters:
    x_values = np.append(x_values,maximum_index-filter)
    times = np.append(times,Sector_Generator.Plot_HR_Diagram_Using_Heatmap(['parallax','parallax'], 'phot_g_mean_mag', 'bp_rp', 2400, Magnitude_Range, Color_Range, False, filter=round(filter)))

Figure_1 = plt.Figure()
ax = sns.scatterplot(x = x_values, y = times)
ax.invert_xaxis()
ax.set_xlabel("Number of Stars in Simulation")
ax.set_ylabel("Time taken to complete")
ax.set_title("Time to completion vs n:")
plt.show()