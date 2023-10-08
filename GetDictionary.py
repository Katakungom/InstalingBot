import codecs

def GetDictionary(FileName):
    with open(FileName, encoding='utf-8') as File:
        dictionary = {}

        for line in File:
            line = line.rstrip()
            Translation = line.split("|")
            dictionary.update({Translation[0]:Translation[2]})
              
    return dictionary
