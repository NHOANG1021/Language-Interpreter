import unittest
from grin.statements import *
from grin.grin_io import *


class TestStatements(unittest.TestCase):
    def setUp(self):
        x = ['LET A 1', 'ADD A 5', 'SUB B 1', 'MULT A 1', 'DIV B 1' ,'PRINT A', '.']
        self.info = get_token_info(list(parse_statements(x))[0])
        self.statement = get_statement(self.info)
    def test_Statement(self):
        obj = Statement(self.statement, self.info)
        self.assertTrue(isinstance(obj, Statement))

    def test_VarValue(self):
        obj = VarValue(self.statement, self.info)
        self.assertTrue(isinstance(obj, VarValue))

    def test_let(self):
        obj = VarValue(self.statement, self.info)
        obj.let({})
        self.assertEqual(obj.var, 'A')

    def test_print(self):
        obj = VarValue(self.statement, self.info)
        obj.print()
        self.assertEqual(obj.value, 'A')

    def test_add(self):
        obj = VarValue(self.statement, self.info)
        obj.add()
        self.assertEqual(obj.var, 'A')
    def test_sub(self):
        obj = VarValue(self.statement, self.info)
        obj.sub()
        self.assertEqual(obj.var, 'A')

    def test_mult(self):
        obj = VarValue(self.statement, self.info)
        obj.mult()
        self.assertEqual(obj.var, 'A')

    def test_div(self):
        obj = VarValue(self.statement, self.info)
        obj.div()
        self.assertEqual(obj.var, 'A')

    def test_Goto(self):
        obj = Goto(self.statement, self.info)
        self.assertTrue(isinstance(obj, Goto))
        self.assertTrue(isinstance(obj, Statement))


if __name__ == '__main__':
    unittest.main()