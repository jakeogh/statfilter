#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from shutil import get_terminal_size
from kcl.assertops import maxone
from kcl.assertops import verify
from kcl.inputops import human_filesize_to_int
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
        #ic(len(chunk))
        buf += chunk
        sep = buf.find(byte)
        #ic(sep, len(buf))

        while sep != -1:
            #sep_end_marker = len(buf) - 1
            #ic(sep_end_marker)
            #if sep == sep_end_marker:
            #    ic(sep, "return")
            #    return

            ret, buf = buf[:sep], buf[sep + 1:]
            yield ret
            sep = buf.find(byte)
            #ic("after", sep)


    #ic("fell off end")
    #  Decide what you want to do with leftover


def statfilter(line,
               size=None,
               min_mtime=None,
               max_mtime=None,
               empty_dir=False,
               exists=False,
               precise=False,
               verbose=False):

    if not precise:
        if min_mtime is not None:
            min_mtime = int(min_mtime)
        if max_mtime is not None:
            max_mtime = int(max_mtime)

    try:
        stat = os.stat(line)
    except FileNotFoundError as e:
        if exists:
            return False
        else:
            raise e

    if precise:
        st_mtime = stat.st_mtime
    else:
        st_mtime = int(stat.st_mtime)

    if size is not None:
        if stat.st_size < size:
            return False

    if min_mtime is not None:
        if st_mtime < min_mtime:
            return False

    if max_mtime is not None:
        if st_mtime > max_mtime:
            return False

    if empty_dir:
        line_path = Path(line)
        if not line_path.is_dir():
            return False
        if len(list(line_path.glob('*'))) > 0:
            return False

    return True


@click.command()
@click.option("--size", type=str)
@click.option("--min-mtime", type=float)
@click.option("--max-mtime", type=float)
@click.option("--empty-dir", is_flag=True)
@click.option("--exists", is_flag=True)
@click.option("--null", is_flag=True)
@click.option("--precise", is_flag=True)
@click.option("--count", is_flag=True)
@click.option("--delete", is_flag=True)
@click.option("--summary", is_flag=True)
@click.option("--verbose", is_flag=True)
def cli(size, min_mtime, max_mtime, empty_dir, exists, null, precise, count, delete, summary, verbose):

    if size:
        try:
            size = int(size)
        except ValueError:
            size = human_filesize_to_int(size, verbose=verbose)
            if verbose:
                ic(size)

    if count:
        count = 0

    if exists:
        verify(maxone([size, min_mtime, max_mtime, exists, empty_dir]))

    byte = b'\n'
    if null:
        byte = b'\x00'

    for index, line in enumerate(read_by_byte(sys.stdin.buffer, byte=byte)):
        if verbose:
            ic(line)

        if statfilter(line=line,
                      size=size,
                      min_mtime=min_mtime,
                      max_mtime=max_mtime,
                      empty_dir=empty_dir,
                      exists=exists,
                      precise=precise,
                      verbose=verbose):

            if count is not False:
                count += 1

            print(Path(os.fsdecode(line)).absolute().as_posix())
            if delete:
                os.remove(line)

    if count:
        ic(count)

    if summary:
        ic(index)
