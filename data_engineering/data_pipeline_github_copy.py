import requests #Handles HTTP requests to fetch web contents from the federal reserve
from bs4 import BeautifulSoup #Parses HTML content for web web scraping. It extracts the quarterly bank data tables from the downloaded HTML pages. 
import re #performs string pattern and substitution. It sanitizes filenames
from datetime import datetime #Manages date/time operations to generated quarterly ranges and formats timestamps for filenames. 
import os #Interfaces with the operating system. 
import pandas as pd #Data manipulation and analysis from the dataframes converted from the HTML file tables. Cleans and transforms data. Converts dataframes into csv files. 
import lxml #Optimal parser for beautiful soup. 
import numpy as np #Numerical computing and NaN handling. 
import json #Serializes and deserializes Python objects to JSON format. Formats payloads for Github API requests during file uploads. 
import base64 #Converts file content to base64 for Github API uploads.
import pathlib

html_dir=r"D:\CoB\Data Pipeline Component\html_files"
csv_dir=r"D:\CoB\Data Pipeline Component\csv_files"

#============================Webscraping & File Conversion=======================================================


#---------------------------Quarterly Dates Generation Function--------------------------------
"Develops a list of quarterly end dates from a given start year up to the current year."
def generate_quarterly_dates(start_year):
    """Generates a list of quarterly end dates from a given start year up to the current year."""
    end_year = datetime.now().year  # Current year
    quarters = ["March 31,", "June 30,", "September 30,", "December 31,"]
    formatted_dates = []
    for year in range(start_year, end_year + 1):
        for quarter in quarters:
            formatted_dates.append(quarter + " " + str(year))
    return formatted_dates

generate_quarterly_dates(2003)

#----------------------Date to Quarter Conversion Function-------------------------------------

'''Converts a date to a quarter.'''
def date_to_quarter(month, day):
    if month == 3 and day == 31:
        return 'Q1'
    elif month == 6 and day == 30:
        return 'Q2'
    elif month == 9 and day == 30:
        return 'Q3'
    elif month == 12 and day == 31:
        return 'Q4'
    else:
        return None
    
date_to_quarter(3, 31)

#-------------------Webscrape, Update and Rename Files Function-----------------------------------

'''
Webscrapes the Federal Reserve website for large commercial bank data, updates the files, 
and renames them according to a specified format.
'''

def update_and_rename_files():
    """Downloads data, uploads to local directory, and renames files according to a specified format."""
    URL = "https://www.federalreserve.gov/releases/lbr/" #URL of the Federal Reserve website
    quarterly_dates = generate_quarterly_dates(2003) #Recalling the function that generates a list of quarterly end dates
    response = requests.get(URL) #Sending a GET request to the URL
    soup = BeautifulSoup(response.text, "html.parser") #Parsing the HTML content
    all_links = soup.find_all('a', href=True) #Finding all 'a' elements with 'href' attribute
    links = [(link['href'], link.text) for link in all_links if any(date in link.text for date in quarterly_dates)] #Extracting 'href' and 'text' attributes from 'a' elements

    for href, date in links: #Looping through the extracted 'href' and 'text' attributes
        full_url = URL + href #Constructing the full URL
        table_response = requests.get(full_url) #Sending a GET request to the full URL
        filename = re.sub(r'\W+', '_', href) + ".html" #Sanitizing the filename
        date_obj = datetime.strptime(date, "%B %d, %Y") #Converting the 'text' attribute to a datetime object
        datenum = date_obj.strftime("%Y%m%d") #Converting the datetime object to a string
        quarter = date_to_quarter(date_obj.month, date_obj.day) #Calling the function that converts a date to a quarter
        new_filename = f'{datenum}_{quarter}_{date_obj.year}_large_commercial_banks.html' #Constructing the new filename
        current_path = os.path.join(html_dir, filename) # Path to current file
        new_path = os.path.join(html_dir, new_filename) # Path to new file
        #new_path = new_path.replace("\\","/")

        #Write the content of the respons to a file
        with open(new_path, 'w', encoding='utf-8') as f: #Write the content of the response to a file
            f.write(table_response.text) 

update_and_rename_files()

