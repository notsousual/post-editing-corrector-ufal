INSTRUCTION: T_V_distinction_script.py

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
