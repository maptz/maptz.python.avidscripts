
#C:\Users\steph\AppData\Local\Programs\Python\Python37\Lib\site-packages\opentimelineio
## NB As a prerequisite, I had to: 
# VS2019 with C++ components installed.
# Python 3.7.9
# Running `pip install opentimelineio` in the Developer Command Prompt for VS 2019.

## THen I had to go to `C:\Users\steph\AppData\Local\Programs\Python\Python37\Lib\site-packages\opentimelineio` and move the two dlls



import opentimelineio as openio

timeline = openio.adapters.read_from_file("E:\\+++SHARED\\AVID TX\\20200816\\PULLS - IV - ALICE LASCELLES - Blending for the first time.01 - SB_010-BLEND - no breakout.aaf")
for clip in timeline.each_clip():
  print(clip.name, clip.duration())