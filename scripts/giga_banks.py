
import yfinance as yf
import pandas as pd


#Create the ticker objects for the Big Four
tickers={
    'JPM':'Chase',
    'BAC':'Bank of America',
    'WFC':'Wells Fargo',
    'C':'Citigroup',
}

#Create a list of the institutional holders Giga Banks of the Big Four:
inst_giga_banks={'Vanguard Group Inc':'Vanguard',
                 'Blackrock Inc.': 'Blackrock',
                 'State Street Corporation':'State Street',
                 'FMR, LLC':'Fidelity',}

#Create a list of mutal funds that are Giga Banks of the Big Four:
mf_giga_banks={'Vanguard Total Stock Market Index Fund': 'Vanguard',
                'Vanguard 500 Index Fund': 'Vanguard',
                'Vanguard Institutional Index Fund': 'Vanguard',
                'Vanguard/Primecap Fund': 'Vanguard',
                'Vanguard Index-Value Index Fund': 'Vanguard',
                'Vanguard Institutional Index Fund-Institutional Index Fund	': 'Vanguard',
                'Vanguard Whitehall Funds-High Dividend Yield Index Fund': 'Vanguard',
                'Vanguard Specialized-Dividend Appreciation Index Fund': 'Vanguard',
                'Vanguard/Windsor II': 'Vanguard',
               'Fidelity 500 Index Fund': 'Fidelity',}

#Create a function to update the ownership data for BAC
def update_bac_holders(inst_giga_banks, mf_giga_banks):
    # Confirm the institutional holders of BAC
    bac = yf.Ticker('BAC')
    bac_inst_holders = bac.institutional_holders
    filt_bac_inst_holders = bac_inst_holders[bac_inst_holders['Holder'].isin(inst_giga_banks.keys())]

    # Create a list of the institutional holders of BAC with a Giga Banks column
    filt_bac_inst_holders.loc[:, 'Giga Banks'] = filt_bac_inst_holders['Holder'].map(inst_giga_banks)

    # Create the dataframe of the mutual fund holders of BAC
    bac_hedge_holders = bac.mutualfund_holders

    # Filter the mutual funds holders based on the Giga Banks
    filt_bac_hedge_holders = bac_hedge_holders[bac_hedge_holders['Holder'].isin(mf_giga_banks.keys())]
    filt_bac_hedge_holders.loc[:, 'Giga Bank'] = filt_bac_hedge_holders['Holder'].map(mf_giga_banks)

    # Concatenate the mutual fund and institutional holders of BAC
    all_bac_holders = pd.concat([filt_bac_inst_holders, filt_bac_hedge_holders], axis=0)

    all_bac_holders['Giga Banks'] = all_bac_holders['Giga Banks'].fillna(all_bac_holders['Giga Bank'])
    all_bac_holders = all_bac_holders.drop(columns=['Giga Bank'])

    aggregated_bac_holders = all_bac_holders.groupby('Giga Banks').agg({'pctHeld':'sum', 'Shares':'sum', 'Value':'sum'})

    aggregated_bac_holders.loc['Total'] = aggregated_bac_holders.sum()

    #Display the aggregated ownership data
    return aggregated_bac_holders

update_bac_holders(inst_giga_banks, mf_giga_banks)
#Create a function to update the ownership data for JPM

def update_jpm_holders(inst_giga_banks, mf_giga_banks):
    # Confirm the institutional holders of BAC
    jpm = yf.Ticker('JPM')
    jpm_inst_holders = jpm.institutional_holders
    filt_jpm_inst_holders = jpm_inst_holders[jpm_inst_holders['Holder'].isin(inst_giga_banks.keys())]

    # Create a list of the institutional holders of BAC with a Giga Banks column
    filt_jpm_inst_holders.loc[:, 'Giga Banks'] = filt_jpm_inst_holders['Holder'].map(inst_giga_banks)

    # Create the dataframe of the mutual fund holders of BAC
    jpm_hedge_holders = jpm.mutualfund_holders

    # Filter the mutual funds holders based on the Giga Banks
    filt_jpm_hedge_holders = jpm_hedge_holders[jpm_hedge_holders['Holder'].isin(mf_giga_banks.keys())]
    filt_jpm_hedge_holders.loc[:, 'Giga Bank'] = filt_jpm_hedge_holders['Holder'].map(mf_giga_banks)

    # Concatenate the mutual fund and institutional holders of BAC
    all_jpm_holders = pd.concat([filt_jpm_inst_holders, filt_jpm_hedge_holders], axis=0)

    all_jpm_holders['Giga Banks'] = all_jpm_holders['Giga Banks'].fillna(all_jpm_holders['Giga Bank'])
    all_jpm_holders = all_jpm_holders.drop(columns=['Giga Bank'])

    aggregated_jpm_holders = all_jpm_holders.groupby('Giga Banks').agg({'pctHeld':'sum', 'Shares':'sum', 'Value':'sum'})

    aggregated_jpm_holders.loc['Total'] = aggregated_jpm_holders.sum()

    #Display the aggregated ownership data
    return aggregated_jpm_holders

update_jpm_holders(inst_giga_banks, mf_giga_banks)


#Create a function to update the ownership data for Citigroup

