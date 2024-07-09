import re

m_pronouns = ["He", "Him", "His", "he", "him", "his"]
f_pronouns = ["She", "Her", "Hers", "she", "her", "hers"]
pronoun_pairs = {"He":"She", "Him":"Her", "His":"Hers", "he":"she", "him":"her", "his":"her", "She":"He", "Her":"Him", "Hers":"His", "she":"her", "her":"him", "hers":"his"}

def evaluate_gender(context_dict):
    """
    Calculate the gender split for a given translation context.

    Args:
        context_dict (dict of dict of dict): the dictionary of a given context; for example limited-context or no-context.

    Returns:
        male_percentage: the percentage sentences that inferred a masculine pronoun
        female_percentage: the percentage sentences that inferred a masculine pronoun
    """
    inferred_male = 0
    inferred_female = 0
    for key in context_dict.keys():
        for sentence_id in context_dict[key].keys():
            translated_sentence = context_dict[key][sentence_id]["translated_sentence"]
            pronoun = find_pronoun(translated_sentence)
            if pronoun in m_pronouns:
                inferred_male += 1
            elif pronoun in f_pronouns:
                inferred_female += 1
    
    total = inferred_male + inferred_female
    male_percentage = (inferred_male / total) * 100
    female_percentage = (inferred_female / total) * 100
    return male_percentage, female_percentage

    

# used within full_context to evaluate if the translated genders agree with the original genders in the sentence
# returns true or false
def gender_agreement(expected_rel, translation, gen_probabilities):
    """
    Checks to see if the pronoun in the translated sentence matches the expected pronoun.

    Args:
        expected_rel (str): the expected gender of the relationship; either "male" or "female"
        translation (str): the translated text to check
        gen_probabilities (dict of dict): the probabilities of word generation given by the translate function

    Returns:
        male_percentage: the percentage sentences that inferred a masculine pronoun
        female_percentage: the percentage sentences that inferred a masculine pronoun
    """
    translated_pronoun = find_pronoun(translation)

    if expected_rel == "male":
        if translated_pronoun not in m_pronouns:
            given_prob, op_prob = compare_gender_probabilities(translated_pronoun, gen_probabilities)
            return False, (given_prob - op_prob)
    elif expected_rel == "female":
        if translated_pronoun not in f_pronouns:
            given_prob, op_prob = compare_gender_probabilities(translated_pronoun, gen_probabilities)
            return False, (given_prob - op_prob)
    
    return True, 0

def compare_gender_probabilities(pronoun, gen_probabilities):
    """
    Compares the probability of the translated pronoun with the expected pronoun

    Args:
        pronoun (str): the pronoun in a given translation
        gen_probabilities (dict of dict): the probabilities of word generation given by the translate function

    Returns:
        given_prob: the probability, as a decimal, of the given pronoun
        opp_prob: the probability, as a decimal, of the expected pronoun
    """
    gen_probs_pronoun = gen_probabilities[pronoun]

    opp_pronoun = None

    for p in pronoun_pairs.keys():
        if pronoun == p:
            opp_pronoun = pronoun_pairs[p]

    if opp_pronoun:
        given_prob = 0
        if pronoun in gen_probs_pronoun.keys():
            given_prob = gen_probs_pronoun[pronoun]
        opp_prob = 0
        if opp_pronoun in gen_probs_pronoun.keys():
            opp_prob = gen_probs_pronoun[opp_pronoun]

        return given_prob, opp_prob

def find_pronoun(translation):
    """
    Finds the pronoun in the translated sentence.

    Args:
        translation (str): the translation with a pronoun to search for

    Returns:
        pronoun (str): the pronoun found in the translated sentence
    """
    for pronoun in m_pronouns:
        for word in translation.split(" "):
            if re.fullmatch(pronoun, word):
                return pronoun
    for pronoun in f_pronouns:
        for word in translation.split(" "):
            if re.fullmatch(pronoun, word):
                return pronoun
            
def average_results(translations):
    results = ""
    for dict_key in translations.keys():
        if dict_key == "full_context":
            results = results + " \n"
            for case_key in translations[dict_key].keys():
                case = "error"
                if case_key == "male_occ+male_relation":
                    case = "Male / Male relationship"
                elif case_key == "male_occ+female_relation":
                    case = "Male / Female relationship"
                elif case_key == "female_occ+male_relation":
                    case = "Female / Male relationship"
                elif case_key == "female_occ+female_relation":
                    case = "Female / Female relationship"
                results = results + "\n" + case + ": "
                case_avg = 0
                total_false = 0
                for sentence_key in translations[dict_key][case_key].keys():
                    if translations[dict_key][case_key][sentence_key]["correct"] == False:
                        diff_prob = translations[dict_key][case_key][sentence_key]["diff_prob"]
                        case_avg += diff_prob
                        total_false += 1
                if total_false != 0:
                    case_avg = case_avg / total_false
                    case_prob = case_avg*100
                else:
                    case_prob = 0.00
                results = results + "`" + str(case_prob) + " %` \n"

    return results

def count_results(results):
    """
    Counts the results and prints the correct and incorrent numbers for each context

    Args:
        results (dict of dict of dict of dict): the translations dictionary in main
    """
    result_str = ""
    for dict_key in results.keys():
        if dict_key == "full_context":
            result_str = result_str + " \n"
            for case_key in results[dict_key].keys():
                case = "error"
                if case_key == "male_occ+male_relation":
                    case = "Male / Male relationship"
                elif case_key == "male_occ+female_relation":
                    case = "Male / Female relationship"
                elif case_key == "female_occ+male_relation":
                    case = "Female / Male relationship"
                elif case_key == "female_occ+female_relation":
                    case = "Female / Female relationship"
                result_str = result_str + "\n" + case + ": "
                correct = 0
                incorrect = 0
                for sentence_id in results[dict_key][case_key].keys():
                    if results[dict_key][case_key][sentence_id]["correct"] == True:
                        correct += 1
                    elif results[dict_key][case_key][sentence_id]["correct"] == False:
                        incorrect += 1
                result_str = result_str + "`" + str(correct) + " Correct`, `" + str(incorrect) + " Incorrect`\n"
    
    return result_str
