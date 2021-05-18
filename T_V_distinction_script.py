# This script changes T-V distinction between 2 characters in the scenarios.

# Copy-paste your scenario into dialog.txt
# The final output will be in result.txt as well as in the console

# Particular qualities:
# - This script erases all blank space between lines in the output text (can be changed if needed)
# - Capitilizes all Vy/Váš forms in the text (can be changed)

# PROBLEMS:
# 1) 'ti' (shortend 'ty' in dative case) may be tagged by MorphoDiTa REST API with a lemma 'ten', 
# therefore it doesn't get changed
# => The script always considers 'ti' with the lemma 'ty' and not 'ten'.
# 2) tvá tvé not changing = FIXED

# Function TV_corrector():

# the first parameter is a string you want to post-edit
# the second is whether you want to use T (TV = 'T') or V (TV = 'V') distinction.


import requests, json

f = open("dialog.txt", "r")

#appending all sentences to a list

test_data = []
bugs = []

for line in f:
    stripped_line = line.strip()
    test_data.append(stripped_line)
    # if stripped_line != '':
    #     all.append(stripped_line)


f.close()


ty = ['POS=V','Per=2', 'Num=S', 'PNu=S']
vy = ['POS=V', 'Per=2', 'Num=P', 'PNu=P']
verb_number_1 = 'Num=S' # ty verbs
verb_number_2 = 'Num=P' # vy verbs
pronoun_number_1 = 'PNu=S' # tvůj
pronoun_number_2 = 'PNu=P' # váš
condition5 = 'SubPOS=H' # tě ti atd.
#  tě a zkrácené formy ~ SubPOS=H
# tebe vás ~ SubPOS=P


TV = input('Do you want to use V (vykání) or T (tykání) distinction between 2 characters? Enter either V or T: ')


'/ / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / '


