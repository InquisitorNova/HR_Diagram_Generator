"""
To source the data needed for the HR diagram Generator, I used the GAIA archive. For small enough files, I can obtain the GAIA IDs by
using astroquery to make requests to the name resolver Simbad to obtain GAIA DR3 values, and failing that I can make requests to the mast catalgoue 
for GAIA DR2 values. With the GAIA DR3 and GAIA DR2 values I skip the need to rely on the RA and DEC coordinates of the stars, which is prone to mistmatches
and returning null stars. This program does not perform a bulk search, but rather sends requests TIC id by TIC id. The result is that is quite slow. 
Therefore for large requests of 200,000 stars or more the recommendation is to use the TICv8 catalogue to convert TIC ids into GAIA DR2 values or to use 
the RA and DEC values provided for the TIC ids.
"""

from astroquery.simbad import Simbad
from astroquery.mast import Catalogs
import numpy as np
import warnings 
import re
import pandas as pd
warnings.filterwarnings("ignore") # Removes the run time warning that can occur during the run of the program.
Simbad.TIMEOUT = 3600 # Extends the time the server has to return a result to our request.
def get_GAIA_ID(tic_id):
    """
    This is a function designed to return the GAIA ID of a star using it's TIC id. 
    The function uses a hybrid approach, first relying on simbad to return a GAIADR3/DR2/DR1 value
    and then failing that switching over to the the mast catalogue to return a GAIA DR2 value. 
    To later separate the Simbad and Mast catalogue results, the function returns the source it derived the GAIA ID from
    as well as the TIC ID and the GAIA ID.
    """
    result_table = Simbad.query_objectids(tic_id)  # Query the the Simbad archive and return information on this tic_id

    try:
        if len(result_table) > 0: # If the length of the table is > 0, an entry exists.
            for ID in list((result_table)['ID']): # Pull out the ID information
                ID = str(ID) 
                if re.match("Gaia DR3",ID[:9]): 
                    return int(ID[9:]),"Simbad Gaia DR3" # If the result is GAIA DR3 return the GAIA DR3 ID and Source
                elif re.match("Gaia DR2", ID[:9]):
                    return int(ID[9:]), "Simbad Gaia DR2" # If the result is GAIA DR2 return the GAIA DR2 ID and Source
                elif re.match("Gaia DR1",ID[:9]):
                    return int(ID[9:]), "Simbad Gaia DR1" # If the result is GAIA DR1 return the GAIA DR1 ID and Source
                elif re.match("--",ID):
                    return np.nan, "Simbad" # If Simbad has found no GAIA ID return a null value and Source
    except TypeError:
        pass

    result_table = Catalogs.query_criteria(catalog="TIC", ID = int(tic_id[3:])) # Queries the TIC V8 catalog based on TIC ID
    if len(result_table) > 0: # If the length of the TIC ID is bigger than 0, it exists
            gaia_ID,Source = (result_table['GAIA'].value[0]).compressed(),"Mast Catalogue GAIA DR2" # Returns GAIA ID and the Source from catalogue
            if gaia_ID == []:
                gaia_ID = np.nan # If the list is empty set the ID to nan.
            gaia_ID = str(result_table['GAIA'].value[0])
            if re.match("--",gaia_ID): # If the GAIA ID has the string -- return a null value. 
                return np.nan, "Mast Catalogue GAIA DR2"
    else:
        gaia_ID,Source = np.nan,"Mast Catalogue GAIA DR2" # Should the table have 0 length return GAIA ID nan and Source as Mast.
    return gaia_ID,Source

# Since the function runs quite slowly I have written a backup stripped down version of TIC_ID that runs as backup.
def HR_det(ticid):            
    """
    This function searches the Mast Catalogue for the TIC ID and returns the GAIA DR2 results.
    """
    c = Catalogs.query_criteria(catalog="TIC", ID = int(ticid[3:])) #  Queries the TIC V8 catalog based on TIC ID
    if len(c) > 0:  # If the length of the TIC ID is bigger than 0, it exists                    
        gaia_ID,Source = int(c['GAIA'].value[0]), "Mast Catalogue GAIA DR2" # Returns the GAIA ID and the Source from the catalogue
    else:
        gaia_ID = np.nan # If the length is 0 return nan
    return gaia_ID,Source