#---------------------------Convert HTML to CSV Function---------------------------------------------
" Reads a specific table from an HTML file."
def read_specific_table(html_file):
    with open(html_file, 'r', encoding='utf8') as file:  # It's a good practice to define encoding
        contents = file.read()

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(contents, 'html.parser')  # You can switch back to 'lxml' or use 'html.parser'

        '''Create OR statements to account for differences in the attributes in the html code for the html files'''
        def matches_table_attribute(tag):
            is_table = tag.name == 'table'
            cellpadding_match = tag.get('cellpadding') in ['1', '7']
            border_match = tag.get('border') in ['1', '1px']
            frame_match = tag.get('frame') in ['BOX', 'box']
            return is_table and cellpadding_match and border_match and frame_match
        
        #Find all tables that match our custom criteria
        tables=soup.find_all(matches_table_attribute)

        #Return the first matching table
        if tables:
            #Parse the table with Pandas
            df=pd.read_html(str(tables[0]))[0] #Read the table into a dataframe. The [0] is to get the first table
            return df
        else:
            #Handle the case where no table is found
            print(f"No table found in file: {html_file}")
            return None

for file in os.listdir(html_dir): 
    if file.endswith('.html'):
        #Read the aspecific table from the HTML file
        df=read_specific_table(os.path.join(html_dir,file))

        #Write the DataFrame to a CSV file
        csv_file=os.path.splitext(file)[0]+'.csv' #[0] is the file name without the extension
        #Save the csv file in the csv directory
        df.to_csv(os.path.join(csv_dir,csv_file),index=False)
        print(f"File {csv_file} has been saved.")  

#===================Data Cleaning=======================================================

#-------------------------------------------Define uniform columns-------------------------------------------------------

#Defining the path to the csv files
csv_files=os.listdir(csv_dir) #List of all the csv files in the directory

#Define the uniform column names
uniform_columns= [
    'Name',
    'Natl Rank',
    'Bank ID',
    'Bank Location',
    'Charter',
    'Consolidated Assets',
    'Domestic Assets',
    'Percentage Domestic Assets',
    'Percentage Cumulative Assets',
    'Domestic Branches',
    'Foreign Branches',
    'IBF',
    'Percentage Foreign Owned',
]

#Loop through each CSV file and append to the uniform_columns
for csv_file in csv_files:
    try:
        #construct the full path to the CSV file
        csv_path=os.path.join(csv_dir,csv_file)

        #Read the CSV file into a Dataframe
        df=pd.read_csv(csv_path)

        #Check if the DataFrame has the same number of columns as 'uniform_columns'
        if len(df.columns) < len(uniform_columns):
            #Add the missing columns and fill them with NaN
            missing_cols=len(uniform_columns)-len(df.columns)
            for _ in range(missing_cols):
                df[uniform_columns[-missing_cols]]=np.nan

        #Read the columns
        df.columns=uniform_columns

        #Write the DataFrame back to the CSV file
        df.to_csv(csv_path,index=False)

        print(f"Successfully converted {csv_file}")
    except Exception as e:
        print(f"Error converting {csv_file}: {e}") 


#---------------------------------------------Datatypes---------------------------------------------------------

'''Change datatypes for columns and add new columns'''
#Define the columns to covnert the integer
integer_columns=['Natl Rank', 'Consolidated Assets', 'Domestic Assets', 'Domestic Branches', 'Foreign Branches']

#Define the columns to convert to floats
float_columns=['Percentage Domestic Assets', 'Percentage Cumulative Assets', 'Percentage Foreign Owned']