def TV_corrector(str_to_post_edit, TV='V'):
    # the first parameter is a string you want to post-edit
    # the second is whether you want to use T (TV = 'T') or V (TV = 'V') distinction.

    if TV == 'T':
        verb_number_1 = 'Num=S' # ty verbs
        verb_number_2 = 'Num=P' # vy verbs

        pronoun_number_1 = 'PNu=S' # for vas !tvuj
        pronoun_number_2 = 'PNu=P' # !váš
        
    if TV == 'V':
        verb_number_1 = 'Num=P'  # vy verbs
        verb_number_2 = 'Num=S' # ty verbs

        pronoun_number_1 = 'PNu=P' # !váš 
        pronoun_number_2 = 'PNu=S' # for vas !tvuj

    preposition = 'POS=R'
    
    #  tě a zkrácené formy ~ SubPOS=H
    # tebe vás ~ SubPOS=P
    
    searched_form = 'ERROR'
  
    all = [str(str_to_post_edit)]

    my_response = requests.get("http://lindat.mff.cuni.cz/services/morphodita/api/tag?data=" + all[0] + "&convert_tagset=pdt_to_conll2009&output=json")
    my_response.encoding = 'utf8'

    tagged = json.loads(my_response.text)

    #merging multiple tagged sentences into one list without list-in-a-list structure
    original_tagged_sentences = []

    for bracket in tagged['result']:
        for element in bracket:
            original_tagged_sentences.append(element)

    sentences_to_change = original_tagged_sentences.copy()

    for index in range(len(original_tagged_sentences)):
        
        current_sentence = all[0]

        # !!! 'Ti' fix, The script always considers 'ti' with the lemma 'ty' and not 'ten'
        if (original_tagged_sentences[index]['token'] == 'ti') and TV == 'V':
            temp = {"token":"ti","lemma":"ty","tag":"POS=P|SubPOS=H|Num=S|Cas=3|Per=2"}
            if 'space' in original_tagged_sentences[index]: temp['space'] = original_tagged_sentences[index]['space']
            original_tagged_sentences[index] = temp


        # TY-VY FORMS
        if original_tagged_sentences[index]['lemma'] == 'ty':

            #capitalizes all Vy forms
            if original_tagged_sentences[index]['token'][0].upper() == 'V':
                
                all[0] = current_sentence.replace(original_tagged_sentences[index]['token'], original_tagged_sentences[index]['token'].capitalize(), 1)
                
            if verb_number_1 not in original_tagged_sentences[index]['tag']:

                r = requests.get("http://lindat.mff.cuni.cz/services/morphodita/api/generate?data=" + original_tagged_sentences[index]['lemma'] + "&convert_tagset=pdt_to_conll2009&output=json")
                r.encoding = 'utf8'
                r1 = json.loads(r.text)
                generated = r1['result'][0] #generated original_tagged_sentences[index] forms

                cur_tag = str(original_tagged_sentences[index]['tag'])
                needed_tag = cur_tag.replace(verb_number_2, verb_number_1)

                #fixing short tě-ti incorrect transition tagging to V
                if 'SubPOS=H' in cur_tag and verb_number_1 == 'Num=P':
                    needed_tag = needed_tag.replace('SubPOS=H', 'SubPOS=P')                

                # getting needed original_tagged_sentences[index] form

                for item in generated:
                    if item['tag'] == needed_tag:

                        searched_form = item
                
                        # this part corrects tebe-tě variations if replaced from e.g. vás
                        if index != 0 and 'Num=S' in needed_tag:
        
                            # if the word before is not a preposition then:
                            if preposition not in original_tagged_sentences[index - 1]['tag']:

                                assumption = item['tag'].replace('SubPOS=P', 'SubPOS=H')

                                for i in generated:
                                    if assumption == i['tag']:
                                        searched_form = i
                                        
                        
                        if 'space' in original_tagged_sentences[index]: 
                            searched_form['space'] = original_tagged_sentences[index]['space']
                        
                        searched_form['token'] = searched_form.pop('form')

                        break

            
                if original_tagged_sentences[index]['token'][0].isupper() is True or searched_form['token'][0] == 'v':
                    for_capitalization = searched_form['token'].capitalize()
                    searched_form['token'] = for_capitalization
                # Replace previous word with a searched word form

                if searched_form != 'ERROR':
                    sentences_to_change[index] = searched_form


        # replace TVŮJ-VÁŠ

        if original_tagged_sentences[index]['lemma'] == 'tvůj':

            #capitalizes all Vy forms
            if original_tagged_sentences[index]['token'][0] == 'v':
                for_capitalization = searched_form['token'].capitalize()
                searched_form['token'] = for_capitalization
            
            if pronoun_number_1 not in original_tagged_sentences[index]['tag']:
               
                r = requests.get("http://lindat.mff.cuni.cz/services/morphodita/api/generate?data=" + original_tagged_sentences[index]['lemma'] + "&convert_tagset=pdt_to_conll2009&output=json")
                r.encoding = 'utf8'
                r1 = json.loads(r.text)
                generated = r1['result'][0] #generated word forms
        
                cur_tag = str(original_tagged_sentences[index]['tag'])
                needed_tag = cur_tag.replace(pronoun_number_2, pronoun_number_1)
        
                #tvá tvé not changing fix
                if 'Var=1' in needed_tag and TV == 'V':
                    needed_tag = needed_tag.replace('Gen=I', 'Gen=H')
                    needed_tag = needed_tag.replace('Gen=F', 'Gen=H')
                    needed_tag = needed_tag.replace('|Var=1', '')
            
            
                # getting needed word form
                for item in generated:
                    if item['tag'] == needed_tag:
                
                        searched_form = item

                        if 'space' in original_tagged_sentences[index]: 
                            searched_form['space'] = original_tagged_sentences[index]['space']
                        searched_form['token'] = searched_form.pop('form')

                        break

                if searched_form != 'ERROR':
                    if original_tagged_sentences[index]['token'][0].isupper() is True or searched_form['token'][0] == 'v':
                        
                        for_capitalization = searched_form['token'].capitalize()
                        searched_form['token'] = for_capitalization
                    
                    # Replace previous word with searched word form
                    sentences_to_change[index] = searched_form


        # replace verbs in the present tense for T-V

        if 'POS=V' in original_tagged_sentences[index]['tag'] and 'Per=2' in original_tagged_sentences[index]['tag']: 
            
            if verb_number_1 not in original_tagged_sentences[index]['tag']:
                searched_form = 'ERROR'

                # make a request, change the token

                r = requests.get("http://lindat.mff.cuni.cz/services/morphodita/api/generate?data=" + original_tagged_sentences[index]['lemma'] + "&convert_tagset=pdt_to_conll2009&output=json")
                r.encoding = 'utf8'
                r1 = json.loads(r.text)
                generated = r1['result'][0]

                cur_tag = str(original_tagged_sentences[index]['tag'])
                needed_tag = cur_tag.replace(verb_number_2, verb_number_1)
                    
                for item in generated:
                    if item['tag'] == needed_tag:

                        searched_form = item

                        if 'space' in original_tagged_sentences[index]: 
                            searched_form['space'] = original_tagged_sentences[index]['space']
                        searched_form['token'] = searched_form.pop('form')

                        break
                
                # Replace previous word with searched word form

                if original_tagged_sentences[index]['token'][0].isupper() is True:
                    for_capitalization = searched_form['token'].capitalize()
                    searched_form['token'] = for_capitalization
                
                if searched_form['token'] == 'bodeš': searched_form['token'] = 'budeš'
                if searched_form['token'] == 'bodete': searched_form['token'] = 'budete'
                if searched_form['token'] == 'Bodeš': searched_form['token'] = 'Budeš'
                if searched_form['token'] == 'Bodete': searched_form['token'] = 'Budete'
                

                if searched_form != 'ERROR':
                    sentences_to_change[index] = searched_form
            

        # 'BY SES' correction
        #If it's  'byste se' > will be changed to > 'bys se'

        if original_tagged_sentences[index]['token'] == 'ses' and TV == 'V':
        
            if original_tagged_sentences[index - 1]['token'] == 'by':
                sentences_to_change[index - 1] = {"token":"byste","lemma":"být","tag":"POS=V|SubPOS=c|Num=P|Per=2"}
                sentences_to_change[index] = {"token":"se","lemma":"se","tag":"POS=P|SubPOS=7|Num=X|Cas=4"}

                if original_tagged_sentences[index - 1]['token'][0].isupper() is True: sentences_to_change[index - 1]["token"] = "Byste"
                if original_tagged_sentences[index]['token'][0].isupper() is True: sentences_to_change[index]["token"] = "Se"

                if 'space' in original_tagged_sentences[index - 1]: sentences_to_change[index - 1]['space'] = original_tagged_sentences[index - 1]['space']
                if 'space' in original_tagged_sentences[index]: sentences_to_change[index]['space'] = original_tagged_sentences[index - 1]['space']

        if original_tagged_sentences[index]['token'] == 'sis' and TV == 'V':
            if original_tagged_sentences[index - 1]['token'] == 'by':

                sentences_to_change[index - 1] = {"token":"byste","lemma":"být","tag":"POS=V|SubPOS=c|Num=P|Per=2"}
                sentences_to_change[index] = {"token":"si","lemma":"se","tag":"POS=P|SubPOS=7|Num=X|Cas=3"}

                if original_tagged_sentences[index - 1]['token'][0].isupper() is True: sentences_to_change[index - 1]["token"] = "Byste"
                if original_tagged_sentences[index]['token'][0].isupper() is True: sentences_to_change[index]["token"] = "Si"
                
                if 'space' in original_tagged_sentences[index - 1]: sentences_to_change[index - 1]['space'] = original_tagged_sentences[index - 1]['space']
                if 'space' in original_tagged_sentences[index]: sentences_to_change[index]['space'] = original_tagged_sentences[index - 1]['space']



    final_string_list = []

    for item in sentences_to_change:
        final_string_list.append(item['token'])
        if 'space' in item:
            final_string_list.append(item['space'])

    final_string = ''.join(final_string_list)

    print('final string returned: ' + final_string)

    return final_string


'/ / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / '


ttt = open("result.txt", "w")

for string in test_data:
    ttt.write(TV_corrector(string, TV) + '\n')

ttt.close()
