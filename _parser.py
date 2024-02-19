import ply.yacc as yacc
from lexer import tokens
import sys
from generate.generate_code import Generator
from generate import *

generator = Generator()

def throw_error(p, massage):
    print(f"Error at line {p.lineno(3)}, position {p.lexpos(3)}: " + massage)
    sys.exit()

# Define precedence
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV'),
    ('left', 'MOD'),
)

# Define the start symbol
start = 'program_all'

# Define the grammar rules
def p_program_all(p):
    '''program_all : procedures main'''
    p[0] = program_all.Program_All(p[1], p[2])

def p_procedures_decl(p):
    '''procedures : procedures PROCEDURE proc_head IS declarations IN commands END'''
    # p[0] = procedures.Procedure_Decl(p[1], p[3], p[5], p[7])
    p[1].addProcadure(procedures.Procedure_Decl(p[3], p[5], p[7], p.lineno(8)))
    p[0] = p[1]
    
def p_procedures(p):
    '''procedures : procedures PROCEDURE proc_head IS IN commands END'''
    p[1].addProcadure(procedures.Procedure(p[3], p[6], p.lineno(7)))
    p[0] = p[1]
    
    
def p_procedures_empty(p):
    '''procedures : '''
    p[0] = procedures.Procedures()

def p_main_with_decl(p):
    '''main : PROGRAM IS declarations IN commands END'''
    p[0] = main.Progam_Decl(p[3], p[5])

def p_main(p):
    '''main : PROGRAM IS IN commands END'''
    p[0] = main.Program(p[4])

def p_mult_commands(p):
    '''commands : commands command'''
    p[1].add_command(p[2])
    p[0] = p[1]
    
def p_commands(p):
    '''commands : command'''
    p[0] = commands.Commands()
    p[0].add_command(p[1])

# def p_command(p):
#     '''command : identifier ASSIGN expression SEMICOLON
#                | IF condition THEN commands ELSE commands ENDIF
#                | IF condition THEN commands ENDIF
#                | WHILE condition DO commands ENDWHILE
#                | REPEAT commands UNTIL condition SEMICOLON
#                | proc_call SEMICOLON
#                | READ identifier SEMICOLON
#                | WRITE value SEMICOLON'''
#     # Implementation goes here

def p_command_assign(p):
    '''command : identifier ASSIGN expression SEMICOLON'''
    p[0] = command.Assign(p[1], p[3])
    
def p_command_if_else(p):
    '''command : IF condition THEN commands ELSE commands ENDIF'''
    p[0] = command.IfThenElse(p[2], p[4], p[6])
    
def p_command_if(p):
    '''command : IF condition THEN commands ENDIF'''
    p[0] = command.IfThen(p[2], p[4])
    
def p_command_while(p):
    '''command : WHILE condition DO commands ENDWHILE'''
    p[0] = command.WhileDo(p[2], p[4])
    
def p_command_repeat(p):
    '''command : REPEAT commands UNTIL condition SEMICOLON'''
    p[0] = command.RepeatUntil(p[2], p[4])
    
def p_command_proc_call(p):
    '''command : proc_call SEMICOLON'''
    p[0] = command.Proc_Call(p[1])
    
def p_command_read(p):
    '''command : READ identifier SEMICOLON'''
    p[0] = command.Read(p[2])
    
def p_command_write(p):
    '''command : WRITE value SEMICOLON'''
    p[0] = command.Write(p[2])

# def p_write(p):
#     '''command : WRITE value SEMICOLON'''
#     res = generator.write()
#     if res == -1:
#         throw_error(p, f"Variable \"{p[2]}\" is not defined")

# def p_assing(p):
#     '''command : identifier ASSIGN expression SEMICOLON'''
#     res = generator.assign(p[1])
#     if res == -1:
#         throw_error(p, f"Variable \"{p[1]}\" is not defined")


def p_proc_head(p):
    '''proc_head : IDENTIFIER OPEN_PAREN args_decl CLOSE_PAREN'''
    p[0] = proc_head.Proc_Head(identifier.Pidentifier(p[1], p.lineno(1)), p[3], p.lineno(1))

def p_proc_call(p):
    '''proc_call : IDENTIFIER OPEN_PAREN args CLOSE_PAREN'''
    p[0] = proc_call.Proc_Call(identifier.Pidentifier(p[1], p.lineno(1)), p[3])

# def p_declarations(p):
#     '''declarations : declarations COMMA pidentifier
#                     | declarations COMMA pidentifier OPEN_BRACKET num CLOSE_BRACKET
#                     | pidentifier
#                     | pidentifier OPEN_BRACKET num CLOSE_BRACKET'''
#     # Implementation goes here
    
