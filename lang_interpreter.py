import grin


def main() -> None:
    """
    Runs the program in its entirety.
    """
    statements = grin.start()
    grin.check_errors(grin.parse_statements(statements))
    parse_grin_tokens = list(grin.parse_statements(statements))
    grin.run(parse_grin_tokens)

if __name__ == '__main__':
    main()
