#!/usr/bin/env python3

import os
import sys
import click
from pathlib import Path
from kcl.assertops import maxone
from kcl.assertops import verify
from icecream import ic
ic.configureOutput(includeContext=True)
from shutil import get_terminal_size
ic.lineWrapWidth, _ = get_terminal_size((80, 20))

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


def read_by_byte(file_object, byte):    # by ikanobori
    buf = b""

    for chunk in iter(lambda: file_object.read(4096), b""):
        #ic(chunk)
        buf += chunk
        nul = buf.find(byte)

        while nul != -1:
            if nul == len(buf) - 1:
                return

            ret, buf = buf[:nul], buf[nul+1:]
            yield ret
            nul = buf.find(byte)

    # TODO: Decide what you want to do with leftover


@click.command()
@click.option("--size", type=int)
@click.option("--min-mtime", type=float)
@click.option("--max-mtime", type=float)
@click.option("--empty-dir", is_flag=True)
@click.option("--exists", is_flag=True)
@click.option("--null", is_flag=True)
@click.option("--precise", is_flag=True)
@click.option("--verbose", is_flag=True)
def cli(size, min_mtime, max_mtime, empty_dir, exists, null, precise, verbose):

    if exists:
        verify(maxone([size, min_mtime, max_mtime, exists, empty_dir]))

    byte = b'\n'
    if null:
        byte = b'\x00'

    for line in read_by_byte(sys.stdin.buffer, byte=byte):
        if verbose:
            ic(line)

        try:
            stat = os.stat(line)
        except FileNotFoundError as e:
            if exists:
                continue
            else:
                raise e

        if not precise:
            min_mtime = int(min_mtime)
            max_mtime = int(max_mtime)

        if precise:
            st_mtime = stat.st_mtime
        else:
            st_mtime = int(stat.st_mtime)

        if size:
            if stat.st_size < size:
                continue

        if min_mtime:
            if st_mtime < min_mtime:
                continue

        if max_mtime:
            if st_mtime > max_mtime:
                continue

        if empty_dir:
            line_path = Path(line)
            if not line_path.is_dir():
                continue
            if len(list(line_path.glob('*'))) > 0:
                continue

        print(Path(os.fsdecode(line)).absolute().as_posix())


if __name__ == "__main__":
    cli()
