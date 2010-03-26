'''
Created on 26.3.2010

@author: Peterko
'''
def dictToTuple(data):
    '''
    Vytvori zo slovnika, kde su vnorene dalsie slovniky alebo listy, velky tuple, ktory sa da porovnavat potom
    '''
    if type(data) ==  type({}):
        items = data.items()
        # zoradit, aby sa to dalo porovnavat
        items.sort()
        return tuple([(item[0], dictToTuple(item[1])) for item in items])
    elif type(data) == type([]):
        return tuple([dictToTuple(item) for item in data])
    else:
        return unicode(data or '')