#Loop through each CSV file and convert the columns to the correct data types
for csv_file in csv_files:
    try:
        print(f"Processing file: {csv_file}")
        csv_path=os.path.join(csv_dir,csv_file)
        df=pd.read_csv(csv_path)

        #Convert to float columns
        for col in integer_columns:
            df[col]=pd.to_numeric(df[col],errors='coerce').fillna(0).astype(float)

        #Mutiply 'Consolidated Assets' and 'Domestic Assets' by 1,000,000
        df['Consolidated Assets']=df['Consolidated Assets']*1000000 #*1000000 use to multiply the 'Consolidated Assets', 'Domestic Assets' columns
        df['Domestic Assets']=df['Domestic Assets']*1000000 #*1000000 use to multiply the 'Consolidated Assets', 'Domestic Assets' columns

        #Convert float columns and divide by 100 to get decimal representation
        for col in float_columns:
            df[col]=pd.to_numeric(df[col],errors='coerce').div(100) #.div(100) use to divide 'Percentage Domestic Assets', 'Percentage Cumulative Assets', 'Percentage Foreign Owned'columns

        #Save the cleaned DataFrame back to the CSV file
        df.to_csv(csv_path,index=False)

        print(f"Successfully cleaned file: {csv_file}")
    except Exception as e:
        print(f"Error processing file: {csv_file}: {e}")



#------------------------------------------Create new columns--------------------------------------------------


'''Create another column in each one of the csv files that would allow 
me to see the percentage of the consolidated assets of each bank compared
 to the sum of the consolidated assets of all banks'''

#Loop through all the CSV files to create a percentage column based on the consolidated assets:
for csv_file in csv_files:
    csv_path=os.path.join(csv_dir,csv_file)
    df=pd.read_csv(csv_path)

    #Calculate tthe sum of consolidated assets for each bank
    total_assets=df['Consolidated Assets'].sum()

    #Calculate the percentage of consolidated assets for each bank
    df['Percentage of Total Cosolidated Assets']=(df['Consolidated Assets']/total_assets)

    #Round the percentage to 4 decimal places
    df['Percentage of Total Cosolidated Assets']=df['Percentage of Total Cosolidated Assets'].round(4)

    #Convert 'Percentage of Total Cosolidated Assets' column into a float column
    df['Percentage of Total Cosolidated Assets']=df['Percentage of Total Cosolidated Assets'].astype(float)

    # Save the updated dataframe back to the CSV file
    df.to_csv(csv_path,index=False)

    
'''
Crete date and quarter column in each one of the csv files
based on the file name format in which '20170331_Q1_2017_large_commercial_banks.csv' 
stands for ''yyyymmdd_Qx_yyyy_large_commercial_banks.csv'. 

The date column should be in the format 'mm/dd/yyyy' (in date data type fomat) and the quarter column 
should be in the format 'Qx-yyyy' format in date data type fomat.
'''

#Loop through all the CSV files to create the date and quarter columns
for csv_file in csv_files:
    csv_path=os.path.join(csv_dir,csv_file)
    df=pd.read_csv(csv_path)

    #Extract the date from the file name
    date_str=csv_file.split('_')[0] #split('_')[0] use to extract the date from the file name. The [0] is the first element in the list
    date=pd.to_datetime(date_str,format='%Y%m%d')
    df['Date']=date

    #Extract the quarter from the file name
    quarter_str=csv_file.split('_')[1] #split('_')[1] use to extract the quarter from the file name. The [1] is the second element in the list
    year_str=csv_file.split('_')[2] #split('_')[2] use to extract the year from the file name. The [2] is the third element in the list
    quarter=f"{quarter_str}-{year_str}" #f"{quarter_str}-{year_str}" use to format the quarter and year
    df['Quarter']=quarter #Add the quarter column to the DataFrame

    #Save the updated DataFrame back to the CSV file
    df.to_csv(csv_path,index=False)

    print(f"Successfully processed file: {csv_file}")

#=====================================Data Wrangling=================================================

#Define the path to save the plot ready dataframes in the form of csv files
dataset_dir=r'D:\CoB\Data Pipeline Component\datasets'
#-------------------Creation of the master dataframe--------------------------------------
'''
Function reads multiple CSV files and concatenates them into a single DataFrame.
It sorts the DataFrame by 'Date' in the descending order.
It groups the DataFrame by 'Bank ID' and gets the first 'Name' for each group.
It maps the bank_names_series to the 'Bank ID' column in the concatenated_df.
It sums the consolidated assets of all banks per quarter.
It turns 'total_assets_per_quarter' into a dataframe.
It saves the concatenated_df dataframe to a CSV file.
'''

