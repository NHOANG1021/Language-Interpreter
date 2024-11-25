from grin.parsing import *
from grin.lexing import *
from grin.location import *
from grin.token import *
from grin.statements import *
from grin.state import *

def start() -> list:
    """
    Takes continual user input until an end-of-program marker (.) is entered.
    Each statement is stored in a list, then returned.
    """
    statements = []
    while True:
        user_input = input()
        statements.append(user_input)
        if user_input.strip() == '.':
            break

    return statements


def lex_statements(statements: list) -> list:
    """
    This will lex the user input to make sure all the lexemes make sense.
    Returns a list of GrinTokens if successful, raises GrinLexError if not.
    """
    lex_grin_tokens = []
    for index, statement in enumerate(statements):
        token = to_tokens(statement, index + 1)
        lex_grin_tokens.append(token)

    return lex_grin_tokens


def parse_statements(statements: list):
    """
    This will parse the statements to make sure all the statements make sense.
    Returns a generator of GrinTokens if successful, raises GrinParseError if not.
    """
    parse_grin_tokens = parse(statements)
    return parse_grin_tokens

# Unable to test due to to exit() statements
def check_errors(grin_tokens: list) -> None:
    """
    Goes through each of the tokens to test for lex / parse errors
    """
    try:
        for tokens in grin_tokens:
            pass
            for token in tokens:
                pass
    except GrinLexError as e:
        print(e)
        exit()

    except GrinParseError as e:
        print(e)
        exit()


def get_token_info(tokens: list) -> list:
    """
    Given a list of GrinTokens, its information is extracted and returned in a list of tuples.
    """
    info = []
    for token in tokens:
        info.append((token.kind().index(), token.kind().category(), token.text(), token.location(), token.value()))

    return info

def get_statement(info: list) -> list:
    """
    Given token info in the form of a list of tuples,
    a statement is reconstructed and returned in a list
    """
    statement = []
    for value in info:
        statement.append(value[-1])

    return statement


