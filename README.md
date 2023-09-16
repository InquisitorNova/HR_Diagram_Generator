# HR_Diagram_Generator
The HR diagram is a small python project used to quickly produce HR diagrams. This readme will explain in detail the process I used to for obtaining the data I used to produce the images in the blog. A guide for how to use the HR diagram generator is then provided.
## The data required for this program to run
The HR diagram generator produces an observational Hertzpsrung Russell Diagram, a scatterplot of a stars' absolute magnitude vs it's colour. To produce the scatterplot it converts apparent magnitude values into absolute magnitudes and then plots this against the colour. For the function to work it requires a dataset in csv form containing a distance measure either a parallax column in mili arcseconds (mas) or distance column in parsecs. It also requires a column containing the apparent magnitude measure say photometric g band values. Finally it requires a column containing a colour index, say the Gaia BP RP colour index. The program then asks for adjustment details, the ranges of the x and y axis, the increments etc. Additional information on this is provided below.
## Obtaining the Data
First, we need to obtain the TIC ids for the stars of the northern and southern ecliptic hemisphere that are observed by TESS. This is achieved by going to the MAST, 
Mikulski Archive for Space Telescopes, archive of TESS light curves from full frame Images or "TESS-SPOC". SPOC refers to the TESS Science Processing Operations 
Centre (SPOC) a pipeline which is used to generate target pixel files, light curves, calibrate the full-frame images and associated products.