def process_data(csv_files, csv_dir):
    # Create an empty list to store the dataframes
    dfs = []

    # Iterate over each CSV file
    for file in csv_files:
        # Read the CSV file into a dataframe
        df = pd.read_csv(os.path.join(csv_dir, file))
        # Append the dataframe to the list
        dfs.append(df)

    # Concatenate all dataframes into a single dataframe
    concatenated_df = pd.concat(dfs)

    # Sort the dataframe by 'Date' in the descending order
    concatenated_df = concatenated_df.sort_values('Date', ascending=False)

    # Group by 'Bank ID' and get the first 'Name' for each group
    bank_names_series = concatenated_df.groupby(by='Bank ID')['Name'].first()

    # Map the bank_names_series to the 'Bank ID' column in the concatenated_df
    concatenated_df['Bank Name'] = concatenated_df['Bank ID'].map(bank_names_series)

    # Sum the consolidated assets of all banks per quarter
    total_assets_per_quarter = concatenated_df.groupby('Quarter')['Consolidated Assets'].sum()

    # Turn 'total_assets_per_quarter' into a dataframe
    total_assets_per_quarter = total_assets_per_quarter.to_frame()

    #Save the concatenated_df dataframe to a CSV file
    concatenated_df.to_csv(os.path.join(dataset_dir, 'concatenated_df.csv'), index=False)

    return concatenated_df, total_assets_per_quarter


    # Call the process_data function
concatenated_df, total_assets_per_quarter = process_data(csv_files, csv_dir)

#---------------------------Creation of the dataframe for the line plot----------------------------------

'''
Function creates a pivot table of the concatenated_df dataframe to set 'Date' as the index, 'Commercial Name' as the columns, and 'Total Assets' as the values.
* It adds 'Total Assets' column to the big_four_pivot dataframe.
* It sums the consolidated assets of the Big Four banks for each quarter and adds the result to the 'big_four_pivot' dataframe as 'Big Four Assets'.
* It adds 'Other Banks' column to the 'big_four_pivot' dataframe by subtracting 'Total Assets' from 'Big Four Assets'.
* It adds 'Share of Consolidated Assets' column to the 'big_four_pivot' dataframe by dividing 'Big Four Assets' by 'Total Assets'.
* It saves the 'big_four_pivot' dataframe to a CSV file.

'''

def create_big_four_line(concatenated_df, total_assets_per_quarter):
    
    # Create a dictionary to map the Big Four banks
    big_four_banks = {
        'JPMORGAN CHASE BK NA/JPMORGAN CHASE & CO': 852218,
        'BANK OF AMER NA/BANK OF AMER CORP': 480228,
        'CITIBANK NA/CITIGROUP': 476810,
        'WELLS FARGO BK NA/WELLS FARGO & CO': 451965
    }

    # Filter the dataframe to only include the Big Four banks
    big_four_df = concatenated_df[concatenated_df['Bank ID'].isin(big_four_banks.values())]

    # Create a dictionary to map the Big Four banks to their commercial names
    big_four_commercial_names = {
        852218: 'Chase',
        480228: 'Bank of America',
        476810: 'Citibank',
        451965: 'Wells Fargo'
    }

    # Add a 'Commercial Name' column to the big_four_df dataframe
    big_four_df['Commercial Name'] = big_four_df['Bank ID'].map(big_four_commercial_names)

    # Pivot the big_four_df dataframe to set 'Date' as the index, 'Commercial Name' as the columns, and 'Total Assets' as the values
    big_four_pivot = big_four_df.pivot_table(index=['Date', 'Quarter'], columns='Commercial Name', values='Consolidated Assets').reset_index()

    # Add 'Total Assets' column to the big_four_pivot dataframe
    big_four_pivot['Total Assets'] = big_four_pivot['Quarter'].map(total_assets_per_quarter['Consolidated Assets'])

    # Sum the consolidated assets of the Big Four banks for each quarter and add the result to the 'big_four_pivot' dataframe as 'Big Four Assets'
    big_four_pivot['Big Four Assets'] = big_four_pivot['Chase'] + big_four_pivot['Bank of America'] + big_four_pivot['Citibank'] + big_four_pivot['Wells Fargo']

    # Divide the 'Total Assets' column by the 'Big Four Assets' column to get the percentage of the total assets held by the Big Four banks and add the result to the 'big_four_pivot' dataframe as 'Percentage of Total Assets'
    big_four_pivot['Share of Consolidated Assets'] = big_four_pivot['Big Four Assets'] / big_four_pivot['Total Assets']

    # Display the 'Share of Consolidated Assets' column in percentage format with two decimal places
    big_four_pivot['Share of Consolidated Assets'] = big_four_pivot['Share of Consolidated Assets'].map(lambda x: ' {:.2%}'.format(x))

    # Save the big_four_pivot DataFrame to a CSV file
    big_four_pivot.to_csv(os.path.join(dataset_dir, 'bank_asset_line.csv'), index=False)

    #big_four_pivot.to_csv(os.path.join(csv_dir, 'line_plot.csv'), index=False)

    return big_four_pivot

