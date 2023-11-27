import os

import numpy as np
import pandas as pd

"""
Checks uniprot IDs in the no_annotation folder 
and looks for matches in the foldseek results
checks if there is a foldseek match that has 
a log10 evalue of less than -5

TODO: for each of the foldseek matches, check if 
there is any annotation in InterPro (or similar)

"""

def main():
    for fname in os.listdir('no_annotation'):
        uniprot_id = fname.split('_data')[0]
        foldseek_df = look_for_foldseek_match(uniprot_id)
        if foldseek_df is None:
            continue
        if foldseek_df.log10_evalue.min() < -10:
            bp=1

def look_for_foldseek_match(uniprot_id):
    foldseek_results_cols = ['query_id', 'subject_id', 'pct_id', 'aln_len',
                             'mismatches', 'gap_openings', 'q_start', 'q_end',
                             's_start', 's_end', 'evalue', 'bit_score']


    foldseek_files = [f for f in os.listdir(foldseek_dir) if uniprot_id in f]
    if len(foldseek_files) == 0:
        return None
    else:
        for fname in foldseek_files:
            try:
                df = pd.read_csv(os.path.join(foldseek_dir, fname), header=None, sep='\t')
            except pd.errors.EmptyDataError:
                continue
            if len(df) > 0:
                df.columns = foldseek_results_cols
                df['log10_evalue'] = df.evalue.apply(lambda x: np.log10(x))
                return df

if __name__ == '__main__':
    foldseek_dir = '../data_for_domdet/discover_cath_domains/leishmania_chainsaw_foldseek_preds/leishmania_foldseek_results'
    main()