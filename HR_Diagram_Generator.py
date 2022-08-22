import numpy as np
import re
import math
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns; sns.set_theme(style = 'whitegrid')
from matplotlib.colors import LogNorm

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
class HR_Diagram_Generator:

    def nearest_five(self,number,base):
        return base*round(number/base,1)

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
        else:
            self.Sectors_DataSet.rename(columns = {Distance_Measure[0]: 'Distance'}, inplace = True)
            self.Sectors_DataSet['Absolute_Magnitude'] = self.Sectors_DataSet[Magnitude_Measure] - 5*np.log10(self.Sectors_DataSet.Distance/10)
        
        if re.match('parallax', Distance_Measure[1]):
            self.Candidates_DataSet['Distance'] = 1/(self.Candidates_DataSet[Distance_Measure[1]]/1000)
            self.Candidates_DataSet['Absolute_Magnitude'] = self.Candidates_DataSet[Magnitude_Measure] -5*np.log10(self.Candidates_DataSet.Distance/10)
        else:
            self.Candidates_DataSet.rename(columns = {Distance_Measure[1]:'Distance'}, inplace = True)
            self.Candidates_DataSet['Absolute_Magnitude'] = self.Candidates_DataSet[Magnitude_Measure] -5*np.log10(self.Candidates_DataSet.Distance/10)

        self.Candidates_DataSet.drop_duplicates(subset = 'Absolute_Magnitude',inplace = True)
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
        self.Reduced_Sectors_DataSet_Fq = pd.crosstab(index = self.Reduced_Sectors_DataSet.CatAbsMag,columns = self.Reduced_Sectors_DataSet.CatColor,dropna = False)
        self.Reduced_Sectors_DataSet_Fq = self.Reduced_Sectors_DataSet_Fq.rename(columns =  lambda x: float(re.sub(r'[][()]+','',str(x)).replace(","," ").split()[0]))
        self.Reduced_Sectors_DataSet_Fq = self.Reduced_Sectors_DataSet_Fq.rename(index = lambda x: float(re.sub(r'[][()]+','',str(x)).replace(","," ").split()[0]))
        self.Reduced_Sectors_DataSet_Fq = self.Reduced_Sectors_DataSet_Fq.fillna(0)

        self.Reduced_Candidates_DataSet = self.Candidates_DataSet[["CatColor","CatAbsMag"]]
        self.Reduced_Candidates_Norm = pd.crosstab(index = self.Reduced_Candidates_DataSet.CatAbsMag,columns = self.Reduced_Candidates_DataSet.CatColor, dropna = False)
        self.Reduced_Candidates_Norm = self.Reduced_Candidates_Norm.rename(columns = lambda x: float(re.sub(r'[][()]+','',str(x)).replace(","," ").split()[0]))
        self.Reduced_Candidates_Norm = self.Reduced_Candidates_Norm.rename(index = lambda x: float(re.sub(r'[][()]+','',str(x)).replace(","," ").split()[0]))
        self.Reduced_Candidates_Norm = self.Reduced_Candidates_Norm.fillna(0)

        for index,Magnitude in enumerate(self.Reduced_Sectors_DataSet_Fq.columns.values):
            if round(Magnitude) == math.ceil(Magnitude_Range[0]):
                start_index_m = index
            if round(Magnitude) == math.ceil(Magnitude_Range[1]):
                end_index_m = index
        
        for index,Color in enumerate(self.Reduced_Sectors_DataSet_Fq.index.values):
            if round(Color) == math.ceil(Color_Range[0]):
                start_index_c = index
            if round(Color) == math.ceil(Color_Range[1]):
                end_index_c = index
        
        self.Reduced_Sectors_DataSet_Fq_Cut = self.Reduced_Sectors_DataSet_Fq.iloc[start_index_c:end_index_c,start_index_m:end_index_m]
        self.Reduced_Candidates_Norm_Cut = self.Reduced_Candidates_Norm.iloc[start_index_c:end_index_c,start_index_m:end_index_m]
        
        for index in range(0,len(self.Reduced_Candidates_Norm_Cut.index.values)):
            self.Reduced_Candidates_Norm_Cut.index.values[index] = index

        for index in range(0,len(self.Reduced_Candidates_Norm_Cut.columns.values)):
            self.Reduced_Candidates_Norm_Cut.columns.values[index] = index
        
        mapping_tool_indices = {key:value for key,value in zip(self.Reduced_Sectors_DataSet_Fq_Cut.index.values,self.Reduced_Candidates_Norm_Cut.index.values)}
        mapping_tool_columns = {key:value for key,value in zip(self.Reduced_Sectors_DataSet_Fq_Cut,self.Reduced_Candidates_Norm_Cut)}

        x_values = []
        for index,string in enumerate(self.Candidates_DataSet.CatColor):
            list_element = re.sub(r'[][()]+','',str(string)).replace(","," ").split()
            x_values.append(mapping_tool_columns.get(float(list_element[0])))

        y_values = []
        for index,string in enumerate(self.Candidates_DataSet.CatAbsMag):
            list_element = re.sub(r'[][()]+','',str(string)).replace(","," ").split()
            y_values.append(mapping_tool_indices.get(float(list_element[0])))

        self.Reduced_Sectors_DataSet_Fq_Cut = self.Reduced_Sectors_DataSet_Fq_Cut.rename(columns = lambda x: self.nearest_five(x,5))
        self.Reduced_Sectors_DataSet_Fq_Cut = self.Reduced_Sectors_DataSet_Fq_Cut.rename(index = lambda x: self.nearest_five(x,5))

        Figure2,ax2 = plt.subplots()
        heats = sns.heatmap(self.Reduced_Sectors_DataSet_Fq_Cut, linewidths = 0, norm = LogNorm(), cmap = 'rocket', cbar_kws = {'label': 'Number Density'}, zorder = -1)
        if plot_candidates:
            sns.scatterplot(x = x_values,y = y_values, s = 2, color = 'c', markers = ["*"])
        plt.locator_params(axis = 'both', nbins = 7)
        ax2.set_xlabel("Gaia BP_RP Colour")
        ax2.set_ylabel("Gaia G Absolute Magnitude")
        plt.savefig("HR_Diagram.pdf", bbox_inches = 'tight', dpi = 400, facecolor = 'w')
        plt.show()