![image](https://user-images.githubusercontent.com/97238126/193291717-8007b0e9-c8e2-4bd6-b833-311693743eea.png)*Light Curve Data, Target Pixel Files, Target List Data and associated products produced by TESS-SPOC for Years 1 (Sectors 1-13) and Years 2 (Sectors 14-26) TESS Data.*

Scrolling down the page the webpage includes the target lists for sectors 1-55 and are tabulated in the years of the TESS mission. Years 1,2 and 3 are complete hence 
the full list of sectors for those years, while year 4 has began and hence has an incomplete list of sectors. For Sectors 1-55 we download Target List csv files 
download into our local drive by clicking on the link attached to the target list. For clarity I have separated the data into the folders Northern Hemisphere year 2 
and year 4 as well as the Southern Hemisphere year 1 and year 3. 

![image](https://user-images.githubusercontent.com/97238126/193293224-6d9a2383-ed52-43d4-b6cf-307c892ce047.png)
 *The image above shows the contents of the sector 1 target list csv file. The first column is the TIC id with the second and third column giving the position of the star in the night sky using the right ascension (RA J2000 deg) and the declination (Dec J200 deg) coordinate system. This target list now provides us with two options for obtaining the data.*

Firstly, since the TESS Input Catalogue is derived from GAIADR2, we could make a direct conversion from tic ids to GAIADR2 ids. This would require access to the TICv8 such that you could make a bulk request to convert the values. Another problem is that it would return GAIADR2 ids which would potentially limit our search of the GAIA archive to DR2 values as GAIADR3 and GAIADR2 source ids do not necessarily match for a star. Direct access to the TICv8 Catalogue is not an option for everyone,(I was able to access the TICv8 catalogue through my institution) in which case it is best to use the second method.
The second method is to feed the RA and Dec values directly into the GAIA archive and request the archive to perform a cross match, i.e. look for stars in the nearby proximity of the position specified. Performing this basic cone search GAIA then returns the closest star to that position. The main problem here is that the high proper motion stars in the target list will have moved out of the specified position. The archive will then return no match. Furthermore, for a particularly dense part of the sky the GAIA archive may mismatch the star, returning a star outside of the target list. A more advanced cone search can correct for these issues by feeding information about a stars proper motion RA and Dec values, as well as it’s radial velocity, however for our purposes it will be sufficient to stick to a basic cone search and restrict the region of sky, the cone radius to a few arcseconds.
To obtain the GAIA DR3 data from the GAIA archive, we must first setup an GAIA archive account so that we can upload user tables onto the archive. To do this go to the Gaia user account registration page and follow the instructions. Once an account has been set up go to the Gaia archive home page then clicked search then advanced. 

![image](https://user-images.githubusercontent.com/97238126/193302683-7e37e073-3a86-492b-8c6c-cc10f7f5d38f.png) *A screenshot of the Gaia archive search advanced page. Gaia makes use of Astronomical Data Query Language (ADQL) a language similar to Structured Query Language (SQL) to structure and query the database. Image taken from the [Gaia Archive](https://gea.esac.esa.int/archive/)

The screenshot above is that of the advanced menu of the Gaia archive. The textbox is used to enter ADQL commands, which are then executed by pressing the submit query button. Once submitted the Gaia archive will then query the database and return the results as entry in the job table below the textbox. To the left are a list of the names tables in the archive and the list of their column names. To upload the target lists into the Gaia archive, click on the upload button represented by image of the database with an up arrow in the top left corner of the screen.

![image](https://user-images.githubusercontent.com/97238126/193303045-8070927d-54ab-45d9-926a-38681e92389c.png) *A screenshot showing the Gaia catalogue upload menu. Image taken from the [Gaia Archive](https://gea.esac.esa.int/archive/)*

On the Catalogue menu enter the name of the sector and use the choose file button to select the file from the local drive, change the file format to to csv and then press upload to transfer create a copy to the Gaia archive. The Gaia archive will refresh and the sector target list will now appear in the user table at the bottom left of the left panel (Find it by scrolling down). Repeat this process till all the sectors are uploaded into the Gaia archive. 

In the left panel scroll down to the user tables at the bottom. Click on the plus sign to extend the view to show all tables. Click on the checkbox of the target list table. A tick should now appear. Then click on the table icon in the left panel to reveal the Gaia table editor.

![Screenshot 2022-09-30 163935](https://user-images.githubusercontent.com/97238126/193306966-cd9d8417-bd16-4d1e-a5d8-a7481133bcc1.png) *A screenshot showing the Gaia catalogue table editor. Image taken from the [Gaia Archive](https://gea.esac.esa.int/archive/)*

Change the flags of the ra and dec values to RA and DEC respectively and press the update button. The symbol of the table should now change to indicate that Gaia treats the table as giving position data.

To obtain the data for each star we first need to perform a cross match between the target list csv file now uploaded to the Gaia archive and the gaia data release 3, gaiadr3.gaia_source. This is to obtain the gaiadr3 source ids. For those wanting to perform this operation using ADQL, the Gaia archive provides documentation in the help section of the Gaia archive homepage on how to perform this. For those unfamiliar with ADQL, Gaia provides either premade common cross matches in the “Cross-match” table or has a prebuilt function that will perform the cross match for you. We will be using the prebuilt function as it is the simplest approach.

![Screenshot 2022-09-30 163116](https://user-images.githubusercontent.com/97238126/193305180-a0ce80c0-99a1-4841-85f0-9f66425cb6db.png) *A screenshot of the Gaia Archive advanced search menu , showing the prebuilt Gaia Crossmatch function menu, Image taken from the [Gaia Archive](https://gea.esac.esa.int/archive/)*

Clicking on the double star button in the left panel of the Gaia Advanced Search menu brings up the prebuilt Gaia Archive cross match function. Change the table A to either the gaiadr3.gaia_source or gaiadr2.gaia_source depending on whether you want data from the gaiadr3 or from the gaiadr2 tables. Change the table B to the name of the user table that contains the RA and DEC values of the target ids. Then click execute. The left panel will refresh and the cross match will now appear as a user table with a star icon. Open the table editor using the instructions provided above. Change the name of the table and columns to a suitable name which can easily be referenced. 

Now with the gaia ids for the tic ids, we use ADQL to create queries that will search the archive and return the parallax, colour, radial velocity etc for our targets. To obtain the the data needed for HR diagram Generator the query I used is shown in the image below.

![Screenshot 2022-10-01 122444](https://user-images.githubusercontent.com/97238126/193407253-aa301bed-2594-4276-a011-69e80453fa92.png) *A screenshot of the Gaia archive advanced search menu, showing the ADQL I used to query the archive for the data used in the HR diagram. Image taken from the [Gaia Archive](https://gea.esac.esa.int/archive/)*

Typing in the code above and pressing the submit query button, executes the code. Gaia calls this execution a job. The results of the job can be accessed in the bottom panel. A job is shown as a row in the job panel. A sucessesfull job is shown by a tick in the status column wheras a failed execution is shown as a cross. Clicking on the table icon on the right hand side of the row displays the results of the search. 

To download the table, return to the Advanced(ADQL) menu, first change the download format to csv. Then move the cursor to the row the job just produced is in and click on the third icon from the right which shows a database with a downwards pointing button. The file should now start downloading. The process is repeated above to obtain Gaia dr3 data for all of the sectors. As explained earlier as the process used to obtain the gaia dr3 source ids involves the use of basic cone search using RA and DEC values there is the potential for mismatch and for missing stars. The resulting table from the ADQL query will also produce stars with missing parallax and colour values. This means that the final HR diagram will not contain the complete set of stars forming the sectors.

## Producing a HR diagram from the data obtained from the Gaia archive
Before executing the HR diagram python file a decision needs to be made whether the file paths of the csv files containing the sector information will be entered individually or as a group. If the data is be grouped, store the file paths in a text file with the files separated by new lines. The image below shows how this could be done.

![Screenshot 2022-10-01 124640](https://user-images.githubusercontent.com/97238126/193408056-d7b9d8ed-47ed-4354-8ff8-74f05ea2f5eb.png) *An image showing a txt file containing a list of file paths for the csv files containing the sector data.*

With the above decision made, the program can be executed. There are two options for running the HR diagram generator, either directly through importing the module and running it in python or from using the text based user interface HR diagram Practice. Below I outline the two approaches.

### Using the text based user interface
To produce the HR diagrams using the text based user interface, run the HR diagram Practice python files. Running the program, you will then be prompted to answer a series of questions about the data being imported in the python file. Firstly it asks whether this is your first time using the program. Typing Y, the program will return a short description of the program's function and what it requires.

The next prompt is whether the file paths for the files containing the data being used to produce the heatmap of the HR diagram are going to be uploaded individually or as a group with a single file path containing the list of file paths being entered instead. If the file path is to be entered individually, press singlefile, copy and paste the file path into the prompt, press enter and then repeat until all file paths have been entered. Once you are done type done to stop the loop. If the file path is be entered as a group, press textfile, and copy and paste the file path of the text file containing all the individual file paths of the sector data. 

The following prompt is a repeat of the previous but now for the file paths of the csv files containing the data for the candidates. If there are no candidate stars enter SingleFile and then press enter and then type done to skip this prompt. The next prompt asks fo what distance measures are being used ie whether we measure the distance to the stars in parallax or parsecs. This will be the name of the distance column obtained from the gaia archive query. Enter the distance measure for the Sector and Candidate data seperately using a comma to seperate them.

The next prompt requests the name of the apparent magnitude measure being used as a categorical measurement of the stars brightness e.g. phot_g_mean_mag. This again will be the name of the magnitude column obtained from the gaia archive query. It is assumed here that the magnitude measure will be the same for the sector and candidate stars. 

The next prompt requests the name of the colour index, a measurement that roughly corresponds with a stars temperature e.g. GAIA's bp_rp colour index. Enter name of the colour index column obtained from the gaia archive query. It is again assumed that the colour index used here is the same for the sector and candidate stars.

The program then asks for the lower bound, upper bound and interval of the magnitude. Enter the range of values you wish to appear in the final diagram and the interval of the major axis tickers. The program will ask the same for the colour values.

The prompt that follows after then asks for how many stars are be removed from the final plot. This is for filtering purposes. This is followed by a question asking for the resolution of the final png image, ( I default to 1000). 

The following prompt is used to filter out bins which have been filled with a certain number of stars, this is mainly to counter the mismatching that can occur from the basic cone search which makes the final plot quite messy. I entered the list 0,1 to ensure bins containing 0 or 1 stars were changed to contain exactly 0 stars.

The program then asks whether or not the candidate stars are to be plotted. If there are no candidate stars type N. This is followed by question specifing the number of N bins that the pandas cut function will split the colour and magnitude in. The final diagram will produce an image contain N^2 bins. The higher the bin count the greater the resolution but the more sparse the data will appear. For the images in the blog a resolution of 2400 bins is used.

The last question is on whether the Sector/Background stars forming a heatmap should be plotted. If you are after a scatterplot of the candidate stars type N. If you are after a heatmap of the Sector stars type Y. 

The program will now plot the scatterplot, returning statistics on the data and then producing the final image. It will then prompt whether further images are to be produced.
The image below shows the above in the command terminal. 

![Screenshot 2022-10-01 135706](https://user-images.githubusercontent.com/97238126/193410681-426de176-81e5-446f-8a05-e6f7ee49b787.png)

### Generating a HR diagram by importing the module
For those that are familiar with the python programming language, the text based user interface is simply obtaining the necessary data and then passing it to a function of the HR diagram Generator. Thus using python, the process of typing the data in is significantly quicker. Below I generated a HR diagram for 3 of the northern sectors by initialising a HR diagram generator object providing it with the file paths for the sector data and the information explained in the text based interface section of this readme.


![Screenshot 2022-10-01 144441](https://user-images.githubusercontent.com/97238126/193412823-cf72e322-325a-4b86-8162-ee699b7e4b3f.png) *This is screenshot showing the steps required to produce a HR diagram using the HR diagram Generator. The module is imported, a HR diagram generator object created. Sector data is then imported by passing a list of file paths to the add sector data method. The plot is then created by using the plot hr diagram using heatmap method and passing the values above.*


![Screenshot 2022-10-01 145339](https://user-images.githubusercontent.com/97238126/193412879-4bf31eb2-37b1-4504-8567-636b8f376d34.png) *This is a screenshot showing the results of code above.*


