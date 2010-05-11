'''
Created on 26.3.2010

@author: Peterko
'''
def dictToTuple(data):
    '''
    Creates tuple from dictionary, which is suitable for comparing
    @type data: dic
    @param data: dictionary tobe converted
    '''
    if type(data) ==  type({}):
        items = data.items()
        
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
    Invert method for dictToTuple
    @type data: tuple
    @param data: Tuple to be converted 
    '''
    
    if type(data) == type(()):
        if (len(data) == 0) or (len(data) >= 1 and type(data[0][0]) != type('')):
            return [tupleToDict(item) for item in data]
        else:
            return dict(zip([i[0] for i in data], [tupleToDict(i[1]) for i in data]))
    else:
        return data
    