INSTRUCTION:  T_V_distinction_script.py

This script changes T-V distinction between 2 characters in the scenarios.

Copy-paste your scenario into dialog.txt
The final output will be in result.txt as well as in the console

Particular qualities:
- to be add

PROBLEMS:
1) 'ti' (shortend 'ty' in dative case) may be tagged by MorphoDiTa REST API with a lemma 'ten', 
therefore it may not get changed to the needed form.

All potential mistakes and inaccuracies are outputed into the file manually_check.txt


INSTRUCTION: characters_name_change.py

This script changes all names of the characters in the play
that are in the beginning of each new line by suggesting the user 
to manually replace all names to the needed ones.

Copy-past your scenario into to_change.txt
Output is in changed.txt

ATTENTION: 
1) This script won't work if the symbol after a character name on a new line isn't a colon (':'). 
2) Only works for character names in the beginning of the sentence.
3) In order for it to work with other symbols right after character names, change all occurences of ':' up to your choice in the script.


MorphoDiTa REST API is used within project for ÚFAL/Charles University needs.
For any questions: t e l e g r a m ~ @ g l a v o l a m (w/o spaces)
