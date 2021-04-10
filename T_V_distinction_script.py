# This  script changes T-V distinction between 2 characters in the scenarios.

# Copy-paste your scenario into dialog.txt
# The final output will be in result.txt as well as in the console

# Particular qualities:
# - This script erases all blank space between lines in the output text (can be changed if needed)
# - Capitilizes all Vy/Váš forms in the text (can be changed)

# PROBLEMS:
# 1) 'ti' (shortend 'ty' in dative case) may be tagged by MorphoDiTa REST API with a lemma 'ten', 
# therefore it doesn't get changed

# All potential mistakes and inaccuracies are outputed into the file manually_check.txt



import requests, json

f = open("dialog.txt", "r")

#appending all sentences to a list

all = []
bugs = []

for line in f:
    stripped_line = line.strip()
    all.append(stripped_line)
    # if stripped_line != '':
    #     all.append(stripped_line)


f.close()

ty = ['POS=V','Per=2', 'Num=S', 'PNu=S']
vy = ['POS=V', 'Per=2', 'Num=P', 'PNu=P']
condition1 = 'Num=S' # ty verbs
condition2 = 'Num=P' # vy verbs
condition3 = 'PNu=S' # tvůj
condition4 = 'PNu=P' # váš
condition5 = 'SubPOS=H' # tě ti atd.
#  tě a zkrácené formy ~ SubPOS=H
# tebe vás ~ SubPOS=P


TV = input('Do you want to use V (vykání) or T (tykání) distinction between 2 characters? Enter either V or T: ')

if TV == 'T':
    condition1 = 'Num=S' # ty verbs
    condition2 = 'Num=P' # vy verbs

    condition3 = 'PNu=S' # for vas !tvuj
    condition4 = 'PNu=P' # !váš
    
if TV == 'V':

    condition1 = 'Num=P'  # vy verbs
    condition2 = 'Num=S' # ty verbs

    condition3 = 'PNu=P' # !váš 
    condition4 = 'PNu=S' # for vas !tvuj


# ALGORITHM
# check coditions

searched_form = 'ERROR'
current_sentence = all[0]

