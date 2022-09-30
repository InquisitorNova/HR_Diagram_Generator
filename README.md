# HR_Diagram_Generator
The HR diagram is a small python project used to quickly produce HR diagrams. This readme will explain in detail the process I used to for obtaining the data I used to
produce the images in the blog. A guide for how to use the HR diagram generator is then provided.
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

![image](https://user-images.githubusercontent.com/97238126/193303045-8070927d-54ab-45d9-926a-38681e92389c.png) * A screenshot showing the Gaia catalogue upload menu. Image taken from the [Gaia Archive](https://gea.esac.esa.int/archive/)*

On the Catalogue menu enter the name of the sector and use the choose file button to select the file from the local drive, change the file format to to csv and then press upload to transfer create a copy to the Gaia archive. The Gaia archive will refresh and the sector target list will now appear in the user table at the bottom left of the left panel (Find it by scrolling down). Repeat this process till all the sectors are uploaded into the Gaia archive. 

In the left panel scroll down to the user tables at the bottom. Click on the plus sign to extend the view to show all tables. Click on the checkbox of the target list table. A tick should now appear. Then click on the table icon in the left panel to reveal the Gaia table editor.

![Screenshot 2022-09-30 163935](https://user-images.githubusercontent.com/97238126/193306966-cd9d8417-bd16-4d1e-a5d8-a7481133bcc1.png) * A screenshot showing the Gaia catalogue table editor. Image taken from the [Gaia Archive](https://gea.esac.esa.int/archive/)*

Change the flags of the ra and dec values to Ra and Dec respectively and press the update button. The symbol of the table should now change to indicate that Gaia treats the table as giving position data.

To obtain the data for each star we first need to perform a cross match between the target list csv file now uploaded to the Gaia archive and the gaia data release 3, gaiadr3.gaia_source. This is to obtain the gaiadr3 source ids. For those wanting to perform this operation using ADQL, the Gaia archive provides documentation in the help section of the Gaia archive homepage on how to perform this. For those unfamiliar with ADQL, Gaia provides either premade common cross matches in the “Cross-match” table or has a prebuilt function that will perform the cross match for you. We will be using the prebuilt function as it is the simplest approach.

![Screenshot 2022-09-30 163116](https://user-images.githubusercontent.com/97238126/193305180-a0ce80c0-99a1-4841-85f0-9f66425cb6db.png) * A screenshot of the Gaia archive, showing the prebuilt Gaia Crossmatch function menu. Image taken from the [Gaia Archive](https://gea.esac.esa.int/archive/)

Clicking on the double star button in the left panel of the Gaia Advanced Search menu brings up the prebuilt Gaia Archive cross match function. Change the table A to either the gaiadr3.gaia_source or gaiadr2.gaia_source depending on whether you want data from the gaiadr3 or from the gaiadr2 tables. Change the table B to the 

