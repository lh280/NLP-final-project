import csv
import random


# converts sentence parameters into a small random subset of sentences
def gen_sentences_sample(csv_file):
    
    sentences = []
    num_sentences_of_each_type = 40

    csv_reader = csv.reader(csv_file)
    file_lines = []

    # process each line into elements
    for line in csv_reader:
        row = []
        i = 1
        while i < len(line):
            row += [line[i]]
            i += 1
        file_lines += [row]
    
    ### SENTENCES WITH FULL CONTEXT - 
    # GENDERED OCCUPATION w RELATIONSHIP VERB
    MM = []
    MF = []
    FM = []
    FF = []

    for i in range(0, num_sentences_of_each_type): 
        gender = random.choice([0, 1]) # M (0) or F (1) occ
        occ = random.choice(file_lines[gender])
        if gender == 0:
            gender_other = random.choice([6, 7]) # M (6) or F (7) rel verb
            v_phrase = random.choice(file_lines[gender_other])
            sentence = "El " + occ + " " + v_phrase + "."
            if gender_other == 6:
                MM += [sentence] 
            else:
                MF += [sentence] 
        else:
            gender_other = random.choice([6, 7]) # M (6) or F (7) rel verb
            v_phrase = random.choice(file_lines[gender_other])
            sentence = "La " + occ + " " + v_phrase + "."
            if gender_other == 6:
                FM += [sentence] 
            else:
                FF += [sentence] 
    
    with_context = [MM, MF, FM, FF]

    ### SENTENCES WITH LIMITED/INFERRED CONTEXT - 
    # GENDERED OCCUPATION w OCC VERB, NAME w RELATIONSHIP VERB
    occM_lim_context = []
    occF_lim_context = []
    name_relM_lim_context = []
    name_relF_lim_context = []

    for i in range(0, num_sentences_of_each_type):
        subj_type = random.choice([0,1]) # occ (0) or name (1) subject
        if subj_type == 0:
            gender = random.choice([0, 1]) # M (0) or F (1) occ
            occ = random.choice(file_lines[gender])
            v_phrase = random.choice(file_lines[4])
            sentence = "Su " + occ + " " + v_phrase + "."
            if gender == 0:
                occM_lim_context += [sentence]
            else:
                occF_lim_context += [sentence]
        else:
            name = random.choice(file_lines[3])
            gender_other = random.choice([6, 7]) # M (6) or F (7) rel verb
            v_phrase = random.choice(file_lines[gender_other])
            sentence = name + " " + v_phrase + "."
            if gender == 0:
                name_relM_lim_context += [sentence]
            else:
                name_relF_lim_context += [sentence]

    limited_context = [occM_lim_context, occF_lim_context, name_relM_lim_context, name_relF_lim_context]

    ### SENTENCES WITH NO CONTEXT - 
    # OCC VERB, RELATIONSHIP VERB
    occ_sent = []
    relM_sent = []
    relF_sent = []

    for i in range(0, num_sentences_of_each_type): 
        verb_type = random.choice([4, 6, 7]) # occ (4) or relM (6) or relF (7) verb
        v_phrase = random.choice(file_lines[verb_type])
        sentence = v_phrase.capitalize() + "."
        if verb_type == 4:
            occ_sent += [sentence]
        elif verb_type == 6:
            relM_sent += [sentence]
        else:
            relF_sent += [sentence]

    no_context = [occ_sent, relM_sent, relF_sent]

    sentences += [with_context, limited_context, no_context]
    
    return sentences



