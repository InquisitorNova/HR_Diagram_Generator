from HR_Diagram_Generator import HR_Diagram_Generator

#Sector1 = HR_Diagram_Generator(r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector1_Position_Data_v2.csv")
#Sector1to13 = HR_Diagram_Generator(r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector1_Position_Data_v2.csv")


Sector1to39 = HR_Diagram_Generator(r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector1_Position_Data_v2.csv",
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
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector31_Positions_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector32_Positions_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector33_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector34_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector35_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector36_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector37_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector38_Position_Data_v2.csv",
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector39_Position_Data_v2.csv",)

Sector1to39.add_Candidate_Stars(r"D:\44730\Documents\URSS Exoplanet Research\CandidateData\Heir to CandidateDataSet.csv")
Magnitude_Range = [-4.0,14.0,0.5]
Color_Range = [-0.5,4.0,0.5]

Sector1to39.Plot_HR_Diagram_Using_Heatmap(['parallax','parallax'], 'phot_g_mean_mag', 'bp_rp', 2400, Magnitude_Range, Color_Range, True)


