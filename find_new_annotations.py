# =======================================================================================================
# =======================================================================================================
# Topic: Find new functional annotations - chainsaw foldseek
# Date: 28/11/2023
# =======================================================================================================
# =======================================================================================================

# =======================================================================================================
# Import necessary statements
# =======================================================================================================
import os
import shutil
import numpy as np
import pandas as pd
import requests
import json

# =======================================================================================================
# Set path
# =======================================================================================================
no_matches_output_directory  = "/Users/liobaberndt/Desktop/Github/leishmania_chainsaw/no_ann"
foldseek_dir = '/Users/liobaberndt/Desktop/Github/leishmania_foldseek_results'
output_folder = '/Users/liobaberndt/Desktop/Github/foldseek_matching_files'
combined_data_folder = '/Users/liobaberndt/Desktop/Github/combined_data'
base_url = "https://www.ebi.ac.uk/pdbe/api/mappings/"

# =======================================================================================================
# Foldseek similarity annotations
# =======================================================================================================
def main():
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(combined_data_folder, exist_ok=True)
# -------------------------------------------------------------------------------------------------------
# Load uniport_ids
# -------------------------------------------------------------------------------------------------------
    for fname in os.listdir(no_matches_output_directory):
        uniprot_id = fname.split('_data')[0]
# -------------------------------------------------------------------------------------------------------
# Look for uniprot_ids in foldseek folder
# -------------------------------------------------------------------------------------------------------
        foldseek_df = look_for_foldseek_match(uniprot_id)
# -------------------------------------------------------------------------------------------------------
# No foldseek match 
# -------------------------------------------------------------------------------------------------------
        if foldseek_df is None:
            print("None")
            continue
# -------------------------------------------------------------------------------------------------------
# Foldseek match and log10 value of less than -5
# -------------------------------------------------------------------------------------------------------
        if foldseek_df.log10_evalue.min() < -5:
            print(uniprot_id)
            copy_matching_files(uniprot_id)
# -------------------------------------------------------------------------------------------------------
# Get subject_id for matches log10 value of less than -5
# -------------------------------------------------------------------------------------------------------
            for _, row in foldseek_df.iterrows():
                subject_id = row['subject_id']
                first_four_letters = subject_id[:4]
# -------------------------------------------------------------------------------------------------------
# Get json data from https://www.ebi.ac.uk/pdbe/api/mappings/ for pdb_id
# -------------------------------------------------------------------------------------------------------
                api_data = query_pdbe_api(first_four_letters)
                pdb_id = row['subject_id'].split('_')[0]
                output_filename = f"{pdb_id}_combined_data.json"
                output_filepath = os.path.join(combined_data_folder, output_filename)
# -------------------------------------------------------------------------------------------------------
# Combine information foldseek and api_data + save
# -------------------------------------------------------------------------------------------------------
                combined_data = {"foldseek_data": row.to_dict(), "pdbe_api_data": api_data}
                with open(output_filepath, 'w') as json_file:
                   json.dump(combined_data, json_file)
                print(f"Saved combined data for {pdb_id} to {output_filename}")
            else:
                print(f"Skipping {subject_id} due to API error")
# -------------------------------------------------------------------------------------------------------
# Define look_for_foldseek_match
# -------------------------------------------------------------------------------------------------------
def look_for_foldseek_match(uniprot_id):
# -------------------------------------------------------------------------------------------------------
# Names foldseek cols
# -------------------------------------------------------------------------------------------------------
    foldseek_results_cols = ['query_id', 'subject_id', 'pct_id', 'aln_len',
                             'mismatches', 'gap_openings', 'q_start', 'q_end',
                             's_start', 's_end', 'evalue', 'bit_score']
    foldseek_files = [f for f in os.listdir(foldseek_dir) if uniprot_id in f]
# -------------------------------------------------------------------------------------------------------
# No matches
# -------------------------------------------------------------------------------------------------------
    if len(foldseek_files) == 0:
        return None
    else:
        for fname in foldseek_files:
# -------------------------------------------------------------------------------------------------------
# Load folseek file
# -------------------------------------------------------------------------------------------------------
            try:
                df = pd.read_csv(os.path.join(foldseek_dir, fname), header=None, sep='\t')
            except pd.errors.EmptyDataError:
                continue
            if len(df) > 0:
                df.columns = foldseek_results_cols
# -------------------------------------------------------------------------------------------------------
# Find log10 value
# -------------------------------------------------------------------------------------------------------
                df['log10_evalue'] = df.evalue.apply(lambda x: np.log10(x))
                print(df)
                return df
# -------------------------------------------------------------------------------------------------------
# Define copy_matching_files
# -------------------------------------------------------------------------------------------------------
def copy_matching_files(uniprot_id):
    foldseek_files = os.listdir(foldseek_dir)
    condition = lambda fname: f'F-{uniprot_id}-F' in fname
    for fname in foldseek_files:
        if condition(fname):
            shutil.copy(
                os.path.join(foldseek_dir, fname),
                os.path.join(output_folder, fname)
            )
# -------------------------------------------------------------------------------------------------------
# Define query_pdbe_api
# -------------------------------------------------------------------------------------------------------
def query_pdbe_api(first_four_letters):
    api_url = f"{base_url}{first_four_letters}"
    response = requests.get(api_url)
# -------------------------------------------------------------------------------------------------------
# If annoations found
# -------------------------------------------------------------------------------------------------------
    if response.status_code == 200:
        api_data = response.json()
        print(f"PDBe API data for {first_four_letters}: {api_data}")
        print(response.text)
        return api_data
# -------------------------------------------------------------------------------------------------------
# If no annoations 
# -------------------------------------------------------------------------------------------------------
    else:
        print(f"Error querying PDBe API for {first_four_letters}. Status code: {response.status_code}")
        return None
# -------------------------------------------------------------------------------------------------------
# Call main()
# -------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()