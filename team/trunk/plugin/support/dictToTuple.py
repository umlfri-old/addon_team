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
    elif type(data) == type([]) or type(data) == type(()):
        return tuple([dictToTuple(item) for item in data])
    else:
        try:
            result = unicode(int(unicode(data)))
            return result
        except:
            result = unicode(data or '')
            
        try:
            result = unicode(round(float(data),12))
            return result
        except:
            result = unicode(data or '')
            
        
        return result
    
def tupleToDict(data):
    '''
    Spiatocna metoda
    '''
    
    if type(data) == type(()):
        if (len(data) == 0) or (len(data) >= 1 and type(data[0][0]) != type('')):
            return [tupleToDict(item) for item in data]
        else:
            return dict(zip([i[0] for i in data], [tupleToDict(i[1]) for i in data]))
    else:
        return data
    