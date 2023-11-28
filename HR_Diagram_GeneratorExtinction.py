"""
This is the main python module out of the selection of files here. The HR Diagram Generator is the workhorse of the operations.
It takes in the data provided by the text based interface, prepocesses the data and outputs the scatterplot and heatmap. The bulk
of the code is in preprocessing the data, locating the relevant bins and plotting the final functions. The HR Diagram Generator is a class.
Initialising the HR Diagram Generator as an object allows it to be used in other python files for quick scatterplots of candidate stars and 
sector stars. 
"""
import numpy as np
import time
from statistics import mean
import re
import warnings
import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns; sns.set_theme(style = 'whitegrid') #Set the theme of the seaborn figures to whitegrid
from matplotlib.colors import LogNorm
import matplotlib.ticker as ticker
from scipy.stats import linregress
from matplotlib.pyplot import cm
plt.rcParams["figure.figsize"] = (16,9) #Set the figure sizes
"""
Created on Tue 16/08/2022 13:13

@author: Kaylen Smith Darnbrook, Inquisitor Nova

URSS HR_Diagram Plot
-Import the csv files containing the parallex,colour and temperature information for all 13 sectors.
-Explore the data to determine missing values, outliers and anomalies
-Calculate the distance form parallex measurements.
-Calculate the absolute magnitude from the photo_mean_mag.
-Bin the continous data of the distance and absolute magnitude into discrete bins
-Plot a scatterplot
-Plot a heatmap
-Adjust titles,x&ytickvalues. 
-Present data.
"""
warnings.filterwarnings("ignore") # Remove the run time warnings to improve the clarity of the user interface.
class HR_Diagram_Generator: 

    def nearest_base(self,number,base):
        """
        A method used to round numbers to their nearest base. ie to the nearest 2,5,7
        """
        return base*round(number/base,1)
    
    def avg(self,num_1,num_2):
        """
        A method used to average two numbers
        """
        return(float(num_1)+float(num_2))/2

    def Bin_Locator(self,DataFrame,Value,tolerance,series,zero_points):
            """
            The Bin locator is used to convert the colour/magnitude continous value into a bin index. 
            This is used primarily to find the bin indexes for the starting and end points of the x and y axes and to 
            find the bin indexes for the major tickers of the axes. The bin locator changes its behaviour depending
            on whether this is a column or row value.
            """
            locator_weight = 0.00001 # A tolerance value used to detemrine the range of acceptable values
            early_stopping = 5 # This value determines how many neighbours it scans left and right of the function to determine the axis location
            if type(zero_points) != str: # The Bin_Locator is feed the zero points of the axes as these can be difficult to find.
                zeropoint_row = zero_points[0] # Zero point for one axis
                zeropoint_column = zero_points[1] # Zero point for the other axis
            else:
                print(zero_points) # if the zero points cannot be assigned, the locator prints the zeropoints. This is primarily for error checking
            if Value == 0.0 and series in "columns": # Assigns the bin index of the imported column zeropoint if the value requested is 0
                    bin_index = zeropoint_column # Assigns the bin index of the imported column zeropoint
                    value_chosen = DataFrame.columns[zeropoint_column] # Assigns the corresponding zeropoint column value for that bin index
                    return int(bin_index),value_chosen # Returns the bin index and corresponding zeropoint column value
            elif Value == 0.0 and series in "rows": # A repeat of the above, but for the rows
                    bin_index = zeropoint_row
                    value_chosen = DataFrame.index[zeropoint_row]
                    return int(bin_index),value_chosen
            for Index in range(0,1000): # Creates a for loop to try and identify a suitable bin with a value close to the user requested value 
                if float(Value) != 0.0: # Checks that it is not the zeropoint to stop ZeroDivision Errors
                    try:
                        """
                        Below sets the range of acceptance surrounding the user requested value. 
                        Should a bin have a column/row value in this acceptance range, the function will return 
                        the bin value and the index of that bin. 
                        """
                        tolerance = abs(1/Value * locator_weight) 
                    except ZeroDivisionError:
                        pass
                lower_bound = Value - abs(Value*tolerance) # Creates the lower bound based off the tolerance
                upper_bound = Value + abs(Value*tolerance) # Creates the uppper bound based off the tolerance.
                if series in "columns": # Below applies to the column values
                    for index,value in enumerate(DataFrame.columns.values): #Iterate through the column values of the frequency table
                        if (value >= lower_bound and value < upper_bound): 
                            # Should the bin value fall within the range of acceptance, capture it's bin_index and value_chosen
                            bin_index = index
                            value_chosen = value
                            try:
                                # To ensure that this is the best possible bin survey the surrounding neighbours
                                neighbours_index = [bin_index-early_stopping,bin_index+early_stopping+1] 
                                for neighbour_index in neighbours_index:
                                    neighbour = DataFrame.columns.values[neighbour_index]
                                    if abs(neighbour - Value) < abs(value_chosen-Value):
                                        # Should a neighbour perform better capture it's bin_index and value_chosen instead
                                        bin_index = neighbour_index
                                        value_chosen = neighbour
                            except IndexError:
                                pass
                            break
                elif series in "rows": # This is a repeat of above but applied to the row values
                    for index,value in enumerate(DataFrame.index.values):
                        if (value >= lower_bound and value < upper_bound):
                            bin_index = index
                            value_chosen = value
                            try:
                                neighbours_index = [bin_index-early_stopping,bin_index+early_stopping+1]
                                for neighbour_index in neighbours_index:
                                    neighbour = DataFrame.index.values[neighbour_index]
                                    if abs(neighbour - Value) < abs(value_chosen-Value):
                                        bin_index = neighbour_index
                                        value_chosen = neighbour
                            except:
                                pass
                            break
                try:
                    bin_index,value_chosen # Check that the bin_index and value_chosen have been found given the range of acceptance.
                    break # Should this be successfull break the for loop.
                except NameError:
                    # Should that not be the case, increase the range of tolerance.
                    locator_weight *= 1.1
            try:
                return(int(bin_index),value_chosen,index) # Return the best match for the bin index and value.
            except NameError:
                print("Cannot find bin index for ",Value,tolerance,series) # Should this fail display to the user that the bin could not be found.

    """
    There are situations where the user inputted colour and magnitude range is larger than the range of the colour
    and magnitude ranges provided by the data. In that situation, the HR Diagram Generator needs to extend the 
    frequency table to match the user requested ranges. When this is required, the run time increases significantly. 
    """
    def Extend_Table(self,DataFrame,avg_dist_in,avg_dist_col,Col_Range,Mag_Range):
        """
        Takes a frequency table and extends the tables it to match the specified colour and magnitude ranges.
        Works by creating a loop that creates additional rows and columns until the range of the columns and rows
        matches the specifiled range.
        """
        case = True
        while case: # Creates a do while loop
            lower_bound_m = DataFrame.index.values[0] # Sets the lower magnitude bound
            upper_bound_m = DataFrame.index.values[-1] # Sets the upper magnitude bound

            lower_bound_c = DataFrame.columns.values[0] # Sets the lower colour bound
            upper_bound_c = DataFrame.columns.values[-1] # Sets the upper colour bound

            # If the user inputted lower magnitude bound is lower than the lower_magnitude bound extend the table by the average separation of column bin values
            if abs(Mag_Range[0]) + 1 > abs(lower_bound_m): 
                index_value = DataFrame.index.values[0] - avg_dist_in
                data = {key:value for key,value in zip(DataFrame.columns.values,np.zeros(len(DataFrame.columns.values),dtype = int))}
                row = pd.DataFrame(data, index = [index_value])
                frames = [row,DataFrame]
                DataFrame = pd.concat(frames, axis = 0)
            
            # If the user inputted upper magnitude bound is higher than the lower magnitude bound extend the table by the average separation of column bin values
            elif abs(Mag_Range[1]) + 1 > abs(upper_bound_m):
                index = DataFrame.index.values[-1] + avg_dist_in 
                DataFrame.loc[index] = np.zeros(len(DataFrame.columns.values), dtype = int)
            
            # If the user inputted lower colour bound is lower than the lower colour bound extend the table by the average separation of row bin values
            elif abs(Col_Range[0]) + 1  > abs(lower_bound_c):
                DataFrame.insert(0,DataFrame.columns.values[0] - avg_dist_col, 0)
        
            # If the user inputted upper colour bound is higher than the upper colour bound extend the table by the average separation of row bins values
            elif abs(Col_Range[1]) + 1 > abs(upper_bound_c):
                column_name = DataFrame.columns.values[-1] + avg_dist_col
                column_values = np.zeros(len(DataFrame.index.values), dtype = int)
                datas = {column_name:column_values}
                column = pd.DataFrame(data = datas, index = DataFrame.index.values)
                frames = [DataFrame,column]
                DataFrame = pd.concat(frames, axis = 1)
            else:
                case = False # Once the table has been extended, switch case to a falde value
                return DataFrame # Return the Dataframe.

    def Avg_Finder(self,DataFrame):
        """
        The average finder is used by the extend table function to find create the new column and row values for the frequency table.
        It works by the finding the difference between the column and row values, storing the differences in the list. 
        It then finds the average difference in column and row values, which it returns.
        """

        difference_0 = [] # Create the list to store the differences in column values
        difference_1 = [] # Create the list to store the differences in row values

        # Create a for loop that searches through the column list values, calculates the differences then stores them in a list.
        for index in range(0,len(DataFrame.columns.values)):
            try:
                diff = DataFrame.columns.values[index+1] - DataFrame.columns.values[index]
                difference_0.append(diff)
            except IndexError:
                continue

        # Create a for loop that searches through the row list values, calculates the differences then stores them in a list.
        for index in range(0,len(DataFrame.index.values)):
            try:
                diff = DataFrame.index.values[index+1] - DataFrame.index.values[index]
                difference_1.append(diff)
            except IndexError:
                continue
        
        # Calculate the average row and column difference then return them
        average_distance_columns = mean(difference_0)
        average_distance_index = mean(difference_1)
        return average_distance_columns,average_distance_index

    def add_Sectors_Stars(self,Sectors):
        """
        This method is used to input the csv file containing information about the magnitude, colour and distances of the stars
        that will form the heatmap of the HR diagram. It takes in the file paths for the Sector csv files, reads and 
        then converts the csv files into dataframes. These are merged into a single DataFrame. 
        Finally it removes the gaia source ids. Only add Sector stars if there are sector stars to add otherwise the function
        will raise a file not found error and crash the program.
        """
        try:
            # If the Sectors variable is not empty and a single file path it reads and then converts the csv file into a dataframe
            if type(Sectors) == str and Sectors != '': 
                self.Sectors_DataSet_Original = pd.read_csv(Sectors)
            # If the Sectors variable is not empty and is a list of file paths, it reads the file paths line by line,
            # Converting them into dataframes and then merging the final result.
            elif type(Sectors) == list:
                self.Sectors_DataSet_Original = pd.DataFrame()
                for Sector in Sectors:
                    if Sector != '':
                        self.Sectors_DataSet_Original = pd.concat([self.Sectors_DataSet_Original,pd.read_csv(Sector)])
            else:
                #Raises file not found error and displays error message if the sector data list is empty.
                print("The Sectors data is not a file or a list of files. Try again.") 
                raise FileNotFoundError
            try:
                # Removes the duplicates using gaia source id if gaia source id is present
                self.Sectors_DataSet_Original.drop_duplicates(subset = ['source_id'],inplace = True)
            except:
                pass
        except IndexError:
            print("Index out of bounds") # For error checking purposes
            raise IndexError
        except FileNotFoundError:
            # Raises file not found message if the file paths are invalid or lead to no file. Displays error message.
            print("Files cannot be found using file paths either because the files do not exist or the file path is invalid.")
            raise FileNotFoundError

    def add_Candidate_Stars(self,Candidates):
        """
        This method is used to input the csv file containing information about the magnitude, colour and distances of the stars
        that will form the scatterplot superimposed onto the HR diagram. It takes in the file paths for the Candidate csv files, reads and 
        then converts the csv files into dataframes. These are merged into a single DataFrame. 
        Finally it removes the gaia source ids. Only add Candidate stars if there are Candidate stars to add otherwise the function
        will raise a file not found error and crash the program
        """
        try:
            # If the candidates file is not empty and is a single file path, it reads the file and converts it into a dataframe
            if type(Candidates) == str and Candidates != '':
                self.Candidates_DataSet = pd.read_csv(Candidates)
            # If the candidates file is not empty and is a list of file paths, it reads each file and converts them into dataframes
            # It then merges them
            elif type(Candidates) == list:
                self.Candidates_DataSet = pd.DataFrame()
                for Candidate_read in Candidates:
                    if Candidate_read != '':
                        self.Candidates_DataSet = pd.read_csv([self.Candidates_DataSet,pd.read_csv(Candidate_read)])
            else:
                # Raises File not found error if the candidate data list is empty and displays message to the user
                print("The Candidates data is not a file or a list of files. Try again.") 
                raise FileNotFoundError
        except IndexError:
            print("Index out of bounds") # For error checking purposes
            raise IndexError
        except FileNotFoundError:
            # Raises file not found error if the file paths are invalid or leads to non existing files. Displays message to user.
            print("Files cannot be found using file paths as the file does not exist or the file paths are invalid") 
            raise FileNotFoundError

    def get_length_Of_Sector_DataSet(self):
        """
        This is a getter method used to access the length of the Sector Data.
        Used primarily for error checking and for insuring the correct amount of stars are being plotted
        """
        return len(self.Sectors_DataSet_Original)

    def Plot_HR_Diagram_Using_Heatmap(self,Distance_Measure,Magnitude_Measure,Color_Measure, Ag_Measure, Extinction_Measure, bin_resolution = "Default",Magnitude_Range = "Default",Color_Range = "Default",plot_candidates = True,plot_sectors = True,filter = np.array([0]),image_resolution = 400,filter_choice = 0):
        """
        Plot HR Diagram is main workhorse of the HR diagram Generator, it takes in the sector and candidate data, does some prepocessing and 
        returns 3 scatterplots and 1 heatmap. This is achieved by converting the dataframes into a 2D grid, a frequency table, and then plotting the frequency table.
        The plotting of such a large frequency diagram using the seaborn heatmap function damages the automated axes and ticks and so they are manually determined and
        fed into the plot. The plot HR diagram reports the amount of data present in the heatmap, the amount of data with null values, and percentage of data that will appear in the diagram
        The plot HR diagram will then return the time taken to run and the bin resolution used. 
        """
        start_time = time.time() # Starts the timer
        self.Sectors_DataSet = self.Sectors_DataSet_Original.copy() # Creates a copy of the sector data 
        Maximum_index_Sectors = len(self.Sectors_DataSet) # Finds the current number of stars
        try:
            self.Sectors_DataSet = self.Sectors_DataSet.iloc[:Maximum_index_Sectors-filter_choice] # Removes from the Sectors Dataset the amount of stars requested by the user
        except IndexError:
            print("filter greater than maximum amount of stars") # Raises an IndexError and displays message should the filter exceed the number of stars in the dataset
            raise IndexError
        except:
            print("The filter you entered is invalid") # Raises an IndexError and displays message should the filter not be an integer value
            raise ValueError
        
        try:
            self.Sectors_DataSet[Color_Measure] = self.Sectors_DataSet[Color_Measure] - self.Sectors_DataSet[Extinction_Measure] # Checks that the colour measure specified by the user exists in the dataframe.
        except KeyError:
            # Raises an error if no colour measure exists.
            print("The Color measure you have entered does not exist in the Sector Dataset, try again") 
            raise KeyError
        
        if plot_candidates:
            try:
                self.Candidates_DataSet[Color_Measure] = self.Candidates_DataSet[Color_Measure] - self.Candidates_DataSet[Extinction_Measure] # Attempts the above with the candidate dataset
            except KeyError:
                print("The Color measure you have entered does not exist in the Candidate Dataset, try again")
                raise KeyError

        print("The original number of stars plotted from the Sectors DataSet is: ",len(self.Sectors_DataSet)) # Displays to the user the original number of sector stars

        if re.match("parallax",Distance_Measure[0]) and plot_sectors: # Should the user have entered parallax values and wish to plot the heatmap do below.
            try:
                self.Sectors_DataSet['Distance'] = 1/(self.Sectors_DataSet[Distance_Measure[0]]/1000) # Convert the parallax into parsecs
            except KeyError:
                # Should the user have provided a distance measure that does not exist, raise an error
                print("The Sector Distance Measure you entered does not exist in the table, try again.")
                raise KeyError
            try:
                # Should the user have provided a magnitude measure that does not exist, raise an error
                self.Sectors_DataSet['Absolute_Magnitude'] = self.Sectors_DataSet[Magnitude_Measure] - 5*np.log10(self.Sectors_DataSet.Distance/10) - self.Sectors_DataSet[Ag_Measure]
            except KeyError:
                print("The Sector Magnitude measure you entered does not exist in the table, try again.")
                raise KeyError

            # Determines the percentage of the sector dataset with missing distance values.
            self.Filled_Distance_Sectors = len(self.Sectors_DataSet[self.Sectors_DataSet.Distance.isnull() == False])
            self.Empty_Distance_Sectors = len(self.Sectors_DataSet[self.Sectors_DataSet.Distance.isnull() == True])
            self.Missing_Distance_Percentage_Sectors = self.Empty_Distance_Sectors/(self.Empty_Distance_Sectors+self.Filled_Distance_Sectors)*100
            print(f"The percentage of the Sectors DataSet with missing parallax data is {round(self.Missing_Distance_Percentage_Sectors,3)}%")
            
        elif plot_sectors:
            # If the Distance measure provided was not parallax, but was a distance in parsecs the method renames the given the distance measure.
            # Renames the Distance Measure to Distance to enable the rest of the program to work
            try:
                self.Sectors_DataSet[Distance_Measure[0]]
                self.Sectors_DataSet.rename(columns = {Distance_Measure[0]: 'Distance'}, inplace = True)
            except KeyError:
                # Checks whether the Distance Measure exists in the table and if not raises an error.
                print("The Sector Distance Measure you provided does not exist in the table try again.")
                raise KeyError

            try:
                # Calculates the absolute magnitude from the magnitude measure and checks whether the distance measure exists.
                self.Sectors_DataSet['Absolute_Magnitude'] = self.Sectors_DataSet[Magnitude_Measure] - 5*np.log10(self.Sectors_DataSet.Distance) - self.Sectors_DataSet[Ag_Measure]
            except KeyError:
                # Raises a KeyError and displays an error message should the distance measure not exist.
                print("The Sector Magnitude Measure you have provided does not exist in the table, try again.")
                raise KeyError
            
            # Determines the percentage of the sector dataset with missing distance values.
            self.Filled_Distance_Sectors = len(self.Sectors_DataSet[self.Sectors_DataSet.Distance.isnull() == False])
            self.Empty_Distance_Sectors = len(self.Sectors_DataSet[self.Sectors_DataSet.Distance.isnull() == True])
            self.Missing_Distance_Percentage_Sectors = self.Empty_Distance_Sectors/(self.Empty_Distance_Sectors+self.Filled_Distance_Sectors)*100
            print(f"The percentage of the Sectors DataSet with missing distances is {round(self.Missing_Distance_Percentage_Sectors,3)}%")
        
        # Repeats what was done for the Sector data, but now with the candidate data.
        if re.match('parallax', Distance_Measure[1]) and plot_candidates:
            try:
                self.Candidates_DataSet['Distance'] = 1/(self.Candidates_DataSet[Distance_Measure[1]]/1000)
            except KeyError:
                print("The candidate distance measure you entered does not exist in the table.")
                raise KeyError

            try:
                self.Candidates_DataSet['Absolute_Magnitude'] = self.Candidates_DataSet[Magnitude_Measure] -5*np.log10(self.Candidates_DataSet.Distance/10) - self.Candidates_DataSet[Ag_Measure]
            except KeyError:
                print("The Candidate Magnitude Measure you entered does not exist in the table")
                raise KeyError
            
            self.Filled_Distance_Candidates = len(self.Candidates_DataSet[self.Candidates_DataSet.Distance.isnull() == False])
            self.Empty_Distance_Candidates = len(self.Candidates_DataSet[self.Candidates_DataSet.Distance.isnull() == True])
            self.Missing_Distance_Percentage_Candidates = self.Empty_Distance_Candidates/(self.Empty_Distance_Candidates+self.Filled_Distance_Candidates)*100
            print(f"The percentage of the Candidates DataSet with missing parallax is {round(self.Missing_Distance_Percentage_Candidates,3)}%")

        elif plot_candidates:
            try:
                self.Candidates_DataSet[Distance_Measure[1]]
                self.Candidates_DataSet.rename(columns = {Distance_Measure[1]:'Distance'}, inplace = True)
            except KeyError:
                print("The Candidate Distance measure you provided does not exist in the table, try again")
                raise KeyError
            try:
                self.Candidates_DataSet['Absolute_Magnitude'] = self.Candidates_DataSet[Magnitude_Measure] -5*np.log10(self.Candidates_DataSet.Distance) - self.Candidates_DataSet[Ag_Measure]
            except KeyError:
                print("The Candidate Magnitude measure you provided does not exist in the table, try again.")
                raise KeyError
            
            self.Filled_Distance_Candidates = len(self.Candidates_DataSet[self.Candidates_DataSet.Distance.isnull() == False])
            self.Empty_Distance_Candidates = len(self.Candidates_DataSet[self.Candidates_DataSet.Distance.isnull() == True])
            self.Missing_Distance_Percentage_Candidates = self.Empty_Distance_Candidates/(self.Empty_Distance_Candidates+self.Filled_Distance_Candidates)*100
            print(f"The percentage of the Candidates DataSet with missing distances is {round(self.Missing_Distance_Percentage_Candidates,3)}%") 
        
        # Removes the duplicates in the gaia ids and calculates the percentage of candidate stars with missing colour values
        if plot_candidates:
            try:
                self.Candidates_DataSet.drop_duplicates(subset = 'source_id',inplace = True)
            except:
                pass
            try:
                self.Filled_Colors_Candidates = len(self.Candidates_DataSet[self.Candidates_DataSet[Color_Measure].isnull() == False])
                self.Empty_Colors_Candidates = len(self.Candidates_DataSet[self.Candidates_DataSet[Color_Measure].isnull() == True])
                self.Missing_Color_Percentage_Candidates = self.Empty_Colors_Candidates/(self.Empty_Colors_Candidates+self.Filled_Colors_Candidates)*100
                print(f"The percentage of the Candidates DataSet with missing colors is {round(self.Missing_Color_Percentage_Candidates,3)}%")
            except KeyError:
                print("You have provided a colour measure that does not exist in the table, try again.")
                raise KeyError

        # Should the user have set the Color range and Magnitude range to default to see what the heatmap looks naturally, 
        # This code will generate the Color and Magnitude ranges.
        if type(Color_Range) == str and plot_sectors:
                Color_Range = [self.Sectors_DataSet[Color_Measure].min(),self.Sectors_DataSet[Color_Measure].max(),0.5]
        if type(Magnitude_Range) == str and plot_sectors:
                Magnitude_Range = [self.Sectors_DataSet[Magnitude_Measure].min(),self.Sectors_DataSet[Magnitude_Measure].max(),0.5]
        
        if type(Color_Range) != list and plot_sectors:
            print("You have neither typed in the colour range as default or entered in a list of values, please try again.")
            raise ValueError
        if type(Magnitude_Range) != list and plot_sectors:
            print("You have neither typed in the magnitude range as default or entered in a list, try again.")
            raise ValueError
        
        # This code ensures the color range and magnitude range has been entered appropriately
        if len(Color_Range) != 3:
            print("You have entered a Color_Range with a list length not equal to 3, try again.")
            raise ValueError
        if len(Magnitude_Range) != 3:
            print("You have entered a Magnitude_Range with a list length not equal to 3, try again.")
            raise ValueError

        # Display the colour range and magnitude range to the user
        print("The Color_Range: ",Color_Range)
        print("The Magnitude_Range: ",Magnitude_Range)  
        
        # Calculates the percentage of the sector dataset with missing colours
        if plot_sectors:
            self.Filled_Colors_Sectors = len(self.Sectors_DataSet[self.Sectors_DataSet[Color_Measure].isnull() == False])
            self.Empty_Colors_Sectors = len(self.Sectors_DataSet[self.Sectors_DataSet[Color_Measure].isnull() == True])
            self.Missing_Color_Percentage_Sectors = self.Empty_Colors_Sectors/(self.Empty_Colors_Sectors+self.Filled_Colors_Sectors)*100
            print(f"The percentage of the Sectors DataSet with missing colors is {round(self.Missing_Color_Percentage_Sectors,3)}%")
        
        # Calculates the percentage of the sector datset with missing data
        if re.match("parallax",Distance_Measure[0]) and plot_sectors:
            A = self.Sectors_DataSet[self.Sectors_DataSet[Color_Measure].isnull() == True]
            B = A[A.parallax.isnull() == True]
            self.Missing_Data_Percentage_Sectors = ((self.Empty_Distance_Sectors+self.Empty_Colors_Sectors)-len(B))/len(self.Sectors_DataSet)*100
            print(f"The percentage of the Sectors DataSet that will be missing from the HR_Diagram is {round(self.Missing_Data_Percentage_Sectors,3)}%")
        elif plot_sectors:
            A = self.Sectors_DataSet[self.Sectors_DataSet[Color_Measure].isnull() == True]
            B = A[A.Distance.isnull() == True]
            self.Missing_Data_Percentage_Sectors = ((self.Empty_Distance_Sectors+self.Empty_Colors_Sectors)-len(B))/len(self.Sectors_DataSet)*100
            print(f"The percentage of the Sectors DataSet that will be missing from the HR_Diagram is {round(self.Missing_Data_Percentage_Sectors,3)}%")
        
        # Calculates the percentage of the Candidates dataset with missing data
        if plot_candidates and  re.match("parallax",Distance_Measure[1]):
            A = self.Candidates_DataSet[self.Candidates_DataSet[Color_Measure].isnull() == True]
            B = A[A.parallax.isnull() == True]
            self.Missing_Data_Percentage_Candidates = ((self.Empty_Distance_Candidates+self.Empty_Colors_Candidates)-len(B))/len(self.Candidates_DataSet)*100
            print(f"The percentage of the Candidates DataSet that will be missing from the HR_Diagram is {round(self.Missing_Data_Percentage_Candidates,3)}%")
        elif plot_candidates:
            A = self.Candidates_DataSet[self.Candidates_DataSet[Color_Measure].isnull() == True]
            B = A[A.Distance.isnull() == True]
            self.Missing_Data_Percentage_Candidates = ((self.Empty_Distance_Candidates+self.Empty_Colors_Candidates)-len(B))/len(self.Candidates_DataSet)*100
            print(f"The percentage of the Candidates DataSet that will be missing from the HR_Diagram is {round(self.Missing_Data_Percentage_Candidates,3)}%")
        
        # Removes the negative parallax values and parallax values with an error greater than 0.4
        if plot_sectors and re.match('parallax',Distance_Measure[0]):
            self.Sectors_DataSet = self.Sectors_DataSet[self.Sectors_DataSet.parallax.ge(0)]
            try:
                self.Sectors_DataSet = self.Sectors_DataSet[self.Sectors_DataSet.parallax_error < 0.4]
            except KeyError:
                print("You have not provided the error for the parallax as 'parallax_error', the program will continue nevertheless.")
        
        # Generates a bin resolution for diagram if the bin resolution is set to default
        if type(bin_resolution) == str:
            bin_resolution = round(0.0009*len(self.Sectors_DataSet)+1000)
        
        # Transforms the the continous values of the absolute magnitude and colour into pandas intervals (Categoric Values)
        try:
            self.Sectors_DataSet['CatAbsMag'] = pd.cut(self.Sectors_DataSet.Absolute_Magnitude,bins = bin_resolution, ordered = True)
            self.Sectors_DataSet['CatColor'] = pd.cut(self.Sectors_DataSet[Color_Measure],bins = bin_resolution, ordered = True)
        except:
            # Returns an error if it is unable to perform the operation
            print("Attempted to cut the continous Sector data into discrete data and failed. Try again.")
            raise ValueError
            
        # Determines the bin intervals of the Sector Dataset's Colour
        lists = [] # Creates a list to store the intervals for Colours
        for interval in self.Sectors_DataSet.CatColor.cat.categories: # Iterates through the panda intervals
            list_element = re.sub(r'[][()]+','',str(interval)).replace(","," ").split() # Converts the pandas intervals into the lower bound and upper bound
            lists.append(float(list_element[0])) # Adds the lower bound of the interval to the list
            lists.append(float(list_element[1])) # Adds the upper bound of the interval to the list

        data = {'row':lists} # Stores the data as a dictionary 
        Lister = pd.DataFrame(data) # Converts the data to pandas dataframe
        Lister.drop_duplicates(inplace = True) # Drops the duplicates in intervals
        bins_Color = [getattr(row,'row') for row in Lister.itertuples()] # Extracts the intervals storing them as a list 

        # Determines the bin intervals of the Sector Dataset's Magnitude, performs a repeat of the above
        lists = []
        for interval in self.Sectors_DataSet.CatAbsMag.cat.categories:
            list_element = re.sub(r'[][()]+','',str(interval)).replace(","," ").split()
            lists.append(float(list_element[0]))
            lists.append(float(list_element[1]))

        data = {'row':lists}
        Lister = pd.DataFrame(data)
        Lister.drop_duplicates(inplace = True)
        bins_CatsAbsMag = [getattr(row,'row') for row in Lister.itertuples()]

        # To ensure that the frequency tables for the Sector and Candidate data match we cut the colour and magnitude values of the candidate data into
        # the same bins.
        if plot_candidates:
            try:
                # Convert the continous values into categoric values using the same bin intervals the sector data has.
                self.Candidates_DataSet['CatColor'] = pd.cut(self.Candidates_DataSet[Color_Measure],bins = bins_Color,ordered = True)
                self.Candidates_DataSet['CatAbsMag'] = pd.cut(self.Candidates_DataSet.Absolute_Magnitude,bins = bins_CatsAbsMag, ordered = True)
            except:
                # Raises an Error, should this process fail. Mainly for error checking processes
                print("Attempted to cut the continous Candidate into discrete data and failed. Try again.")
                raise ValueError
        
        """
        The HR diagram uses data from a frequency table. The data is binned and at this point its colour and magnitude are an interval value.
        The frequency table then renames the columns and rows using the average of the interval value of that pandas interval. By doing this we are making 
        an approximation. The true colour may lie between 1.0000005 and 1.0000004 but it's reported colour will now be 1.00000045. This is fine because the number
        of bins should be sufficiently high enough that this approximation is accurate enough for a figure, but is not accurate for a very low number of bins.
        A low number of bins should thus be igorned.
        """

        # Isolates the columns needed for the Sector part of the HR diagram, then creates a frequency table from the sector data.
        self.Reduced_Sectors_DataSet = self.Sectors_DataSet[['CatColor','CatAbsMag']] # Creates a dataframe consisting only of the Categoric Colour and Categoric Magnitude
        self.Reduced_Sectors_DataSet_Fqt = pd.crosstab(index = self.Reduced_Sectors_DataSet.CatAbsMag,columns = self.Reduced_Sectors_DataSet.CatColor,dropna = False) # Creates the frequency dataframe.
        self.Reduced_Sectors_DataSet_Fqt = self.Reduced_Sectors_DataSet_Fqt.rename(columns = lambda x: float(self.avg(re.sub(r'[][()]+','',str(x)).replace(","," ").split()[0],re.sub(r'[][()]+','',str(x)).replace(","," ").split()[1]))) # Converts the column names from pandas intervals to the average of that interval
        self.Reduced_Sectors_DataSet_Fqt = self.Reduced_Sectors_DataSet_Fqt.rename(index = lambda x: float(self.avg(re.sub(r'[][()]+','',str(x)).replace(","," ").split()[0],re.sub(r'[][()]+','',str(x)).replace(","," ").split()[1]))) # Converts the row names from pandas intervals to the average of that interval
        self.Reduced_Sectors_DataSet_Fqt = self.Reduced_Sectors_DataSet_Fqt.fillna(0) # Fill in the null values with zeros
        

        self.Reduced_Sectors_DataSet_Fqt.replace(to_replace = filter, value = 0,inplace = True) # To clear the HR diagram of mismatched data, a filter can be imposed that replaces all bins of a certain value with zero

        # Isolates the columns needed for the Candidate part of the HR diagram, then creates a frequency table from the sector data. Does the same as above.
        if plot_candidates:
            self.Reduced_Candidates_DataSet = self.Candidates_DataSet[["CatColor","CatAbsMag"]]
            self.Reduced_Candidates_Fqt = pd.crosstab(index = self.Reduced_Candidates_DataSet.CatAbsMag,columns = self.Reduced_Candidates_DataSet.CatColor, dropna = False)
            self.Reduced_Candidates_Fqt = self.Reduced_Candidates_Fqt.rename(columns = lambda x: float(self.avg(re.sub(r'[][()]+','',str(x)).replace(","," ").split()[0],re.sub(r'[][()]+','',str(x)).replace(","," ").split()[1])))
            self.Reduced_Candidates_Fqt = self.Reduced_Candidates_Fqt.rename(index = lambda x: float(self.avg(re.sub(r'[][()]+','',str(x)).replace(","," ").split()[0],re.sub(r'[][()]+','',str(x)).replace(","," ").split()[1])))
            self.Reduced_Candidates_Fqt = self.Reduced_Candidates_Fqt.fillna(0)
        
            
        avg_dist_col_sector,avg_dist_in_sector = self.Avg_Finder(self.Reduced_Sectors_DataSet_Fqt) # Finds the average separation between the average intervals
        Sector_Norm = self.Extend_Table(self.Reduced_Sectors_DataSet_Fqt,avg_dist_in_sector,avg_dist_col_sector,Color_Range,Magnitude_Range) # Extends the frequency table to the users requirements

        if plot_candidates:
            avg_dist_col_candidates,avg_dist_in_candidates = self.Avg_Finder(self.Reduced_Candidates_Fqt) # Finds the average separation between the average interval
            Candidates_Norm = self.Extend_Table(self.Reduced_Candidates_Fqt,avg_dist_in_candidates,avg_dist_col_candidates,Color_Range,Magnitude_Range) # Extends the frequency table to the users requirements

        
        self.Reduced_Sectors_DataSet_Fqt = Sector_Norm.copy() # Restores the data as reduced sectors frequency dataset
        if plot_candidates:    
            self.Reduced_Candidates_Fqt = Candidates_Norm.copy() # Restores the data as reduced candidates frequency dataset
        
        # Finds the zeropoints using a slightly altered method to the method used by the bin locator
        if plot_sectors:
            value_drop_row,value_drop_column = 0.009,0.009 # Sets the initial range of acceptance
            comparison_row,comparison_column = 0.01,0.01 # Sets the initial row and column zeropoints to compare against
            value_chosen_row = 10 
            value_chosen_column = 10
            for incrementor in range(0,100):
                # Iterates through the index values looking for a zeropoint that is less than the initial range of acceptance.
                # Compares against the comparison row, to converge on the closest value to zero
                for index,value in enumerate(self.Reduced_Sectors_DataSet_Fqt.index.values): 
                    if abs(value) < abs(value_drop_row):
                        zeropoint_row = index # Updates the index
                        value_chosen_row = value # Updates the value
                try:
                    if abs(value_chosen_row) < abs(comparison_row): # Compares against the comparison values
                        comparison_row = value_chosen_row # Updates the comparison row
                        value_drop_row = value_chosen_row # Updates the range of acceptance
                except:
                    pass
                # Repeats the above for the column values
                for index,value in enumerate(self.Reduced_Sectors_DataSet_Fqt.columns.values):
                    if abs(value) < abs(value_drop_column):
                        zeropoint_column = index
                        value_chosen_column = value
                try:
                    if abs(value_chosen_column) < abs(comparison_column):
                        comparison_column = value_chosen_column
                        value_drop_column = value_chosen_column    
                except:
                    pass
                try:
                    zeropoint_row # Checks to see if a zeropoint could be found, if not increases the range of acceptance
                except NameError:
                    value_drop_row *= 1.05
                    comparison_row *= 1.05
                try:
                    zeropoint_column # Checks to see if a zeropoint could be found, if not increases the range of acceptance
                except NameError:
                    value_drop_column *= 1.05
                    comparison_column *= 1.05
            try:
                zero_points = [zeropoint_row,zeropoint_column] # Returns the zeropoints as a list containing the zeropoint for the row and column
            except:
                print("Zeropoints not found") # If the zeropoint cannot be found, the user is informed and the zeropoints is set to NaN.
                zero_points = "NaN"

            # The boundaries of the figure are created below, a padding is created to ensure that the ranges are inclusive. 
            self.padding_start_m = -0.1 # Padding for magnitude values
            self.padding_end_m = 0.1

            self.padding_start_c = 0.0 # Padding for colour values
            self.padding_end_c = 0.02

            start_m = Magnitude_Range[0]+self.padding_start_m # Sets the starting magnitude value for the axis
            end_m = Magnitude_Range[1]+self.padding_end_m  # Sets the ending magnitude value for the axis

            start_c = Color_Range[0]+self.padding_start_c # Sets the starting colour value for the axis
            end_c = Color_Range[1]+self.padding_end_c # Sets the ending colour value for the axis

            start_index_m = self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt,start_m,0.02,"rows",zero_points)[0] # Produces the bin index for the starting magnitude value
            end_index_m = self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt,end_m,0.008,"rows",zero_points)[0] # Produces the bin index for the ending magnitude value
            start_index_c = self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt,start_c,0.008,"columns",zero_points)[0] # Produces the bin index for starting colour value
            end_index_c = self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt,end_c,0.001,"columns",zero_points)[0] # Produces the bin index for the ending colour value

            try:
                 # Filters the Sector frequency table to produce a frequency table with the specified magnitude and colour ranges
                self.Reduced_Sectors_DataSet_Fqt_Cut = self.Reduced_Sectors_DataSet_Fqt.iloc[start_index_m:end_index_m+1,start_index_c:end_index_c+1]
            except IndexError:
                print("The Colour and Magnitude Range you have entered is out of bounds for the Sectors dataset, please try again.")
                # If the colour and magnitude ranges are out of bounds and extend table failed an IndexError is raised 
                raise IndexError
            
            # The shape of the Sectors_Dataset and Candidate dataset is calculated to ensure the dataset is being handled properly
            print("The shape of the Sectors_Dataset array is", self.Reduced_Sectors_DataSet.shape)
            if plot_candidates: # The above is done to the candidate dataset
                print("The shape of the candidates dataSet is", self.Reduced_Candidates_DataSet.shape)
                try:
                    self.Reduced_Candidates_Fqt_Cut = self.Reduced_Candidates_Fqt.iloc[start_index_m:end_index_m+1,start_index_c:end_index_c+1]
                except IndexError:
                    print("The Colour and Magnitude Range you have entered are out of bounds for the candidate dataset, please try again")

                for index in range(0,len(self.Reduced_Candidates_Fqt_Cut.index.values)):
                    self.Reduced_Candidates_Fqt_Cut.index.values[index] = index
                for index in range(0,len(self.Reduced_Candidates_Fqt_Cut.columns.values)):
                    self.Reduced_Candidates_Fqt_Cut.columns.values[index] = index
        
        # Finds the zeropoints again, repeating the above but for the filtered frequency table this time.
        if plot_sectors:  
            value_drop_row,value_drop_column = 0.1,0.1
            comparison_row,comparison_column = 0.1,0.1
            value_chosen_row = 10
            value_chosen_column = 10

            for _ in range(0,100):
                for index,value in enumerate(self.Reduced_Sectors_DataSet_Fqt_Cut.index.values):
                    if abs(value) < abs(value_drop_row):
                        zeropoint_row = index
                        value_chosen_row = value
                if abs(value_chosen_row) < abs(comparison_row):
                    comparison_row = value_chosen_row
                    value_drop_row = value_chosen_row

                for index,value in enumerate(self.Reduced_Sectors_DataSet_Fqt_Cut.columns.values):
                    if abs(value) < abs(value_drop_column):
                        zeropoint_column = index
                        value_chosen_column = value

                if abs(value_chosen_column) < abs(comparison_column):
                    comparison_column = value_chosen_column
                    value_drop_column = value_chosen_column
                try:
                    zeropoint_row
                except NameError:
                    value_drop_row *= 1.05
                    comparison_row *= 1.05
                try:
                    zeropoint_column
                except NameError:
                    value_drop_column *= 1.05
                    comparison_column *= 1.05
                try:
                    zero_points = [zeropoint_row,zeropoint_column]
                except:
                    print("Zeropoints not found")
                    zero_points = "NaN"

            tolerance = 0.008

            Color_Range = np.arange(Color_Range[0],Color_Range[1]+Color_Range[2],Color_Range[2]) # Creates the Color range based off the user import
        
            # Uses the bin locator to determine the bin index values of the colour values
            Positions_Of_Color_Ticks = [] # Creates a list to store the bin index values for the colour ticks of the colour axis
            for Color in Color_Range: # Creates a for loop that searches through the colour range list
                try:
                    Positions_Of_Color_Ticks.append(self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt_Cut,Color,tolerance,"columns",zero_points)[0]) # Returns the bin index for that colour major tick
                except:
                    print("I Could not find the coluor ",self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt_Cut,Color,tolerance,"columns",zero_points)) # Returns the full output of the bin locator should the locator fail to find to find the colour
            """
            Below is for error checking purposes
            print("Colour Range: ",Color_Range)
            for position in Positions_Of_Color_Ticks:
                print(self.Reduced_Sectors_DataSet_Fqt_Cut.columns[position])
            """
            Magnitudes_Range = np.arange(Magnitude_Range[0],Magnitude_Range[1]+Magnitude_Range[2],Magnitude_Range[2]) # Creates the Magnitude range based off the user import
            Positions_Of_Magnitude_Ticks = [] # Generates a list to store the bin indexes of the bin range list
            for Magnitude in Magnitudes_Range: # Creates a for loop that searches the magnitude range list 
                try:
                    Positions_Of_Magnitude_Ticks.append(self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt_Cut,Magnitude,tolerance,"rows",zero_points)[0]) # Returns the bin index for the magnitude major tick
                except:
                    print("Could not find Magnitude value: ",self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt_Cut,Magnitude,tolerance,"rows",zero_points)) # Returns the full output of the bin locator should the locator fail to find the magnitude
            #print("Magnitude Range: ",Magnitudes_Range) For error checking purposes

            #  Below  creates a map that maps the colour and magnitude values of the candidate stars to bin indexes using the candidate and sector frequency table.
            if plot_candidates:
                self.Candidates_DataSet.dropna(subset = ["CatColor","CatAbsMag"],inplace = True) # Removes the null values from the dataset
                mapping_tool_rows = {key:value for key,value in zip(self.Reduced_Sectors_DataSet_Fqt_Cut.index.values,self.Reduced_Candidates_Fqt_Cut.index.values)} # Creates the map that maps a bin from the sector dataset to the candidate dataset for the rows
                mapping_tool_columns = {key:value for key,value in zip(self.Reduced_Sectors_DataSet_Fqt_Cut,self.Reduced_Candidates_Fqt_Cut)} # Creates a map that maps a bin from the sector dataset to the candidate for the columns

                x_values = [] # Creates a list to store the bin indexes of the candidate colour values
                for index,string in enumerate(self.Candidates_DataSet.CatColor): # Iterates through the colour pandas interval transforming the interval into a x bin index coordinate
                    try:
                        list_element = self.avg(re.sub(r'[][()]+','',str(string)).replace(","," ").split()[0],re.sub(r'[][()]+','',str(string)).replace(","," ").split()[1]) # Calculates the average value of the pandas interval
                        x_value = mapping_tool_columns.get(float(list_element)) # Converts the candidate bin index value into a sector bin index value
                        x_values.append(x_value) # Adds the index value to the list
                    except IndexError:
                        print("I cannot find this index, string pair: ",index,string) # Should the index not be found report the colour value to the user. Primarily for error checking

                y_values = [] # Creates a list to store the bin indexes of the candidate magnitude values
                for index,string in enumerate(self.Candidates_DataSet.CatAbsMag): # Repeats above but for the magnitude values
                    try:
                        list_element = self.avg(re.sub(r'[][()]+','',str(string)).replace(","," ").split()[0],re.sub(r'[][()]+','',str(string)).replace(","," ").split()[1])
                        y_values.append(mapping_tool_rows.get(float(list_element)))
                    except IndexError:
                        print("I cannot find this index, string pair:",index,string)
            
            # The code below finds the labels for the x and y axis of the HR diagram
            if plot_sectors: 
                labels_x_axis = [] # Creates a list to store the labels of the colour axis
                for label_index in Positions_Of_Color_Ticks: # Creates a for loop that scans through the positions of colour ticks
                    element = round(self.Reduced_Sectors_DataSet_Fqt_Cut.columns[label_index],1) # Returns the corresponding bin value for that bin index. Then rounds it.
                    if abs(element) == 0.0: # Looks for the zeropoint
                        element = abs(element) # ensures the zeropoint is not negative
                    labels_x_axis.append(element) # Adds the label to the label list.

                labels_y_axis = [] # Repeats the above but for the y axis
                temp = []
                for label_index in Positions_Of_Magnitude_Ticks:
                    element = round(self.Reduced_Sectors_DataSet_Fqt_Cut.index[label_index],1)
                    if abs(element) == 0.0:
                        element = abs(element)
                    labels_y_axis.append(element)
                    temp.append(label_index)
            
                #if plot_candidates:
                    #print("The candidate coordinates are: ",x_values,y_values) This is primarily for error checking
                
                Positions_Of_Magnitude_Ticks_Adjusted = temp

                # This code determines the number of stars that will be plotted on the HR diagram.
                number = 0
                for column in self.Reduced_Sectors_DataSet_Fqt_Cut.columns: # Iterate through each column
                    number += self.Reduced_Sectors_DataSet_Fqt_Cut[column].sum() # Sum the values in that column then add it to the number variable

                print(f"Given your selection of the colour and magnitude range, and cutting out errorous data, the HR Diagram now contains {number} Sector stars")
        

        if plot_candidates:
            try:
                # Plots the first figure, a simple scatterplot of the candidate stars 
                Figure_1= plt.figure() # Create a figure
                ax_1 = sns.scatterplot(x = Color_Measure, y = 'Absolute_Magnitude', data = self.Candidates_DataSet) # Plot a scatterplot
                ax_1.set_xlabel(f"{Color_Measure} Color") # Set the x label to name of the colour measure
                ax_1.set_ylabel("Absolute Magnitude") # Set the y label to the name of the magnitude measure
                ax_1.invert_yaxis()
                Figure_1.savefig('HR_Candidate_Raw_Scatter_Plot.jpg', bbox_inches='tight', dpi=400) # Save the figure 
                plt.clf()
                plt.close() # Close the figure and plot
            except:
                print("Figure 1 could not be plotted") # Should this fail, display that the plot could not be plotted

            try:
                """
                This figure is more complex, requiring in addition to the magnitude and colour information
                - A column containinig the rv_amplitude_robust values
                - A column containing the the star type ( Single Star, Spectroscopic Binary, Eclipsing Binary, Astrometric Binary ) which the GAIA archive calls non single star
                Due to this fact the plot will not always be produced and will not crash the program if this is the case.
                """
                # Plots the second figure, a scatterplot of the candidate stars with the radial velocity amplitudes as a colorbar
                Figure_2 = plt.figure() # Create a figure
                norm = LogNorm(self.Candidates_DataSet["rv_amplitude_robust"].min(),self.Candidates_DataSet['rv_amplitude_robust'].max()) # Create a lognorm to scale the colorbar
                ax_2 = sns.scatterplot(x = Color_Measure, y = 'Absolute_Magnitude', hue = 'rv_amplitude_robust', hue_norm = norm, data = self.Candidates_DataSet, style = 'non_single_star',markers = {0:'o',1:'s',2:'^',3:'*'},alpha = 0.9, legend = 'brief') # Plot the scatterplot
                ax_2.invert_yaxis() # Invert the axis to obey HR Diagram standards
                sm = cm.ScalarMappable(cmap = 'rocket_r', norm = norm)  # Create a colormap using created LogNorm
                sns.color_palette('flare', as_cmap = True) # Set color palette to flare
                sm.set_array([])
                ax_2.figure.colorbar(sm,label = "Log Radial Velocities(Kms)") # Create a colorbar with the label Log Radial Velocities (Kms)
                handles, _ = ax_2.get_legend_handles_labels() # Get the legend handles
                ax_2.legend(handles[4:],['Single_Star','Astrometric Binary','Ecplising Binary','Spectroscopic Binary']) # Ditch the handles after 4, then names the 4
                ax_2.set_xlabel(f'GAIA {Color_Measure} Color') # Names the x label
                ax_2.set_ylabel(f'Absolute_Magnitude') # Names the y label
                Figure_2.savefig('HR_Candidate_Radial_Plot.jpg', bbox_inches='tight', dpi=400) # Saves the figure
                plt.clf() # Closes the figure
                plt.close() # Closes matplotlib tab
            except NameError:
                print("Either no column called rv_amplitude_robust or non_single_star in dataset provided, thus no HR_Diagram_Radial_Plot(Figure2) has been produced") # If the radial velocity amplitude or non single star is not provided figure 2 does not plot. Displays this to the user 
            except:
                print("Figure 2 could not be plotted") # Should the figure fail for other reasons this is displayed.

            try:
                # The code below fits a linear fit to the candidate data
                mask = ~np.isnan(self.Candidates_DataSet[Color_Measure]) & ~np.isnan(self.Candidates_DataSet['Absolute_Magnitude']) # Creates a mask to filter the data with NaN entries
                x = self.Candidates_DataSet[Color_Measure] # Sets the x values to the colour measure
                y = self.Candidates_DataSet['Absolute_Magnitude'] # Sets the y value to the magnitude measure
                m,c,r_value,p_value,std_error = linregress(x[mask],y[mask]) # Obtains the fit parameters from scipy linregress
                # Displays the fit parameters to the user
                print(f"A linear fit has been drawn to the HR Diagram. The gradient is {round(m,2)}, the intercept is {round(c,2)}.") 
                print(f"The r_value is {round(r_value,2)}, the p_value is {round(p_value,2)}, the standard error is {round(std_error,2)}.")
                
                # Plots figure 2 but with a linear fit superimposed on the scatterplot
                Figure_3 = plt.figure()
                norm = LogNorm(self.Candidates_DataSet["rv_amplitude_robust"].min(),self.Candidates_DataSet['rv_amplitude_robust'].max())
                ax_3 = sns.scatterplot(x = Color_Measure,y = 'Absolute_Magnitude', hue = 'rv_amplitude_robust', hue_norm = norm, data = self.Candidates_DataSet, style = 'non_single_star',markers = {0:'o',1:'s',2:'^',3:'*'},alpha = 0.9, legend = 'brief')
                plt.plot(self.Candidates_DataSet[Color_Measure],m*self.Candidates_DataSet[Color_Measure]+c) # Plots the straight line onto the data
                ax_3.invert_yaxis()
                sm = cm.ScalarMappable(cmap = 'rocket_r', norm = norm)
                sns.color_palette('flare', as_cmap = True)
                sm.set_array([])
                ax_3.figure.colorbar(sm,label = "Log Radial Velocities(Kms)", ax = ax_3)
                handles,_ = ax_3.get_legend_handles_labels()
                ax_3.legend(handles[4:],['Single_Star','Astrometric Binary','Ecplising Binary','Spectroscopic Binary'])
                ax_3.set_xlabel(f'GAIA {Color_Measure} Color')
                ax_3.set_ylabel('Absolute_Magnitude')
                Figure_3.savefig('HR_Candidate_Linear_Radial_Plot.jpg', bbox_inches='tight', dpi=400)
                plt.clf()
                plt.close()
            except NameError:
                print("No column called rv_amplitude_robust in dataset provided, thus no HR_Diagram_Radial_Plot has been produced")
            except:
                print("Figure 3 could not be plotted")
        
        # Plots the main figure, the observational HR diagram, a scatterplot of a stars colour versus it's magnitude.
        if plot_sectors:      
            # Renames the column and row names, rounding them to the nearest 1
            self.Reduced_Sectors_DataSet_Fqt_Cut = self.Reduced_Sectors_DataSet_Fqt_Cut.rename(columns = lambda x: self.nearest_base(x,1))
            self.Reduced_Sectors_Data = self.Reduced_Sectors_DataSet_Fqt_Cut.rename(index = lambda x: self.nearest_base(x,1))


            Figure_4 = plt.figure() # Creates the figure for the plot
            ax_4 = sns.heatmap(self.Reduced_Sectors_DataSet_Fqt_Cut,norm = LogNorm(),cmap = 'rocket', cbar_kws = {'label': 'Number Density','pad':0.01}, linewidths = 0) # Plots the heatmap of stars and creates a LogNorm colourbar
            plt.rc('font',size = 30) # Sets the font size to 39
            cbar = ax_4.collections[0].colorbar # Accesses the colorbar created for the heatmap

            cbar.ax.get_yaxis().set_ticks([cbar.vmin,np.sqrt((cbar.vmax-cbar.vmin)),cbar.vmax]) # Sets the major colorbar ticks 
            cbar.ax.tick_params(labelsize = 20) # Sets the size of the tick bar labels
            cbar.set_label(label = "Number Density", fontsize = 20, fontname = "Times New Roman") # Sets the label for the colorbar
            #cbar.set_ticks([1,10,100])
            cbar.set_ticklabels([round(cbar.vmin),round(np.sqrt((cbar.vmax-cbar.vmin))),round(cbar.vmax,-1)]) # Sets the colorbar tick labels
            
            # Sets the colorbar tick labels to Times New Roman
            for l in cbar.ax.yaxis.get_ticklabels():
                l.set_family("Times New Roman")

            if plot_candidates: 
                sns.scatterplot(x = x_values,y = y_values, s = 30, color = 'navy', markers = ["*"], edgecolors = 'black') # Plots the candidates as a scatterplot superimposed onto the heatmap

            ax_4.xaxis.set_major_locator(ticker.FixedLocator(Positions_Of_Color_Ticks)) # Assigns the major ticks of the x axis using the bin index values of the desired color ticks found earlier
            ax_4.yaxis.set_major_locator(ticker.FixedLocator(Positions_Of_Magnitude_Ticks_Adjusted)) # Assigns the major ticks of the y axis using the bin index values of the desired magnitude ticks found earlier
            ax_4.tick_params(which = 'major', width = 0.5, length = 1, labelsize = 20) # Sets the tick label size, length and width
            ax_4.xaxis.set_major_formatter(ticker.FixedFormatter(labels_x_axis)) # Sets the names of the major ticks of the x axis using the bin values of the desired color ticks found earlier
            ax_4.yaxis.set_major_formatter(ticker.FixedFormatter(labels_y_axis)) # Sets the name of the major ticks of the y axis using the bin values of the desired magnitude ticks found earlier
            pos = (end_index_m-(start_index_m+1)) # Finds the position of the x-axis

            plt.axhline(pos,color = 'black') # Creates the x axis line
            plt.axvline(1,color = 'black') # Creates the y axis line 

            
            ax_4.set_xlabel(r"$G_{BP} - G_{RP} - E(BP - RP)[mag]$",fontsize = 20,fontname = "Times New Roman")
            ax_4.set_ylabel(r"$G - 5log_{10}d - A_g[mag]$",fontsize = 20, fontname = "Times New Roman")
            
            #ax_4.set_xlabel(f"{Color_Measure}",fontsize = 20,fontname = "Times New Roman") # Sets the label of the x axis
            #ax_4.set_ylabel(f"{Magnitude_Measure}",fontsize = 20, fontname = "Times New Roman") # Sets the label of y axis

            for tick in ax_4.get_xticklabels(): # Changes the font of the x tick labels to Times New Roman
                tick.set_fontname("Times New Roman")
            for tick in ax_4.get_yticklabels(): # Changes the font of the y tick labels to Times New Roman
                tick.set_fontname("Times New Roman")
    
            print(start_index_c,end_index_c,start_index_m,end_index_m)
            ax_4.grid() # Plots onto the figure a grid

            Figure_4.savefig("HR_Diagram_Complete.pdf", bbox_inches = 'tight', dpi = image_resolution, facecolor = 'w') # Saves the figure
        time_interval = time.time()-start_time # Calculates the run time
        print(f"This process took: {time_interval} seconds.") # Displays the time taken to execute the program
        try:
            if filter_choice == 0:
                print("The filter applied is: ",filter_choice) # If the filter was 0 the HR diagram plot method then shows the figure and displays the filter
                plt.show()

            if filter_choice != 0:
                print("The filter applied is: ",filter_choice) # If the filter was not 0 the HR diagram plot method does not show the figure, displaying only the filter
                plt.clf()
                plt.close()
        except:
            print("Failed to produce final results. Try again")  # If the figure fails to show the HR diagram plot method displays this error message
            raise ValueError
        return time_interval,bin_resolution # The plot method returns run time and the bin resolution