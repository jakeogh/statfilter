#!/usr/bin/env python3

import os
import sys
import click
from pathlib import Path
from icecream import ic
ic.configureOutput(includeContext=True)
from shutil import get_terminal_size
ic.lineWrapWidth, _ = get_terminal_size((80, 20))
#ic.disable()


# DONT CHANGE FUNC NAME
@click.command()
@click.option("--size", type=int)
def cli(size):
    for line in sys.stdin:
        line = line[:-1]
        if os.stat(line).st_size >= size:
            print(line)


if __name__ == "__main__":
    cli()