# Call the create_big_four_line function

big_four_pivot = create_big_four_line(concatenated_df, total_assets_per_quarter)

#---------------------------Creation of the dataframe for the scatter plot----------------------------------

'''
The function 'create_melted_scatter_df' melts the 'big_four_pivot' dataframe to create a new dataframe called 'melted_line_df'.
The 'melted_line_df' dataframe is then saved to a CSV file in the 'dataset_dir' directory.
It also defines a function 'quarter_to_num' to convert the 'Quarter' column to a numerical format.

'''
def create_melted_scatter_df(big_four_pivot, dataset_dir):
    # Melt the DataFrame
    melted_line_df = big_four_pivot.melt(id_vars=['Quarter','Date'], value_vars=['Chase', 'Bank of America', 'Citibank', 'Wells Fargo'], var_name='Bank', value_name='Assets')

    # Define function to convert the quarter string to a numerical format
    def quarter_to_num(quarter_string):
        # Split the quarter string into year and quarter parts
        parts = quarter_string.split('-')
        year = int(parts[1])
        quarter = parts[0]

        # Map the quarter part to a fraction of the year
        quarter_mapping = {'q1': 0.25, 'q2': 0.5, 'q3': 0.75, 'q4': 1.0}
        numerical_quarter = year + quarter_mapping[quarter.lower()]

        return numerical_quarter

    # Apply the quarter_to_num function to the 'Quarter' column
    melted_line_df['Numeric_Quarter'] = melted_line_df['Quarter'].apply(quarter_to_num)

    # Create the 'Quarter_Ordinal' column
    melted_line_df['Quarter_Ordinal'] = melted_line_df['Numeric_Quarter'].rank(method='dense').astype(int)

    # Save melted_line_df to a CSV file to the dataset_dir
    melted_line_df.to_csv(os.path.join(dataset_dir, 'bank_asset_scatter.csv'))


    return melted_line_df

# Call the create_melted_scatter_df function
create_melted_scatter_df(big_four_pivot, dataset_dir)


#----------------------------------Creation of the dataframe for the racing pie chart------------------------

'''
'transform_and_save' function transforms the 'big_four_pivot' dataframe to calculate the percentage share of each bank's assets and the percentage of the total assets held by the rest of the other banks.
It then saves the 'percentage_df' dataframe to a Excel file in the 'dataset_dir' directory.

'''
def transform_and_save(big_four_pivot, dataset_dir):
    # Create a copy of the original dataframe
    percentage_df = big_four_pivot.copy()

    columns_to_convert = ['Bank of America', 'Chase', 'Citibank', 'Wells Fargo']

    # List of columns to drop
    columns_to_drop = ['Quarter', 'Total Assets', 'Big Four Assets', 'Share of Consolidated Assets']

    for column in columns_to_convert:
        # Calculate the percentage share of each bank's assets
        percentage_df[column] = percentage_df[column] / percentage_df['Total Assets']

        # Add a column that calculates the percentage of the total assets of the rest of the other banks
        percentage_df['Other Banks'] = (percentage_df['Total Assets'] - percentage_df['Big Four Assets']) / percentage_df['Total Assets']

        #Reduce the decimal places to two and maintain the datatype as a float
        percentage_df[column] = percentage_df[column].map(lambda x: round(x, 4))

        percentage_df['Other Banks'] = percentage_df['Other Banks'].map(lambda x: round(x, 4))

        
    # Remove the name of the index
    percentage_df.columns.name = None

    #Set the 'date' column as datetime datatype
    percentage_df['Date'] = pd.to_datetime(percentage_df['Date'])

    # Reset the index without keeping old index
    percentage_df.reset_index(drop=True, inplace=True)

    # Drop the columns in the 'columns_to_drop' list
    percentage_df = percentage_df.drop(columns=columns_to_drop)

    # Save the percentage_df dataframe to a Excel file
    percentage_df.to_excel(os.path.join(dataset_dir, 'bank_asset_percentage.xlsx'), index=False)

    return percentage_df

