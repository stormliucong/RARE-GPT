import os
import requests
import re

def is_gene_name(gene):
    return gene.isupper()

def is_gene_line(line):
    # remove leading . or _
    line = line.strip()
    # match 1. or 1_(gene_name)
    if '.' in line:
        split_line = line.split('.')
        if split_line[0].isdigit():
            if is_gene_name(split_line[1].strip()):
                return True
    elif ',' in line:
        split_line = line.split(',')
        for gene in split_line:
            if not is_gene_name(gene.strip()):
                return False
        return True
    else:
        return False
    return False       



dx_dict = {}
data_folder = '/Users/cl3720/Desktop/copilot-examples/GPT_Gene_Prioritization/Data/Original_data'

with open(os.path.join(data_folder, 'probe_info')) as f:
    for line in f:
        line = line.strip()
        # change multiple spaces or tabs to a single tab
        while '  ' in line:
            line = line.replace('  ', ' ')
        line = line.replace(' ', '\t')
        line = line.split('\t')
        # get the first element
        folder_name = line[0]
        # get the second element
        file_name = line[1]
        # get the third element
        gene = line[2]
        
        # get the full path of the file
        file_path = os.path.join(data_folder, folder_name, file_name)
        # add to dict. key: file name, value: gene
        dx_dict[file_path] = gene.strip()


# go over all files in a directory
results = []
for file_path in dx_dict.keys():
    dx_gene = dx_dict[file_path]
    file_name = os.path.basename(file_path)
    folder_name = os.path.basename(os.path.dirname(file_path))
    result = {}
    result['file_path'] = file_path
    result['dx_gene'] = dx_gene


    for top_n in ['5', '10', '50']:
        result['predict_made_in_top_'+top_n] = 0
        result['predict_correct_in_top_'+top_n] = 0
        output_path = os.path.join('.', 'Data', 'GPT_response', 'top_' + top_n, folder_name, file_name)
        output_error_path = os.path.join('.', 'Data', 'GPT_response', 'top_' + top_n, folder_name, file_name + '_error')    

        if os.path.exists(output_path):
            # open output_path
            with open(output_path) as f:
                try:
                    output_content = f.read()
                    lines = output_content.splitlines()
                    for line in lines:
                        if is_gene_line(line):
                            result['predict_made_in_top_'+top_n] = 1
                            genes = line.strip().split(',')
                            for gene in genes:
                                gene = gene.strip()
                                if dx_gene == gene.strip():
                                    result['predict_correct_in_top_'+top_n] = 1 # predicted in top n and correct
                                    break
                except Exception as e:
                    print(e)
    results.append(result)



# convert dictionary to csv
import csv
with open('/Users/cl3720/Desktop/copilot-examples/GPT_Gene_Prioritization/Data/Results/GPT4_top_prediction.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['file_path', 'dx_gene', 'predict_made_in_top_5', 'predict_correct_in_top_5', 'predict_made_in_top_10', 'predict_correct_in_top_10', 'predict_made_in_top_50', 'predict_correct_in_top_50'])
    writer.writeheader()
    for result in results:
        writer.writerow(result)

                
                
