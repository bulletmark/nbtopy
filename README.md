## NBTOPY - Converts Jupyter notebook files to Python files
[![PyPi](https://img.shields.io/pypi/v/nbtopy)](https://pypi.org/project/nbtopy/)
[![AUR](https://img.shields.io/aur/version/nbtopy)](https://aur.archlinux.org/packages/nbtopy/)

[nbtopy](http://github.com/bulletmark/nbtopy) is a Linux command line
utility to convert one or more [Jupyter](https://jupyter.org/) notebook
files (`.ipynb`) to Python files (`.py`). My primary purpose for
creating this utility is to quickly and easily create Python files to
use with the superb [Python
Interactive](https://code.visualstudio.com/docs/python/jupyter-support-py)
mode in [Visual Studio Code](https://code.visualstudio.com/), which I
often prefer to use instead of the Jupyter notebook. In the generated
code, Python code blocks are delimited by `# %%` tags and markdown
blocks are delimited by `# %% [markdown]` tags.

A typical use case is when you download a directory of Jupyter notebook
files and want run them using a VS Code [Python
Interactive](https://code.visualstudio.com/docs/python/jupyter-support-py)
window. Just run `nbtopy .` in the directory and all the Python files
are created and ready to use. You could use VS Code's inbuilt command to
create a Python file from the notebook but that is slow and awkward
because you have to run it explicitly for each notebook, and then
manually rename each created file. Also, VS Code uses Jupyter's
[`nbconvert`](https://nbconvert.readthedocs.io/) tool to do the
conversion and that runs *much* slower than `nbtopy`.

This program uses only pure Python and does not require any
[Jupyter](https://jupyter.org/) or 3rd party software or utilities to be
installed.

### Examples

1. Convert single `myfile.ipynb` file to new `myfile.py`:

    ```
    $ nbtopy myfile.ipynb
    ```

2. Convert all `*.ipynb` files in current directory to `*.py`:

    ```
    $ nbtopy . (effectively same as nbtopy *.ipynb)
    ```

3. Write all `*.py` files to directory `pyfiles/` instead of current dir:

    ```
    $ nbtopy -d pyfiles .
    ```

4. Recurse through all child directories and write `*.py` files to
   directory `pyfiles/` in same directories as source `**/*.ipynb`
   files.

    ```
    $ nbtopy -r -d pyfiles .
    ```

5. Recurse through all child directories and write `*.py` files to new
   and independent tree rooted under `pyfiles/`. Specify this by using
   an absolute (rather than relative) path for `-d/--dir`.

    ```
    $ nbtopy -r -d $PWD/pyfiles .
    ```

## Installation or Upgrade

Arch users can install [nbtopy from the AUR](https://aur.archlinux.org/packages/nbtopy/).

Python 3.6 or later is required. Note [nbtopy is on
PyPI](https://pypi.org/project/nbtopy/) so just ensure that
`python3-pip` and `python3-wheel` are installed then type the following
to install (or upgrade):

```
$ sudo pip3 install -U nbtopy
```

Or, to install from this source repository:

```
$ git clone http://github.com/bulletmark/nbtopy
$ cd nbtopy
$ sudo pip3 install -U .
```

To upgrade from the source repository:

```
$ cd nbtopy # i.e. to git source dir above
$ git pull
$ sudo pip3 install -U .
```

This program runs on pure Python. No 3rd party packages are required.
Note that this program does not require Jupyter's
[nbconvert](https://nbconvert.readthedocs.io/) tool.

## Command Line Options

Type `nbtopy -h` to view the usage summary:

```
usage: nbtopy [-h] [-m] [-M] [-c] [-e] [-x] [-f] [-r] [-p] [-q] [-w]
                 [-o OUT] [-d DIR]
                 ipynb_path [ipynb_path ...]

Converts Jupyter notebook file[s] to Python (interactive) file[s].

positional arguments:
  ipynb_path            input ipynb file (dir for *.ipynb files)

options:
  -h, --help            show this help message and exit
  -m, --no-markdown-tag
                        do not add markdown tag on markdown cells
  -M, --no-markdown     do not output markdown cells at all
  -c, --no-code-tag     do not add code tag on code cells
  -e, --include-empty   include empty/blank cells in output
  -x, --exclude-no-code
                        skip file if it contains no Python code cells
  -f, --force           force overwrite existing file[s]
  -r, --recurse         recursively process files in all sub-directories
  -p, --purge           just purge associated output file[s]
  -q, --quiet           suppress messages about processed file[s]
  -w, --no-warnings     suppress warning messages about processed file[s]
  -o OUT, --out OUT     alternative output file name, or '-' for stdout
  -d DIR, --dir DIR     output directory, default = ".". Specify absolute path
                        to create separate tree of output files

Note you can set default options in ~/.config/nbtopy-flags.conf.
```

## Default Options

You can add default options to a personal configuration file
`~/.config/nbtopy-flags.conf`. If that file exists then each line of
options will be concatenated and automatically prepended to your
`nbtopy` command line options. Type `nbtopy -h` to see the options
supported.

E.g. in your `~/.config/nbtopy-flags.conf` you could have the line
`--no-markdown-tag` so that markdown cells are always merely aded as
comments, without an explicit markdown tag.

## License

Copyright (C) 2022 Mark Blakeney. This program is distributed under the
terms of the GNU General Public License. This program is free software:
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation,
either version 3 of the License, or any later version. This program is
distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License at
<http://www.gnu.org/licenses/> for more details.

<!-- vim: se ai syn=markdown: -->
