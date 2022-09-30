# HR_Diagram_Generator
The HR diagram is a small python project used to quickly produce HR diagrams. This readme will explain in detail the process I used to for obtaining the data I used to
produce the images in the blog. A guide for how to use the HR diagram generator is then provided.
## Obtaining the Data
First, we need to obtain the TIC ids for the stars of the northern and southern ecliptic hemisphere that are observed by TESS. This is achieved by going to the MAST, 
Mikulski Archive for Space Telescopes, archive of TESS light curves from full frame Images or "TESS-SPOC". SPOC refers to the TESS Science Processing Operations 
Centre (SPOC) a pipeline which is used to generate target pixel files, light curves, calibrate the full-frame images and associated products.

![image](https://user-images.githubusercontent.com/97238126/193291717-8007b0e9-c8e2-4bd6-b833-311693743eea.png)
*Light Curve Data, Target Pixel Files, Target List Data and associated products produced by TESS-SPOC for Years 1 (Sectors 1-13) and Years 2 (Sectors 14-26) TESS Data.*

Scrolling down the page the webpage includes the target lists for sectors 1-55 and are tabulated in the years of the TESS mission. Years 1,2 and 3 are complete hence 
the full list of sectors for those years, while year 4 has began and hence has an incomplete list of sectors. For Sectors 1-55 we download Target List csv files 
download into our local drive by clicking on the link attached to the target list. For clarity I have separated the data into the folders Northern Hemisphere year 2 
and year 4 as well as the Southern Hemisphere year 1 and year 3. 

![image](https://user-images.githubusercontent.com/97238126/193293224-6d9a2383-ed52-43d4-b6cf-307c892ce047.png)
*
