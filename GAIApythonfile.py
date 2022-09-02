from astroquery.gaia import Gaia
from astroquery.mast import Catalogs
from astroquery.mast import Observations
import numpy as np
import random

def HR_det(ticid):            #Finds a particular TIC ID, queries the MAST catalog and prints the data columns asked for
    
        c = Catalogs.query_criteria(catalog="TIC", ID = ticid)      #queries the TIC V8 catalog based on TIC ID
        if len(c) > 0:                                              #if the length of the TIC ID is bigger than 0, it exists
            gaia_ID = c['GAIA']
        
        else:
            gaia_ID = np.nan
        return gaia_ID

gaia_source_id = []
with open(r"C:\Users\44730\Downloads\sample_list1.txt","r+") as file:
    TIC_ids = file.readlines()
    TIC_ids = list(set(TIC_ids))
    temp = []
    for TIC_id in TIC_ids:
        TIC_Id = TIC_id.replace("\n","")
        temp.append(TIC_Id)
    TIC_ids = temp
    length = len(TIC_ids)
    print("The length of the array is: ",length)
    TIC_Lists =  []
    size = 28353
    for incrementor in range(0,len(TIC_ids),size):
        TIC_Lists.append(TIC_ids[incrementor:incrementor+size])
    if len(TIC_Lists) != 5:
        print("Kaylen break the code!",len(TIC_Lists))
    file.close()

with open(r"C:\Users\44730\Downloads\Cait_Cullen_HR_Diagram_TIC_processed.txt","r+") as file:
	TIC_ids_1 = file.readlines()
	TIC_ids_1 = list(set(TIC_ids_1))
	print(len(TIC_ids_1))
	file.close()

temp = []
for tic_id in TIC_ids:
	try:
		temp.append(int(tic_id[3:]))
	except ValueError:
		continue
TIC_ids = list(set(temp)-set(TIC_ids_1))
random.shuffle(TIC_ids)
print(len(TIC_ids))

gaia_source_ids = []
with open(r"C:\Users\44730\Downloads\Cait_Cullen_HR_Diagram_Gaia_Source_ids_6.txt","w+") as file:
	TIC_processed = []
	error_rate = 0
	id_count = 0
	while True:
		print("Ticl",length)
		try:
			for TIC_id in TIC_ids:
				while True:
					pass_case = False
					try:
						try:
							gaia_source_id = HR_det(TIC_id).value
						except AttributeError:
							gaia_source_id = HR_det(TIC_id)
						try:
							gaia_source_ids.append(gaia_source_id[0])
							file.write(str(gaia_source_id[0])+"\n")
						except TypeError:
							gaia_source_ids.append(gaia_source_ids)
							file.write(str(gaia_source_id)+"\n")

						print("id count is: ",id_count)
						pass_case = True
					except ConnectionError:
						print("Connection_Error")
					if pass_case:
						TIC_processed.append(TIC_id)
						print("TIC_processed: ",len(TIC_processed))
						id_count+=1
						break
				if len(TIC_processed) >= length:
					print("For loop broken")
					break
		except:
			TIC_ids = list(set(TIC_ids)-set(TIC_processed))
			error_rate+=1
			print(f"Error {error_rate} occured, new length is {len(TIC_ids)}")
			id_count = 0
			with open(r"C:\Users\44730\Downloads\Cait_Cullen_HR_Diagram_TIC_processed.txt","a"):
				file.write("\n")
				for tic in TIC_processed:
					file.write(tic+"\n")
				file.close()
			TIC_processed = []
			length = len(TIC_ids)
		if len(TIC_ids) <= 0 or len(TIC_processed) >= len(TIC_ids):
			print("Reached Inglorious end")
			break
                
	file.close()


with open(r"C:\Users\44730\Downloads\Cait_Cullen_HR_Diagram_Gaia_Source_ids_3.txt","w+") as file:
	for gaia_source_id in gaia_source_ids:
		file.write(str(gaia_source_id)+"\n")
	file.close()
print("The source ids are: ",gaia_source_ids)
