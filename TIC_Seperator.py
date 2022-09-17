with open(r"C:\Users\44730\Downloads\Cait_Cullen_HR_Diagram_Gaia_Source_ids_6.txt","r+") as file:
    mess = file.readlines()
    GAIA_ids = []
    TIC_ids = []
    for messy in mess:
        if "--" in messy:
            continue 
        elif len(messy) >= 19:
            GAIA_ids.append(messy)
        else:
            TIC_ids.append(messy)
    file.close()

with open(r"C:\Users\44730\Downloads\Cait_Cullen_HR_Diagram_Gaia_Source_ids_7.txt","w+") as file:
    for GAIA_id in GAIA_ids:
        file.write(str(GAIA_id))
    file.close()

with open(r"C:\Users\44730\Downloads\Cait_Cullen_HR_Diagram_Gaia_Source_processed.txt","w+") as file:
    for TIC_id in TIC_ids:
        file.write(str(TIC_id))
    file.close()
