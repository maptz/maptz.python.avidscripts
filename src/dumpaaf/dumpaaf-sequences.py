#!/usr/bin/python
import sys
import avb
import json
import os
import aaf2
import inspect
# pip install pyaaf2
#http://markreidvfx.github.io/pyaaf/index.html


def printProperties(theObject):
    # for property, value in vars(theObject).iteritems():
    #     print(property, ": ", value)
    for name,thing in inspect.getmembers(theObject):
        print(name)

##NB Looks like you can add a TAGGEDVALUE
##tag = f.create.TaggedValue("_COLOR_R",  49664) #think this is 16bit color value
##mob['MobAttributeList'].append(tag)

def dumpAAF(binPath):
    with aaf2.open(binPath, "r") as f:
        #f.dump()
        # get the main composition
        main_compostion = next(f.content.toplevel())

        # print the name of the composition
        print("Composition name: " + main_compostion.name)
        #printProperties(main_compostion)

        # AAFObjects have properties that can be
        # accessed just like a dictionary
        print("Creation Time: " + str(main_compostion['CreationTime'].value))

        # video, audio and other track types are
        # stored in slots on a mob object.
        for slot in main_compostion.slots:
            segment = slot.segment
            print("SEGMENT" + str(segment) + segment.media_kind)
            #if (True):
            if (segment.media_kind == "Sound"):
                for component in segment.components:
                    for ar in component.slot.segment.property_entries:
                        ass =component.slot.segment.property_entries[ar]
                        if (ass.name == "StartTime"):
                            val = ass.value
                            s = component.slot.segment
                            print("StartTime ", val)

                    print(" SLOT PROPERTIES")
                    for pr in component.slot.property_entries:
                        print("   PROPERTY ENTRY: ", component.slot.property_entries[pr].name, " val: ", component.slot.property_entries[pr].value)
                    print(" MOB PROPERTIES ", component.mob.name)
                    for pr in component.mob.property_entries:
                        print("   PROPERTY ENTRY: ", component.mob.property_entries[pr].name, " val: ", component.mob.property_entries[pr].value)

                    
                    

            

print("************************************")
print("***     Dumping Avid AAF file    ***")
print("***    to .txt and .json files   ***")
print("************************************")

def generateAAF():
    with aaf2.open("example2.aaf", 'w') as f:
        # objects are create with a factory
        # on the AAFFile Object
        mob = f.create.MasterMob("Demo2")

        # add the mob to the file
        f.content.mobs.append(mob)

        edit_rate = 25

        # lets also create a tape so we can add timecode (optional)
        tape_mob = f.create.SourceMob()
        f.content.mobs.append(tape_mob)

        timecode_rate = 25
        start_time = timecode_rate * 60 * 60 # 1 hour
        tape_name = "Demo Tape"

        # add tape slots to tape mob
        tape_mob.create_tape_slots(tape_name, edit_rate,
                                   timecode_rate, media_kind='picture')

        # create sourceclip that references timecode
        tape_clip = tape_mob.create_source_clip(1, start_time)

        # now finally import the generated media
        mob.import_dnxhd_essence("sample.dnxhd", edit_rate, tape_clip)
        mob.import_audio_essence("sample.wav", edit_rate)

binPath=""
if (len(sys.argv) < 2):
    # print("Not enough arguments. Exiting.")
    # exit()
    #binPath="E:\\+++SHARED\\AVID TX\\20200815\\PREMIERE SIMPLE AUDIO EXPORT.aaf"
    binPath="E:\\+++SHARED\\AVID TX\\20200815\\SIMPLE AAF FROM AVID NICKT07.aaf"
else:
    binPath = sys.argv[1]


dumpAAF(binPath)