# converts sentence parameters into all possible combination of sentences
def gen_sentences_full(csv_file):
    
    sentences = []

    csv_reader = csv.reader(csv_file)
    file_lines = []

    # process each line into elements
    for line in csv_reader:
        row = []
        i = 1
        while i < len(line):
            row += [line[i]]
            i += 1
        file_lines += [row]
    
    ### subject
    # 0 - M occ
    # 1 - F occ
    # 3 - amb name

    ### verb phrase 
    # 4 - occupational
    # 6 - M rel 
    # 7 - F rel 

    relevant_lines = [ [0,1,3] , [4,6,7] ]
    
    ### all sentence groups
    # with context
    MM = []
    MF = []
    FM = []
    FF = []
    # limited context
    occM_lim_context = []
    occF_lim_context = []
    name_relM_lim_context = []
    name_relF_lim_context = []
    # no context
    occ_sent = []
    relM_sent = []
    relF_sent = []

    # with context and limited context
    for subj_type in relevant_lines[0]:
        for subject in range(0, len(file_lines[subj_type])-1):
            for verb_type in relevant_lines[1]:
                for verb in range(0, len(file_lines[verb_type])-1):
                    # create subject and verb phrase
                    subj = file_lines[subj_type][subject]
                    v_phrase = file_lines[verb_type][verb]

                    # construct sentences & add to correct list
                    if subj_type == 0: # M occ 
                        if verb_type == 4: # occ verb 
                            sentence = "Su " + subj + " " + v_phrase + "."
                            occM_lim_context += [sentence]
                        elif verb_type == 6: # M rel verb 
                            sentence = "El " + subj + " " + v_phrase + "."
                            MM += [sentence]
                        else: # F rel verb 
                            sentence = "El " + subj + " " + v_phrase + "."
                            MF += [sentence]
                    elif subj_type == 1: # F occ 
                        if verb_type == 4: # occ verb 
                            sentence = "Su " + subj + " " + v_phrase + "."
                            occF_lim_context += [sentence]
                        elif verb_type == 6: # M rel verb 
                            sentence = "La " + subj + " " + v_phrase + "."
                            FM += [sentence]
                        else: # F rel verb 
                            sentence = "La " + subj + " " + v_phrase + "."
                            FF += [sentence]
                    else: # amb name 
                        sentence = subj + " " + v_phrase + "."
                        if verb_type == 6: # M rel verb 
                            name_relM_lim_context += [sentence]
                        elif verb_type == 7: # F rel verb 
                            name_relF_lim_context += [sentence]

    # no context
    for verb_type in relevant_lines[1]:
        for verb in range(0, len(file_lines[verb_type])-1):
            # construct sentence
            sentence = file_lines[verb_type][verb].capitalize() + "."

            # add to correct list 
            if verb_type == 4: # occ verb 
                occ_sent += [sentence]
            elif verb_type == 6: # M rel verb 
                relM_sent += [sentence]
            else: # F rel verb 
                relF_sent += [sentence]
    
    with_context = [MM, MF, FM, FF]
    limited_context = [occM_lim_context, occF_lim_context, name_relM_lim_context, name_relF_lim_context]
    no_context = [occ_sent, relM_sent, relF_sent]

    sentences += [with_context, limited_context, no_context]
    
    return sentences



