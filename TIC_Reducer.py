"""
The TIC reducer is a small python file that is used to remove the duplicate TIC ids from a file and store the results in a new file.
"""
with open(r"","r+") as file, open(r"","w") as file_2: # Open the target list file and create a new file. 
    # Insert the file paths in the empty strings above 
    TIC_ids = file.readlines() # Read the file, store the TIC_ids as a list
    TIC_ids = list(set(TIC_ids)) # Remove the duplicates
    temp = [] # Creates a temporary array to store the tic ids in.
    for TIC_id in TIC_ids:
        TIC_Id = TIC_id.replace("\n","") # Remove the new lines
        temp.append(TIC_Id) 
    TIC_ids = temp
    for TIC_id in TIC_ids: 
        file_2.write(str(TIC_id)+"\n") # Write the non_duplicate TIC ids to the files.
    file_2.close()  # Close the files
    file.close()
