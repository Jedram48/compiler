import sys
import os
from lexer import lexer
from _parser import get_generated_code
def main():
    if len(sys.argv) != 3:
        print("python compiler.py <input_file.imp> <output_file.mr>")
        exit()
    
    with open(sys.argv[1], "r") as f:
        code = f.read()

    output = get_generated_code(code, lexer=lexer)
    with open(sys.argv[2], "w") as f:
        for asmc in output:
            f.write(asmc + '\n')
    
if __name__ == "__main__":
    main()