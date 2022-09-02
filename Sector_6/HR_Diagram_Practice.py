from HR_Diagram_Generator import HR_Diagram_Generator

#Sector1 = HR_Diagram_Generator(r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector1_Position_Data_v2.csv")
#Sector1to13 = HR_Diagram_Generator(r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector1_Position_Data_v2.csv")


Sector1to39 = HR_Diagram_Generator(r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector6_Position_Data_v2.csv")

Sector1to39.add_Candidate_Stars(r"D:\44730\Documents\URSS Exoplanet Research\CandidateData\Heir to CandidateDataSet.csv")
Magnitude_Range = [-4.0,14.0,0.5]
Color_Range = [-0.5,4.0,0.5]

Sector1to39.Plot_HR_Diagram_Using_Heatmap(['parallax','parallax'], 'phot_g_mean_mag', 'bp_rp', 2400, Magnitude_Range, Color_Range, True)