def update_citi_holders(inst_giga_banks, mf_giga_banks):
    # Confirm the institutional holders of Citi
    citi = yf.Ticker('C')
    citi_inst_holders = citi.institutional_holders
    filt_citi_inst_holders = citi_inst_holders[citi_inst_holders['Holder'].isin(inst_giga_banks.keys())]

    # Create a list of the institutional holders of Citi with a Giga Banks column
    filt_citi_inst_holders.loc[:, 'Giga Banks'] = filt_citi_inst_holders['Holder'].map(inst_giga_banks)

    # Create the dataframe of the mutual fund holders of Citi
    citi_hedge_holders = citi.mutualfund_holders

    # Filter the mutual funds holders based on the Giga Banks
    filt_citi_hedge_holders = citi_hedge_holders[citi_hedge_holders['Holder'].isin(mf_giga_banks.keys())]
    filt_citi_hedge_holders.loc[:, 'Giga Bank'] = filt_citi_hedge_holders['Holder'].map(mf_giga_banks)

    # Concatenate the mutual fund and institutional holders of Citi
    all_citi_holders = pd.concat([filt_citi_inst_holders, filt_citi_hedge_holders], axis=0)

    all_citi_holders['Giga Banks'] = all_citi_holders['Giga Banks'].fillna(all_citi_holders['Giga Bank'])
    all_citi_holders = all_citi_holders.drop(columns=['Giga Bank'])

    aggregated_citi_holders = all_citi_holders.groupby('Giga Banks').agg({'pctHeld':'sum', 'Shares':'sum', 'Value':'sum'})

    aggregated_citi_holders.loc['Total'] = aggregated_citi_holders.sum()

    # Display the aggregated ownership data
    return aggregated_citi_holders

update_citi_holders(inst_giga_banks, mf_giga_banks)

#Create a function to update the ownership data for Wells Fargo

def update_wells_holders(inst_giga_banks, mf_giga_banks):
    # Confirm the institutional holders of Wells Fargo
    wells = yf.Ticker('WFC')
    wells_inst_holders = wells.institutional_holders
    filt_wells_inst_holders = wells_inst_holders[wells_inst_holders['Holder'].isin(inst_giga_banks.keys())]

    # Create a list of the institutional holders of Wells Fargo with a Giga Banks column
    filt_wells_inst_holders.loc[:, 'Giga Banks'] = filt_wells_inst_holders['Holder'].map(inst_giga_banks)

    # Create the dataframe of the mutual fund holders of Wells Fargo
    wells_hedge_holders = wells.mutualfund_holders

    # Filter the mutual funds holders based on the Giga Banks
    filt_wells_hedge_holders = wells_hedge_holders[wells_hedge_holders['Holder'].isin(mf_giga_banks.keys())]
    filt_wells_hedge_holders.loc[:, 'Giga Bank'] = filt_wells_hedge_holders['Holder'].map(mf_giga_banks)

    # Concatenate the mutual fund and institutional holders of Wells Fargo
    all_wells_holders = pd.concat([filt_wells_inst_holders, filt_wells_hedge_holders], axis=0)

    all_wells_holders['Giga Banks'] = all_wells_holders['Giga Banks'].fillna(all_wells_holders['Giga Bank'])
    all_wells_holders = all_wells_holders.drop(columns=['Giga Bank'])

    aggregated_wells_holders = all_wells_holders.groupby('Giga Banks').agg({'pctHeld':'sum', 'Shares':'sum', 'Value':'sum'})

    aggregated_wells_holders.loc['Total'] = aggregated_wells_holders.sum()

    # Display the aggregated ownership data
    return aggregated_wells_holders

update_wells_holders(inst_giga_banks, mf_giga_banks)

# Call the functions to get the dataframes
jpm_holders = update_jpm_holders(inst_giga_banks, mf_giga_banks)
boa_holders = update_bac_holders(inst_giga_banks, mf_giga_banks)
citi_holders=update_citi_holders(inst_giga_banks, mf_giga_banks)
wells_holders=update_wells_holders(inst_giga_banks, mf_giga_banks)

#Rename the columns to include the bank names:
boa_holders.columns = ['BOA_' + col for col in boa_holders.columns]
jpm_holders.columns = ['JPM_' + col for col in jpm_holders.columns]
citi_holders.columns = ['CITI_' + col for col in citi_holders.columns]
wells_holders.columns = ['WELLS_' + col for col in wells_holders.columns]

#Concatenate along the columns
combine_df=pd.concat([jpm_holders, boa_holders,citi_holders,wells_holders], axis=1)

#Drip the 'Shares' and 'Value' columns from the combined DataFrame
combine_df=combine_df.drop(columns=['JPM_Shares', 'JPM_Value', 'BOA_Shares', 'BOA_Value', 'CITI_Shares', 'CITI_Value', 'WELLS_Shares', 'WELLS_Value'])

#Change the JMP_pctHeld and BOA_pctHeld columns names to Chase and Bank of America
combine_df.columns=['Chase', 'Bank of America', 'Citigroup', 'Wells Fargo']

#Convert the decimal values to percentages
combine_df = combine_df.applymap(lambda x: f'{x*100:.2f}%')

#Download the data to a CSV file
combine_df.to_csv('datasets/giga_banks.csv')


