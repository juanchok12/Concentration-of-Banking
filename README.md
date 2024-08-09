# Concentration-of-Banking  💰 🏦




https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/cde51fa1-443b-4252-a060-971be95625b4




You can find the app in the Dash Explore Page:
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
    c. [Phylogenetic Tree](#9)<br>

## Goal & Description <a id="0"></a>
The goal is to quantitfy the concentration/decentralization/equilibrium of banking as a property/process/phenomena in the economy from 2003-2023 by seeing trends in consolidated assets of large commercial banks and merging. I will focus on a juxtaposition between the Big Four banks and the rest of the large commercial banks in the U.S. The Big Four group includes:

* Chase
* Bank of America
* Wells Fargo
* Citibank

Additionally, I can observe the acquisition & merging activies by the Big Four to understand the state of banking in the U.S.

The *concentration of banking* is the tendency of capital centralizing more and more around a few financial institutions, creating a financial network where a small number of banks and industrial monopolies wield enormous power over production, investment, and commerce.

**Research questions**:
* What is the current market share of banking in the U.S. as measured by the share of consolidated assets? 

* What is the historical (2003-2023) trend of monopolization/dispersion/equilibrium of banking in the U.S.?
  
* What do the trends in mergers and acquisitions of the biggest four commercial banks tell us about the monopolization/decentralization of banking in the U.S.?

## Hypothesis <a id="1"></a>
Given a trend in the increase in the amount of consolidated assets held by the Big Four from the period 2003-2023, I can hypothesize a correlation between the increase in the monopolistic tendencies in finance capital over time (in this study, I use consolidated assets as only one metric through which I can measure the centralization of banking). This hypothesis is furthered by the acquisition & merger behavior of the biggest four commercial banks over the last couple of decades. 

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
*	Transforming the data from HTML to CSV documents so that I can manipulate the data.
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
 * "history.csv". Each one of the Big Four banks has a history csv file that can be found by entering the RSSD number in the National Information Center search engine. "history.csv" displays the history of bank, uncluding mergers and acquistions. Since not all RSSD numbers are identifiable through the "Attributes.csv" file, I can rely on the "history.csv" to fill the gaps on the missing pieces. [Link](https://www.ffiec.gov/NPW)

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

Aside from the phylogenetic tree I have the “Giga Banks Ownership on the Big Four” table and the “Historical Share Price” line plot covering the other half of the tab. Both items extract their data from Yahoo! Finance through the yfinance API. The “Giga Banks Ownership on the Big Four” table represents the share ownership of the biggest asset management firms in the U.S. (AKA the Giga Banks) on the Big Four banks, which demonstrate another layer on the concentration of banking. The data for the Giga Banks table was processes through the *'giga_banks.py'* file under the "script" folder repository. This file is scheduled to be executed every quarter through the Github workflow "Update and Upload Giga Banks Data" which is based on the "quarterly_update_giga_banks.yml" file within the ".github/workflows" folder. This allows us to have an updated table on the percentage own by the Giga Banks on the Big Four banks. 

The "Historical Share Price" line plot is collected from the yfinance API through a bot in our data app script. The line plot displays the close stock price of each of the Big Four banks, updated daily.  

yfinance Github: https://github.com/ranaroussi/yfinance/tree/main<br>
Yahoo! Finance: https://finance.yahoo.com/
 
 
## Data Application <a id="6"></a> <br>
I used Plotly Dash as the python framework to create the interactive web application. The data application itself is hosted by AWS Elastic Beanstalk. The application script and its requirements can be found in the 'deploy' folder.
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



### Phylogenetic Tree <a id="9"></a>

Used [Highcharts](https://www.highcharts.com/docs/chart-and-series-types/treegraph-chart) to develop the phylogenetic tree. The files used to generate the tree can be find under "script>phylogenetic tree script". 

![phylogenetic tree](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/4b90d849-9ff1-43ab-981b-c05464740999)