def run(grin_tokens: list) -> None:
    """
    After collecting user input and GrinTokens, it is used to execute commands,
    with functionality corresponding to the "Grin quick reference".
    """
    variables = {}
    labels = grin_labels(grin_tokens)
    total = len(grin_tokens)
    current_line = 0
    goto_target = {}
    gosub_lines = []

    while current_line < total:
        try:
            token = grin_tokens[current_line]
            current_line += 1
        # Unsure how to test during run time
        except IndexError:
            break
        if (token[0].kind() == GrinTokenKind.LET or token[0].kind() == GrinTokenKind.PRINT or
                token[0].kind() == GrinTokenKind.INNUM or token[0].kind() == GrinTokenKind.INSTR or
                token[0].kind() == GrinTokenKind.ADD or token[0].kind() == GrinTokenKind.SUB or
                token[0].kind() == GrinTokenKind.MULT or token[0].kind() == GrinTokenKind.DIV or
                token[0].kind() == GrinTokenKind.GOSUB or token[0].kind() == GrinTokenKind.GOTO or
                token[0].kind() == GrinTokenKind.END or token[0].kind() == GrinTokenKind.RETURN):
            # print('TOKEN IS EXECUTING', token[0].kind())
            info = get_token_info(token)
            statement = get_statement(info)
            obj = VarValue(statement, info)

            if token[0].kind() == GrinTokenKind.LET:
                obj.let(variables)
                if token[2].kind() == GrinTokenKind.IDENTIFIER:
                    if obj.value in variables.keys():
                        obj.value = variables[obj.value]
                    else:
                        obj.value = 0

                variables[obj.var] = obj.value

            # Unable to test a portion due to input() (handles an INNUM/INSTR case)
            elif token[0].kind() == GrinTokenKind.PRINT:
                check = None
                obj.print()
                if obj.value not in variables.keys():
                    for token in grin_tokens:
                        if token[0].kind() == GrinTokenKind.INNUM or token[0].kind() == GrinTokenKind.INSTR:
                            check = True
                    if check:
                        print(obj.value)
                    else:
                        print(0)
                else:
                    print(variables[obj.value])

            # Unable to test due to input()
            elif token[0].kind() == GrinTokenKind.INNUM:
                user_input = input()
                if user_input.isdigit() or user_input.replace('-', '').isdigit():
                    user_input = int(user_input)
                elif user_input.replace(".", "", 1).replace("-", "", 1).isdigit():
                    user_input = float(user_input)
                else:
                    print('You must enter an integer or a float!')
                    exit()
                obj.innum(user_input)
                variables[obj.var] = obj.value
            # Unable to test due to input()
            elif token[0].kind() == GrinTokenKind.INSTR:
                user_input = input()
                obj.instr(user_input)
                variables[obj.var] = obj.value

            elif token[0].kind() == GrinTokenKind.ADD:
                try:
                    obj.add()
                    old = variables[obj.var]
                    if obj.value in variables.keys():
                        variables[obj.var] = old + variables[obj.value]
                    else:
                        variables[obj.var] = old + obj.value
                except TypeError:
                    print('Error when trying to add!')
                    exit()
                except KeyError:
                    pass

            elif token[0].kind() == GrinTokenKind.SUB:
                try:
                    obj.sub()
                    old = variables[obj.var]
                    if obj.value in variables.keys():
                        variables[obj.var] = old - variables[obj.value]
                    else:
                        variables[obj.var] = old - obj.value
                except TypeError:
                    print("Error when trying to subtract!")
                    exit()
                except KeyError:
                    pass

            elif token[0].kind() == GrinTokenKind.MULT:
                try:
                    obj.mult()
                    old = variables[obj.var]
                    if obj.value in variables.keys():
                        variables[obj.var] = old * variables[obj.value]
                    else:
                        variables[obj.var] = old * obj.value
                except TypeError:
                    print('Error when trying to multiply!')
                    exit()
                except KeyError:
                    pass

            elif token[0].kind() == GrinTokenKind.DIV:
                try:
                    obj.div()
                    old = variables[obj.var]
                    if obj.value in variables.keys():
                        if type(old) is int and type(variables[obj.value]) is int:
                            variables[obj.var] = old // variables[obj.value]
                        else:
                            variables[obj.var] = old / variables[obj.value]
                    else:
                        if type(old) is int and type(obj.value) is int:
                            variables[obj.var] = old // obj.value
                        else:
                            variables[obj.var] = old / obj.value
                except TypeError:
                    print('Error when trying to divide!')
                    exit()
                except ZeroDivisionError:
                    print('You can not divide by zero!')
                    exit()
                except KeyError:
                    pass
            elif token[0].kind() == GrinTokenKind.GOTO:
                try:
                    if token[2].kind() == GrinTokenKind.IF:
                        # print('ENTER IF STATEMENT')
                        obj = GotoIf(statement, info)
                        obj.get_conditional()
                        values = obj.replace_conditional(variables)
                        left, right = values
                        result = obj.check_conditional(left, right)
                        # print(left, obj.conditional, right, result, obj.target)
                        if result:
                            if isinstance(obj.target, int):
                                # print('enter', current_line, obj.target)
                                goto_target[current_line] = current_line + obj.target
                                current_line = goto_target[current_line] - 1  # Jump to the target line
                                # print(goto_target, current_line)
                            elif isinstance(obj.target, str) and obj.target in labels.keys():
                                goto_target[current_line] = labels[obj.target] - 1
                                current_line = goto_target[current_line]
                            elif isinstance(obj.target, str) and obj.target in variables.keys():
                                try:
                                    goto_target[current_line] = current_line + variables[obj.target]
                                    current_line = goto_target[current_line] - 1
                                except TypeError:
                                    goto_target[current_line] = labels[variables[obj.target]]
                                    current_line = goto_target[current_line] - 1
                except IndexError:
                    obj = Goto(statement, info)
                    obj.check_target(labels, total, current_line, variables)
                    if isinstance(obj.target, int):
                        goto_target[current_line] = current_line + obj.target
                        current_line = goto_target[current_line] - 1  # Jump to the target line, -1 since self increments
                    elif isinstance(obj.target, str) and obj.target in labels.keys():
                        goto_target[current_line] = labels[obj.target] - 1
                        current_line = goto_target[current_line]
                    elif isinstance(obj.target, str) and obj.target in variables.keys():
                        try:
                            goto_target[current_line] = current_line + variables[obj.target]
                            current_line = goto_target[current_line] - 1
                        except TypeError:
                            goto_target[current_line] = labels[variables[obj.target]]
                            current_line = goto_target[current_line] - 1


            elif token[0].kind() == GrinTokenKind.GOSUB:
                try:
                    if token[2].kind() == GrinTokenKind.IF:
                        # print('ENTER IF STATEMENT')
                        obj = GotoIf(statement, info)
                        obj.get_conditional()
                        values = obj.replace_conditional(variables)
                        left, right = values
                        result = obj.check_conditional(left, right)
                        # print(left, obj.conditional, right, result, obj.target)
                        if result:
                            if isinstance(obj.target, int):
                                # print('enter', current_line, obj.target)
                                goto_target[current_line] = current_line + obj.target
                                current_line = goto_target[current_line] - 1  # Jump to the target line
                                # print(goto_target, current_line)
                            elif isinstance(obj.target, str) and obj.target in labels.keys():
                                goto_target[current_line] = labels[obj.target] - 1
                                current_line = goto_target[current_line]
                            elif isinstance(obj.target, str) and obj.target in variables.keys():
                                try:
                                    goto_target[current_line] = current_line + variables[obj.target]
                                    current_line = goto_target[current_line] - 1
                                except TypeError:
                                    goto_target[current_line] = labels[variables[obj.target]]
                                    current_line = goto_target[current_line] - 1
                except IndexError:
                    # print('gosub', current_line)
                    gosub_lines.append(current_line)
                    # print(gosub_lines)
                    obj = Goto(statement, info)
                    obj.check_target(labels, total, current_line, variables)
                    if isinstance(obj.target, int):
                        # print('entered')
                        goto_target[current_line] = current_line + obj.target
                        current_line = goto_target[current_line] - 1  # Jump to the target line, -1 since self increments
                        # print(goto_target, current_line, gosub_lines)
                    elif isinstance(obj.target, str) and obj.target in labels.keys():
                        goto_target[current_line] = labels[obj.target] - 1
                        current_line = goto_target[current_line]
                    elif isinstance(obj.target, str) and obj.target in variables.keys():
                        try:
                            goto_target[current_line] = current_line + variables[obj.target]
                            current_line = goto_target[current_line] - 1
                        except TypeError:
                            goto_target[current_line] = labels[variables[obj.target]]
                            current_line = goto_target[current_line] - 1

            elif token[0].kind() == GrinTokenKind.RETURN:
                current_line = gosub_lines[-1]
                gosub_lines.remove(gosub_lines[-1])

            # Unable to test due to exit()
            elif token[0].kind() == GrinTokenKind.END:
                exit()
