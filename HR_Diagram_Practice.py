from HR_Diagram_Generator import HR_Diagram_Generator

Sector1to13 = HR_Diagram_Generator(r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector1_Position_Data_v2.csv",
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
r"D:\44730\Documents\URSS Exoplanet Research\HR-Diagram PositionData\Sector13_Position_Data_v2.csv"
)

Sector1to13.add_Candidate_Stars(r"D:\44730\Documents\URSS Exoplanet Research\CandidateData\GDR3_DataSet_Results_Stars_FInal.csv",r"D:\44730\Documents\URSS Exoplanet Research\CandidateData\Astrophysical_Parameters_Results_Stars_Final.csv")

Sector1to13.Plot_HR_Diagram_Using_Heatmap(['parallax','distance_gspphot'],'phot_g_mean_mag','bp_rp',[-6.0,13.5],[-0.5,4], 2000, True)