def p_mult_declarations_array(p):
    '''declarations : declarations COMMA IDENTIFIER OPEN_BRACKET NUM CLOSE_BRACKET'''
    p[1].add_array(p[3], p[5], p.lineno(1))
    p[0] = p[1]
    
def p_mult_declarations_id(p):
    '''declarations : declarations COMMA IDENTIFIER'''
    p[1].add_identifier(p[3], p.lineno(1))
    p[0] = p[1]



def p_declaration_array(p):
    '''declarations : IDENTIFIER OPEN_BRACKET NUM CLOSE_BRACKET'''
    p[0] = declarations.Declarations()
    p[0].add_array(p[1], p[3], p.lineno(1))

def p_declaration_id(p):
    '''declarations : IDENTIFIER'''
    p[0] = declarations.Declarations()
    p[0].add_identifier(p[1], p.lineno(1))


    

# def p_declarations(p):
#     '''declarations : IDENTIFIER'''
#     generator.add_variable(p[1])
                    
# def p_mult_declarations(p):
#     '''declarations : declarations COMMA IDENTIFIER'''
#     generator.add_variable(p[3])

# def p_args_decl(p):
#     '''args_decl : args_decl COMMA pidentifier
#                  | args_decl COMMA T pidentifier
#                  | pidentifier
#                  | T pidentifier'''
#     # Implementation goes here
    
def p_mult_args_id(p):
    '''args_decl : args_decl COMMA IDENTIFIER'''
    p[1].add_identifier(p[3], False, p.lineno(3))
    p[0] = p[1]
    
def p_args_mult_array(p):
    '''args_decl : args_decl COMMA T IDENTIFIER'''
    p[1].add_identifier(p[4], True, p.lineno(3))
    p[0] = p[1]
    
def p_args_decl_id(p):
    '''args_decl :  IDENTIFIER'''
    p[0] = args_decl.Args_Decl()
    p[0].add_identifier(p[1], False, p.lineno(1))
    
def p_args_array(p):
    '''args_decl : T IDENTIFIER'''
    p[0] = args_decl.Args_Decl()
    p[0].add_identifier(p[2], True, p.lineno(1))

def p_args(p):
    '''args : args COMMA IDENTIFIER'''
    p[1].add_identifier(identifier.Pidentifier(p[3], p.lineno(3)))
    p[0] = p[1]

def p_args_id(p):
    '''args : IDENTIFIER'''
    p[0] = args.Args()
    p[0].add_identifier(identifier.Pidentifier(p[1], p.lineno(1)))

def p_expression_value(p):
    '''expression : value'''
    p[0] = expressions.Expression_Value(p[1])

def p_expression(p):
    '''expression : value PLUS value
                  | value MINUS value
                  | value TIMES value
                  | value DIV value
                  | value MOD value'''
    p[0] = expressions.Expressions(p[1], p[2], p[3])
# def p_expression(p):
#     '''expression : value'''
#     p[0] = generator.expression(p[1], None, None)

def p_condition(p):
    '''condition : value EQ value
                 | value NEQ value
                 | value GT value
                 | value LT value
                 | value GE value
                 | value LE value'''
    p[0] = conditions.Contidion(p[1], p[2], p[3])

# def p_value(p):
#     '''value : NUM
#              | identifier'''
#     p[0] = generator.value(p[1])
#     if p[0] == -1:
#         throw_error(p, f"Variable \"{p[1]}\" is not defined")

def p_value_num(p):
    '''value : NUM'''
    p[0] = value.Num(p[1])
    
def p_value_id(p):
    '''value : identifier'''
    p[0] = value.Identifier(p[1], p.lineno(1))

# def p_identifier(p):
#     '''identifier : pidentifier
#                   | pidentifier OPEN_BRACKET NUM CLOSE_BRACKET
#                   | pidentifier OPEN_BRACKET pidentifier CLOSE_BRACKET'''
                  
#     # Implementation goes here
    
def p_identifier_id(p):
    '''identifier : IDENTIFIER'''
    p[0] = identifier.Pidentifier(p[1], p.lineno(1))
    
def p_identifier_arr_num(p):
    '''identifier : IDENTIFIER OPEN_BRACKET NUM CLOSE_BRACKET'''
    p[0] = identifier.Array_Num(p[1], p[3], p.lineno(1))
    
def p_identifier_arr_id(p):
    '''identifier : IDENTIFIER OPEN_BRACKET IDENTIFIER CLOSE_BRACKET'''
    p[0] = identifier.Array_ID(p[1], p[3], p.lineno(1))

# def p_identifier(p):
#     '''identifier : IDENTIFIER'''
#     p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
    print(f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected token '{p.value}'")
    print(p)

def get_generated_code(code, lexer):
    parser = yacc.yacc()
    prsed = parser.parse(code, lexer=lexer)
    return generator.generate(prsed)