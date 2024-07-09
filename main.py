from translate import translate
from analyze import gender_agreement, average_results, count_results, evaluate_gender
from batch import batch_process_csv
from utilities import assignToDictionary
import sys

from tqdm import tqdm
from multiprocessing import Pool

translations = {}

lim_cont_masc = float()
lim_cont_fem = float()
no_cont_masc = float()
no_cont_fem = float()

total_sent = int()
full_c = int()
lim_c = int()
no_c = int()

filename = ""

scope = sys.argv[1]

if scope == "all":
    filename = "sentences_all.csv"
elif scope == "test":
    filename = "sentences_test.csv"
elif scope == "mini_test":
    filename = "sentences_mini_test.csv"

job_number = sys.argv[2]

# put within some loop to do multiple times, and strings accessed from csv file with sentences
with open(filename, 'r') as file:
    
    #Load the sentences from the CSV and batch them into contexts
    full_context, limited_context, no_context = batch_process_csv(file)
    #Create a dictionary of the contexts that can be iterated through
    contexts = {"full_context":full_context, "limited_context":limited_context,"no_context":no_context}
    
    sentence_id = 0
    full_context = 0
    limited_context = 0
    no_context = 0

    for context in tqdm(contexts.keys(), desc="Context loop"):
        translations[context] = {}
        for relation in tqdm(contexts[context].keys(), desc="Relation loop"):  # for relation in contexts[context].keys():
            translations[context][relation] = {}
            for sentence in tqdm(contexts[context][relation], desc="Sentence loop"):  # for sentence in contexts[context][relation]:
                sentence_id += 1
                if context == "full_context":
                    full_context += 1
                    translation, decoded_translation, probs = translate(sentence)
                    gender = ""
                    if relation == "male_occ+male_relation" or relation == "male_occ+female_relation":
                        gender = "male" #the desired pronoun is masculine
                    elif relation == "female_occ+female_relation" or relation == "female_occ+male_relation":
                        gender = "female" #the desired pronoun is feminine
                    result, diff_prob = gender_agreement(gender, decoded_translation, probs)
                    assignToDictionary(sentence_id, result, diff_prob, context, relation, decoded_translation, sentence, translations)
                elif context == "limited_context":
                    limited_context += 1
                    _, decoded_translation, _ = translate(sentence)
                    assignToDictionary(sentence_id, False, 0, context, relation, decoded_translation, sentence, translations)
                elif context == "no_context":
                    no_context += 1
                    _, decoded_translation, _ = translate(sentence)
                    assignToDictionary(sentence_id, False, 0, context, relation, decoded_translation, sentence, translations)

    total_sent = sentence_id
    full_c = full_context
    lim_c = limited_context
    no_c = no_context

    lim_cont_masc, lim_cont_fem = evaluate_gender(translations["limited_context"])
    no_cont_masc, no_cont_fem = evaluate_gender(translations["no_context"])

file.close()

results_filename = "./results/results_" + scope + "_" + job_number + ".md"

with open(results_filename, 'w') as output:
    output.write("# Overview\n")
    output.write("#### " + str(total_sent) + " total sentences translated.\n")

    output.write("\n## No Context Results\n")
    output.write("#### " + str(no_c) + " sentences.\n\n")
    output.write("Inferred Masculine: `" + str(no_cont_masc) + " %` " + "\n\nInferred Feminine: `" + str(no_cont_fem) + " %`\n")

    output.write("\n## Limited Context Results\n")
    output.write("#### " + str(lim_c) + " sentences.\n\n")
    output.write("Inferred Masculine: `" + str(lim_cont_masc) + " %` " + "\n\nInferred Feminine: `" + str(lim_cont_fem) + " %`\n")

    output.write("\n## Full Context Results\n")
    output.write("#### " + str(full_c) + " sentences.\n")
    output.write("\n### Number of Correct vs Incorrect Translations:" + count_results(translations))
    output.write("\n### Average bias differential for incorrect translations in:" + average_results(translations))
    output.write("\n##### Note: the bias differential refers to how much more likely the incorrectly translated gender was than the correct gender, i.e. the probability of the word in the actual translation minus the probability of the correct translation, averaged for all mis-translations within a sentence classification (e.g. Male / Male)")
output.close()
