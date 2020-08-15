#!/usr/bin/python
import sys
import avb
import json
import os
# pip install pyavb
#http://markreidvfx.github.io/pyaaf/index.html


def dumpAvb(binPath):
    outputDirPath = os.path.dirname(os.path.abspath(binPath))
    fileNameWOExt = os.path.splitext(os.path.basename(binPath))[0]
    items = []
    distinctKeys = {}
    distinctKeys['name'] = 1
    distinctKeys['type'] = 1
    print("Opening .avb file: " + binPath)
    with avb.open(binPath) as f:
      print("Opened .avb file. Extracting sequences.")
      s=f
      for mob in f.content.mobs:
        if (mob.mob_type == 'SourceMob'):
            pass
        elif (mob.mob_type == 'MasterMob'):
            # attr1 = mob.property_data['attributes']
            # attr2 = mob.property_data['attributes']['_USER']
            # ndict = {}
            # ndict['name'] = mob.property_data['name']
            # ndict['type'] = "MASTER"
            # for key in attr2:
            #     ndict[key] = attr2[key]
            #     if key not in distinctKeys:
            #         distinctKeys[key] = 1
            # items.append(ndict)
            pass
        elif (mob.mob_type == 'CompositionMob'):
            attr1 = mob.property_data['attributes']
            attr2 = mob.property_data['attributes']['_USER']
            ndict = {}
            ndict['name'] = mob.property_data['name']
            ndict['type'] = "SEQUENCE"
            for key in attr2:
                ndict[key] = attr2[key]
                if key not in distinctKeys:
                    distinctKeys[key] = 1
            items.append(ndict)
            pass
        else:
            print(mob.name + " - " + mob.mob_type)
        # for track in mob.track:
        #     print(track.component)
    
    print("Dumping sequences to .json file.")
    json_string = json.dumps(items)
    jsonPath = os.path.join(outputDirPath, fileNameWOExt + ".json")
    with open(jsonPath, "w") as text_file:
        text_file.write(json_string)

    print("Dumping sequences to .txt file.")
    csv = ""
    for key in distinctKeys:
        csv += key + '\t'
    csv += '\n'
    for it in items:
        line = ""
        for key in distinctKeys:
            if key in it:
                line = line + it[key] + '\t'
            else:
                line = line + '\t'
        csv = csv + line + '\n'

    csvPath=os.path.join(outputDirPath, fileNameWOExt + ".txt")
    with open(csvPath, "w", encoding='utf-8') as text_file:
        text_file.write(csv)

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))

print("************************************")
print("***     Dumping Avid AVB file    ***")
print("***    to .txt and .json files   ***")
print("************************************")

binPath=""
if (len(sys.argv) < 2):
    # print("Not enough arguments. Exiting.")
    # exit()
    binPath="X:\\RUSHES.ARCHIVE - 2018 - ALL - SEQUENCES.avb"
else:
    binPath = sys.argv[1]


dumpAvb(binPath)

# with avb.open("C:/Users/steph/OneDrive/Desktop/TANJA TODO/RUSHES.ARCHIVE - 2017 - VIDEO - ALL.avb") as f:
#     for i, chunk in enumerate(f.chunks()):
#                 if chunk.class_id in  avb.utils.AVBClaseID_dict:

#                     item = f.read_object(i)
#                     print(item)