# Concentration-of-Banking  💰 🏦 
https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/ad37bbf8-56b7-4b71-961a-b474b36d2a6d
## Goal & Description
Quantifying the concentration/decentralization/equilibrium of banking as a property/process/phenomena of in the economy from 2003-2023 by seeing trends in consolidated assets of large commercial banks and merging & acquisition activies by large commercial banks. 

The *concentration of banking* is the tendency of capital centralizing more and more around a few financial institutions, creating a financial network where a small number of banks and industrial monopolies wield enormous power over production, investment, and commerce. It subordinates the separated regional economies of a society into a singularity. 

**Research questions**:
* What is the current market share of banking in the U.S. as measured by the share of consolidated assets? 

* What is the historical (2003-2023) trend of monopolization/dispersion/equilibrium of banking in the U.S.?
  
* What do the trends in mergers and acquisitions of the biggest four commercial banks tell us about the monopolization/decentralization of banking in the U.S.?


## Hypothesis
Given a trend in the increase in the amount of consolidated assets by large commercial banks (specifically, the rate the consolidation on these assets of the biggest 4 & 7 bank groups) from the period 2003-2023, we can hypothesize a correlation between the increase in the monopolistic tendencies in finance capital over time through the concentration of banking (i.e. one of the several metrics of centralization of banking). This hypothesis is furthered by the acquisition and merger behavior of the biggest four commercial banks over last couple of decades. 

## Data Product




## Data Sources
**Data for consolidated assets:** <br>
![Data pipeline for consolidated assets](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/7f6f5806-15c6-4b34-a9d2-b799cd4355c6)


The Board of Governors of the Federal Reserve System publishes quarterly tables with the following important points for our research: 
 * Name of bank
 * Bank ID (know as the RSSD ID, which is a unique identifier assigned to institutions by the Federal Reserve)
 * Consolidated assets

Link: https://www.federalreserve.gov/releases/lbr/

<img src="https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/6f25c9ed-cfc7-4301-9d70-e2940b5dd2a7" width="65%" alt="data_source">

The document "automated_data_pipeline.py" automates the process of 
*	Web scraping each quarterly link 
*	Transforming the data from HTML to CSV documents so that we can manipulate the data.
*	Data cleaning: standardization of column headers and data, adding columns that calculate percentages. 
*	Data wrangling: Setting master data frames, pivoting, concatenating dataframes that develop plot ready data frames.
*	Uploads data frames into Github repository.


**Data for mergers and acquisitions:** <br>
Two datasets were utilized to construct a viable network plot model of the biggest 4 commercial banks in the U.S. (here referred to as the Big Four):

 * Relationships.csv: important data points were...
      * Predecessor Bank ID (RSSD)
      * Successor Bank ID (RSSD)
      * Date of transformation (the date in which the merger or acquisition occurred)
 * Attributes.csv: Since the "Relationships.csv" file only has RSSD as identifiers for banks, it was necessary to cross reference the "Attributes.csv" file to obtain the legal name of the financial entities of interest.

Both were obtained from the National Information Center.<br>
 "Relationships.csv" & "Attributes.csv". National Information Center. Federal Financial Instututions Examination Council. Feb. 5, 2024. [Link](https://www.ffiec.gov/npw/FinancialReport/DataDownload).
 


## Analysis of Consolidated Assets

### a) From web scraping HTML tables to CSV files to creating pivot data frames using Python: 
   
   1) Webscraping: Webscraped the Federal Reserve data on large commercial banks by identifying the HTML tables, downloaded the tables into HTML files and transformed these files into CSV files. 
    
   2) Transformation: Cleaned data, normalized to standardize columns and banks names (to avoid repeated bank entities but with different names or for banks that had merged together in the past).
    
   3) Pivot: Combined the different data points per quarter into a master list of all data quarters using Python. From the master database, I then further pivoted other dataframes according to the needs of data visualization.

![HTML to CSV to DF](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/a4d7549b-a649-4b3c-b6da-bbbd2312dd91)


### b) Animated pie chart: 
I used the [SJ Visualizer](https://github.com/SjoerdTilmans/sjvisualizer) package to display the changes in the percentage dominance of the consolidated assets of the biggest 7 banks (size based on consolidated assets).

https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/28c33417-e0b7-4aa0-8b78-53cbbcda23b8

### c) Interactive line plots: 
I used Plotly's line plots to observe the two decade trend in the accumulation of consolidated assets between the biggest 7 banks in trillions of dollars. I also grouped all the large commercial banks into one group and the 7 biggest banks into another group to compare their consolidated assets over time (second GIF).
![Line Plot GIF](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/ccdb13ed-5eed-4155-8c9f-06b2ef443bca)

![Two Line Plot GIF](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/16e11ec1-5cc3-40c4-8e8b-1f6cece471b7)

### d) Interactive treemap: 
Used Plotly to create an interactive treemap with parent to daughter sub-category relationships.
![Treemap Video GIF](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/98bddfa5-97f8-460e-afce-76c635a37a73)

### e)Statistical inferential analysis-linear regression model: 
developed a linear regression model on the changes in the amount of consolidated assets held by two bank groups 1) the 7 biggest banks 2) the 4 biggest banks. This outputted a linear function that gives me the rate of change in consolidated asset concentration over time (in the function "B" stands for billions in dollar).


## Dash App-Analysis of Network of Acquisitions and Assets of the Big Four
![Untitled video - Made with Clipchamp (8)](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/774d8614-6cb0-444a-8145-55751b612a2c)

### a) Data wrangling:
Although the 'Transformations.csv' file gives a detail dataset on the mergers, acquisitions, branch and subsidiary consolidations between financial instutiotions, it does not reference the RSSD (the uniquie bank ID) to its legal name. Therefore, we cross reference the data 'Transformations.csv' with the of the 'Attributes.csv' to gives more detail on the properties of the financial institution, including the legal name. 

<div align="center">
   <img src="https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/7bda601e-9279-412d-bb26-89bc53f7c3d1" width="60%"></div>

On top of this, I created a list of registered transformations in the 'Transformations.csv' that were branch consolidations. This is because I wanted to give the user the ability to filter out data points that were branch mergers with its national association bank. All of this data wrangling in in the 'big_4_MnA_network_plot_2-6-2024 _Github.ipynb' Jupyter Notebook

### b) Network plotting the acquisitions and mergers of the Big Four:
In the same Jupyter Notebook, I create the network plots that I transposed into the Dash app. The main idea is allow the user to see the historical pattern of mergers and acquisitions of the Big Four from 1960's (the earliest time for which the dataset has available data) up until Feb. 2024. 

<div>
   <img src="https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/a022299b-875c-4046-83d8-b7d0aef3d66b" width="80%">

### c) Dash app of network plots with filters
The final product is a Dash app that allows the user to filter the data points based on the following categories:

  * Transformation is a branch consolidation.
  * Accouting method: determining if the transformation was a purchase, acquisition, merger, or its not applicable.
  * Transformation code:
      * Charter discontinued
      * Split
      * Sale of assets
      * Charter retained
      * Failure
   
This allows the user to dynamically see the trends based on this preliminary categories.   

![IMG_6833](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/d442031b-7693-4a1c-8529-f9f58eb99ccd)

