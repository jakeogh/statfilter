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

def read_by_null(file_object):
    buf = b""

    for chunk in iter(lambda: file_object.read(4096), b""):
        #ic(chunk)
        buf += chunk
        nul = buf.find(b"\x00")

        while nul != -1:
            if nul == len(buf) - 1:
                print("returning")
                return

            ret, buf = buf[:nul], buf[nul+1:]
            yield ret
            nul = buf.find(b"\x00")

    # Decide what you want to do with leftover




# DONT CHANGE FUNC NAME
@click.command()
@click.option("--size", type=int)
@click.option("--min-mtime", type=int)
@click.option("--max-mtime", type=int)
@click.option("--empty-dir", is_flag=True)
@click.option("--exists", is_flag=True)
@click.option("--null", is_flag=True)  # todo
@click.option("--verbose", is_flag=True)  # todo
def cli(size, min_mtime, max_mtime, empty_dir, exists, null, verbose):

    # todo null, see func from irc
    if exists:
        verify(maxone([size, min_mtime, max_mtime, exists, empty_dir]))

    assert(null)

    for line in read_by_null(sys.stdin.buffer):
        if verbose:
            print(repr(line))

    #for line in sys.stdin:
    #    line = line[:-1]

        try:
            stat = os.stat(line)
            if b'glide.1' in line:
                ic(stat)
        except FileNotFoundError as e:
            if exists:
                continue
            else:
                raise e

        if size:
            if stat.st_size < size:
                continue

        if min_mtime:
            if b'glide.1' in line:
                ic(line)
            if stat.st_mtime < min_mtime:
                continue

        if max_mtime:
            if stat.st_mtime > max_mtime:
                continue

        if empty_dir:
            line_path = Path(line)
            if not line_path.is_dir():
                continue
            if len(list(line_path.glob('*'))) > 0:
                continue

        print(line)


if __name__ == "__main__":
    cli()
