# protein_function_annotation
Look for protein domains (identified by Chainsaw) that might have novel functional annotations

Take as input a directory full of predicted Chainsaw domains (in the form of pdb files)
Extract the uniprot code for each pdb file
Extract the residue numbers and sequence associated with the predicted protein domain
Search for functional annotations on those domains

Data for leishmania infantum predicted domains can be found here:
https://drive.google.com/drive/folders/1De5hrmzyd8o6gtX0rfKPpalXjEhJwGA3?usp=sharing

You can work out which residues (and their corresponding indices) are included in each predicted domain 
from the PDB file (where there are multiple PDB files for each protein - each one containing a predicted domain)

Residue indexes can be extracted from columns 23-26 in ATOM lines in the PDB file.
Residue names can be extracted from columns 18-20 in ATOM lines.

Alternatively the Chainsaw predicted domains (written as residue indices) can be read
from the csv files in chainsaw_domains_csv in the google drive.
