"""
This is a small python file used to check that that the TIC list of two csv files is the same. The code is applied to the TIC list
obtained from Gaia_Source_Finder_3.py to ensure that all the TIC lists have been found properly. The primary purpose of this file is
for error checking.
"""
def check_same_contents(num1,num2):
    """
    This function checks whether the a number is found in the lists num1 and num2 and in the same frequency
    """
    for x in set(num1+num2): # Produce a set of the combined lists.
        if num1.count(x) != num2.count(x): #Check that the TIC ids occur in the list in the same frequency.
            return False
    return True
with open(r"","r+") as file:
    TIC_list_1 = file.readlines() # Read the Tic_list in the first file and convert it into a list.
    file.close()
with open(r"","r+") as file:
    TIC_list_2 = file.readlines() # Read the Tic_list in the second file and convert it into a list.
    file.close()
TIC_list_temp_1 = []
TIC_list_temp_2 = []
for TIC in TIC_list_1:
    TIC = TIC.replace(" ","")
    TIC_list_temp_1.append(TIC[3:]) #Remove the TIC string from the TIC id
for TIC in TIC_list_2:
    TIC = TIC.replace(" ","")
    TIC_list_temp_2.append(TIC[3:]) #Remove the TIC string from the TIC id
print(len(TIC_list_1))
print(len(TIC_list_2))
TIC_list_1 = TIC_list_temp_1 # Rewrite TIC_list_1 so that it does not have a TIC in front of the numbers
TIC_list_2 = TIC_list_temp_2 # Rewrite TIC_list_2 so that it does not have a TIC in front of the numberds
print(check_same_contents(TIC_list_1,TIC_list_2)) # Display whether the lists have the same TIC values
TIC_list_1,TIC_list_2 = set(TIC_list_1),set(TIC_list_2) # Convert the to lists to sets
print("The number of disparities is: ",TIC_list_1 - TIC_list_2) # Display the TIC numbers not present.
