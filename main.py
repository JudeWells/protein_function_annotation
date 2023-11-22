# =======================================================================================================
# =======================================================================================================
# Topic: Identifying functional annotations - chainsaw 
# Date: 22/11/2023
# Note: Script is not properly working yet 
# =======================================================================================================
# =======================================================================================================

# =======================================================================================================
# Import necessary statements
# =======================================================================================================
import os
import re
import csv
import requests
import xml.etree.ElementTree as ET

# =======================================================================================================
# Set path
# =======================================================================================================
directory_path = "/Users/liobaberndt/Desktop/Github/leishmania_chainsaw_csv"
output_file_path = "/Users/liobaberndt/Desktop/Github/leishmania_chainsaw/uniprot_ids.csv"
annotation_file_path = "/Users/liobaberndt/Desktop/Github/leishmania_chainsaw/ann.csv"
no_annotation_file_path = "/Users/liobaberndt/Desktop/Github/leishmania_chainsaw/no_ann.csv"

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
# Define function get_interpro_annotations
# -------------------------------------------------------------------------------------------------------
def get_interpro_annotations(uniprot_id):
    interpro_api_url = f"https://www.ebi.ac.uk/interpro/api/protein/{uniprot_id}"
    response = requests.get(interpro_api_url)
    if response.status_code == 200:
        data = response.json()
        if 'entries' in data:
            return data['entries']
    return None
# -------------------------------------------------------------------------------------------------------
# Define function process_uniprot_ids
# -------------------------------------------------------------------------------------------------------
def process_uniprot_ids(output_file_path, annotation_file_path, no_annotation_file_path):
# -------------------------------------------------------------------------------------------------------
# Create annotation file
# -------------------------------------------------------------------------------------------------------
    with open(annotation_file_path, 'w', newline='') as annotation_csv:
        annotation_writer = csv.writer(annotation_csv)
        annotation_writer.writerow(['UniProt ID', 'Functional Annotation'])
# -------------------------------------------------------------------------------------------------------
# Create no annotation file
# -------------------------------------------------------------------------------------------------------
        with open(no_annotation_file_path, 'w', newline='') as no_annotation_csv:
            no_annotation_writer = csv.writer(no_annotation_csv)
            no_annotation_writer.writerow(['UniProt ID'])
# -------------------------------------------------------------------------------------------------------
# Get uniprot_id
# -------------------------------------------------------------------------------------------------------
            with open(output_file_path, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                uniprot_ids = [row.get('UniProt ID', '') for row in csv_reader]
# -------------------------------------------------------------------------------------------------------
# Loop over uniprot_ids
# -------------------------------------------------------------------------------------------------------
                for uniprot_id in uniprot_ids:
                    annotations = get_interpro_annotations(uniprot_id)
                    print(f"\nUniProt ID: {uniprot_id}")
# -------------------------------------------------------------------------------------------------------
# If annotation
# -------------------------------------------------------------------------------------------------------    
                if annotations is not None:  
                        if annotations:
                            print("Functional annotations:")
                            for entry in annotations:
                                print(f"- {entry['name']} ({entry['type']})")
                                annotation_writer.writerow([uniprot_id, f"{entry['name']} ({entry['type']})"])
                        else:
                            print("No functional annotations found.")
                            if all(
                                entry['name'].lower() == 'uncharacterized' and entry.get('go_terms') == 'None' 
                                for entry in annotations
                            ):
                                print("Adding to no annotation file.")
                                no_annotation_writer.writerow([uniprot_id])
# -------------------------------------------------------------------------------------------------------
# If no annotation
# -------------------------------------------------------------------------------------------------------
                else:
                        print("Error: No annotations available for this UniProt ID.")
                        no_annotation_writer.writerow([uniprot_id])
# -------------------------------------------------------------------------------------------------------
# Call function process_uniprot_ids
# -------------------------------------------------------------------------------------------------------
process_uniprot_ids(output_file_path, annotation_file_path, no_annotation_file_path)







"""
 import os
 import requests
 import xml.etree.ElementTree as 


def query_uniprot(uniprot_id):
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.xml"
    response = requests.get(url)
    if response.status_code == 200:
        return ET.fromstring(response.content)
    return None

def query_interpro(uniprot_id):
    url = f"https://www.ebi.ac.uk/interpro/api/protein/UniProt/{uniprot_id}/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def query_gene_ontology(uniprot_id):
    url = f"https://www.ebi.ac.uk/QuickGO/services/annotation/search?geneProductId={uniprot_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def extract_and_save_annotations(uniprot_id):
    uniprot_data = query_uniprot(uniprot_id)
    interpro_data = query_interpro(uniprot_id)
    go_data = query_gene_ontology(uniprot_id)

    # Here you can extract specific data from these responses and save them as needed
    # For example, let's just print out the responses
    print("UniProt Data:", uniprot_data)
    print("InterPro Data:", interpro_data)
    print("GO Data:", go_data)

def extract_uniprot_id_from_filename(filename):
    return filename.split("-")[1]

def main():
    for file_name in os.listdir(chainsaw_domain_directory):
        uniprot_id = extract_uniprot_id_from_filename(file_name)
        extract_and_save_annotations(uniprot_id)


if __name__=="__main__":
    chainsaw_domain_directory = "../leishmania_chainsaw_domains"
    main()
"""