from pickletools import read_unicodestring8
from tempfile import TemporaryFile
from unittest.util import strclass
import numpy as np
import time
from statistics import mean
import re
import warnings
import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns; sns.set_theme(style = 'whitegrid')
from matplotlib.colors import LogNorm,Normalize
import matplotlib.ticker as ticker
from scipy.stats import linregress
from matplotlib.pyplot import cm
plt.rcParams["figure.figsize"] = (16,9)
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
warnings.filterwarnings("ignore")
class HR_Diagram_Generator:

    def nearest_base(self,number,base):
        return base*round(number/base,1)
    
    def avg(self,num_1,num_2):
        return(float(num_1)+float(num_2))/2

    def Bin_Locator(self,DataFrame,Value,tolerance,series,zero_points):
            locator_weight = 0.00001
            early_stopping = 5
            if type(zero_points) != str:    
                zeropoint_row = zero_points[0]
                zeropoint_column = zero_points[1]
            else:
                print(zero_points)
            if Value == 0.0 and series in "columns":
                    bin_index = zeropoint_column
                    value_chosen = DataFrame.columns[zeropoint_column]
                    return int(bin_index),value_chosen
            elif Value == 0.0 and series in "rows":
                    bin_index = zeropoint_row
                    value_chosen = DataFrame.index[zeropoint_row]
                    return int(bin_index),value_chosen
            for Index in range(0,1000):
                if float(Value) != 0.0:
                    try:
                        tolerance = abs(1/Value * locator_weight)
                    except ZeroDivisionError:
                        pass
                lower_bound = Value - abs(Value*tolerance)
                upper_bound = Value + abs(Value*tolerance)
                if series in "columns":
                    for index,value in enumerate(DataFrame.columns.values):
                        if (value >= lower_bound and value < upper_bound):
                            bin_index = index
                            value_chosen = value
                            try:
                                neighbours_index = [bin_index-early_stopping,bin_index+early_stopping+1]
                                for neighbour_index in neighbours_index:
                                    neighbour = DataFrame.columns.values[neighbour_index]
                                    if abs(neighbour - Value) < abs(value_chosen-Value):
                                        bin_index = neighbour_index
                                        value_chosen = neighbour
                            except IndexError:
                                pass
                            break
                elif series in "rows":
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
                    bin_index,value_chosen
                except NameError:
                    locator_weight *= 1.1
            try:
                return(int(bin_index),value_chosen,index)
            except NameError:
                print("Cannot find bin index for ",Value,tolerance,series)
    def Extend_Table(self,DataFrame,avg_dist_in,avg_dist_col,Col_Range,Mag_Range):
        case = True
        while case:
            lower_bound_m = DataFrame.index.values[0]
            upper_bound_m = DataFrame.index.values[-1]

            lower_bound_c = DataFrame.columns.values[0]
            upper_bound_c = DataFrame.columns.values[-1]

            if abs(Mag_Range[0]) + 1 > abs(lower_bound_m):
                index_value = DataFrame.index.values[0] - avg_dist_in
                data = {key:value for key,value in zip(DataFrame.columns.values,np.zeros(len(DataFrame.columns.values),dtype = int))}
                row = pd.DataFrame(data, index = [index_value])
                frames = [row,DataFrame]
                DataFrame = pd.concat(frames, axis = 0)
            
            elif abs(Mag_Range[1]) + 1 > abs(upper_bound_m):
                index = DataFrame.index.values[-1] + avg_dist_in 
                DataFrame.loc[index] = np.zeros(len(DataFrame.columns.values), dtype = int)
            
            elif abs(Col_Range[0]) + 1  > abs(lower_bound_c):
                DataFrame.insert(0,DataFrame.columns.values[0] - avg_dist_col, 0)
        
            elif abs(Col_Range[1]) + 1 > abs(upper_bound_c):
                column_name = DataFrame.columns.values[-1] + avg_dist_col
                column_values = np.zeros(len(DataFrame.index.values), dtype = int)
                datas = {column_name:column_values}
                column = pd.DataFrame(data = datas, index = DataFrame.index.values)
                frames = [DataFrame,column]
                DataFrame = pd.concat(frames, axis = 1)
            else:
                case = False
                return DataFrame
    def Avg_Finder(self,DataFrame):
        difference_0 = []
        difference_1 = []
        for index in range(0,len(DataFrame.columns.values)):
            try:
                diff = DataFrame.columns.values[index+1] - DataFrame.columns.values[index]
                difference_0.append(diff)
            except IndexError:
                continue
        for index in range(0,len(DataFrame.index.values)):
            try:
                diff = DataFrame.index.values[index+1] - DataFrame.index.values[index]
                difference_1.append(diff)
            except IndexError:
                continue
        average_distance_columns = mean(difference_0)
        average_distance_index = mean(difference_1)
        return average_distance_columns,average_distance_index

    def __init__(self, Sectors):
        self.Sectors_DataSet_Original = pd.DataFrame()
        try:
            for Sector in Sectors:
                self.Sectors_DataSet_Original = pd.concat([self.Sectors_DataSet_Original,pd.read_csv(Sector)])
            self.Sectors_DataSet_Original.drop_duplicates(subset = ["source_id"],inplace = True)
        except:
            print("Entered in bad file paths")
    def add_Candidate_Stars(self,Candidates):
        self.Candidates_DataSet = pd.read_csv(Candidates[0])
        try:
            for index in range(1,len(Candidates)):
                Candidate_read = pd.read_csv(Candidates[index])
                self.Candidates_DataSet.set_index('source_id').join(Candidate_read.set_index('source_id'),lsuffix = 'teff_gspphot')
        except IndexError:
            print("Out_Of_Bounds")

    def get_length_Of_Sector_DataSet(self):
        return len(self.Sectors_DataSet_Original)

    def Plot_HR_Diagram_Using_Heatmap(self,Distance_Measure,Magnitude_Measure,Color_Measure,bin_resolution = "Default",Magnitude_Range = "Default",Color_Range = "Default",plot_candidates = True,filter = 0):
        
        start_time = time.time()
        self.Sectors_DataSet = self.Sectors_DataSet_Original.copy()
        Maximum_index_Sectors = len(self.Sectors_DataSet)
        self.Sectors_DataSet = self.Sectors_DataSet.iloc[:Maximum_index_Sectors-filter]
        print("The length of the Sectors DataSet is: ",len(self.Sectors_DataSet))

        if re.match("parallax",Distance_Measure[0]):
            self.Sectors_DataSet['Distance'] = 1/(self.Sectors_DataSet[Distance_Measure[0]]/1000)
            self.Sectors_DataSet['Absolute_Magnitude'] = self.Sectors_DataSet[Magnitude_Measure] - 5*np.log10(self.Sectors_DataSet.Distance/10)
           
            self.Filled_Parallax_Sectors = len(self.Sectors_DataSet[self.Sectors_DataSet.parallax.isnull() == False])
            self.Empty_Parallax_Sectors = len(self.Sectors_DataSet[self.Sectors_DataSet.parallax.isnull() == True])
            self.Missing_Parallax_Percentage_Sectors = self.Empty_Parallax_Sectors/(self.Empty_Parallax_Sectors+self.Filled_Parallax_Sectors)*100
            print(f"The percentage of the Sectors DataSet with missing parallax is {round(self.Missing_Parallax_Percentage_Sectors,3)}%")
            
        else:
            self.Sectors_DataSet.rename(columns = {Distance_Measure[0]: 'Distance'}, inplace = True)
            self.Sectors_DataSet['Absolute_Magnitude'] = self.Sectors_DataSet[Magnitude_Measure] - 5*np.log10(self.Sectors_DataSet.Distance/10)
            
            self.Filled_Distance_Sectors = len(self.Sectors_DataSet[self.Sectors_DataSet.Distance.isnull() == False])
            self.Empty_Distance_Sectors = len(self.Sectors_DataSet[self.Sectors_DataSet.Distance.isnull() == True])
            self.Missing_Distance_Percentage_Sectors = self.Empty_Distance_Sectors/(self.Empty_Distance_Sectors+self.Filled_Distance_Sectors)*100
            print(f"The percentage of the Sectors DataSet with missing distances is {round(self.Missing_Distance_Percentage_Sectors,3)}%")
            
        if re.match('parallax', Distance_Measure[1]) and plot_candidates:
            self.Candidates_DataSet['Distance'] = 1/(self.Candidates_DataSet[Distance_Measure[1]]/1000)
            self.Candidates_DataSet['Absolute_Magnitude'] = self.Candidates_DataSet[Magnitude_Measure] -5*np.log10(self.Candidates_DataSet.Distance/10)
            
            self.Filled_Parallax_Candidates = len(self.Candidates_DataSet[self.Candidates_DataSet.parallax.isnull() == False])
            self.Empty_Parallax_Candidates = len(self.Candidates_DataSet[self.Candidates_DataSet.parallax.isnull() == True])
            self.Missing_Parallax_Percentage_Candidates = self.Empty_Parallax_Candidates/(self.Empty_Parallax_Candidates+self.Filled_Parallax_Candidates)*100
            print(f"The percentage of the Candidates DataSet with missing parallax is {round(self.Missing_Parallax_Percentage_Candidates,3)}%")

        elif plot_candidates:
            self.Candidates_DataSet.rename(columns = {Distance_Measure[1]:'Distance'}, inplace = True)
            self.Candidates_DataSet['Absolute_Magnitude'] = self.Candidates_DataSet[Magnitude_Measure] -5*np.log10(self.Candidates_DataSet.Distance/10)
            
            self.Filled_Distance_Candidates = len(self.Candidates_DataSet[self.Candidates_DataSet.Distance.isnull() == False])
            self.Empty_Distance_Candidates = len(self.Candidates_DataSet[self.Candidates_DataSet.Distance.isnull() == True])
            self.Missing_Distance_Percentage_Candidates = self.Empty_Distance_Candidates/(self.Empty_Distance_Candidates+self.Filled_Distance_Candidates)*100
            print(f"The percentage of the Candidates DataSet with missing distances is {round(self.Missing_Distance_Percentage_Candidates,3)}%") 
        
        if plot_candidates:
            self.Candidates_DataSet.drop_duplicates(subset = 'Absolute_Magnitude',inplace = True)

            self.Filled_Colors_Candidates = len(self.Candidates_DataSet[self.Candidates_DataSet.bp_rp.isnull() == False])
            self.Empty_Colors_Candidates = len(self.Candidates_DataSet[self.Candidates_DataSet.bp_rp.isnull() == True])
            self.Missing_Color_Percentage_Candidates = self.Empty_Colors_Candidates/(self.Empty_Colors_Candidates+self.Filled_Colors_Candidates)*100
            print(f"The percentage of the Candidates DataSet with missing colors is {round(self.Missing_Color_Percentage_Candidates,3)}%")
        
        if type(Color_Range) == str:
                Color_Range = [self.Sectors_DataSet[Color_Measure].min(),self.Sectors_DataSet[Color_Measure].max(),0.5]
        if type(Magnitude_Range) == str:
                Magnitude_Range = [self.Sectors_DataSet[Magnitude_Measure].min(),self.Sectors_DataSet[Magnitude_Measure].max(),0.5]
        
        print("The Color_Range and Magnitude_Range are: " ,Color_Range,Magnitude_Range)  
        
        self.Filled_Colors_Sectors = len(self.Sectors_DataSet[self.Sectors_DataSet.bp_rp.isnull() == False])
        self.Empty_Colors_Sectors = len(self.Sectors_DataSet[self.Sectors_DataSet.bp_rp.isnull() == True])
        self.Missing_Color_Percentage_Sectors = self.Empty_Colors_Sectors/(self.Empty_Colors_Sectors+self.Filled_Colors_Sectors)*100
        print(f"The percentage of the Sectors DataSet with missing colors is {round(self.Missing_Color_Percentage_Sectors,3)}%")
        
        if re.match("parallax",Distance_Measure[0]):
            A = self.Sectors_DataSet[self.Sectors_DataSet.bp_rp.isnull() == True]
            B = A[A.parallax.isnull() == True]
            self.Missing_Data_Percentage_Sectors = ((self.Empty_Parallax_Sectors+self.Empty_Colors_Sectors)-len(B))/len(self.Sectors_DataSet)*100
            print(f"The percentage of the Sectors DataSet that will be missing from the HR_Diagram is {round(self.Missing_Data_Percentage_Sectors,3)}%")
        else:
            A = self.Sectors_DataSet[self.Sectors_DataSet.bp_rp.isnull() == True]
            B = A[A.Distance.isnull() == True]
            self.Missing_Data_Percentage_Sectors = ((self.Empty_Distance_Sectors+self.Empty_Colors_Sectors)-len(B))/len(self.Sectors_DataSet)*100
            print(f"The percentage of the Sectors DataSet that will be missing from the HR_Diagram is {round(self.Missing_Data_Percentage_Sectors,3)}%")
        
        if plot_candidates and  re.match("parallax",Distance_Measure[1]):
            A = self.Candidates_DataSet[self.Candidates_DataSet.bp_rp.isnull() == True]
            B = A[A.parallax.isnull() == True]
            self.Missing_Data_Percentage_Candidates = ((self.Empty_Parallax_Candidates+self.Empty_Colors_Candidates)-len(B))/len(self.Candidates_DataSet)*100
            print(f"The percentage of the Candidates DataSet that will be missing from the HR_Diagram is {round(self.Missing_Data_Percentage_Candidates,3)}%")
        elif plot_candidates:
            A = self.Candidates_DataSet[self.Candidates_DataSet.bp_rp.isnull() == True]
            B = A[A.Distance.isnull() == True]
            self.Missing_Data_Percentage_Candidates = ((self.Empty_Distance_Candidates+self.Empty_Colors_Candidates)-len(B))/len(self.Candidates_DataSet)*100
            print(f"The percentage of the Candidates DataSet that will be missing from the HR_Diagram is {round(self.Missing_Data_Percentage_Candidates,3)}%")
        
        if type(bin_resolution) == str:
            bin_resolution = 0.0009*len(self.Sectors_DataSet)+1000

        self.Sectors_DataSet['CatAbsMag'] = pd.cut(self.Sectors_DataSet.Absolute_Magnitude,bins = bin_resolution, ordered = True)
        self.Sectors_DataSet['CatColor'] = pd.cut(self.Sectors_DataSet[Color_Measure],bins = bin_resolution, ordered = True)

        lists = []
        for interval in self.Sectors_DataSet.CatColor.cat.categories:
            list_element = re.sub(r'[][()]+','',str(interval)).replace(","," ").split()
            lists.append(float(list_element[0]))
            lists.append(float(list_element[1]))
        data = {'row':lists}
        Lister = pd.DataFrame(data)
        Lister.drop_duplicates(inplace = True)
        bins_Color = [getattr(row,'row') for row in Lister.itertuples()]

        lists = []
        for interval in self.Sectors_DataSet.CatAbsMag.cat.categories:
            list_element = re.sub(r'[][()]+','',str(interval)).replace(","," ").split()
            lists.append(float(list_element[0]))
            lists.append(float(list_element[1]))

        data = {'row':lists}
        Lister = pd.DataFrame(data)
        Lister.drop_duplicates(inplace = True)
        bins_CatsAbsMag = [getattr(row,'row') for row in Lister.itertuples()]

        if plot_candidates:
            self.Candidates_DataSet['CatColor'] = pd.cut(self.Candidates_DataSet[Color_Measure],bins = bins_Color,ordered = True)
            self.Candidates_DataSet['CatAbsMag'] = pd.cut(self.Candidates_DataSet.Absolute_Magnitude,bins = bins_CatsAbsMag, ordered = True)
        
        self.Reduced_Sectors_DataSet = self.Sectors_DataSet[['CatColor','CatAbsMag']]
        self.Reduced_Sectors_DataSet_Fqt = pd.crosstab(index = self.Reduced_Sectors_DataSet.CatAbsMag,columns = self.Reduced_Sectors_DataSet.CatColor,dropna = False)
        self.Reduced_Sectors_DataSet_Fqt = self.Reduced_Sectors_DataSet_Fqt.rename(columns = lambda x: float(self.avg(re.sub(r'[][()]+','',str(x)).replace(","," ").split()[0],re.sub(r'[][()]+','',str(x)).replace(","," ").split()[1])))
        self.Reduced_Sectors_DataSet_Fqt = self.Reduced_Sectors_DataSet_Fqt.rename(index = lambda x: float(self.avg(re.sub(r'[][()]+','',str(x)).replace(","," ").split()[0],re.sub(r'[][()]+','',str(x)).replace(","," ").split()[1])))
        self.Reduced_Sectors_DataSet_Fqt = self.Reduced_Sectors_DataSet_Fqt.fillna(0)
        
        if plot_candidates:
            self.Reduced_Candidates_DataSet = self.Candidates_DataSet[["CatColor","CatAbsMag"]]
            self.Reduced_Candidates_Fqt = pd.crosstab(index = self.Reduced_Candidates_DataSet.CatAbsMag,columns = self.Reduced_Candidates_DataSet.CatColor, dropna = False)
            self.Reduced_Candidates_Fqt = self.Reduced_Candidates_Fqt.rename(columns = lambda x: float(self.avg(re.sub(r'[][()]+','',str(x)).replace(","," ").split()[0],re.sub(r'[][()]+','',str(x)).replace(","," ").split()[1])))
            self.Reduced_Candidates_Fqt = self.Reduced_Candidates_Fqt.rename(index = lambda x: float(self.avg(re.sub(r'[][()]+','',str(x)).replace(","," ").split()[0],re.sub(r'[][()]+','',str(x)).replace(","," ").split()[1])))
            self.Reduced_Candidates_Fqt = self.Reduced_Candidates_Fqt.fillna(0)
        
        avg_dist_col_sector,avg_dist_in_sector = self.Avg_Finder(self.Reduced_Sectors_DataSet_Fqt)
        avg_dist_col_candidates,avg_dist_in_candidates = self.Avg_Finder(self.Reduced_Sectors_DataSet_Fqt)
        Sector_Norm = self.Extend_Table(self.Reduced_Sectors_DataSet_Fqt,avg_dist_in_sector,avg_dist_col_sector,Color_Range,Magnitude_Range)
        if plot_candidates:
            Candidates_Norm = self.Extend_Table(self.Reduced_Candidates_Fqt,avg_dist_in_candidates,avg_dist_col_candidates,Color_Range,Magnitude_Range)

        self.Reduced_Sectors_DataSet_Fqt = Sector_Norm.copy()
        if plot_candidates:    
            self.Reduced_Candidates_Fqt = Candidates_Norm.copy()
        
        value_drop_row,value_drop_column = 0.009,0.009
        comparison_row,comparison_column = 0.01,0.01
        value_chosen_row = 10
        value_chosen_column = 10
        for incrementor in range(0,100):
            for index,value in enumerate(self.Reduced_Sectors_DataSet_Fqt.index.values):
                if abs(value) < abs(value_drop_row):
                    zeropoint_row = index
                    value_chosen_row = value
            try:
                if abs(value_chosen_row) < abs(comparison_row):
                    comparison_row = value_chosen_row
                    value_drop_row = value_chosen_row
            except:
                pass
        
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

        
        self.padding_start_m = -0.1
        self.padding_end_m = 0.1

        self.padding_start_c = 0.0
        self.padding_end_c = 0.02

        start_m = Magnitude_Range[0]+self.padding_start_m
        end_m = Magnitude_Range[1]+self.padding_end_m

        start_c = Color_Range[0]+self.padding_start_c
        end_c = Color_Range[1]+self.padding_end_c

        start_index_m = self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt,start_m,0.02,"rows",zero_points)[0]
        end_index_m = self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt,end_m,0.008,"rows",zero_points)[0]
        start_index_c = self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt,start_c,0.008,"columns",zero_points)[0]
        end_index_c = self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt,end_c,0.001,"columns",zero_points)[0]
            
        self.Reduced_Sectors_DataSet_Fqt_Cut = self.Reduced_Sectors_DataSet_Fqt.iloc[start_index_m:end_index_m+1,start_index_c:end_index_c+1]
        if plot_candidates:
            print(self.Reduced_Candidates_DataSet.shape)
            self.Reduced_Candidates_Fqt_Cut = self.Reduced_Candidates_Fqt.iloc[start_index_m:end_index_m+1,start_index_c:end_index_c+1]
            
            for index in range(0,len(self.Reduced_Candidates_Fqt_Cut.index.values)):
                self.Reduced_Candidates_Fqt_Cut.index.values[index] = index
            for index in range(0,len(self.Reduced_Candidates_Fqt_Cut.columns.values)):
                self.Reduced_Candidates_Fqt_Cut.columns.values[index] = index
        
        value_drop_row,value_drop_column = 0.1,0.1
        comparison_row,comparison_column = 0.1,0.1
        value_chosen_row = 10
        value_chosen_column = 10

        for incremator in range(0,100):
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
        Color_Range = np.arange(Color_Range[0],Color_Range[1]+0.5,Color_Range[2])
        
        Positions_Of_Color_Ticks = []
        for Color in Color_Range:
            try:
                Positions_Of_Color_Ticks.append(self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt_Cut,Color,tolerance,"columns",zero_points)[0])
            except:
                print("Could not find color ",self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt_Cut,Color,tolerance,"columns",zero_points))
        print("Colour Range: ",Color_Range)
        for position in Positions_Of_Color_Ticks:
            print(self.Reduced_Sectors_DataSet_Fqt_Cut.columns[position])
        Magnitudes_Range = np.arange(Magnitude_Range[0],Magnitude_Range[1]+0.5,Magnitude_Range[2])

        Positions_Of_Magnitude_Ticks = []
        for Magnitude in Magnitudes_Range:
            try:
                Positions_Of_Magnitude_Ticks.append(self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt_Cut,Magnitude,tolerance,"rows",zero_points)[0])
            except:
                print("Could not find Magnitude value: ",self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt_Cut,Magnitude,tolerance,"rows",zero_points))
        print("Magnitude Range: ",Magnitudes_Range)
        if plot_candidates:
            self.Candidates_DataSet.dropna(subset = ["CatColor","CatAbsMag"],inplace = True)
            mapping_tool_rows = {key:value for key,value in zip(self.Reduced_Sectors_DataSet_Fqt_Cut.index.values,self.Reduced_Candidates_Fqt_Cut.index.values)}
            mapping_tool_columns = {key:value for key,value in zip(self.Reduced_Sectors_DataSet_Fqt_Cut,self.Reduced_Candidates_Fqt_Cut)}

            x_values = []
            for index,string in enumerate(self.Candidates_DataSet.CatColor):
                try:
                    list_element = self.avg(re.sub(r'[][()]+','',str(string)).replace(","," ").split()[0],re.sub(r'[][()]+','',str(string)).replace(","," ").split()[1])
                    x_value = mapping_tool_columns.get(float(list_element))
                    x_values.append(x_value)
                except IndexError:
                    print(index,string)

            y_values = []
            for index,string in enumerate(self.Candidates_DataSet.CatAbsMag):
                try:
                    list_element = self.avg(re.sub(r'[][()]+','',str(string)).replace(","," ").split()[0],re.sub(r'[][()]+','',str(string)).replace(","," ").split()[1])
                    y_values.append(mapping_tool_rows.get(float(list_element)))
                except IndexError:
                    print(index,string)
        
        labels_x_axis = []
        for label_index in Positions_Of_Color_Ticks:
            element = round(self.Reduced_Sectors_DataSet_Fqt_Cut.columns[label_index],1)
            if abs(element) == 0.0:
                element = abs(element)
            labels_x_axis.append(element)

        labels_y_axis = []
        temp = []
        for label_index in Positions_Of_Magnitude_Ticks:
            element = round(self.Reduced_Sectors_DataSet_Fqt_Cut.index[label_index],1)
            if element.is_integer() and element % 2 == 0:
                if abs(element) == 0.0:
                    element = abs(element)
                labels_y_axis.append(int(element))
                temp.append(label_index)
        
        if plot_candidates:
            print("The candidate coordinates are: ",x_values,y_values)

        Positions_Of_Magnitude_Ticks_Adjusted = temp

        if plot_candidates:
            Figure_1= plt.figure()
            ax_1 = sns.scatterplot(x = Color_Measure, y = 'Absolute_Magnitude', data = self.Candidates_DataSet)
            ax_1.set_xlabel(f"GAIA {Color_Measure} Color")
            ax_1.set_ylabel("Absolute_Magnitude")
            ax_1.invert_yaxis()
            Figure_1.savefig('HR_Candidate_Raw_Scatter_Plot.jpg', bbox_inches='tight', dpi=400)
            plt.clf()
            plt.close()
            try:
                Figure_2 = plt.figure()
                norm = LogNorm(self.Candidates_DataSet["rv_amplitude_robust"].min(),self.Candidates_DataSet['rv_amplitude_robust'].max())
                ax_2 = sns.scatterplot(x = 'bp_rp',y = 'Absolute_Magnitude', hue = 'rv_amplitude_robust', hue_norm = norm, data = self.Candidates_DataSet, style = 'non_single_star',markers = {0:'o',1:'s',2:'^',3:'*'},alpha = 0.9, legend = 'brief')
                ax_2.invert_yaxis()
                sm = cm.ScalarMappable(cmap = 'rocket_r', norm = norm)
                sns.color_palette('flare', as_cmap = True)
                sm.set_array([])
                ax_2.figure.colorbar(sm,label = "Log Radial Velocities(Kms)")
                handles, _ = ax_2.get_legend_handles_labels()
                ax_2.legend(handles[4:],['Single_Star','Astrometric Binary','Ecplising Binary','Spectroscopic Binary'])
                ax_2.set_xlabel('GAIA Bp_Rp Color')
                ax_2.set_ylabel('Absolute_Magnitude')
                Figure_2.savefig('HR_Candidate_Radial_Plot.jpg', bbox_inches='tight', dpi=400)
                plt.clf()
                plt.close()
            except NameError:
                print("No column called rv_amplitude_robust in dataset provided, thus no HR_Diagram_Radial_Plot has been produced")

            try:
                mask = ~np.isnan(self.Candidates_DataSet[Color_Measure]) & ~np.isnan(self.Candidates_DataSet['Absolute_Magnitude'])
                x = self.Candidates_DataSet[Color_Measure]
                y = self.Candidates_DataSet['Absolute_Magnitude']
                m,c,r_value,p_value,std_error = linregress(x[mask],y[mask])
                print(f"A linear fit has been drawn to the HR Diagram. The gradient is {round(m,2)}, the intercept is {round(c,2)}.")
                print(f"The r_value is {round(r_value,2)}, the p_value is {round(p_value,2)}, the standard error is {round(std_error,2)}.")

                Figure_3= plt.figure()
                norm = LogNorm(self.Candidates_DataSet["rv_amplitude_robust"].min(),self.Candidates_DataSet['rv_amplitude_robust'].max())
                ax_3 = sns.scatterplot(x = Color_Measure,y = 'Absolute_Magnitude', hue = 'rv_amplitude_robust', hue_norm = norm, data = self.Candidates_DataSet, style = 'non_single_star',markers = {0:'o',1:'s',2:'^',3:'*'},alpha = 0.9, legend = 'brief')
                plt.plot(self.Candidates_DataSet[Color_Measure],m*self.Candidates_DataSet[Color_Measure]+c)
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
            except:
                print("No column called rv_amplitude_robust in dataset provided, thus no HR_Diagram_Radial_Plot has been produced")
                
        self.Reduced_Sectors_DataSet_Fqt_Cut = self.Reduced_Sectors_DataSet_Fqt_Cut.rename(columns = lambda x: self.nearest_base(x,1))
        self.Reduced_Sectors_Data = self.Reduced_Sectors_DataSet_Fqt_Cut.rename(index = lambda x: self.nearest_base(x,1))

        Figure_4 = plt.figure()
        ax_4 = sns.heatmap(self.Reduced_Sectors_DataSet_Fqt_Cut,norm = LogNorm(),cmap = 'rocket', cbar_kws = {'label': 'Number Density','pad':0.01}, linewidths = 0)
        plt.rc('font',size = 30)
        cbar = ax_4.collections[0].colorbar

        cbar.ax.get_yaxis().set_ticks([cbar.vmin,np.sqrt((cbar.vmax-cbar.vmin)),cbar.vmax])
        cbar.ax.tick_params(labelsize = 20)
        cbar.set_label(label = "Number Density", fontsize = 20, fontname = "Times New Roman")
        #cbar.set_ticks([1,10,100])
        cbar.set_ticklabels([round(cbar.vmin),round(np.sqrt((cbar.vmax-cbar.vmin))),round(cbar.vmax)])

        for l in cbar.ax.yaxis.get_ticklabels():
            l.set_family("Times New Roman")

        if plot_candidates:
            sns.scatterplot(x = x_values,y = y_values, s = 30, color = 'navy', markers = ["*"], edgecolors = 'black')

        ax_4.xaxis.set_major_locator(ticker.FixedLocator(Positions_Of_Color_Ticks))
        ax_4.yaxis.set_major_locator(ticker.FixedLocator(Positions_Of_Magnitude_Ticks_Adjusted))
        ax_4.tick_params(which = 'major', width = 0.5, length = 1, labelsize = 20)
        ax_4.xaxis.set_major_formatter(ticker.FixedFormatter(labels_x_axis))
        ax_4.yaxis.set_major_formatter(ticker.FixedFormatter(labels_y_axis))
        pos = (end_index_m-(start_index_m+1))

        plt.axhline(pos,color = 'black')
        plt.axvline(1,color = 'black')
        ax_4.set_xlabel(r"$G_{BP} - G_{RP}$",fontsize = 20,fontname = "Times New Roman")
        ax_4.set_ylabel(r"$M_{G}$",fontsize = 20, fontname = "Times New Roman")

        for tick in ax_4.get_xticklabels():
            tick.set_fontname("Times New Roman")
        for tick in ax_4.get_yticklabels():
            tick.set_fontname("Times New Roman")
    
        print(start_index_c,end_index_c,start_index_m,end_index_m)
        plt.grid()

        Figure_4.savefig("HR_Diagram.png", bbox_inches = 'tight', dpi = 400, facecolor = 'w')
        time_interval = time.time()-start_time
        print("This process took: ",time_interval)

        if filter == 0:
            print("The filter applied is: ",filter)
            plt.show()

        if filter != 0:
            print("The filter applied is: ",filter)
            plt.clf()
            plt.close()
            return time_interval