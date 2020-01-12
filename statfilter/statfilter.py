#!/usr/bin/env python3

import os
import sys
import click
from pathlib import Path
from uhashfs.utils import maxone
from uhashfs.utils import verify
from icecream import ic
ic.configureOutput(includeContext=True)
from shutil import get_terminal_size
ic.lineWrapWidth, _ = get_terminal_size((80, 20))
#ic.disable()


#'st_atime'
#'st_atime_ns'
#'st_blksize'
#'st_blocks'
#'st_ctime'
#'st_ctime_ns'
#'st_dev'
#'st_gid'
#'st_ino'
#'st_mode'
#'st_mtime'
#'st_mtime_ns'
#'st_nlink'
#'st_rdev'
#'st_size'
#'st_uid'


# DONT CHANGE FUNC NAME
@click.command()
@click.option("--size", type=int)
@click.option("--min-mtime", type=int)
@click.option("--max-mtime", type=int)
@click.option("--exists", is_flag=True)
@click.option("--null", is_flag=True)  # todo
def cli(size, min_mtime, max_mtime, exists, null):

    if exists:
        verify(maxone([size, min_mtime, max_mtime, exists]))

    for line in sys.stdin:
        line = line[:-1]

        try:
            stat = os.stat(line)
        except FileNotFoundError as e:
            if exists:
                continue
            else:
                raise e

        if size:
            if stat.st_size < size:
                continue

        if min_mtime:
            if stat.st_mtime < min_mtime:
                continue

        if max_mtime:
            if stat.st_mtime > max_mtime:
                continue

        print(line)


if __name__ == "__main__":
    cli()
