with open(r"D:\44730\Documents\URSS Exoplanet Research\Cait Cullen HR_Diagram\Cait_Cullen_HR_Diagram_Gaia_Source_ids.txt") as file:
    TIC_ids = file.readlines()
    TIC_ids = list(set(TIC_ids))
    print(len(TIC_ids))
