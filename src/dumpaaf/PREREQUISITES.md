pip install pyaaf2

Looks like SourceFile is sotred as a TaggedValue on the MasterMob. 
Then the start timecode is on the TimelineMobSlot.segment.starttime. 


I think you need to look for the slots on the sourcemob. Then look for the timelineMobSlot.segment.starttime. 


##Open timeline 
pip install opentimelineio
winget install --id=Kitware.CMake -e

import opentimelineio as otio

timeline = otio.adapters.read_from_file("foo.aaf")
for clip in timeline.each_clip():
  print clip.name, clip.duration()



Once you have installed opentimelineio

otioview path/to/your/file.edl



https://www.ics.uci.edu/~pattis/common/handouts/mingweclipse/mingw.html


VS CMake
C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\Tools\vsdevcmd\ext