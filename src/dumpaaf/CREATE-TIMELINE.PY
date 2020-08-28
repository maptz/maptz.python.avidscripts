import aaf2

# mocked up dictionary from Layout
maya_seq = {
        'aaf_name': 'Layout_Seq_AAF',
        'seq_name': 'Layout Send to Edit',
        'tracks': [
            {
                'v_track': 1,
                'v_track_name': 'Track 1',
                'clips': [
                    {'name': 'filler', 'frames': 50},
                    {'name': '960_010', 'frames': 100, 'start': 20, 'tape': '960_010_tape'}
                ]
            },
            {
                'v_track': 2,
                'v_track_name': 'Track 2',
                'clips': [
                    {'name': 'filler', 'frames': 130},
                    {'name': '960_020a', 'frames': 96, 'start': 1, 'tape': '960_020a_tape'}
                ]
            },
            {
                'v_track': 3,
                'v_track_name': 'Track 3',
                'clips': [
                    {'name': 'filler', 'frames': 130},
                    {'name': '960_020b', 'frames': 96, 'start': 1, 'tape': '960_020b_tape'}
                ]
            }

        ]
    }

with aaf2.open(maya_seq['aaf_name']+'.aaf', 'w') as f:

    edit_rate = 23.976
    timecode_fps = 24

    comp_mob = f.create.CompositionMob()
    comp_mob.usage = "Usage_TopLevel"
    comp_mob.name = maya_seq['seq_name']
    f.content.mobs.append(comp_mob)

    tc_slot = comp_mob.create_empty_sequence_slot(edit_rate, media_kind='timecode')
    tc = f.create.Timecode(24, True)
    tc.start = 86400
    tc_slot.segment.components.append(tc)

    nested_slot = comp_mob.create_timeline_slot(edit_rate)
    nested_slot['PhysicalTrackNumber'].value = 1
    nested_scope = f.create.NestedScope()
    nested_slot.segment= nested_scope

    for i in maya_seq['tracks']:
        sequence = f.create.Sequence(media_kind="picture")
        nested_scope.slots.append(sequence)

        for j in i['clips']:
            if j['name'] == 'filler':
                if i['v_track'] <= 1:
                    comp_fill = f.create.Filler("picture", j['frames'])
                else:
                    comp_fill = f.create.ScopeReference("picture", j['frames'])
                    comp_fill['RelativeSlot'].value = 1
                    comp_fill['RelativeScope'].value = 0

                sequence.components.append(comp_fill)

            else:

                tape_mob = f.create.SourceMob()
                tape_name = j['tape']
                tape_slot, tape_timecode_slot = tape_mob.create_tape_slots(tape_name, edit_rate, timecode_fps, media_kind='picture')
                tape_slot.segment.length = (j['frames'] + 86400)
                f.content.mobs.append(tape_mob)

                file_mob = f.create.SourceMob()
                tm_clip = tape_mob.create_source_clip(slot_id=1, start=86400, length=j['frames'])

                # NOTE: if you use the import_dnxhd_essence on master_mob you can skip the file_mobs
                #file_mob.import_dnxhd_essence(j['name']+".dnxhd", edit_rate, tm_clip)
                ## SE
                #//import_audio_essence
                #file_mob.create_essence(edit_rate=edit_rate, media_kind='picture', slot_id=1)
                file_mob.create_empty_slot(edit_rate=edit_rate, media_kind='picture', slot_id=1)

                file_mob.name = j['name']
                f.content.mobs.append(file_mob)

                master_mob = f.create.MasterMob()
                master_mob.name = j['name']
                f.content.mobs.append(master_mob)

                fm_clip = file_mob.create_source_clip(slot_id=1, length=j['frames'])
                print(fm_clip.start, fm_clip.length)

                slot = master_mob.create_picture_slot(edit_rate)
                slot.segment.components.append(fm_clip)

                mm_clip = master_mob.create_source_clip(slot_id=1, start=(j['start']-1), length=j['frames'])
                sequence.components.append(mm_clip)

    # comp_mob.dump()