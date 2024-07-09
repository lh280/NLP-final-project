import csv

def batch_process_csv(filepath):
    csv_reader = csv.reader(filepath)

    full_context = {"male_occ+male_relation":[], "male_occ+female_relation":[], "female_occ+male_relation":[], "female_occ+female_relation":[]}
    limited_context = {"male_occ+occ_verb":[], "female_occ+occ_verb":[], "male_name+rel_verb":[], "female_name+rel_verb":[]}
    no_context = {"occ_verb":[], "male_rel_verb":[], "female_rel_verb":[]}

    array_keys = list(full_context.keys()) + list(limited_context.keys()) + list(no_context.keys())
    index_line = 0
    for line in csv_reader:
        i = 0
        while i < len(line):
            if index_line < len(full_context.keys()):
                full_context[array_keys[index_line]].append(line[i])
            elif index_line < (len(full_context.keys()) + len(limited_context.keys())) :
                limited_context[array_keys[index_line]].append(line[i])
            elif index_line < (len(full_context.keys()) + len(limited_context.keys()) + len(no_context.keys())):
                no_context[array_keys[index_line]].append(line[i])
            i += 1
        index_line += 1

    return full_context, limited_context, no_context

