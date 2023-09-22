# Concentration-of-Banking
![IMG_6833](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/d442031b-7693-4a1c-8529-f9f58eb99ccd)

## Goal
Quantifying the concentration/decentralization/equilibrium of banking as a property of monopoly capitalism from 2003-2023 by seeing trends in consolidated assets of large commercial banks.

## Description 
Concentration of banking, as a property of monopoly capitalism, is the tendency of capital centralizing more and more around a few financial institutions, creating a financial network where a small number of banks and industrial monopolies wield anormous power over production (or under-production), investment (or lack of it), and commerce (or its stultification). It subordinates the separated regional economies of a society into a singularity. 


## Methodology

**a) From web scraping HTML tables to CSV files to creating pivot data frames using Python**: 
   
    1) Webscraping: I webscraped the Federal Reserve data on large commercial data links and downloaded tables into CSV files. 
    
    2) Transformation: Cleaned data, normalized to standardize columns and banks names (to avoid repeated bank entities but with different names or for banks that had merged together in the past).
    
    3) Pivot: Combined the different data points release per quarter into a master list of all data points using Python. From the master database, I then further pivoted other dataframes according to the needs of data visualization.

![HTML to CSV to DF](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/a4d7549b-a649-4b3c-b6da-bbbd2312dd91)


**b) Animated pie chart**: I used the [SJ Visualizer]([url](https://www.sjdataviz.com/software)) package to display the changes in the percentage dominance of the consolidated assets of the biggest 7 banks.

https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/28c33417-e0b7-4aa0-8b78-53cbbcda23b8

**c) Interactive line plots**: I used Plotly's line plots to observe the two decate trend in the accumulation of consolidated assets between the biggest 7 banks in the magnitude of their dollar value. I also grouped the 7 biggest banks into a group and the rest of the banks to compare their consolidated assets (second GIF).
![Line Plot GIF](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/ccdb13ed-5eed-4155-8c9f-06b2ef443bca)

![Two Line Plot GIF](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/16e11ec1-5cc3-40c4-8e8b-1f6cece471b7)

**d) Interactive treemap**: Used Plotly to create an interactive treemap with parent to daughter sub-category relationships.
![Treemap Video GIF](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/98bddfa5-97f8-460e-afce-76c635a37a73)

e) Statistical inferential analysis: developed a linear regression model on the changes in the amount of consolidated assets held by two banks groups 1) the 7 biggest banks 2) the 4 biggest banks. This allowed to develop a linear function that gives me the rate of change in consolidated asset concentration over time (in the function "B" stands for billions in dollar).

![linear_reg_big7](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/7a6332d0-b647-40b6-b2fb-2b8c6780e3ab)


![linear_reg_4big](https://github.com/juanchok12/Concentration-of-Banking/assets/116334702/7c43a1c5-1242-4aba-9da7-eec564b0a738)






