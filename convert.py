import json

# Read output json file from WebAnno (Annotation tool)
with open('input_json.json') as data_file:    
    data = json.load(data_file)

# Extract original sentences
sentences_list = data['_referenced_fss']['12']['sofaString'].split('\n')

# Extract entity start/ end positions and names
ent_loc = data['_views']['_InitialView']['NamedEntity']

# Extract Sentence start/ end positions
Sentence = data['_views']['_InitialView']['Sentence']

# Set first sentence starting position 0
Sentence[0]['begin'] = 0
ent_loc[0]['begin'] = 0

# Prepare spacy formatted training data
TRAIN_DATA = []
ent_list = []
for sl in range(len(Sentence)):
    ent_list_sen = []
    for el in range(len(ent_loc)):
        if(ent_loc[el]['begin'] >= Sentence[sl]['begin'] and ent_loc[el]['end'] <= Sentence[sl]['end'] and 'value' in ent_loc[el]):
            ## Need to subtract entity location with sentence begining as webanno generate data by treating document as a whole
            ent_list_sen.append([(ent_loc[el]['begin']-Sentence[sl]['begin']),(ent_loc[el]['end']-Sentence[sl]['begin']),ent_loc[el]['value']])
    ent_list.append(ent_list_sen)
    ## Create blank dictionary
    ent_dic = {}
    ## Fill value to the dictionary
    ent_dic['entities'] = ent_list[-1]
    ## Prepare final training data
    try:
        TRAIN_DATA.append([sentences_list[sl],ent_dic])
    except:
        print("Index issue:", sl)
    
TRAIN_DATA