for sentence in range(len(all)):

    #tags sentence

    my_response = requests.get("http://lindat.mff.cuni.cz/services/morphodita/api/tag?data=" + all[sentence] + "&convert_tagset=pdt_to_conll2009&output=json")
    my_response.encoding = 'utf8'

    tagged = json.loads(my_response.text)

    tagged_sentence = []

    for i in tagged['result']:
        tagged_sentence.append(i)

    # тут 2 + листа с тегами в листе


    tagged_sentences = []

    #merging multiple tagged sentences into one list without list-in-a-list structure

    for lists in tagged_sentence:
        for element in lists:
            tagged_sentences.append(element)

    

    for index in range(len(tagged_sentences)):
        # print(tagged_sentences[index])
        
        current_sentence = all[sentence]

        # TY-VY FORMS
        if tagged_sentences[index]['lemma'] == 'ty':

            #capitalizes all Vy forms
            if tagged_sentences[index]['token'][0].upper() == 'V':
                
                all[sentence] = current_sentence.replace(tagged_sentences[index]['token'], tagged_sentences[index]['token'].capitalize(), 1)
                
            if condition1 not in tagged_sentences[index]['tag']:
                word_to_replace = tagged_sentences[index]['token']

                r = requests.get("http://lindat.mff.cuni.cz/services/morphodita/api/generate?data=" + tagged_sentences[index]['lemma'] + "&convert_tagset=pdt_to_conll2009&output=json")
                r.encoding = 'utf8'
                r1 = json.loads(r.text)
                generated = r1['result'][0] #generated tagged_sentences[index] forms

                cur_tag = str(tagged_sentences[index]['tag'])

                needed_tag = cur_tag.replace(condition2, condition1)

                if 'SubPOS=H' in cur_tag and condition1 == 'Num=P':
                    needed_tag = needed_tag.replace('SubPOS=H', 'SubPOS=P')                

                # getting needed tagged_sentences[index] form

                for item in generated:
                    if item['tag'] == needed_tag:

                        searched_form = item['form']
                       
                        # this part corrects tebe-tě variations if replaced from e.g. vás

                        if index != 0 and 'Num=S' in needed_tag:
        
                            # EXPLANAITION: if the word before is not a preposition then:
                            if 'POS=R' not in tagged_sentences[index - 1]['tag']:

                                assumption = item['tag'].replace('SubPOS=P', 'SubPOS=H')

                                for i in generated:
                                    if assumption == i['tag']:
                                        searched_form = i['form']
                           
                        break

                
                if tagged_sentences[index]['token'][0].isupper() is True or searched_form[0] == 'v':
                    searched_form = searched_form.capitalize()
                
                # Replace previous word with a searched word form

                all[sentence] = current_sentence.replace(word_to_replace, searched_form, 1)
        


        # replace TVŮJ-VÁŠ

        if tagged_sentences[index]['lemma'] == 'tvůj':

            #capitalizes all Vy forms
            if tagged_sentences[index]['token'][0] == 'v':
                all[sentence] = current_sentence.replace(tagged_sentences[index]['token'], tagged_sentences[index]['token'].capitalize(), 1)
                
            
            if condition3 not in tagged_sentences[index]['tag']:
                word_to_replace = tagged_sentences[index]['token']

                r = requests.get("http://lindat.mff.cuni.cz/services/morphodita/api/generate?data=" + tagged_sentences[index]['lemma'] + "&convert_tagset=pdt_to_conll2009&output=json")
                r.encoding = 'utf8'
                r1 = json.loads(r.text)
                generated = r1['result'][0] #generated word forms
        
                cur_tag = str(tagged_sentences[index]['tag'])
                needed_tag = cur_tag.replace(condition4, condition3)
                needed_tag = cur_tag.replace(condition4, condition3)

                # getting needed word form
                for item in generated:
                    if item['tag'] == needed_tag:
                        searched_form = item['form']

                        break

                if tagged_sentences[index]['token'][0].isupper() == True or tagged_sentences[index]['token'][0].upper() == 'V':
                    searched_form = searched_form.capitalize()
                
                # Replace previous word with searched word form

                all[sentence] = current_sentence.replace(word_to_replace, searched_form, 1)
            
        

        # replace verbs in the present tense for T-V

        if 'POS=V' in tagged_sentences[index]['tag'] and 'Per=2' in tagged_sentences[index]['tag']: 
            
            if condition1 not in tagged_sentences[index]['tag']:
                word_to_replace = tagged_sentences[index]['token']
                # make a request, change the token
             
                r = requests.get("http://lindat.mff.cuni.cz/services/morphodita/api/generate?data=" + tagged_sentences[index]['lemma'] + "&convert_tagset=pdt_to_conll2009&output=json")
                r.encoding = 'utf8'
                r1 = json.loads(r.text)
                generated = r1['result'][0]
        
                cur_tag = str(tagged_sentences[index]['tag'])
                needed_tag = cur_tag.replace(condition2, condition1)
                    
                for item in generated:
                    if item['tag'] == needed_tag:
                        searched_form = item['form']
                        break
                
                # Replace previous word with searched word form

                # print(tagged_sentences[index]['token'])

                if tagged_sentences[index]['token'][0].isupper() is True:
                    searched_form = searched_form.capitalize()

                final_sentence = current_sentence.replace(word_to_replace, searched_form, 1)

                final_sentence = final_sentence.replace('bodeš', 'budeš')
                final_sentence = final_sentence.replace('Bodeš', 'Budeš')
                final_sentence = final_sentence.replace('bodete', 'budete')
                final_sentence = final_sentence.replace('Bodete', 'Budete')
            
                all[sentence] = final_sentence

        

        #CHECK FOR BUGS

        if tagged_sentences[index]['token'] == 'ti':
            temporary_list_bugs = [' Possible inaccuracy in a line number: ', 'LINE NUMBER', ". Lemma for 'ti' (= 'ty') may be indicated as 'ten'."]
            temporary_list_bugs[1] = str(sentence + 1)
            bugs.append(temporary_list_bugs)
            



 

        
# Outputting result

ttt = open("result.txt", "w")
for line in all:
    print(line)
    ttt.write(line + '\n')

ttt.close()



# Outputting potential problems:

ttt = open("manually_check.txt", "w")
for line in bugs:
    a = ''
    for el in line:
        a += el
    
    # print(line)
    ttt.write(a + '\n')
if bugs == []:
    ttt.write('No inaccuracies have been found. Yay!'+ '\n')
    
ttt.close()
