import ply.lex as lex

# tokens = [
#     'PROGRAM_IS', 'IN', 'END', 'SEMICOLON', 'COMMA',    # 0 program
#     'NUM',                                              # 1 numbers
#     'PLUS', 'MINUS', 'TIMES', 'DIV', 'MOD',             # 2 operators
#     'EQ', 'NEQ', 'LE', 'GE', 'LEQ', 'GEQ',              # 3 relations
#     'ASSIGN',                                           # 4 assign
#     'LBR', 'RBR', 'PROCEDURE', 'IS',                    # 5 procedure 
#     'IF', 'THEN', 'ELSE', 'ENDIF',                      # 6 if
#     'WHILE', 'DO', 'ENDWHILE',                          # 7 while
#     'REPEAT', 'UNTIL',                                  # 8 repeat
#     'READ', 'WRITE',                                    # 9 read/write
#     'ID'                                                # 10 identificators
# ]

tokens = (
    'PROGRAM', 'IS','IN', 'END',
    'PROCEDURE',
    'IF', 'THEN', 'ELSE', 'ENDIF',
    'WHILE', 'DO', 'ENDWHILE',
    'REPEAT', 'UNTIL',
    'READ', 'WRITE',
    'IDENTIFIER',
    'NUM',
    'ASSIGN',
    'PLUS', 'MINUS', 'TIMES', 'DIV', 'MOD',
    'EQ', 'NEQ', 'GT', 'LT', 'GE', 'LE',
    'SEMICOLON', 'COMMA',
    'OPEN_PAREN', 'CLOSE_PAREN', 'OPEN_BRACKET', 'CLOSE_BRACKET',
    'COMMENT',
    'T'
)


#t_ignore_COM = r'\[[^\]\[]*\]'
t_PROGRAM = r'PROGRAM'
t_IS = r'IS'
t_IN = r'IN'
t_END = r'END'
t_IDENTIFIER = r'[_a-z]+'
t_SEMICOLON = r';'
t_COMMA = r','

def t_NUM(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\r?\n+'
    t.lexer.lineno += len(t.value)
    #t.lexer.lineno += 1
    pass

def t_COMMENT(t):
    r'\#.*'
    pass

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

t_T = r'T'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIV = r'\/'
t_MOD = r'\%'

t_EQ = r'='
t_NEQ = r'!='
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='

t_ASSIGN = r':='

t_PROCEDURE = r'PROCEDURE'

t_IF = r'IF'
t_THEN = r'THEN'
t_ELSE = r'ELSE'
t_ENDIF = r'ENDIF'

t_WHILE = r'WHILE'
t_DO = r'DO'
t_ENDWHILE = r'ENDWHILE'

t_REPEAT = r'REPEAT'
t_UNTIL = r'UNTIL'

t_READ = r'READ'
t_WRITE = r'WRITE'

t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_OPEN_BRACKET = r'\['
t_CLOSE_BRACKET = r'\]'

t_ignore = ' \t'

# Build the lexer
lexer = lex.lex()

