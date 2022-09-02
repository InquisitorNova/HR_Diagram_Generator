def check_same_contents(num1,num2):
    for x in set(num1+num2):
        if num1.count(x) != num2.count(x):
            return False
    return True
with open(r"D:\44730\Documents\URSS Exoplanet Research\TICIDList\Identified Exoplanet Candidates\Candidate__DoubleCheck.txt","r+") as file:
    TIC_list_1 = file.readlines()
    file.close()
with open(r"D:\44730\Documents\URSS Exoplanet Research\TICIDList\Identified Exoplanet Candidates\Identified_Exoplanets_Check.txt","r+") as file:
    TIC_list_2 = file.readlines()
    file.close()
TIC_list_temp = []
for TIC in TIC_list_1:
    TIC = TIC.replace(" ","")
    TIC_list_temp.append(TIC[3:])
    print(TIC[3:])
print(len(TIC_list_1))
print(len(TIC_list_2))
TIC_list_1 = TIC_list_temp
print(check_same_contents(TIC_list_1,TIC_list_2))
TIC_list_1 = set(TIC_list_1)
TIC_list_2 = set(TIC_list_2)
print("The number of disparities is: ",TIC_list_1 - TIC_list_2)
TIC_list_1 = list(TIC_list_1)
TIC_list_2 = list(TIC_list_2)
print(TIC_list_2.index("81089255"))
