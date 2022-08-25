import numpy as np
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
        zeropoint_row = zero_points[0]
        zeropoint_column = zero_points[1]
        if float(Value) != 0.0:
            try:
                tolerance = abs(1/Value * 0.01)
            except ZeroDivisionError:
                pass
        lower_bound = Value - abs(Value*tolerance)
        upper_bound = Value + abs(Value*tolerance)
        if Value == 0.0 and series in "columns":
            bin_index = zeropoint_column
            value_chosen = DataFrame.columns[zeropoint_column]
        elif Value == 0.0 and series in "rows":
            bin_index = zeropoint_row
            value_chosen = DataFrame.index[zeropoint_row]
        elif series in "columns":
            for index,value in enumerate(DataFrame.columns.values):
                if (value >= lower_bound and value < upper_bound):
                    bin_index = index
                    value_chosen = value
                    break
        elif series in "rows":
            for index,value in enumerate(DataFrame.index.values):
                if (value >= lower_bound and value < upper_bound):
                    bin_index = index
                    value_chosen = value
                    break
        try:
            return(int(bin_index),value_chosen)
        except:
            return print("Bin_index cannot found",value,Value,tolerance,series)
    
    def __init__(self, *Sectors):
        self.Sectors_DataSet = pd.DataFrame()
        for Sector in Sectors:
            self.Sectors_DataSet = pd.concat([self.Sectors_DataSet,pd.read_csv(Sector)])

    def add_Candidate_Stars(self,*Candidates):
        self.Candidates_DataSet = pd.read_csv(Candidates[0])
        try:
            for index in range(1,len(Candidates)):
                Candidate_read = pd.read_csv(Candidates[index])
                self.Candidates_DataSet.set_index('source_id').join(Candidate_read.set_index('source_id'),lsuffix = 'teff_gspphot')
        except IndexError:
            print("Out_Of_Bounds")

    def Plot_HR_Diagram_Using_Heatmap(self,Distance_Measure,Magnitude_Measure,Color_Measure,Magnitude_Range,Color_Range,bin_resolution,plot_candidates = True):
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

        self.Candidates_DataSet['CatColor'] = pd.cut(self.Candidates_DataSet[Color_Measure],bins = bins_Color,ordered = True)
        self.Candidates_DataSet['CatAbsMag'] = pd.cut(self.Candidates_DataSet.Absolute_Magnitude,bins = bins_CatsAbsMag, ordered = True)
        
        self.Reduced_Sectors_DataSet = self.Sectors_DataSet[['CatColor','CatAbsMag']]
        self.Reduced_Sectors_DataSet_Fqt = pd.crosstab(index = self.Reduced_Sectors_DataSet.CatAbsMag,columns = self.Reduced_Sectors_DataSet.CatColor,dropna = False)
        self.Reduced_Sectors_DataSet_Fqt = self.Reduced_Sectors_DataSet_Fqt.rename(columns = lambda x: float(self.avg(re.sub(r'[][()]+','',str(x)).replace(","," ").split()[0],re.sub(r'[][()]+','',str(x)).replace(","," ").split()[1])))
        self.Reduced_Sectors_DataSet_Fqt = self.Reduced_Sectors_DataSet_Fqt.rename(index = lambda x: float(self.avg(re.sub(r'[][()]+','',str(x)).replace(","," ").split()[0],re.sub(r'[][()]+','',str(x)).replace(","," ").split()[1])))
        self.Reduced_Sectors_DataSet_Fqt = self.Reduced_Sectors_DataSet_Fqt.fillna(0)

        self.Reduced_Candidates_DataSet = self.Candidates_DataSet[["CatColor","CatAbsMag"]]
        self.Reduced_Candidates_Fqt = pd.crosstab(index = self.Reduced_Candidates_DataSet.CatAbsMag,columns = self.Reduced_Candidates_DataSet.CatColor, dropna = False)
        self.Reduced_Candidates_Fqt = self.Reduced_Candidates_Fqt.rename(columns = lambda x: float(self.avg(re.sub(r'[][()]+','',str(x)).replace(","," ").split()[0],re.sub(r'[][()]+','',str(x)).replace(","," ").split()[1])))
        self.Reduced_Candidates_Fqt = self.Reduced_Candidates_Fqt.rename(index = lambda x: float(self.avg(re.sub(r'[][()]+','',str(x)).replace(","," ").split()[0],re.sub(r'[][()]+','',str(x)).replace(","," ").split()[1])))
        self.Reduced_Candidates_Fqt = self.Reduced_Candidates_Fqt.fillna(0)


        for index,value in enumerate(self.Reduced_Sectors_DataSet_Fqt.index.values):
            if abs(value) < 0.01 :
                zeropoint_row = index
        for index,value in enumerate(self.Reduced_Sectors_DataSet_Fqt.columns.values):
            if abs(value) < 0.01:
                zeropoint_column = index
        try:
            zero_points = [zeropoint_row,zeropoint_column]
        except:
            print("Zeropoints not found")

        start_index_m = self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt,Magnitude_Range[0],0.02,"rows",zero_points)[0] - 10
        end_index_m = self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt,Magnitude_Range[1],0.008,"rows",zero_points)[0] + 10
        start_index_c = self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt,Color_Range[0],0.008,"columns",zero_points)[0] -10 
        end_index_c = self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt,Color_Range[1],0.001,"columns",zero_points)[0] + 10

        self.Reduced_Sectors_DataSet_Fqt_Cut = self.Reduced_Sectors_DataSet_Fqt.iloc[start_index_m:end_index_m+1,start_index_c:end_index_c+1]
        self.Reduced_Candidates_Fqt_Cut = self.Reduced_Candidates_Fqt.iloc[start_index_m:end_index_m+1,start_index_c:end_index_c+1]
        
        for index in range(0,len(self.Reduced_Candidates_Fqt_Cut.index.values)):
            self.Reduced_Candidates_Fqt_Cut.index.values[index] = index
        for index in range(0,len(self.Reduced_Candidates_Fqt_Cut.columns.values)):
            self.Reduced_Candidates_Fqt_Cut.columns.values[index] = index
        
        for index,value in enumerate(self.Reduced_Sectors_DataSet_Fqt_Cut.index.values):
            if abs(value) < 0.01 :
                zeropoint_row = index
        for index,value in enumerate(self.Reduced_Sectors_DataSet_Fqt_Cut.columns.values):
            if abs(value) < 0.01:
                zeropoint_column = index
        try:
            zero_points = [zeropoint_row,zeropoint_column]
        except:
            print("Zeropoints not found")

        tolerance = 0.008
        Color_Range_Limits = [-0.5,5.0]
        Color_Range = np.arange(Color_Range_Limits[0],Color_Range_Limits[1],0.5)
        Positions_Of_Color_Ticks = []
        for Color in Color_Range:
            Positions_Of_Color_Ticks.append(self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt_Cut,Color,tolerance,"columns",zero_points)[0])
        
        Magnitudes_Range_Limits = [-7.0,14.5]
        Magnitudes_Range = np.arange(Magnitudes_Range_Limits[0],Magnitudes_Range_Limits[1],0.5)
        Positions_Of_Magnitude_Ticks = []
        for Magnitude in Magnitudes_Range:
            try:
                Positions_Of_Magnitude_Ticks.append(self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt_Cut,Magnitude,tolerance,"rows",zero_points)[0])
            except:
                self.Bin_Locator(self.Reduced_Sectors_DataSet_Fqt_Cut,Magnitude,tolerance,"rows",zero_points)

        
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
        
        print(x_values,y_values)
        labels_x_axis = []
        temp = []
        for label_index in Positions_Of_Color_Ticks:
            element = round(self.Reduced_Sectors_DataSet_Fqt_Cut.columns[label_index],1)
            labels_x_axis.append(element)


        labels_y_axis = []
        temp = []
        for label_index in Positions_Of_Magnitude_Ticks:
            element = round(self.Reduced_Sectors_DataSet_Fqt_Cut.index[label_index],1)
            if element.is_integer() and element % 2 ==0:
                labels_y_axis.append(element)
                temp.append(label_index)

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
            Figure_4 = plt.Figure()
            ax_4 = sns.heatmap(self.Reduced_Sectors_DataSet_Fqt_Cut, linewidths = 0, norm = LogNorm(), cmap = 'rocket', cbar_kws = {'label': 'Number Density'})
            sns.scatterplot(x = x_values,y = y_values, s = 30, color = 'navy', markers = ["*"], edgecolors = 'black')
            ax_4.xaxis.set_major_locator(ticker.FixedLocator(Positions_Of_Color_Ticks))
            ax_4.yaxis.set_major_locator(ticker.FixedLocator(Positions_Of_Magnitude_Ticks_Adjusted))
            ax_4.tick_params(which = 'major', width = 0.5, length = 1)
            ax_4.xaxis.set_major_formatter(ticker.FixedFormatter(labels_x_axis))
            ax_4.yaxis.set_major_formatter(ticker.FixedFormatter(labels_y_axis))
            pos = (end_index_m-(start_index_m+2))
            plt.axhline(pos,color = 'black')
            plt.axvline(1,color = 'black')
            ax_4.set_xlabel("Gaia BP_RP Colour")
            ax_4.set_ylabel("Gaia G Absolute Magnitude")
            print(start_index_c,end_index_c,start_index_m,end_index_m)
            plt.grid()
            Figure_4.savefig("HR_Diagram.png", bbox_inches = 'tight', dpi = 400, facecolor = 'w')
            plt.show()