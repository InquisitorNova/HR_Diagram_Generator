with open(r"","r+") as file:
    ids_list = file.readlines()
    GAIA_ids = []
    TIC_ids = []
    for ids in ids_list:
        if "--" in ids:
            continue 
        elif len(ids) >= 19:
            GAIA_ids.append(ids)
        else:
            TIC_ids.append(ids)
    file.close()

with open(r"","w+") as file:
    for GAIA_id in GAIA_ids:
        file.write(str(GAIA_id))
    file.close()

with open(r"","w+") as file:
    for TIC_id in TIC_ids:
        file.write(str(TIC_id))
    file.close()
