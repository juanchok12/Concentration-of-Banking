# Concentration-of-Banking  💰 🏦

https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/ad37bbf8-56b7-4b71-961a-b474b36d2a6d

https://plotly.com/examples/finance/
## Table of Contents
1. [Goal & Description](#0)<br>
2. [Hypothesis](#1)<br>
3. [Data Sources](#2)<br>
    a. [Data for consolidated assets](#3)<br>
    b. [Data for mergers and acquisitions](#4)<br>
    c. [Data for the phylogenetic tree, ownership table, and historical stock data](#5)<br>
2. [Data App](#6)<br>
    a. [Network plots of acquisitions and mergers for the Big Four](#7)<br>
    b. [Metrics for the consolidated assets of the Big Four](#8)<br>
    c. [Wells Fargo dataframe development](#9)<br>
3. [M&A Network Plot Development](#8) <br>
    a. [Network plot for Chase](#9)<br>
    b. [Metrics for the consolidated assets of the Big Four](#10)<br>
    


## Goal & Description <a id="0"></a>
Quantifying the concentration/decentralization/equilibrium of banking as a property/process/phenomena of in the economy from 2003-2023 by seeing trends in consolidated assets of large commercial banks and merging & acquisition activies by large commercial banks. 

The *concentration of banking* is the tendency of capital centralizing more and more around a few financial institutions, creating a financial network where a small number of banks and industrial monopolies wield enormous power over production, investment, and commerce. It subordinates the separated regional economies of a society into a singularity. 

**Research questions**:
* What is the current market share of banking in the U.S. as measured by the share of consolidated assets? 

* What is the historical (2003-2023) trend of monopolization/dispersion/equilibrium of banking in the U.S.?
  
* What do the trends in mergers and acquisitions of the biggest four commercial banks tell us about the monopolization/decentralization of banking in the U.S.?

## Hypothesis <a id="1"></a>
Given a trend in the increase in the amount of consolidated assets by large commercial banks (specifically, the rate the consolidation on these assets of the biggest 4 & 7 bank groups) from the period 2003-2023, we can hypothesize a correlation between the increase in the monopolistic tendencies in finance capital over time through the concentration of banking (i.e. one of the several metrics of centralization of banking). This hypothesis is furthered by the acquisition and merger behavior of the biggest four commercial banks over last couple of decades. 

## Data Sources <a id="2"></a>
### Data for consolidated assets<a id="3"></a> <br>
![consolidated_assets](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/f051a9b2-7175-484a-b752-95514c1811af)

The Board of Governors of the Federal Reserve System publishes quarterly tables with the following important points for our research: 
 * Name of bank
 * Bank ID (know as the RSSD ID, which is a unique identifier assigned to institutions by the Federal Reserve)
 * Consolidated assets

Link: https://www.federalreserve.gov/releases/lbr/

<img src="https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/6f25c9ed-cfc7-4301-9d70-e2940b5dd2a7" width="50%" alt="data_source">

The document *"automated_data_pipeline.py"* in the "script" folder automates the process of 
*	Web scraping each quarterly link 
*	Transforming the data from HTML to CSV documents so that we can manipulate the data.
*	Data cleaning: standardization of column headers and data, adding columns that calculate percentages. 
*	Data wrangling: Setting master data frames, pivoting, concatenating dataframes that develop plot ready data frames.
*	Uploads data frames into Github repository.

The data pipleline is set to be executed every quarter, effectively automating the updating of the plots in the "Consolidated Assets" tab of the data app.

### Data for mergers and acquisitions<a id="4"></a> <br>
![network for README](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/2019ab0b-4e68-47c3-ad16-b79acfbcdc3d)

The development of the network plot was possible through data from the National Information Center, which is managed by the Federal Reserve.<br>

Three datasets were utilized to construct a network plot of the Big Four banks:
 * Relationships.csv: important data points were...
      * Predecessor Bank ID (RSSD).
      * Successor Bank ID (RSSD).
      * Date of transformation (the date in which the merger/acquisition occurred). [Link](https://www.ffiec.gov/npw/FinancialReport/DataDownload)
 * Attributes.csv: Since the "Relationships.csv" file only has a numerical identifier as an ID for banks, it was necessary to cross reference/map the "Attributes.csv" file (which contains both the numerical identifier and its legal name) to obtain the legal name of the financial entities of interest. [Link]( https://www.ffiec.gov/npw/FinancialReport/DataDownload)
 * "history.csv". Each one of the Big Four banks has a history csv file that can be found by entering the RSSD number in the National Information Center search engine. "history.csv" displays the history of bank, uncluding mergers and acquistions. Since not all RSSD numbers are identifiable through the "Attributes.csv" file, we can rely on the "history.csv" to fill the gaps on the missing pieces. [Link](https://www.ffiec.gov/NPW)

The Jupyter Notebook *network_MnA.ipynb* is file in the "script" folder that cleans, wrangles, and plots the data by carrying the following tasks:
*	Adding missing values, such as the legal names of the entities by concatenating “Tranformations.csv”, “Attributes.csv”, “history.csv” files” to develop a data frame that has the necessary data points...
    *	Date of transformation (merger, acquisition, etc).
    *	Legal name of entity
    *	Notes on the nature of the transformation. 
    *	Transformation code
    *	Accounting method. 
*	Identifying subsidiary entities as a subcategory can be filtered through our app. 
*	Testing the data frames developed from the raw data by ploting the network graph. 


 ### Data for the phylogenetic tree, ownership table, and historical stock data <a id="5"></a>
 ![phylogenetic tree](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/48bc60f6-adca-4804-8a87-8a06dd82141a)

The data on the phylogenetic tree was compiled through corporate research (e.g. looking into business news) to find the historical merging & acquisition history of the Big Four banks. The reason I added phylogenetic tree in addition to the network plot of acquisitions and mergers is because I wanted to have a summarized version of the recent and most important historical activity in the merging & acquisition of the Big Four banks, that gives the additional data point of market value/cost of the merging/acquisition.  

Aside from the phylogenetic tree we have the “Giga Banks Ownership on the Big Four” table and the “Historical Share Price” line plot covering the other half of the tab. Both items extract their data from Yahoo! Finance through the yfinance API. The “Giga Banks Ownership on the Big Four” table represents the share ownership of the biggest asset management firms in the U.S. (AKA the Giga Banks) on the Big Four banks, which demonstrate another layer on the concentration of banking. The data for the Giga Banks table was processes through the *'giga_banks.py'* file under the "script" folder repository. 

The "Historical Share Price" line plot is collected from the yfinance API through a bot in our data app script. The line plot displays the close stock price of each of the Big Four banks, updated daily.  

yfinance Github: https://github.com/ranaroussi/yfinance/tree/main<br>
Yahoo! Finance: https://finance.yahoo.com/
 
 
## Data Application <a id="6"></a> <br>
### Network plots of acquisitions and mergers for the Big Four <a id="7"></a> <br>
Used [NetworkX](https://networkx.org/) Python library in to develop the network plot. 
<div>

![network_plot](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/c265ad89-8432-4a58-bc07-e619205d1fcf)





### Metrics for the consolidated assets of the Big Four <a id="8"></a> <br>
Used the [SJ Visualizer](https://github.com/SjoerdTilmans/sjvisualizer) Python package to develop the animated pie race that displays the market share of large commerical banks based on their dominance of consoldiated assets. The script that developed the pie chart race is *"Animated Pie Chart for Banks.py"* under the "script" folder.
<div>

https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/e105c8b3-ecef-4037-a3f2-97dfca2e49dd

Used [scikit learn]( https://scikit-learn.org/stable/index.html) linear model machine learning module to create the linear regression line and model, which is updated each time the application receives data from the automated data pipeline. This scatter plot, the treemap, the line plot, and including the network plot use Plotly to add interactivity to the graphing of the data. 

![scatter_plot](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/c721feae-a5f1-4d5c-b2f1-ef9344f9dc32)


### a) From web scraping HTML tables to CSV files to creating pivot data frames using Python: 
   
   1) Webscraping: Webscraped the Federal Reserve data on large commercial banks by identifying the HTML tables, downloaded the tables into HTML files and transformed these files into CSV files. 
    
   2) Transformation: Cleaned data, normalized to standardize columns and banks names (to avoid repeated bank entities but with different names or for banks that had merged together in the past).
    
   3) Pivot: Combined the different data points per quarter into a master list of all data quarters using Python. From the master database, I then further pivoted other dataframes according to the needs of data visualization.

![HTML to CSV to DF](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/a4d7549b-a649-4b3c-b6da-bbbd2312dd91)





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

