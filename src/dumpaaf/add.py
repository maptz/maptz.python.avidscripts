from pathlib import Path
import aaf2

data_folder = Path('//example/workspace/Avid MediaFiles/MXF/folder/')

first_mxf = data_folder / '1315LY_v1.mxf'
second_mxf = data_folder / '1315LY_a1.mxf'
third_mxf = data_folder / '1315LY_a2.mxf'
forth_mxf = data_folder / '1315LY_a3.mxf'
fifth_mxf = data_folder / '1315LY_a4.mxf'

out_file = "test2.aaf"
with aaf2.open(out_file, 'w') as f:
    f.content.link_external_mxf(first_mxf)
    f.content.link_external_mxf(second_mxf)
    f.content.link_external_mxf(third_mxf)
    f.content.link_external_mxf(forth_mxf)
    f.content.link_external_mxf(fifth_mxf)