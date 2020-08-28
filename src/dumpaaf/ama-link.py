from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import sys
import os
import subprocess
import json

import aaf2


FFPROBE_EXEC = 'ffprobe'

def probe(path):

    cmd = [FFPROBE_EXEC, '-of','json','-show_format','-show_streams', path]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout,stderr = p.communicate()

    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, "\n{}\n{}".format(subprocess.list2cmdline(cmd), stderr))

    return json.loads(stdout.decode('utf8'))

def makeFiles(files):
    out_file = "ama_link_external_mxf.aaf"
    with aaf2.open(out_file, 'w') as f:
        for path in files:
            name, ext = os.path.splitext(path)
            if ext.lower() == '.mxf':
                metadata = {}
            else:
                metadata = probe(path)

            for mob in f.content.create_ama_link(path, metadata):
                print(mob.name)

#makeFiles(sys.argv[1:])
makeFiles(["F:\\PROJECT FILES - JW\PROXIES\\testfilesshareblob\\20200804_MIV_SOUND\\20Y08M04\\NICKT07.WAV"])