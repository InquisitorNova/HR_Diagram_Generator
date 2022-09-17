from astroquery.gaia import Gaia
from astroquery.mast import Catalogs
from astroquery.mast import Observations
import numpy as np
import random

def HR_det(ticid):            #Finds a particular TIC ID, queries the MAST catalog and prints the data columns asked for
    
        c = Catalogs.query_criteria(catalog="TIC", ID = ticid)      #queries the TIC V8 catalog based on TIC ID
        if len(c) > 0:                                              #if the length of the TIC ID is bigger than 0, it exists
            gaia_ID = c['GAIA'].value
        
        else:
            gaia_ID = np.nan
        return gaia_ID

def pop(file):
    with open(file, 'r+') as f: # open file in read / write mode
        firstLine = f.readline() # read the first line and throw it out
        data = f.read() # read the rest
        f.seek(0) # set the cursor to the top of the file
        f.write(data) # write the data back
        f.truncate() # set the file size to the current size
        return firstLine

with open(r"C:\Users\44730\Downloads\Reduced_Sample_Text.txt","r+") as file_1, open(r"C:\Users\44730\Downloads\Cait_Cullen_HR_Diagram_Gaia_Source_ids_10.txt","a") as file_2:
    id_count = 0
    gaia_source_ids = []
    TIC_ids = file_1.readlines()
    length = len(TIC_ids)
    print("Ticl",length)
    while length >= 1:
        TIC_id = str(pop(r"C:\Users\44730\Downloads\Reduced_Sample_Text.txt")).replace("\n","")
        while True:
            pass_case = False
            try:
                try:
                    gaia_source_id = HR_det(TIC_id).value
                except AttributeError:
                    gaia_source_id = HR_det(TIC_id)
                try:
                    gaia_source_ids.append(gaia_source_id[0])
                    file_2.write(str(gaia_source_id[0])+"\n")
                except TypeError:
                    gaia_source_ids.append(gaia_source_ids)
                    file_2.write(str(gaia_source_id)+"\n")
                    
                print("id count is: ",id_count)
                pass_case = True
            except ConnectionError:
                print("Connection_Error")
            if pass_case:
                id_count+=1
                break
        if length <= 0:
            print("Reached Inglorious end")
            break
    file_1.close()
    file_2.close()
