# Tokens
tokenList = {
    "keywords":{
        'import': 0,
        'implementations': 1,
        'function': 2,
        'main': 3,
        'return': 4,
        'type': 5,
        'double': 6,
        'define': 7,
        'of': 8,
        'begin': 9,
        'display': 10,
        'set': 11,
        'input': 12,
        'if': 13,
        'then': 14,
        'else': 15,
        'endif': 16,
        'not': 17,
        'greater': 18,
        'or': 19,
        'equal': 20,
        'variables': 21,
        'pointer': 22,
    },

    "operators": {
        '+': 401,
        '-': 402,
        '*': 403,
        '/': 404,
        '^': 405,
        '>': 406,
        '<': 407,
        '=': 408,
        '(':409,
        ')':410,

    },

    "specialSymbols": {
        ',': 800,
        '.': 801,
    }
}

class Token:
    def __init__(self, type, id, value):
        self.type = type
        self.id = id
        self.value = value

    def getData(self):
        return [self.type, self.id, self.value]
        