# converts sentence parameters (small set) as csv file
with open('./NLP-Homework/final-project/sentence_parameters_test.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    rows_list = [ #can expand any one row at will (the rows do not need to be the same length)
        ["es_male_occ", "abogado", "doctor", "enfermero", "profesor", "maestro", "jefe", "presidente", "ingeniero", "peluquero", "granjero"], 
        ["es_fem_occ", "abogada", "doctora", "enfermera", "profesora", "maestra", "jefa", "presidenta", "ingeniera", "peluquera", "granjera"], 
        ["en_occ", "lawyer", "doctor", "nurse", "professor", "teacher", "boss", "president", "engineer", "hairdresser", "farmer"], 
        ["amb_names", "Alex", "Max", "Angel", "Avery", "Sam", "Rory", "Skyler", "Charlie"], 
        ["es_verb_phrase_occ", "fue a Madrid para aprender la peluquería", "se fue de casa para asistir a la facultad de medicina", "me recetó unos medicamentos", "fue a la facultad de derecho para ejercer la abogacía", "mostró la presentación al CEO", "enseñó a los niños a contar", "chismea con los demás durante el descanso para comer", "salvó a la familia del edificio en llamas"], 
        ["en_verb_phrase_occ", "went to Madrid to learn hairdressing", "left home to attend medical school", "prescribed me some medicines", "went to law school to practice law", "showed the presentation to the CEO", "taught the children how to count", "gossips with the others during the lunch break", "saved the family from the burning building"], 
        ["es_verb_phrase_male_rel", "ama a su esposo", "besó a su marido", "toma de la mano a su novio cuando ven una película", "mira con amor a su prometido", "salió con su novio"], 
        ["es_verb_phrase_fem_rel", "ama a su esposa", "besó a su marida", "toma de la mano a su novia cuando ven una película", "mira con amor a su prometida", "salió con su novia"], 
        ["en_verb_phrase_male_rel", "loves #pos# husband", "kissed #pos# husband", "holds hands with #pos# boyfriend when they watch a movie", "looks lovingly at #pos# fiancé", "went on a date with #pos# boyfriend"], 
        ["en_verb_phrase_fem_rel", "loves #pos# wife", "kissed #pos# wife", "holds hands with #pos# girlfriend when they watch a movie", "looks lovingly at #pos# fiancée", "went on a date with #pos# girlfriend"]
        # #[tag]# denotes a genderless word in Spanish with a gendered equivalent in English
        # TAGS: pos - possessive

        ### for possible future use:
        # ["male_names", "Michael", "Luke", "Juan", "Jaime", "Guillermo", "Henry", "Eduardo", "Theodore"], #gendered names give basically no info LMAO
        # ["fem_names", "Olivia", "Evelyn", "Daniella", "Sophie", "Cecilia", "Anna", "Chloe", "Victoria"], 
    ]
    
    writer.writerows(rows_list)
file.close()

