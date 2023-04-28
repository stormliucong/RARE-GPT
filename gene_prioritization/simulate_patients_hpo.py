import uuid 
import os
import random




data_output_path = './Data/simulated_pt_input/Original_data'
data_input_path = './Data/HPO_input/Original_data'

if not os.path.isfile(os.path.join(data_output_path, 'hp_id_list.txt')):
    from owlready2 import *
    onto = get_ontology("http://purl.obolibrary.org/obo/hp.owl").load()
    obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
    ontology_classes = obo.HP_0000118.descendants()

    hp_id_list = []
    for current_class in ontology_classes:
        hp_id = current_class.name.replace('_', ':')
        hp_id_list.append(hp_id)

    with open(os.path.join(data_output_path,'hp_id_list.txt'),'w') as f:
        f.write('\n'.join(hp_id_list))

else:
    for root, directories, files in os.walk(data_input_path):
        if root == data_input_path:
            # If it is, skip to the next iteration
            continue
        # Create the new directory structure in the new folder
        new_directory = root.replace(data_input_path, data_output_path)
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)
        # Iterate over all files within the current directory
        for file in files:
            # Create the new file path with the prefix and the same directory structure
            old_file_path = os.path.join(root, file)
            with open(old_file_path, 'r') as f:
                hp_list = [i.strip() for i in f.readlines()]
                hp_list_length = len(hp_list)
                if hp_list_length > 1:
                    sampled_items = random.sample(hp_list, hp_list_length)
                    new_file_path = os.path.join(new_directory, file)
                    # Copy the file to the new path with the modified prefix
                    with open(new_file_path, 'w') as f:
                        f.write('\n'.join(sampled_items))
