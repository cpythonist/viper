try:
    import os
    import sys
    import traceback as tb

    sys.path.insert(1, ".\\core")
    import core.lex as clex
    import core.parse as cparse

    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1], 'r') as f:
                code = f.read()
        except FileNotFoundError:
            print(f"viper: File \"{sys.argv[1]}\" was not found.")
            sys.exit(1)

    elif len(sys.argv) == 1:
        print("viper: One filename argument must be given to parse.")
        sys.exit(1)

    else:
        print("viper: Too many arguments.")
        sys.exit(1)

except ModuleNotFoundError:
    print("viper: Import error while starting the Viper parser.")
    raise SystemExit(1)

except Exception as e:
    print("viper: Unknown error.")
    raise SystemExit(1)

try:
    lexer  = clex.Lexer(code)
    parser = cparse.Parser(lexer)
    parser.parse()

except Exception as e:
    print("viper: An unknown error has occured.")
    try:
        os.makedirs("logs")
    except FileExistsError:
        pass
    
    with open("logs\\mainErr.log", 'a') as f:
        f.write(tb.format_exc())
