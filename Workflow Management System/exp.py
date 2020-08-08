import re

def purify_list(to_purify): #This function cleanses a list to prepare it to be stored into a single cell in a csv file.
        to_purify = re.sub(', ','|',to_purify)
        to_purify = re.sub('\[','',to_purify)
        to_purify = re.sub('\]','',to_purify)
        to_purify = re.sub('\'','',to_purify)
        return to_purify

day = str('cat')

print(day.upper())

