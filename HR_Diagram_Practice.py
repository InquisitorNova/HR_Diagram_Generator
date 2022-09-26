from HR_Diagram_Generator import HR_Diagram_Generator
import numpy as np
import re
while True:
    Quit = False

    Display_Case = input("Hello, is this your first time using the HR Diagram Generator?, Y/N ")

    if "Y" in Display_Case and len(Display_Case) == 1:
        Display_Case = True
    elif "N" in Display_Case and len(Display_Case) == 1:
        Display_Case = False
    else:
        print("You have entered a character that is not Y or N, try again")
        continue

    if Display_Case:
        print("""Welcome to the Hertzsprung Russell Diagram. This application will generate a scatterplot of stars of interest (Referred to as Candidates Stars), that will be
        superimposed onto a heatmap of background stars that form the population of interest (Referred to as Sector Stars). To do this the application file requires two csv files. 
        One for the Candidate Stars and one for the Sector Stars.The csv files should contain a distance measure, either parallax and its error(For parallax measurements, the application will filter out parallax measurements 
        with an error of 0.4 or greater if you pass a csv file with the parallax error with a name as such) or a distance to the star in parsecs, a magnitude measure
        and a temperature measure, either a colour index or temperature. The application will ask for the column names of the distance measure(parallax or a distance metric in parsecs), an apparent magnitude measure and temperature measure. 
        It will ask for the magnitude and temperature ranges in which you wish the plot to display.  
        It will ask for the resolution in bins and whether you want the candidate data to be displayed. If this is the case it also plots the candidate stars 
        without the background heatmap to allow you to study them individually. The HR_diagram generator will display how many Sector and Candidate stars are being plotted, 
        the chosen magnitude and temperature ranges as well as how many stars there are with either missing parallax,distance, magnitude measures or temperature information. 
        The application at default plots all the stars but this can can lead to alot of noise in the diagram. To overcome this the program also asks you to specify how many stars a bin must have to be shown. 
        Try go for values between 1-5 stars to make the final diagram clear. """)
    Sector_Data = []
    Candidate_Data = []
    while True:
        try:
            File_Case = input("Enter whether you wish to enter the paths of the Sector csv files individually or as one, uploaded as a txt file?: SingleFile/TextFile: ").lower()
            if re.search("singlefile",File_Case):
                Case = True
                while Case:
                    Entry = input("Enter the file path of each of the Sector csv files individually. ").replace('"',"").replace("\n","").encode('unicode_escape').decode()
                    Sector_Data.append(Entry)
                    try:
                        breaker = input("Enter 'done' if you are complete, otherwise enter.")
                        if re.search("done",breaker):
                            Case = False
                        elif len(breaker) > 1:
                            print("You have entered neither an enter or breaker try again")
                    except TypeError:
                        pass

            elif re.search("textfile",File_Case):
                Entry = input("Enter the file path of the file that contains all the Sector csv files. ").replace('"',"").replace("\n","").encode('unicode_escape').decode()
                with open(Entry,'r+') as file:
                    temp = []
                    Sector_Data = file.readlines()
                    for Sector in Sector_Data:
                        temp.append(Sector.replace('"',"").replace("\n","").replace(",","").encode('unicode_escape').decode())
                    Sector_Data = temp
                    file.close()
            else:
                print("You have entered neither SingleFile or TextFile, try again")
                continue
        except:
            print("You have entered a format that I can not accept, try again")
            continue
        break
    while True:
        try:
            File_Case = input("Enter whether you wish to enter the paths of the Candidate csv files individually or as one, uploaded as a txt file?: SingleFile/TextFile: ").lower()
            if re.search("singlefile",File_Case):
                Case = True
                while Case:
                    Entry = input("Enter each file path of the Candidate csv files individually as string.").replace('"',"").replace("\n","").encode('unicode_escape').decode()
                    Candidate_Data.append(Entry)
                    try:
                        breaker = input("Type 'done' if you are complete, otherwise enter.")
                        if re.search("done",breaker):
                            Case = False
                        elif len(breaker) > 1:
                            print("You have entered neither an enter or breaker try again")
                    except TypeError:
                        pass
                        
            elif re.search("textfile",File_Case):
                Entry = input("Enter the file path of the file that contains all the Candidate csv files. ").replace('"',"").replace("\n","").encode('unicode_escape').decode()
                with open(Entry,'r+') as file:
                    temp = []
                    Candidate_Data = file.readlines()
                    for Candidate in Candidate_Data:
                        temp.append(Candidate.replace('"',"").replace("\n","").encode('unicode_escape').decode())
                    Candidate_Data = temp
                    file.close()
            else:
                print("You have entered neither SingleFile or TextFile, try again")

                continue

        except:
            print("You have entered an input that I can not accept, try again")
            continue
        break

    while True:
        try:
            Distance_Measure_Sector,Distance_Measure_Candidate = tuple(input("Enter the column name of the distance measure of the Sector and Candidate csv file seperated by comma: ").split(","))
        except TypeError:
            print("You have entered an input I cannot, accept")
            continue
        except ValueError:
            print("You have entered an input that I cannot accept, try again")
            continue
        break
    
    while True:
        try:
            Distance_Measure = [Distance_Measure_Sector,Distance_Measure_Candidate]
        except TypeError:
            print("You have entered in an input that I cannot accept, try again.")
            continue
        except ValueError:
            print("You have entered an input that I cannot accept, try again")
            continue
        break

    while True:
        try:
            Magnitude_Measure = input("Enter the column name of the Magnitude measure of the csv file: ")
            Temperature_Measure = input("Enter the column name of the temperature measure of the csv file: ")
        except TypeError:
            print("You have entered in an input that I cannot accept, try again.")
            continue
        except ValueError:
            print("You have entered an input that I cannot accept, try again")
            continue
        break

    while True:
        try:
            Magnitude_Range_lower, Magnitude_Range_Upper,Magnitude_Interval = tuple(input("Enter the lower bound, upper bound and interval of the Magnitude seperated by commas ").split(","))
            Temperature_Range_lower, Temperature_Range_Upper,Temperature_Interval = tuple(input("Enter the lower bound, upper bound, and interval of the colour seperated by commas ").split(","))

            if float(Magnitude_Range_Upper) <= float(Magnitude_Range_lower):
                print("You have entered an upper bound for the magnitude that is lower or equal in value to the lower bound. Try again")
                raise ValueError

            if float(Temperature_Range_Upper) <= float(Temperature_Range_lower):
                print("You have entered an upper bound for the temperature that is lower or equal in value to the lower bound. Try again")
                raise ValueError

            if float(Magnitude_Interval) > abs(float(Magnitude_Range_Upper) - float(Magnitude_Range_lower)):
                print("You have entered in a magnitude interval greater than the range of values between the upper and lower bounds of the magnitude. Try again ")
                raise ValueError

            if float(Temperature_Interval) > abs(float(Temperature_Range_Upper)-float(Temperature_Range_lower)):
                print("You have entered in a temperature interval greater than the range of values between the upper and lower bounds of the temperature. Try again")
                raise ValueError

        except TypeError:
            print("You have entered in an input that I cannot accept, try again.")
            continue
        except ValueError:
            print("You have entered in an input that I cannot accept, try again.")
            continue
        try:
            Magnitude_Range = [float(Magnitude_Range_lower),float(Magnitude_Range_Upper),float(Magnitude_Interval)]
            Temperature_Range = [float(Temperature_Range_lower),float(Temperature_Range_Upper),float(Temperature_Interval)]
        except TypeError:
            print("The values you have entered in are not numbers I can accept, try again")
            continue
        break

    while True:
        try:
            filter = int(input("Enter the amount of Sector Stars you want removed from the final plot "))
            resolution = int(input("Enter the resolution you wish to set the image to."))
            if resolution <= 0:
                print("You have entered an invalid value for the resolution, try again")
                raise TypeError
            if filter < 0:
                print("You have entered an invalid value for the filter, try again.")
                raise TypeError
        except TypeError:
            print("You have entered in an input that I cannot accept, try again")
            continue
        except ValueError:
            print("You have entered in an input that I cannot accept, try again.")
            continue
        break

    while True:
        try:
            filter_noise = input("Enter a list of values separated by commas which represent the amount of stars a bin should not have in order to be plotted on the diagram: ").split(",")
            for element in filter_noise:
                try:
                    int(element)
                except TypeError:
                    print("You have entered in a number to filter which is not an integer, Try again.")
                    raise TypeError
                if int(element) < 0:
                    print("You have entered in a number to filter which is less than zero, Try again.")
                    raise ValueError
            filter_noise = [int(x) for x in filter_noise]
        except TypeError:
            print("You have entered a value that I cannot accept, try again.")
            continue
        except ValueError:
            print("You have entered a value that I cannot accept, try again")
            continue
        break

    while True:
        try:
            Candidate_Case = input("Do you want the Candidates to be plotted: Y/N ").lower()
            if "y" in Candidate_Case and len(Candidate_Case) == 1:
                Candidate_Case = True
            elif "n" in Candidate_Case and len(Candidate_Case) == 1:
                Candidate_Case = False
            else:
                print("You have entered a character that is not Y or N, try again ")
                continue
            bin_resolution = int(input("Enter the resolution of the HR_Diagram, the more bins the finer the details but also less cohesive the image. "))
        except TypeError:
            print("You have entered in an input that I cannot accept, try again")
            continue
        except ValueError:
            print("You have entered in an input that I cannot accept, try again.")
            continue
        break

    while True:
        try:
            Sectors_Case = input("Do you want the Background Stars to be plotted: Y/N ").lower()
            if "y" in Sectors_Case and len(Sectors_Case) == 1:
                Sectors_Case = True
            elif "n" in Sectors_Case and len(Sectors_Case) == 1:
                Sectors_Case = False
            else:
                print("You have entered a character that is not Y or N, try again ")
                continue
        except TypeError:
            print("You have entered in an input that I cannot accept, try again")
            continue
        except ValueError:
            print("You have entered in an input that I cannot accept, try again.")
            continue
        break


    Sectors = HR_Diagram_Generator()
    
    try:
        Sectors.add_Sectors_Stars(Sector_Data)
        if Candidate_Data != ['']:
            print("I am running this")
        Sectors.add_Candidate_Stars(Candidate_Data)
        try:
            Sectors.Plot_HR_Diagram_Using_Heatmap(Distance_Measure,Magnitude_Measure,Temperature_Measure,bin_resolution,Magnitude_Range,Temperature_Range,Candidate_Case,Sectors_Case,filter = np.array(filter_noise), image_resolution= bin_resolution, filter_choice= filter)
        except:
            print("An error has occured and the HR diagram could not be plotted. To solve this issue, please read the error message and the documentation...")
    except FileNotFoundError:
        print("The Files you entered had bad file paths try again.")
    except IndexError:
        print("An index error has occured. Please try again")

    while True:
        try:
            Result = input("Are there any more plots you wish to make? Y/N ").lower()
            if "y" in Result and len(Result) == 1:
                Result = True
            elif "n" in Result and len(Result) == 1:
                Result = False
            else:
                print("You have entered a character that is not Y or N, try again ")
                continue    
        except TypeError:
            print("You have Entered an input I cannot accept, try again")
            continue
        except ValueError:
            print("You have entered in an input that I cannot accept, try again.")
            continue
        break
    if Result:
        continue
    else:
        break

