from astroquery.simbad import Simbad
from astroquery.mast import Catalogs
import numpy as np
import warnings 
import re
import pandas as pd
warnings.filterwarnings("ignore")
Simbad.TIMEOUT = 3600
def get_GAIA_ID(tic_id):

    result_table = Simbad.query_objectids(tic_id)

    try:
        if len(result_table) > 0:
            for ID in list((result_table)['ID']):
                ID = str(ID)
                if re.match("Gaia DR3",ID[:9]):
                    return int(ID[9:]),"Simbad Gaia DR3"
                elif re.match("Gaia DR2", ID[:9]):
                    return int(ID[9:]), "Simbad Gaia DR2"
                elif re.match("Gaia DR1",ID[:9]):
                    return int(ID[9:]), "Simbad Gaia DR1"
                elif re.match("--",ID):
                    return np.nan, "Simbad"
    except TypeError:
        pass

    result_table = Catalogs.query_criteria(catalog="TIC", ID = int(tic_id[3:]))      #queries the TIC V8 catalog based on TIC ID
    if len(result_table) > 0:                                          #if the length of the TIC ID is bigger than 0, it exists
            gaia_ID,Source = (result_table['GAIA'].value[0]).compressed(),"Mast Catalogue GAIA DR2"
            if gaia_ID == []:
                gaia_ID = np.nan
            gaia_ID = str(result_table['GAIA'].value[0])
            if re.match("--",gaia_ID):
                return np.nan, "Mast Catalogue GAIA DR2"
    else:
        gaia_ID,Source = np.nan,"Mast Catalogue GAIA DR2"
    return gaia_ID,Source

def HR_det(ticid):            #Finds a particular TIC ID, queries the MAST catalog and prints the data columns asked for
    
        c = Catalogs.query_criteria(catalog="TIC", ID = int(ticid[3:]))      #queries the TIC V8 catalog based on TIC ID
        if len(c) > 0:                                              #if the length of the TIC ID is bigger than 0, it exists
            gaia_ID,Source = int(c['GAIA'].value[0]), "Mast Catalogue GAIA DR2"
        
        else:
            gaia_ID = np.nan
        return gaia_ID,Source

print(get_GAIA_ID("TIC178155472"))
r"""
with open(r"D:\44730\Documents\Projects\URSS Exoplanet Research\Cait Cullen HR_Diagram\HR_Diagram TIC Lists\sample_list1.txt","r+") as file:
    TIC_Lists = file.readlines()
    file.close()
    TIC_Lists = list(set(TIC_Lists))
    
#TIC_Lists.sort()

print(len(np.unique(TIC_Lists)))
temp = []
for TIC in TIC_Lists:
    temp.append("TIC" + TIC.replace("\n",""))
TIC_Lists = temp
print(TIC_Lists[:5])
print(len(TIC_Lists))
Simbad.add_votable_fields('typed_id')
result_table = Simbad.query_objectids(TIC_Lists[:5])

print(result_table)
"""
r"""
with open(r"D:\44730\Documents\Projects\URSS Exoplanet Research\Cait Cullen HR_Diagram\HR Diagram GAIA Source_ids\GAIA_Source_IDs_HRCC.txt","w") as file:
    file.write("Tic_id,GAIA_id"+"\n")
    for index in range(len(result_table)):
        file.write(TIC_Lists[index]+",")
        file.write(str(result_table[index]['TYPED_ID']))
        file.write("\n")
    file.close()

with open(r"D:\44730\Documents\Projects\URSS Exoplanet Research\Cait Cullen HR_Diagram\HR_Diagram TIC Lists\HR_Diagram_BS_TIC_List.txt","w+") as file:
    lines = file.readlines()
    if len(lines) == 0:
        for item in TIC_Lists:
            file.write(item)
            file.write("\n")
    file.close()
"""
def pop(file):
    with open(file, 'r+') as f: # open file in read / write mode
        firstLine = f.readline() # read the first line and throw it out
        data = f.read() # read the rest
        f.seek(0) # set the cursor to the top of the file
        f.write(data) # write the data back
        f.truncate() # set the file size to the current size
        return firstLine

