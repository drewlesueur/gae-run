def find_sandwich(stringo, s,e):
    splited = stringo.partition(s)[2]
    ret = splited.partition(e)[0]
    return ret