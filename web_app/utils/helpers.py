import pandas as pd
import matplotlib.pyplot as plt

# datasets
df_players = pd.read_csv('../datasets/euroleague_players.csv')
df_box_score = pd.read_csv('../datasets/euroleague_box_score.csv')
df_teams = pd.read_csv('../datasets/euroleague_teams.csv')
df_points = pd.read_csv('../datasets/euroleague_points.csv')
df_header = pd.read_csv('../datasets/euroleague_header.csv')




#mapping team names

team_mappings = {
    'OLYMPIACOS': ['OLYMPIACOS PIRAEUS B.C.', 'OLYMPIACOS PIRAEUS', 'OLYMPIACOS PIRAEUS BC', 'OLYMPIACOS'],
    'BARCELONA': ['AXA FC BARCELONA', 'REGAL FC BARCELONA', 'REGAL FC BARCELONA ', 'FC BARCELONA REGAL', 
                  'FC BARCELONA', 'FC BARCELONA LASSA'],
    'REAL MADRID': ['REAL MADRID'],
    'CSKA MOSCOW': ['CSKA MOSCOW'],
    'ZALGIRIS': ['ZALGIRIS', 'ZALGIRIS KAUNAS'],
    'PANATHINAIKOS': ['PANATHINAIKOS', 'PANATHINAIKOS BSA ATHENS', 'PANATHINAIKOS ATHENS', 
                      'PANATHINAIKOS SUPERFOODS ATHENS', 'PANATHINAIKOS OPAP ATHENS', 'PANATHINAIKOS AKTOR ATHENS'],
    'PARTIZAN': ['PARTIZAN BC', 'PARTIZAN', 'PARTIZAN IGOKEA', 'PARTIZAN MT:S', 'PARTIZAN MT:S BELGRADE',
                 'PARTIZAN NIS BELGRADE', 'PARTIZAN MOZZART BET BELGRADE'],
    'MILAN': ['MILANO', 'ARMANI JEANS MILANO', 'EA7 EMPORIO ARMANI MILANO', 'AX ARMANI EXCHANGE OLIMPIA MILAN', 
              'AX ARMANI EXCHANGE MILAN'],
    'FENERBAHCE': ['FENERBAHCE ULKER', 'FENERBAHCE ULKER ISTANBUL', 'FENERBAHCE ISTANBUL', 
                   'FENERBAHCE BEKO ISTANBUL', 'FB DOGUS'],
    'MACCABI TEL AVIV': ['MACCABI TEL AVIV', 'MACCABI ELITE TEL AVIV', 'MACCABI ELECTRA TEL AVIV',
                         'MACCABI FOX TEL AVIV', 'MACCABI PLAYTIKA TEL AVIV'],
    'EFES': ['EFES PILSEN ISTANBUL', 'ANADOLU EFES ISTANBUL'],
    'BASKONIA': ['CAJA LABORAL BASKONIA', 'CAJA LABORAL', 'LABORAL KUTXA VITORIA', 
                 'LABORAL KUTXA VITORIA GASTEIZ', 'KIROLBET BASKONIA VITORIA GASTEIZ','KIROLBET BASKONIA VITORIA-GASTEIZ', 'TD SYSTEMS BASKONIA VITORIA-GASTEIZ','BITCI BASKONIA VITORIA-GASTEIZ', 'BASKONIA VITORIA-GASTEIZ', 'CAZOO BASKONIA VITORIA-GASTEIZ'],
    'VALENCIA': ['POWER ELECTRONICS VALENCIA', 'VALENCIA BASKET'],
    'UNICAJA': ['UNICAJA', 'UNICAJA MALAGA'],
    'ALBA BERLIN': ['ALBA BERLIN'],
    'BAYERN MUNICH': ['FC BAYERN MUNICH'],
    'BROSE BAMBERG': ['BROSE BASKETS', 'BASKETS BAMBERG', 'BROSE BASKETS BAMBERG', 'BROSE BAMBERG'],
    'GALATASARAY': ['GALATASARAY MEDICAL PARK', 'GALATASARAY LIV HOSPITAL ISTANBUL', 'GALATASARAY ODEABANK ISTANBUL'],
    'CRVENA ZVEZDA': ['CRVENA ZVEZDA TELEKOM BELGRADE', 'CRVENA ZVEZDA MTS BELGRADE', 'CRVENA ZVEZDA MERIDIANBET BELGRADE'],
    'BILBAO': ['BILBAO BASKET', 'BIZKAIA BILBAO BASKET', 'GESCRAP BB'],
    'VIRTUS BOLOGNA': ['VIRTUS VIDIVICI BOLOGNA', 'VIRTUS SEGAFREDO BOLOGNA'],
    'DARUSSAFAKA': ['DARUSSAFAKA DOGUS ISTANBUL', 'DARUSSAFAKA TEKFEN ISTANBUL'],
    'BUDUCNOST': ['BUDUCNOST VOLI PODGORICA'],
    'MONACO': ['AS MONACO'],
    'KHIMKI': ['BC KHIMKI', 'KHIMKI MOSCOW REGION', 'BC KHIMKI MOSCOW REGION'],
    'LIETUVOS RYTAS': ['LIETUVOS RYTAS', 'LIETUVOS RYTAS VILNIUS'],
    'CIBONA': ['KK CIBONA', 'CIBONA'],
    'UNION OLIMPIJA': ['UNION OLIMPIJA', 'UNION OLIMPIJA LJUBLJANA'],
    'PROKOM': ['PROKOM TREFL SOPOT', 'ASSECO PROKOM SOPOT', 'ASSECO PROKOM GDYNIA', 'ASSECO PROKOM'],
    'VIRTUS ROMA': ['LOTTOMATICA ROMA', 'VIRTUS ROMA'],
    'ASVEL': ['ASVEL LYON', 'LDLC ASVEL VILLEURBANNE'],
    'NANTERRE': ['JSF NANTERRE'],
    'STRASBOURG': ['STRASBOURG'],
    'LIMOGES': ['LIMOGES CSP'],
    'CHOLET': ['CHOLET BASKET'],
    'CHALON': ['ELAN CHALON-SUR-SAONE'],
    'PARIS BASKETBALL': ['PARIS BASKETBALL']
}



