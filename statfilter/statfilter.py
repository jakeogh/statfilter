#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from shutil import get_terminal_size
from kcl.assertops import maxone
from kcl.assertops import verify
from icecream import ic
import click
ic.configureOutput(includeContext=True)
ic.lineWrapWidth, _ = get_terminal_size((80, 20))

# 'st_atime'
# 'st_atime_ns'
# 'st_blksize'
# 'st_blocks'
# 'st_ctime'
# 'st_ctime_ns'
# 'st_dev'
# 'st_gid'
# 'st_ino'
# 'st_mode'
# 'st_mtime'
# 'st_mtime_ns'
# 'st_nlink'
# 'st_rdev'
# 'st_size'
# 'st_uid'


def read_by_byte(file_object, byte):    # by ikanobori
    buf = b""

    for chunk in iter(lambda: file_object.read(4096), b""):
        buf += chunk
        nul = buf.find(byte)

        while nul != -1:
            if nul == len(buf) - 1:
                return

            ret, buf = buf[:nul], buf[nul+1:]
            yield ret
            nul = buf.find(byte)

    #  Decide what you want to do with leftover


@click.command()
@click.option("--size", type=int)
@click.option("--min-mtime", type=float)
@click.option("--max-mtime", type=float)
@click.option("--empty-dir", is_flag=True)
@click.option("--exists", is_flag=True)
@click.option("--null", is_flag=True)
@click.option("--precise", is_flag=True)
@click.option("--count", is_flag=True)
@click.option("--verbose", is_flag=True)
def cli(size, min_mtime, max_mtime, empty_dir, exists, null, precise, count, verbose):

    if count:
        count = 0

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
            if min_mtime is not False:
                min_mtime = int(min_mtime)
            if max_mtime is not False:
                max_mtime = int(max_mtime)

        if precise:
            st_mtime = stat.st_mtime
        else:
            st_mtime = int(stat.st_mtime)

        if size is not False:
            if stat.st_size < size:
                continue

        if min_mtime is not False:
            if st_mtime < min_mtime:
                continue

        if max_mtime is not False:
            if st_mtime > max_mtime:
                continue

        if empty_dir:
            line_path = Path(line)
            if not line_path.is_dir():
                continue
            if len(list(line_path.glob('*'))) > 0:
                continue

        if count is not False:
            count += 1

        print(Path(os.fsdecode(line)).absolute().as_posix())

    if count:
        ic(count)


if __name__ == "__main__":
    cli()
