"""
iterates through the files in the chainsaw directory
for each uniprot id extracted from the filename
get the functional annotations associated with that protein
save the functional annotations in a file which includes
which residues are associated with the functional annotation
"""

import os
import requests
import xml.etree.ElementTree as ET

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
    chainsaw_domain_directory = "../data_for_domdet/discover_cath_domains/leishmania_chainsaw_domains"
    main()