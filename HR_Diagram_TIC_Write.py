import numpy as np
with open(r"D:\44730\Documents\URSS Exoplanet Research\TICIDList\Identified Exoplanet Candidates\Identified_Exoplanets_Check.txt","r+") as file:
    TIC_Lists = file.readlines()
    file.close()

#TIC_Lists.sort()
print(len(np.unique(TIC_Lists)))

with open(r"D:\44730\Documents\URSS Exoplanet Research\TICIDList\Identified Exoplanet Candidates\Identified Exoplanets Candidates Updated.txt","w+") as file:
    """
    seen = set()
    result = []
    for item in TIC_Lists:
        if item not in seen:
            seen.add(item)
            result.append(item)
    """
    for item in TIC_Lists:
        file.write("TIC"+item)
    file.close()