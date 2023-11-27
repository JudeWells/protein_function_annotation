# =======================================================================================================
# =======================================================================================================
# Topic: Identifying functional annotations - chainsaw 
# Date: 22/11/2023
# =======================================================================================================
# =======================================================================================================

# =======================================================================================================
# Import necessary statements
# =======================================================================================================
import os
import re
import csv
import json
import requests
import xml.etree.ElementTree as ET

# =======================================================================================================
# Set path
# =======================================================================================================
directory_path = "/Users/liobaberndt/Desktop/Github/leishmania_chainsaw_csv"
output_file_path = "/Users/liobaberndt/Desktop/Github/leishmania_chainsaw/uniprot_ids.cs"
matches_output_directory = "/Users/liobaberndt/Desktop/Github/leishmania_chainsaw/ann"
no_matches_output_directory  = "/Users/liobaberndt/Desktop/Github/leishmania_chainsaw/no_ann"

# =======================================================================================================
# Extract uniport_id from chainsaw
# =======================================================================================================
# -------------------------------------------------------------------------------------------------------
# Define pattern uniport_id
# -------------------------------------------------------------------------------------------------------
def extract_uniprot_id_from_chain(chain_id):
    pattern = r'F-(.*?)-F'
    match = re.search(pattern, chain_id)
    if match:
        return match.group(1)
    return None
# -------------------------------------------------------------------------------------------------------
# Define function process_csv_files
# -------------------------------------------------------------------------------------------------------
def process_csv_files(directory_path, output_file_path):
# -------------------------------------------------------------------------------------------------------
# Create output csv file for uniport_ids
# -------------------------------------------------------------------------------------------------------
    with open(output_file_path, 'w', newline='') as output_csv:
        csv_writer = csv.writer(output_csv)
        csv_writer.writerow(['UniProt ID'])
# -------------------------------------------------------------------------------------------------------
# Iterate through csv input files 
# -------------------------------------------------------------------------------------------------------
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            if os.path.isfile(file_path) and filename.endswith('.csv'):
                with open(file_path, 'r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
# -------------------------------------------------------------------------------------------------------
# Extract uniport_id
# -------------------------------------------------------------------------------------------------------
                    for row in csv_reader:
                        uniprot_id = extract_uniprot_id_from_chain(row.get('chain_id', ''))
# -------------------------------------------------------------------------------------------------------
# Wite uniport_id in output file
# -------------------------------------------------------------------------------------------------------
                        if uniprot_id:
                            csv_writer.writerow([uniprot_id])
# -------------------------------------------------------------------------------------------------------
# Call process_csv_files function
# -------------------------------------------------------------------------------------------------------
process_csv_files(directory_path, output_file_path)

# =======================================================================================================
# Find functional annotations Interpro database
# =======================================================================================================
# -------------------------------------------------------------------------------------------------------
# Loop uniprot_ids
# -------------------------------------------------------------------------------------------------------
def process_uniprot_ids_from_csv(output_file_path):
    uniprot_ids = []

    # Read UniProt IDs from the CSV file
    with open(output_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            uniprot_id = row.get('UniProt ID', '')
            if uniprot_id:
                uniprot_ids.append(uniprot_id)
    return uniprot_ids
# -------------------------------------------------------------------------------------------------------
# Define function get_interpro_annotations
# -------------------------------------------------------------------------------------------------------
def get_interpro_annotations(uniprot_id):
    interpro_api_url = f"https://www.ebi.ac.uk/interpro/api/protein/UniProt/{uniprot_id}"
    response = requests.get(interpro_api_url)
    print(f"Status code for {uniprot_id}: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Warning: The server responded with a non-200 status code ({response.status_code}).")
        return None
# -------------------------------------------------------------------------------------------------------
# Define save json information
# -------------------------------------------------------------------------------------------------------
def save_json_data(directory, uniprot_id, json_data):
    if not os.path.exists(directory):
        os.makedirs(directory)
    json_file_path = os.path.join(directory, f"{uniprot_id}_data.json")
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
# -------------------------------------------------------------------------------------------------------
# Define main
# -------------------------------------------------------------------------------------------------------
def main():
# -------------------------------------------------------------------------------------------------------
# Get UniProt IDs from the CSV file
# -------------------------------------------------------------------------------------------------------
    uniprot_ids = process_uniprot_ids_from_csv(output_file_path)
# -------------------------------------------------------------------------------------------------------
# Process each UniProt ID
# -------------------------------------------------------------------------------------------------------
    for uniprot_id in uniprot_ids:
        annotations = get_interpro_annotations(uniprot_id)
        print(annotations)
        print(f"\nUniProt ID: {uniprot_id}")
# -------------------------------------------------------------------------------------------------------
# If there are annotations
# -------------------------------------------------------------------------------------------------------
        if annotations:
          print("Functional annotations:")
# -------------------------------------------------------------------------------------------------------
# Check if name is 'uncharacterized' and go_terms='None'
# -------------------------------------------------------------------------------------------------------
          if annotations and 'metadata' in annotations:
             metadata = annotations['metadata']
             if 'name' in metadata:
               print("Name:", metadata['name'])
               if metadata['name'].lower() == 'uncharacterized protein' and metadata.get('go_terms') is None:
                  print("Conditions met, saving to no matches file.")
                  save_json_data(no_matches_output_directory, uniprot_id, annotations)
               else:
                  print("Conditions not met, saving to matches file.")
                  save_json_data(matches_output_directory, uniprot_id, annotations)
             else:
               print("Name not available.")
          else:
            print("Result is None or missing metadata.")
# -------------------------------------------------------------------------------------------------------
# If no annotations
# -------------------------------------------------------------------------------------------------------
        else:
           print("No functional annotations found. Saving to no matches file.")
           save_json_data(no_matches_output_directory, uniprot_id, annotations)
# -------------------------------------------------------------------------------------------------------
# Call main function
# -------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()