percentage_df=transform_and_save(big_four_pivot, dataset_dir)

#----------------------------------Creation of the dataframe for the treemap------------------------

'''
The function 'create_treemap_df' creates a new dataframe called 'treemap_df' from the 'percentage_df' dataframe.
It then saves the 'treemap_df' dataframe to a CSV file in the 'dataset_dir' directory.

'''

def create_treemap_df(percentage_df, big_four_pivot, dataset_dir):
    # Create a copy of the original dataframe
    assets_df = big_four_pivot.copy()

    columns_of_interest = ['Bank of America', 'Chase', 'Citibank', 'Wells Fargo']

    # List of columns to drop
    columns_to_drop = ['Quarter', 'Share of Consolidated Assets']

    # Remove the name of the index
    assets_df.columns.name = None

    assets_df['Date'] = pd.to_datetime(assets_df['Date'])

    # Drop the columns in the 'columns_to_drop' list
    assets_df = assets_df.drop(columns=columns_to_drop)

    # Subtract 'Big Four Assets' from 'Total Assets' to get the 'Other Banks' column
    assets_df['Other Banks'] = assets_df['Total Assets'] - assets_df['Big Four Assets']

    # Convert the 'Date' column to datetime
    last_date_index = percentage_df['Date'].idxmax()

    # Select the row with the latest date
    latest_date = percentage_df.loc[last_date_index]

    # Convert the series into a dataframe and transpose it
    treemap_df = latest_date.to_frame()

    # Reset the index for treemap_df
    if not treemap_df.index.equals(pd.RangeIndex(start=0, stop=len(treemap_df))):
        treemap_df = treemap_df.reset_index()

    # Name the columns of the treemap_df dataframe
    treemap_df = treemap_df.rename(columns={treemap_df.columns[0]: 'Bank', treemap_df.columns[1]: 'Percentage'})

    # Save the 'Date' value from the first row as a variable
    date_note = treemap_df.loc[0, 'Percentage']

    # Drop the first row of the dataframe
    treemap_df = treemap_df.drop(0)

    # Convert the Timestamp into a string and slice it to only include the date part
    date_note = str(date_note)[:10]

    # In the 'date_note variable, re-arrange string to place month first, then day, and finally year as in 'mm-dd-yyyy' format
    date_note = date_note[5:7] + '-' + date_note[8:10] + '-' + date_note[:4]

    # Set the name of the Dataframe to the 'date_note'
    treemap_df.name = date_note

    # Convert the 'Percentage' column into % format
    treemap_df['Percentage'] = treemap_df['Percentage'].apply(lambda x: ' {:.2%}'.format(x) if pd.notnull(x) and isinstance(x, (int, float)) else x)

    # Create a new 'Parent' column and place it as the first column in the dataframe
    treemap_df['Parent'] = 'Big Four'

    # For the 5th row in the dataframe, I need to replace the 'Parent' value with 'Other Banks'
    treemap_df.loc[5, 'Parent'] = 'Other Banks'
    # leave the 'Bank' value as NaN
    treemap_df.loc[5, 'Bank'] = np.nan

    # Convert the 'Date' column to datetime
    last_date_assets = assets_df['Date'].idxmax()

    # Select the row with the latest date
    last_date_assets = assets_df.loc[last_date_index]

    # Drop first row of the dataframe
    last_date_assets = last_date_assets.drop('Date')

    # Drop the 'Total Assets' column
    last_date_assets = last_date_assets.drop('Total Assets')

    # Drop the 'Big Four Assets' column
    last_date_assets = last_date_assets.drop('Big Four Assets')

    # Reset the index for last_date_assets
    last_date_assets = last_date_assets.reset_index()

    # Name the first column 'Banks'
    last_date_assets = last_date_assets.rename(columns={last_date_assets.columns[0]: 'Bank'})

    # Rename the second columns as 'Assets'
    last_date_assets = last_date_assets.rename(columns={last_date_assets.columns[1]: 'Consolidated Assets'})

    # Create a variable named 'Total Assets' that has the value of the 'Total Assets' row under 'Consolidated Assets'
    total_assets = last_date_assets.loc[4, 'Consolidated Assets']

    # Map the values of 'last_date_assets; to the 'treemap_df' dataframe based on the 'Bank' column
    treemap_df['Consolidated Assets'] = treemap_df['Bank'].map(last_date_assets.set_index('Bank')['Consolidated Assets'])

    # Rearrange order of the columns for the 'Parent' column to be first after the index
    treemap_df = treemap_df[['Parent', 'Bank', 'Percentage', 'Consolidated Assets']]

    # Assign the 'Total Assets' variable to the 'Consolidated Assets' column for the 'Other Banks' row under the 'Parent' column
    treemap_df.loc[treemap_df['Parent'] == 'Other Banks', 'Consolidated Assets'] = total_assets
     
    #Download the treemap_df dataframe as a csv file
    treemap_df.to_csv(os.path.join(dataset_dir, 'bank_asset_treemap.csv'))

    return treemap_df

