import os
import requests
import re
import pandas as pd

def find_all_possible_gene_names(text):
    gene_regex = r'\b[A-Z]{2,}\d?\b'
    gene_list = re.findall(gene_regex, text)
    return gene_list

dx_dict = {}
data_folder = './Data/free_text_input/'

free_text_df = pd.read_csv(os.path.join(data_folder, 'free_text_pmid_input.csv'))
free_text_df_subset = free_text_df # for test purpose.

# go over all files in a directory
results = []
for index, row in free_text_df_subset.iterrows():
    free_text = row['Free-text']
    id = row['ID']
    dx_gene = row['Gene']
    seq = str(row['Sequence'])
    
    result = {}
    result['dx_gene'] = dx_gene
    result['file_path'] = id + '_' + seq

    for top_n in ['5', '10', '50']:
        result['predict_made_in_top_'+top_n] = 0
        result['predict_correct_in_top_'+top_n] = 0
        output_path = os.path.join('.', 'Data', 'free_text_input', 'GPT_response', 'top_' + top_n, id + '_' + seq)
        output_error_path = os.path.join('.', 'Data', 'free_text_input', 'GPT_response', 'top_' + top_n, id + '_' + seq + '_error')    

        if os.path.exists(output_path):
            # open output_path
            with open(output_path) as f:
                try:
                    output_content = f.read()
                    gene_list = find_all_possible_gene_names(output_content)
                    if len(gene_list) >= 5:
                        result['predict_made_in_top_'+top_n] = 1
                        if dx_gene in gene_list:
                            result['predict_correct_in_top_'+top_n] = 1 # predicted in top n and correct
                except Exception as e:
                    print(e)
    results.append(result)



# convert dictionary to csv
import csv
with open('./Data/free_text_input/Results/GPT4_top_prediction_RE.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['file_path', 'dx_gene', 'predict_made_in_top_5', 'predict_correct_in_top_5', 'predict_made_in_top_10', 'predict_correct_in_top_10', 'predict_made_in_top_50', 'predict_correct_in_top_50'])
    writer.writeheader()
    for result in results:
        writer.writerow(result)

                
                
