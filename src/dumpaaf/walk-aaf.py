
from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import os
import json

import subprocess
import aaf2
from aaf2 import video, audio


def dummy_print(*args):
    line = " ".join([str(item) for item in args])

def walk_aaf(root, space="", func=dummy_print):
    indent = "  "

    for p in root.properties():
        if isinstance(p, aaf2.properties.StrongRefProperty):
            func(space, p.name, p.typedef)
            walk_aaf(p.value, space + indent, func)

        if isinstance(p, aaf2.properties.StrongRefVectorProperty):
            func(space, p.name, p.typedef)
            for obj in p.value:
                func(space + indent, obj)
                walk_aaf(obj, space + indent*2, func)
            continue

        if isinstance(p, aaf2.properties.StrongRefSetProperty):
            func(space, p.name, p.typedef)
            for key, obj in p.items():
                func(space + indent, obj)
                walk_aaf(obj, space + indent*2, func)

            continue

        func(space, p.name, p.typedef, p.value)
