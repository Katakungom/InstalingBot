import codecs

def GetUsers(FileName):
    with open(FileName, encoding='utf-8') as File:
        dictionary = {}

        for line in File:
            line = line.rstrip()
            Translation = line.split("|")
            dictionary.update({Translation[0]:(Translation[1],Translation[2],Translation[3])})
              
    return dictionary

ListOfUser = GetUsers('Users.txt')