# Assume df_header is your DataFrame and team_mappings has already been defined.

# Create a reverse lookup dictionary from team_mappings
name_to_normalized = {}
for normalized_name, variations in team_mappings.items():
    for variation in variations:
        name_to_normalized[variation.upper()] = normalized_name

# Function to normalize team names
def normalize_team_name(team_name):
    return name_to_normalized.get(team_name.upper(), team_name)  # Return input if no match

# Apply normalization to 'team_a' and 'team_b' columns
df_header['team_a_'] = df_header['team_a'].apply(normalize_team_name)
df_header['team_b_'] = df_header['team_b'].apply(normalize_team_name)



# Assume df_teams is your DataFrame and team_mappings has already been defined.

# Create a mapping of team_id to normalized team names
# In this case, manually map 'team_id' keys to their normalized names.
team_id_to_name = {
    'OLY': 'OLYMPIACOS',
    'BAR': 'BARCELONA',
    'MAD': 'REAL MADRID',
    'CSK': 'CSKA MOSCOW',
    'ZAL': 'ZALGIRIS',
    'PAN': 'PANATHINAIKOS',
    'PAR': 'PARTIZAN',
    'MIL': 'MILAN',
    'IST': 'FENERBAHCE',
    'TEL': 'MACCABI TEL AVIV',
    'EFES': 'EFES',
    'BAS': 'BASKONIA',
    'VAL': 'VALENCIA',
    'MAL': 'UNICAJA',
    'BER': 'ALBA BERLIN',
    'MUN': 'BAYERN MUNICH',
    'BAM': 'BROSE BAMBERG',
    'GAL': 'GALATASARAY',
    'RED': 'CRVENA ZVEZDA',
    'BIL': 'BILBAO',
    'VIR': 'VIRTUS BOLOGNA',
    'DAR': 'DARUSSAFAKA',
    'BUD': 'BUDUCNOST',
    'MCO': 'MONACO',
    'KHI': 'KHIMKI',
    'LIE': 'LIETUVOS RYTAS',
    'CIB': 'CIBONA',
    'LJU': 'UNION OLIMPIJA',
    'SOP': 'PROKOM',
    'ROM': 'VIRTUS ROMA',
    'ASV': 'ASVEL',
    'NTR': 'NANTERRE',
    'STR': 'STRASBOURG',
    'LMG': 'LIMOGES',
    'CHO': 'CHOLET',
    'CHA': 'CHALON',
    'PRS': 'PARIS BASKETBALL'
}

# Function to map team_id to team_name
def map_team_id_to_name(team_id):
    return team_id_to_name.get(team_id, team_id)  # Return the team_id if no match is found

# Apply the mapping to create the new 'team_name' column
df_teams['team_name'] = df_teams['team_id'].apply(map_team_id_to_name)








# Define a function to create the plots with black background
def create_plot(data, title, xlabel, ylabel,color):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(data.index, data.values, color=color)
    
    # Set background color to black
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    # Set the title and labels, changing text color to white for visibility
    ax.set_title(title, color='white')
    ax.set_xlabel(xlabel, color='white')
    ax.set_ylabel(ylabel, color='white')
    
    # Change tick parameters for better readability on black background
    ax.tick_params(axis='x', rotation=45, labelcolor='white')
    ax.tick_params(axis='y', labelcolor='white')
    
    return fig

