import pandas as pd
import matplotlib.pyplot as plt

#@st.cache_data
# datasets
# if executed locally, add "../" to the start of each of the paths to read the CSVs -> '../datasets/euroleague_players.csv'

df_players = pd.read_csv('datasets/euroleague_players.csv')
df_box_score = pd.read_csv('datasets/euroleague_box_score.csv')
df_teams = pd.read_csv('datasets/euroleague_teams.csv')
df_points = pd.read_csv('datasets/euroleague_points.csv')
df_header = pd.read_csv('datasets/euroleague_header.csv')

df_box_score_eurocup = pd.read_csv('datasets/eurocup_box_score.csv')







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
    'IST': 'ANADOLU EFES',
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
    'CHL': 'CHALON',
    'CHA': 'CHALON',
    'PRS': 'PARIS BASKETBALL',
    'ROA': 'CHORALE ROANNE',
    'ULK': 'FENERBAHCE',
    'JOV': 'JOVENTUT DE BADALONA',
    'PAM': 'VALENCIA BASKET',
    'SIE': 'SIENA',
    'ZAG': 'ZAGREB',
    'TIV': 'KRASNODAR',
    'NOV': 'NOVGOROD',
    'NAN': 'NANCY',
    'UNK': 'UNICS KAZAN',
    'MAR': 'MAROUSSI',
    'BES': 'BESIKTAS',
    'SAS': 'SASSARI',
    'NIK': 'BUDIVELNIK',
    'ZGO': 'ZGORZELEC',
    'ARI': 'ARIS',
    'ORL': 'ORLEANS',
    'KSK': 'PINAR KARSIYAKA IZMIR',
    'LEM': 'LE MANS',
    'NIO': 'PANIONIOS',
    'AVE': 'AIR AVELLINO',
    'CAN': 'GRAN CANARIA',
    'DYR': 'ZENIT ST PETERSBURGO',
    'GSS': 'STELMET ZIELONA GORA',
    'KLA': 'KLAIPEDA'
}

# Function to map team_id to team_name
def map_team_id_to_name(team_id):
    return team_id_to_name.get(team_id, team_id)  # Return the team_id if no match is found

# Apply the mapping to create the new 'team_name' column
df_teams['team_name'] = df_teams['team_id'].apply(map_team_id_to_name)


#tiene puntos infinitos por alguna razon
df_players = df_players[df_players['player'] != 'STELMAHERS, ROBERTS']  





# Function to simulate a season for a selected team
def simulate_season(team_id, df_teams, model):
    # Filter teams for the current season
    teams_current_season = df_teams[df_teams['season_code'] == 'E2024']
    teams = teams_current_season['team_id'].unique()
    
    # Ensure the selected team is valid
    if team_id not in teams:
        raise ValueError(f"Team ID {team_id} not found in the current season!")
    
    # Initialize record
    wins = 0
    losses = 0
    results = []  # Store detailed game results

    # Get stats for the selected team
    team_stats = df_teams[df_teams['team_id'] == team_id].iloc[0]

    # Simulate games against all other teams
    for opponent_id in teams:
        if opponent_id == team_id:
            continue  # Skip games against itself
        
        # Get stats for the opponent team
        opponent_stats = df_teams[df_teams['team_id'] == opponent_id].iloc[0]

        # Simulate game 1: selected team as local (team_a), opponent as away (team_b)
        input_data_local = pd.DataFrame([{
            'defensive_rebounds_a': team_stats['defensive_rebounds_per_game'],
            'offensive_rebounds_a': team_stats['offensive_rebounds_per_game'],
            'assists_a': team_stats['assists_per_game'],
            'three_points_made_a': team_stats['three_points_made_per_game'],
            'turnovers_a': team_stats['turnovers_per_game'],
            'blocks_favour_a': team_stats.get('blocks_favour_per_game', 0),
            'steals_a': team_stats.get('steals_per_game', 0),
            'defensive_rebounds_b': opponent_stats['defensive_rebounds_per_game'],
            'offensive_rebounds_b': opponent_stats['offensive_rebounds_per_game'],
            'assists_b': opponent_stats['assists_per_game'],
            'three_points_made_b': opponent_stats['three_points_made_per_game'],
            'turnovers_b': opponent_stats['turnovers_per_game'],
            'blocks_favour_b': opponent_stats.get('blocks_favour_per_game', 0),
            'steals_b': opponent_stats.get('steals_per_game', 0),
        }])

        # Predict scores
        predicted_scores_local = model.predict(input_data_local)
        points_a_local = predicted_scores_local[0][0]
        points_b_local = predicted_scores_local[0][1]

        # Determine the result
        if points_a_local > points_b_local:
            wins += 1
            results.append({'team_a': team_id, 'team_b': opponent_id, 'points_a': points_a_local, 'points_b': points_b_local, 'winner': team_id})
        else:
            losses += 1
            results.append({'team_a': team_id, 'team_b': opponent_id, 'points_a': points_a_local, 'points_b': points_b_local, 'winner': opponent_id})

        # Simulate game 2: selected team as away (team_b), opponent as local (team_a)
        input_data_away = pd.DataFrame([{
            'defensive_rebounds_a': opponent_stats['defensive_rebounds_per_game'],
            'offensive_rebounds_a': opponent_stats['offensive_rebounds_per_game'],
            'assists_a': opponent_stats['assists_per_game'],
            'three_points_made_a': opponent_stats['three_points_made_per_game'],
            'turnovers_a': opponent_stats['turnovers_per_game'],
            'blocks_favour_a': opponent_stats.get('blocks_favour_per_game', 0),
            'steals_a': opponent_stats.get('steals_per_game', 0),
            'defensive_rebounds_b': team_stats['defensive_rebounds_per_game'],
            'offensive_rebounds_b': team_stats['offensive_rebounds_per_game'],
            'assists_b': team_stats['assists_per_game'],
            'three_points_made_b': team_stats['three_points_made_per_game'],
            'turnovers_b': team_stats['turnovers_per_game'],
            'blocks_favour_b': team_stats.get('blocks_favour_per_game', 0),
            'steals_b': team_stats.get('steals_per_game', 0),
        }])

        # Predict scores
        predicted_scores_away = model.predict(input_data_away)
        points_a_away = predicted_scores_away[0][0]
        points_b_away = predicted_scores_away[0][1]

        # Determine the result
        if points_b_away > points_a_away:
            wins += 1
            results.append({'team_a': opponent_id, 'team_b': team_id, 'points_a': points_a_away, 'points_b': points_b_away, 'winner': team_id})
        else:
            losses += 1
            results.append({'team_a': opponent_id, 'team_b': team_id, 'points_a': points_a_away, 'points_b': points_b_away, 'winner': opponent_id})

    # Return the season record and detailed results
    return {'team_id': team_id, 'wins': wins, 'losses': losses, 'results': results}




