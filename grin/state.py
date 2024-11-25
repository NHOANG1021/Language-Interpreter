from grin.token import *
from grin.grin_io import *

def grin_labels(statements: list) -> dict:
    """
    Returns a tuple of two dictionaries containing info
    about labels and line numbers.
    """
    labels = {}
    try:
        for index, statement in enumerate(statements):
            if statement[0].kind() == GrinTokenKind.RETURN:
                pass
            elif statement[0].kind() != GrinTokenKind.END and statement[1].kind() == GrinTokenKind.COLON:
                labels[statement[0].value()] = statement[0].location().line()
                statements[index] = statements[index][2:]
    except IndexError:
        pass
    return labels