#print(get_GAIA_ID("TIC178155472")) # Displays a trial TIC value, used as test case.

#Insert the file path of the original file containing the tic ids into the empty list below.
with open(r"","r+") as file: # Open the file and read the TIC ids, store them as a list.
    TIC_Lists = file.readlines() 
    file.close()
TIC_Lists = list(set(TIC_Lists)) # Remove the duplicates

# The code below creates a dummy file that acts as a copy for the original file containing the tic ids. This copy is the file below reads from. 
#Insert the file path of the dummy file in the empty string.
with open(r"","w+") as file: # Open the file containing the TIC_ids that is to be queried by astroquery, write these TIC_ids into the file if they arent already present.
    lines = file.readlines() # Read the file lines 
    if len(lines) == 0: # If the length of the lines list is zero which occurs once the program is completed running...
        for item in TIC_Lists: # Write the TIC ids to the file.
            file.write(item)
            file.write("\n")
    file.close()

def pop(file):
    """This function removes the the top line being read from the file and returns the line to the user.
    Its primary purpose here is to ensure that even if the program crashes during the run time 
    or computer abruptly stops executing the program due to loss of power, turning off, 
    etc, we do not start again from the beginning."""
    with open(file, 'r+') as f: # open file in read / write mode
        firstLine = f.readline() # read the first line and throw it out
        data = f.read() # read the rest
        f.seek(0) # return the cursor to the top of the file
        f.write(data) # write the data back
        f.truncate() # Change the file size to the current size
        return firstLine

# Insert the file path of the copy file into file_1 open and the file path of where you want the gaia ids to be stored in file_2 open
with open(r"","r+") as file_1, open(r"","a") as file_2: # Open the copy file for the tic ids, Open a new file to store the results of the query
    id_count = 0 # Used as a progress marker to tell when the program is completed.
    gaia_source_ids = [] # A list storing the tic ids.
    TIC_ids = file_1.readlines() # Read the TIC ids from the copy file.
    length = len(TIC_ids) # Determine the number of TIC ids in the copy file.
    print("The number of TIC Ids are: ",length) # Display the number of TIC ids to the user.
    file_2.write("Tic_id,Gaia_id,Source"+"\n") # Create the column names for the csv file.
    while length >= 1: # This creates a do while loop that runs until the length of the TIC id list goes to 0
        try:
            TIC_id = str(pop(r"")).replace("\n","") # Obtain the the TIC id from the copy file, remove the id from the file and remove the newline
        except:
            print("You have entered a id which the program can not extract from the file.") # Inform the user of read error.
            break # Break the do while loop.
        while True: # Create another do while list to ensure that the program encounter a server request error, it makes another attempt.
            pass_case = False # Pass case is initially set to false but becomes true once an id has been found.
            try:
                try:
                    gaia_source_id,Source = get_GAIA_ID(TIC_id) # Return the gaia source id and source.
                except AttributeError:
                    gaia_source_id,Source = HR_det(TIC_id) # Should the above fail use the simplifed version of the function.
                try:
                    gaia_source_ids.append(gaia_source_id) # Add the gaia id to the list.
                    file_2.write(str(TIC_id)+",") # Write an entry in the csv file storing the results. Write the TIC id,
                    file_2.write(str(gaia_source_id)+",") # Write the gaia id,
                    file_2.write(Source+"\n") # Write the source of the gaia id
                except TypeError:
                    file_2.write("Entry could not be written to file") 
                    print("Could not write TIC Id to the file.")
                    #Should program fail to convert TIC_id, GAIA_source_id or source to a string write to file a failed entry
                    
                print("id count is: ",id_count) #Display to the user an indication of a successfull run and the count.
                pass_case = True # Change the pase case to true.
            except ConnectionError:
                print("Connection_Error") # Should the server run into a connection error, catch it and run the request again.
            if pass_case:
                id_count+=1 # Update the counter
                length-=1 # Reduce the length variable value by 1
                break # Break the do while loop
        if length <= 0: #If the length reaches 0 break the master do while loop
            print("Reached Inglorious end") # Display the end of the program to the user
            break # Break the master do while loop.
    file_1.close()
    file_2.close()
