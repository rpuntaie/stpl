#! /usr/bin/env python3
# -*- coding: utf-8 -*

# Homepage: https://github.org/rpuntaie/stpl
# License: See LICENSE file

import bottle
import os

def stpl(file_or_string,**kw):
    return bottle.template(file_or_string
            ,template_lookup = [os.getcwd(),os.path.dirname(os.getcwd())]
            ,**kw
            ) 


def main(**args):
    import codecs
    import sys
    import argparse

    if not args:
        parser = argparse.ArgumentParser(description=
                '''Expands bottle SimpleTemplate. See https://bottlepy.org/docs/dev/stpl.html.
                - stands for stdin. If not a file, then the string is expanded.
                ''')
        parser.add_argument('file_or_string', 
                help='If the input file ends in .stpl this is automatically dropped when a directory is given')
        parser.add_argument('directory', nargs='?',
                help='If no directory, the result is printed to stdout.')
        parser.add_argument('code', nargs='?',
                help='As third parameter python code can define some variables used in the template.')
        args = parser.parse_args().__dict__

    if args['code'] is not None:
        eval(compile(args['code'],'<string>','exec'),globals())

    filename = file_or_string = args['file_or_string']
    directory = args['directory']

    file = None
    isfile = os.path.isfile(file_or_string)
    if not isfile and file_or_string == '-':
        try:
            sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach()) 
        except: pass
        file_or_string = sys.stdin.read()
    elif isfile:
        file = file_or_string.replace('\\','/')
        with open(file,'r',encoding='utf-8') as f:
            file_or_string = f.read()

    g = globals()
    g['__file__'] = file
    result = stpl(file_or_string,**g)

    outfile = None
    opn = lambda x: open(x,'w',encoding='utf-8')
    try:
        if directory is None or directory=='-':
            try:
                sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
            except: pass
            outfile = sys.stdout
        elif os.path.isdir(directory):
            if isfile:
                if filename.endswith('.stpl'):
                    outfile  = opn(os.path.join(directory,filename[:-5]))
                else:
                    outfile  = opn(os.path.join(directory,filename))
            else:
                raise ValueError("Either no input file or no output file was given")
        else:
            outfile  = opn(directory)
        outfile.write(result)
    finally:
        if outfile is not None and outfile != sys.stdout:
            outfile.close()

if __name__ == '__main__':
    main() #pragma: no cover