treemap_df=create_treemap_df(percentage_df, big_four_pivot, dataset_dir)

#=============================Uploading the dataframes into Github repository==============================
def get_file_sha(repo, path, filename, token):
    """
    Retrieve the SHA of an existing file in the specified repository/folder.
    """
    url = f"https://api.github.com/repos/{repo}/contents/{path}/{filename}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('sha')
    return None

def upload_to_github(repo, path, token, file_path):
    """
    Uploads (or updates) a single file to the specified repository and path.
    """
    # Use os.path.basename for cross-platform filename extraction
    filename = os.path.basename(file_path)
    file_sha = get_file_sha(repo, path, filename, token)  # Get SHA if file exists
    api_url = f"https://api.github.com/repos/{repo}/contents/{path}/{filename}"
    
    # Read and encode file content
    with open(file_path, 'rb') as file:
        file_content = base64.b64encode(file.read()).decode('utf-8')
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "message": f"Update {filename}",
        "content": file_content,
        "branch": "main",
    }
    if file_sha:  # Include SHA if updating an existing file
        data['sha'] = file_sha
    
    response = requests.put(api_url, headers=headers, data=json.dumps(data))
    print(f"Response Status Code: {response.status_code} for {filename}")
    print("Response:", response.json())

def upload_multiple_files(repo, path, token, file_paths):
    """
    Loops through a list of file paths and uploads each file to the specified repository and path.
    """
    for file_path in file_paths:
        upload_to_github(repo, path, token, file_path)

# Example usage:

# 1. Upload multiple dataset files to one repository:
file_paths = [
    r'D:\CoB\Data Pipeline Component\datasets\bank_asset_line.csv',
    r'D:\CoB\Data Pipeline Component\datasets\bank_asset_scatter.csv',
    r'D:\CoB\Data Pipeline Component\datasets\bank_asset_treemap.csv',
    r'D:\CoB\Data Pipeline Component\datasets\bank_asset_percentage.xlsx',
]
upload_multiple_files('juanchok12/Concentration-of-Banking', 'datasets', 'github_key_here', file_paths)

# 2. Upload the concatenated_df.csv file to a different repository and folder ("deploy"):
# Define the path as a string rather than a list.
concatenated_file_path = r'D:\CoB\Data Pipeline Component\datasets\concatenated_df.csv'
upload_to_github('juanchok12/Consoldiated-Assets-for-Banks-and-AI', 'deploy', 'github_key_here', concatenated_file_path)


