#!/usr/bin/python
import sys
import avb
import json
import os
import aaf2
import inspect
# pip install pyaaf2
#http://markreidvfx.github.io/pyaaf/index.html
#see here https://github.com/markreidvfx/pyaaf/tree/master/example


#the following will add a "New" composition to your aaf file and place a different clip every 100 edit units separated by 100 units of filler. then dumps the edit position of each sourceclip.
with aaf2.open("aaf_2trks_4clips.aaf", 'rw') as f:
    edit_rate = 25
    c = f.create.CompositionMob("New")
    f.content.mobs.append(c)
    track1 = c.create_sound_slot(edit_rate)

    for mob in f.content.mastermobs():
        length = 100
        start = 0
        slot_id = 3
        filler = f.create.Filler('sound', length)
        audio_clip =  mob.create_source_clip(slot_id, start, length)
        track1.segment.components.append(filler)
        track1.segment.components.append(audio_clip)

    # dump the edit postion of every sourceclip
    edit_pos = 0
    for item in track1.segment.components:
        if isinstance(item, aaf2.components.SourceClip):
            print(item.mob.name, "at", edit_pos)

        edit_pos += item.length
