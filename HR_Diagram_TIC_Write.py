"""
This is a small python file designed to convert a file containing the TIC ids without the TIC header into a file containing the TIC
ids with the TIC header.
"""
import numpy as np

with open(r"","r+") as file: # Insert the file path into the empty string
    TIC_Lists = file.readlines() # Open and read the file containing the TIC ids without the TIC header, store as a list.
    file.close()

#TIC_Lists.sort()
print(len(np.unique(TIC_Lists))) # Display the number of unique TIC ids within the list.

with open(r"","w+") as file:  # Insert the file path into the empty string
    for item in TIC_Lists:
        file.write("TIC"+item) # Write the TIC ids with the TIC header into a new file.
    file.close()