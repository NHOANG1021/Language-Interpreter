import unittest
from grin.token import *
from grin.grin_io import *
from grin.lexing import *
from grin.parsing import *
import contextlib
import io


class TestGrinIO(unittest.TestCase):
    def test_lex_statements(self):
        x = ['LET A 1', 'LET B 2', 'ADD A B', 'PRINT A', '.']
        tokens = lex_statements(x)
        self.assertEqual(type(tokens), list)
        self.assertEqual(type(tokens[0].__next__()), GrinToken)

    def test_parse_statements(self):
        x = ['PRINT A', 'LET A 1', 'PRINT A', '.']
        tokens = parse_statements(x)
        self.assertEqual(type(tokens), type((x for x in range(1))))
    def test_check_error_for_no_error(self):
        x = lex_statements(['LET A 1', 'LET B 2', 'PRINT A', 'PRINT B', '.'])
        error = check_errors(x)
        self.assertEqual(error, None)

    def test_get_token_info(self):
        x = ['PRINT A', 'LET A 1', 'PRINT A', '.']
        tokens = list(parse_statements(x))
        info = get_token_info(tokens[0])
        self.assertEqual(info[0][-1], 'PRINT')

    def test_get_statements(self):
        x = ['PRINT A', 'LET A 1', 'PRINT A', '.']
        tokens = list(parse_statements(x))
        info = get_token_info(tokens[0])
        statement = get_statement(info)
        self.assertEqual(statement, ['PRINT', 'A'])

    def test_run_let(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ['PRINT A', 'LET A 1', 'PRINT A', '.']
            tokens = list(parse_statements(x))
            run(tokens)
            test = output.getvalue()
            self.assertEqual(test, "0\n1\n")

    def test_run_print(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ['PRINT A', '.']
            tokens = list(parse_statements(x))
            run(tokens)
            test = output.getvalue()
            self.assertEqual(test, "0\n")

    def test_run_add(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ['LET A 1', 'ADD A 5', 'PRINT A']
            tokens = list(parse_statements(x))
            run(tokens)
            test = output.getvalue()
            self.assertEqual(test, "6\n")

    def test_run_add_variables(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ['LET A 1', 'LET B 5', 'ADD A B', 'PRINT A']
            tokens = list(parse_statements(x))
            run(tokens)
            test = output.getvalue()
            self.assertEqual(test, "6\n")

    def test_run_sub(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ['LET A 1', 'SUB A 5', 'PRINT A']
            tokens = list(parse_statements(x))
            run(tokens)
            test = output.getvalue()
            self.assertEqual(test, "-4\n")

    def test_run_sub_variables(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ['LET A 1', 'LET B 5', 'SUB A B', 'PRINT A']
            tokens = list(parse_statements(x))
            run(tokens)
            test = output.getvalue()
            self.assertEqual(test, "-4\n")


    def test_run_mult(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ['LET A 1', 'MULT A 5', 'PRINT A']
            tokens = list(parse_statements(x))
            run(tokens)
            test = output.getvalue()
            self.assertEqual(test, "5\n")

    def test_run_mult_variables(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ['LET A 1', 'LET B 5', 'MULT A B', 'PRINT A']
            tokens = list(parse_statements(x))
            run(tokens)
            test = output.getvalue()
            self.assertEqual(test, "5\n")

    def test_run_div_with_ints(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ['LET A 5', 'DIV A 1', 'PRINT A']
            tokens = list(parse_statements(x))
            run(tokens)
            test = output.getvalue()
            self.assertEqual(test, "5\n")

    def test_run_div_variables_with_ints(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ['LET A 5', 'LET B 1', 'DIV A B', 'PRINT A']
            tokens = list(parse_statements(x))
            run(tokens)
            test = output.getvalue()
            self.assertEqual(test, "5\n")

    def test_run_div_with_floats(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ['LET A 5.0', 'DIV A 1.0', 'PRINT A']
            tokens = list(parse_statements(x))
            run(tokens)
            test = output.getvalue()
            self.assertEqual(test, "5.0\n")

    def test_run_div_variables_with_floats(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ['LET A 5.0', 'LET B 1.0', 'DIV A B', 'PRINT A']
            tokens = list(parse_statements(x))
            run(tokens)
            test = output.getvalue()
            self.assertEqual(test, "5.0\n")

    def test_run_GOTO_with_int(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ['LET A 1', 'GOTO 2', 'LET A 2', 'PRINT A']
            tokens = list(parse_statements(x))
            run(tokens)
            test = output.getvalue()
            self.assertEqual(test, "1\n")

    def test_run_GOTO_with_multiple_ints(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ['LET Z 5', 'GOTO 5', 'LET C 4', 'PRINT C', 'PRINT Z', 'END', 'PRINT C', 'PRINT Z', 'GOTO -6', '.']
            tokens = list(parse_statements(x))
            try:
                run(tokens)
            except SystemExit:
                pass
            test = output.getvalue()
            self.assertEqual(test, "0\n5\n4\n5\n")

    def test_run_GOTO_with_labels(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ['LET Z 5', 'GOTO "CZ"', 'CCZ: LET C 4', 'PRINT C', 'PRINT Z', 'END', 'CZ: PRINT C', 'PRINT Z', 'GOTO "CCZ"', '.']
            tokens = list(parse_statements(x))
            try:
                run(tokens)
            except SystemExit:
                pass
            test = output.getvalue()
            self.assertEqual(test, "0\n5\n4\n5\n")

    def test_run_GOTO_with_variables(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ['LET Z 1', 'LET C 11', 'LET F 4', 'LET B "ZC"', 'GOTO F', 'ZC: PRINT Z', 'PRINT C', 'END', 'CZ: PRINT C', 'PRINT Z', 'GOTO B', '.']
            tokens = list(parse_statements(x))
            try:
                run(tokens)
            except SystemExit:
                pass
            test = output.getvalue()
            self.assertEqual(test, "11\n1\n1\n11\n")

    def test_run_GOTO_with_conditional(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ["LET A 3", "LET B 5", "GOTO 2 IF A < 4", "PRINT A", "PRINT B", "."]
            tokens = list(parse_statements(x))
            try:
                run(tokens)
            except SystemExit:
                pass
            test = output.getvalue()
            self.assertEqual(test, "5\n")

    def test_run_GOTO_with_conditional_fail(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ["LET A 3", "LET B 5", "GOTO 2 IF A > 4", "PRINT A", "PRINT B", "."]
            tokens = list(parse_statements(x))
            try:
                run(tokens)
            except SystemExit:
                pass
            test = output.getvalue()
            self.assertEqual(test, "3\n5\n")

    def test_run_GOTO_with_labels_and_conditional(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ['LET Z 5', 'GOTO "CZ" IF 1 = 1', 'CCZ: LET C 4', 'PRINT C', 'PRINT Z', 'END', 'CZ: PRINT C', 'PRINT Z', 'GOTO "CCZ"', '.']
            tokens = list(parse_statements(x))
            try:
                run(tokens)
            except SystemExit:
                pass
            test = output.getvalue()
            self.assertEqual(test, "0\n5\n4\n5\n")

    def test_run_GOTO_with_variables_and_conditional(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ['LET Z 1', 'LET C 11', 'LET F 4', 'LET B "ZC"', 'GOTO F IF 11 >= C', 'ZC: PRINT Z',
                 'PRINT C', 'END', 'CZ: PRINT C', 'PRINT Z', 'GOTO B IF Z = 1', '.']
            tokens = list(parse_statements(x))
            try:
                run(tokens)
            except SystemExit:
                pass
            test = output.getvalue()
            self.assertEqual(test, "11\n1\n1\n11\n")

    def test_run_GOSUB_with_int(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ["LET A 1", "GOSUB 4", "PRINT A", "PRINT B", "END", "LET A 2", "LET B 3", "RETURN", "."]
            tokens = list(parse_statements(x))
            try:
                run(tokens)
            except SystemExit:
                test = output.getvalue()
                self.assertEqual(test, "2\n3\n")

    def test_run_GOSUB_with_label(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ["LET A 3", "GOSUB \"PRINTABC\"", "LET B 4", "GOSUB \"PRINTABC\"", "LET C 5",
                 "GOSUB \"PRINTABC\"", "LET A 1", "GOSUB \"PRINTABC\"", "END", "PRINTABC: PRINT A",
                 "PRINT B", "PRINT C", "RETURN", "."]
            tokens = list(parse_statements(x))
            try:
                run(tokens)
            except SystemExit:
                test = output.getvalue()
                self.assertEqual(test, "3\n0\n0\n3\n4\n0\n3\n4\n5\n1\n4\n5\n")

    def test_run_GOSUB_with_multiple(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = ["LET A 1", "GOSUB 5", "PRINT A", "END", "LET A 3", "RETURN", "PRINT A", "LET A 2",
                 "GOSUB -4", "PRINT A", "RETURN", "."]
            tokens = list(parse_statements(x))
            try:
                run(tokens)
            except SystemExit:
                test = output.getvalue()
                self.assertEqual(test, "1\n3\n3\n")


if __name__ == '__main__':
    unittest.main()