"""
iterates through the files in the chainsaw directory
for each uniprot id extracted from the filename
get the functional annotations associated with that protein
save the functional annotations in a file which includes
which residues are associated with the functional annotation
"""

import os
import requests

def extract_uniprot_id_from_filename(filename):
    return filename.split("-")[1]

def main():
    for file_name in os.listdir(chainsaw_domain_directory):
        uniprot_id = extract_uniprot_id_from_filename(file_name)


if __name__=="__main__":
    chainsaw_domain_directory = "../data_for_domdet/discover_cath_domains/leishmania_chainsaw_domains"
    main()