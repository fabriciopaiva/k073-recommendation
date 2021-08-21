from tokenize import tokenize, NUMBER, STRING, NAME, OP
from collections import defaultdict
import re
import sys


def help_and_exit():
    print( "   *** Usage:", sys.argv[0], "<code_filename> <input_filename> <output_filename>")
    exit(0)


def proccess_file(filename, preffix='in'):
    ''' Searching for features in input_file ...
        multi line; needs split; has int; has float; has string '''
    num_nom_empty_lines=0
    needs_split=0
    has_int=0
    has_float=0
    has_str=0

    with open(filename, 'r') as f:
        for line in f:

            # Multi Line
            line=line.strip()
            if line != '':
                num_nom_empty_lines += 1
            multi_line = 0 if (num_nom_empty_lines <= 1) else 1

            # Needs Split
            line=line.split()
            if len(line) > 1:
                needs_split=1

            # Has int/float/string
            for token in line:
                try:
                    int(token)
                    has_int=1
                    continue
                except:
                    pass

                try:
                    float(token)
                    has_float=1
                    continue
                except:
                    pass

                has_str=1

    print(f'{multi_line} {preffix}_multi_line\n'
          f'{needs_split} {preffix}_needs_split\n'
          f'{has_int} {preffix}_has_int\n'
          f'{has_float} {preffix}_has_float\n'
          f'{has_str} {preffix}_has_str' )


def proccess_code_file( filename ):
    ''' int() float() range() replace() split() for  while
        [] {} Extra space formatter
        +/-/*//   <>=!=
        missin' :  <---------- TODO: Try to ge the error message       
        slice ([:::])'''

    feat=defaultdict(lambda: 0)

    with open(filename, 'rb') as f:

        for toktype, tokval, _, _, _ in tokenize(f.readline):

            if toktype == NAME:
                if tokval == 'int'   : feat['has_int_function'] = 1
                if tokval == 'float' : feat['has_float_function'] = 1
                if tokval == 'range' : feat['has_range_function'] = 1
                if tokval == 'split' : feat['has_split_function'] = 1
                if tokval == 'replace' : feat['has_replace_function'] = 1
                if tokval == 'for'   : feat['has_for'] = 1
                if tokval == 'while' : feat['has_while'] = 1
                if tokval == 'format' : feat['has_format'] = 1

            if toktype == OP:
                if tokval in '[]'      : feat['has_list'] = 1
                if tokval in '\{\}'    : feat['has_dict'] = 1
                if tokval in '+-/*'    : feat['has_arit'] = 1
                if tokval in '<>=!'    : feat['has_logic'] = 1

            if toktype == STRING:
                if tokval.endswith(' ')   : feat['has_extra_space'] = 1
                if tokval.startswith('f') : feat['has_format'] = 1

    with open(filename, 'r') as f:

        for line in f:
            if re.search(r'\'[ \t]*%',line): feat['has_format'] = 1
            if re.search(r'"[ \t]*%',line):  feat['has_format'] = 1
            if re.search(r'\[.*:.*\]',line): feat['has_slice'] = 1

    for k in ('has_int_function',
              'has_float_function',
              'has_range_function',
              'has_split_function',
              'has_replace_function',
              'has_for',
              'has_while',
              'has_format',
              'has_list',
              'has_dict',
              'has_arit',
              'has_logic',
              'has_extra_space',
              'has_slice'):
        print(f'{feat[k]} code_{k}')


if __name__ == '__main__':

    if len(sys.argv) != 4:
        help_and_exit()

    code_file, in_file, out_file = sys.argv[1:]

    proccess_file(in_file)
    proccess_file(out_file, preffix="out")
    proccess_code_file(code_file)

