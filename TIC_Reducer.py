with open(r"C:\Users\44730\Downloads\sample_list1.txt","r+") as file, open(r"C:\Users\44730\Downloads\Reduced_Sample_Text.txt","w") as file_2:
    TIC_ids = file.readlines()
    TIC_ids = list(set(TIC_ids))
    temp = []
    for TIC_id in TIC_ids:
        TIC_Id = TIC_id.replace("\n","")
        temp.append(TIC_Id)
    TIC_ids = temp
    for TIC_id in TIC_ids:
        file_2.write(str(TIC_id)+"\n")
    file_2.close()
    file.close()