with open(r"C:\Users\44730\Downloads\TIC_List_GaiaDR1s.txt","r+") as file_1, open(r"D:\44730\Documents\Projects\URSS Exoplanet Research\Cait Cullen HR_Diagram\HR Diagram GAIA Source_ids\GAIADR1s.txt","a") as file_2:
    id_count = 0
    gaia_source_ids = []
    TIC_ids = file_1.readlines()
    length = len(TIC_ids)
    print("Ticl",length)
    #file_2.write("Tic_id,Gaia_id,Source"+"\n")
    while length >= 1:
        try:
            TIC_id = str(pop(r"C:\Users\44730\Downloads\TIC_List_GaiaDR1s.txt")).replace("\n","")
        except:
            break
        while True:
            pass_case = False
            try:
                try:
                    gaia_source_id,Source = HR_det(TIC_id)
                except AttributeError:
                    gaia_source_id,Source = HR_det(TIC_id)
                try:
                    gaia_source_ids.append(gaia_source_id)
                    file_2.write(str(TIC_id)+",")
                    file_2.write(str(gaia_source_id)+",")
                    file_2.write(Source+"\n")
                except TypeError:
                    gaia_source_ids.append(gaia_source_id)
                    file_2.write(str(TIC_id)+",")
                    file_2.write(str(gaia_source_id)+",")
                    file_2.write(Source+"\n")
                    
                print("id count is: ",id_count)
                pass_case = True
            except ConnectionError:
                print("Connection_Error")
            if pass_case:
                id_count+=1
                length-=1
                break
        if length <= 0:
            print("Reached Inglorious end")
            break
    file_1.close()
    file_2.close()

r"""
Sector_DataSet = pd.read_csv(r"D:\44730\Documents\Projects\URSS Exoplanet Research\Cait Cullen HR_Diagram\HR Diagram GAIA Source_ids\GAIA_Source_IDs_HRCC.txt")
Gaia_DR3_Data = Sector_DataSet[Sector_DataSet.Source == "Simbad Gaia DR3"]
print(len(Gaia_DR3_Data))
Gaia_DR2_Data = Sector_DataSet[(Sector_DataSet.Source == "Simbad Gaia DR2") | (Sector_DataSet.Source == "Mast Catalogue GAIA DR2")]
print(len(Gaia_DR2_Data))
Gaia_DR1_Data = Sector_DataSet[Sector_DataSet.Source == "Simbad Gaia DR1"]
print(len(Gaia_DR1_Data))
#Gaia_DR1_Data.drop_duplicates(subset = ["Gaia_id"],inplace = True)
#Gaia_DR2_Data.drop_duplicates(subset = ["Gaia_id"],inplace = True)
#Gaia_DR3_Data.drop_duplicates(subset = ["Gaia_id"],inplace = True)

Gaia_DR1_Data.dropna(inplace = True)
Gaia_DR2_Data.dropna(inplace = True)
Gaia_DR3_Data.dropna(inplace = True)

print("The initial percentage of data missing is ", (((141765-(len(Gaia_DR3_Data)+len(Gaia_DR2_Data)+len(Gaia_DR1_Data)))/141765)*100))
print(len(Gaia_DR3_Data)+len(Gaia_DR2_Data)+len(Gaia_DR1_Data))
Gaia_DR1_Data.to_csv(r"C:\Users\44730\Downloads\Cait_Cullen_Gaia_DR1_Data.csv",index = False)
Gaia_DR2_Data.to_csv(r"C:\Users\44730\Downloads\Cait_Cullen_Gaia_DR2_Data.csv",index = False)
Gaia_DR3_Data.to_csv(r"C:\Users\44730\Downloads\Cait_Cullen_Gaia_DR3_Data.csv",index = False)

"""