# converts sentence parameters (large set) as csv file
with open('./NLP-Homework/final-project/sentence_parameters_all.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    rows_list = [ 
        ["es_male_occ", "abogado", "doctor", "enfermero", "profesor", "maestro", "jefe", "presidente", "ingeniero", "peluquero", "granjero", "científico", "arquitecto", "empresario", "secretario", "cajero", "empleado", "vendedor", "trabajador", "obrero de la construcción", "desarrollador", "diseñador", "bibliotecario", "escritor", "jefe de cocina", "cocinero"],
        ["es_fem_occ", "abogada", "doctora", "enfermera", "profesora", "maestra", "jefa", "presidenta", "ingeniera", "peluquera", "granjera", "científica", "arquitecta", "empresaria", "secretaria", "cajera", "empleada", "vendedora", "trabajadora", "obrera de la construcción", "desarrolladora", "diseñadora", "bibliotecaria", "escritora", "jefa de cocina", "cocinera"],
        ["en_occ", "lawyer", "doctor", "nurse", "professor", "teacher", "boss", "president", "engineer", "hairdresser", "farmer", "scientist", "architect", "businessperson", "secretary", "teller", "employee", "salesperson", "worker", "construction worker", "developer", "designer", "librarian", "writer", "chef", "cook"],


        ["amb_names", "Alex", "Max", "Angel", "Avery", "Sam", "Rory", "Skyler", "Charlie", "Harley", "Leslie", "Ryder", "Taylor", "Morgan", "Drew"],


        ["es_verb_phrase_occ", "fue a Madrid para aprender la peluquería", "se fue de casa para asistir a la facultad de medicina", "me recetó unos medicamentos", "fue a la facultad de derecho para ejercer la abogacía", "mostró la presentación al CEO", "enseñó a los niños a contar", "chismea con los demás durante el descanso para comer", "salvó a la familia del edificio en llamas", "visitó el sitio del nuevo proyecto", "le preguntó a la gerencia si podrían reunirse", "corrigió el nuevo problema con el producto", "tomó el transporte público para ir a la junta", "limpió el cuarto", "fue en bicicleta al mercado", "se fue de vacaciones a una isla tropical", "regresó de un viaje a Europa", "visitó a un amigo de la familia", "se tomó unos días para navegar alrededor del mundo", "tuvo gran impacto en la cultura de la empresa", "estudió en el extranjero en colegio", "cursó estudios de posgrado", "paseó por el set de filmación en Hollywood"],
        ["en_verb_phrase_occ", "went to Madrid to learn hairdressing", "left home to attend medical school", "prescribed me some medicines", "went to law school to practice law", "showed the presentation to the CEO", "taught the children how to count", "gossips with the others during the lunch break", "saved the family from the burning building", "visited the new project’s location", "asked management if they could meet", "fixed the problem with the product", "took public transit to go to the meeting", "cleaned up the room", "rode a bicycle to the market", "took a vacation to a tropical island", "returned from a trip to Europe" , "visited a family friend", "took time off to sail around the world", "made a big impact on the company’s culture", "studied abroad in college", "pursued graduate education", "toured the film sets at Hollywood"],


        ["es_verb_phrase_male_rel", "ama a su esposo", "besó a su marido", "toma de la mano a su novio cuando ven una película", "mira con amor a su prometido", "salió con su novio", "fue a ver una obra de teatro con su novio", "fue de vacaciones con su novio", "preparó la cena con su novio", "salió a cenar con su novio", "se casó con su marido", "tuvo un hijo con su esposo", "conoció a su futuro marido en colegio" , "rompió con su novio", "fue de acampada con su prometido", "fue a la playa con su novio", "paseó con su novio", "corrió con su novio"],
        ["es_verb_phrase_fem_rel", "ama a su esposa", "besó a su marida", "toma de la mano a su novia cuando ven una película", "mira con amor a su prometida", "salió con su novia", "fue a ver una obra de teatro con su novia", "fue de vacaciones con su novia", "preparó la cena con su novia", "salió a cenar con su novia", "se casó con su marida", "tuvo un hijo con su esposa", "conoció a su futura marida en colegio" , "rompió con su novia", "fue de acampada con su prometida", "fue a la playa con su novia", "paseó con su novia", "corrió con su novia"],
        ["en_verb_phrase_male_rel", "loves #pos# husband", "kissed #pos# husband", "holds hands with #pos# boyfriend when they watch a movie", "looks lovingly at #pos# fiancé", "went on a date with #pos# boyfriend", "went to see a play with #pos# boyfriend", "went on vacation with #pos# boyfriend", "made dinner with #pos# boyfriend", "went out to dinner with #pos# boyfriend", "got married to #pos# husband", "had a child with #pos# husband", "met #pos# future husband at college" , "broke up with #pos# boyfriend", "went camping with #pos# fiancé", "went to the beach with #pos# boyfriend", "went on a walk with #pos# boyfriend", "went on a run with #pos# boyfriend"],
        ["en_verb_phrase_fem_rel", "loves #pos# wife", "kissed #pos# wife", "holds hands with #pos# girlfriend when they watch a movie", "looks lovingly at #pos# fiancée", "went on a date with #pos# girlfriend", "went to see a play with #pos# girlfriend", "went on vacation with #pos# girlfriend", "made dinner with #pos# girlfriend", "went out to dinner with #pos# girlfriend", "got married to #pos# wife", "had a child with #pos# wif", "met #pos# future wife at college" , "broke up with #pos# girlfriend", "went camping with #pos# fiancée", "went to the beach with #pos# girlfriend", "went on a walk with #pos# girlfriend", "went on a run with #pos# girlfriend"]
    ]
    
    writer.writerows(rows_list)
file.close()

# converts test sentences into csv file
with open('./NLP-Homework/final-project/sentences_test.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        sentences = gen_sentences_full(open("./NLP-Homework/final-project/sentence_parameters_test.csv", "r", encoding='UTF8'))
        
        for row in sentences:
            writer.writerows(row)
file.close()

# converts all sentences into csv file
with open('./NLP-Homework/final-project/sentences_all.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        sentences = gen_sentences_full(open("./NLP-Homework/final-project/sentence_parameters_all.csv", "r", encoding='UTF8'))
        
        for row in sentences:
            writer.writerows(row)
file.close()

# random sample of sentences csv file
with open('./NLP-Homework/final-project/sample_sentences.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        sentences = gen_sentences_sample(open("./NLP-Homework/final-project/sentence_parameters_all.csv", "r", encoding='UTF8'))

        for row in sentences:
            writer.writerows(row)
file.close()
