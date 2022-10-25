#!/usr/bin/python3
'Converts Jupyter notebook file[s] to Python (interactive) file[s].'
# Author: Mark Blakeney, May 2022.

import os
import sys
import json
import shlex
import re
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Union

# Some constants
CODETAG = '# %%\n'
MDWNTAG = '# %% [markdown]\n'
CMNTTAG = '# '
PROG = Path(sys.argv[0]).stem
CNFFILE = Path(os.getenv('XDG_CONFIG_HOME', '~/.config'), f'{PROG}-flags.conf')

def write_file(opath: Path, out: str, args: Namespace) -> Union[bool, None]:
    # check if new file has not changed
    exists = opath.exists()
    if exists and opath.read_text() == out:
        return False

    with opath.open('w') as fp:
        fp.write(out)

    return True if exists else None

def convert_file(ipath: Path, dirout: Path, args: Namespace) -> bool:
    'Convert given input file'
    if args.out:
        if args.out == '-':
            opath = None
        else:
            opath = dirout / args.out
    else:
        if not dirout.is_absolute():
            opath = ipath.parent / dirout / ipath.with_suffix('.py').name
        elif ipath.is_absolute():
            opath = dirout / str(ipath.with_suffix('.py'))[1:]
        else:
            opath = dirout / ipath.with_suffix('.py')

    if args.purge:
        if not opath or not opath.exists():
            return False

        if not args.quiet:
            print(f'Purging {opath}')

        parent = opath.parent

        # Also remove the parent dir if empty
        opath.unlink()
        if parent.exists() and not any(parent.iterdir()):
            parent.rmdir()

        return True

    if opath and opath.exists() and not args.out and not args.force:
        if not args.no_warnings:
            print(f'Skipping {opath} : already exists.', file=sys.stderr)
        return False

    try:
        with ipath.open() as fp:
            js = json.load(fp)
    except Exception:
        if not args.no_warnings:
            print(f'Skipping {ipath} : is malformed.', file=sys.stderr)
        return False

    out = []
    if not args.out or convert_file.first:
        out.append('#!/usr/bin/env python3')
        convert_file.first = False

    out.append(f'\n## Built from {ipath} by {PROG} ##\n')

    cellist = js.get('cells')

    # Handle older format notebooks
    if cellist is None:
        wsheets = js.get('worksheets')
        if wsheets is None:
            if not args.no_warnings:
                print(f'Skipping {ipath} : does not appear to be a ipynb file.')
            return False

        cellist = []
        for ws in wsheets:
            cells = ws.get('cells')
            if cells:
                cellist.extend(cells)

    # For each cell in notebook ..
    has_code = False
    for cell in cellist:
        src = cell.get('source') or cell.get('input')
        if src is None:
            continue

        if isinstance(src, str):
            src = src.replace('\\n', '\n').splitlines()

        # Ignore if empty cell
        if not any(ln.strip() for ln in src) and not args.include_empty:
            continue

        cell_type = cell.get('cell_type')
        if cell_type == 'code':
            has_code = True
            hdr = '' if args.no_code_tag else CODETAG
            ldr = ''
        elif cell_type == 'markdown':
            if args.no_markdown:
                continue
            hdr = '' if args.no_markdown_tag else MDWNTAG
            ldr = CMNTTAG
        elif cell_type == 'heading':
            hdr = ''
            ldr = CMNTTAG
        else:
            continue

        # Write this cell's content
        out.append('\n' + hdr)
        for num, line in enumerate(src):
            if num == 0:
                line = line.lstrip('\r\n')

            for subline in (line.rstrip() + '\n').splitlines():
                out.append((ldr + subline).rstrip() + '\n')

    if not has_code:
        if not args.no_warnings:
            print(f'Warning: {ipath} has no Python code.', file=sys.stderr)
        if args.exclude_no_code:
            return False

    outbuf = ''.join(out)

    if opath:
        opath.parent.mkdir(exist_ok=True, parents=True)

        if args.out:
            with opath.open('a') as fp:
                fp.write(outbuf)
            msg = f'Wrote {opath} from {ipath}'
        else:
            res = write_file(opath, outbuf, args)
            if res:
                msg = f'UPDATED {opath}'
            elif res is None:
                msg = f'Created NEW {opath}'
            else:
                msg = f'No change to {opath}'

        if not args.quiet:
            print(msg)

    else:
        sys.stdout.write(outbuf)

    return True

convert_file.first = True

def convert_dir(ipath: Path, dirout: Path, args: Namespace) -> int:
    'Convert files in given input dir'
    count = 0
    for path in ipath.iterdir():
        if path.is_dir():
            if args.recurse:
                count += convert_dir(path, dirout, args)
        elif path.suffix.lower() == '.ipynb':
            count += convert_file(path, dirout, args)

    return count

def main() -> None:
    # Process command line options
    opt = ArgumentParser(description=__doc__.strip(),
            epilog=f'Note you can set default options in {CNFFILE}.')
    opt.add_argument('-m', '--no-markdown-tag', action='store_true',
            help='do not add markdown tag on markdown cells')
    opt.add_argument('-M', '--no-markdown', action='store_true',
            help='do not output markdown cells at all')
    opt.add_argument('-c', '--no-code-tag', action='store_true',
            help='do not add code tag on code cells')
    opt.add_argument('-e', '--include-empty', action='store_true',
            help='include empty/blank cells in output')
    opt.add_argument('-x', '--exclude-no-code', action='store_true',
            help='skip file if it contains no Python code cells')
    opt.add_argument('-f', '--force', action='store_true',
            help='force overwrite existing file[s]')
    opt.add_argument('-r', '--recurse', action='store_true',
            help='recursively process files in all sub-directories')
    opt.add_argument('-p', '--purge', action='store_true',
            help='just purge associated output file[s]')
    opt.add_argument('-q', '--quiet', action='store_true',
            help='suppress messages about processed file[s]')
    opt.add_argument('-w', '--no-warnings', action='store_true',
            help='suppress warning messages about processed file[s]')
    opt.add_argument('-o', '--out',
            help='alternative output file name, or \'-\' for stdout')
    opt.add_argument('-d', '--dir', default='.',
            help='output directory, default = ".". Specify absolute path '
            'to create separate tree of output files')
    opt.add_argument('ipynb_path', nargs='+',
            help='input ipynb file[s] (or dir for all *.ipynb files)')

    # Merge in default args from user config file. Then parse the
    # command line.
    cnflines = ''
    cnffile = CNFFILE.expanduser()
    if cnffile.exists():
        with cnffile.open() as fp:
            cnflines = [re.sub(r'#.*$', '', line).strip() for line in fp]
        cnflines = ' '.join(cnflines).strip()

    args = opt.parse_args(shlex.split(cnflines) + sys.argv[1:])

    dirout = Path(args.dir)

    if args.out:
        if args.out == '-':
            args.quiet = True
        else:
            path = dirout / args.out
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text('')

    count = 0
    for ipath in args.ipynb_path:
        path = Path(ipath)
        if not path.exists():
            if not args.no_warnings:
                print(f'Skipping {path} : does not exist', file=sys.stderr)
        elif path.is_dir():
            count += convert_dir(path, dirout, args)
        elif path.suffix.lower() != '.ipynb':
            if not args.no_warnings:
                print(f'Skipping {path} : does not have .ipynb suffix.',
                        file=sys.stderr)
        else:
            count += convert_file(path, dirout, args)

    if not args.quiet:
        plural = '' if count == 1 else 's'
        action = 'purged' if args.purge else 'converted'
        print(f'{count} file{plural} {action}.')

if __name__ == '__main__':
    main()
