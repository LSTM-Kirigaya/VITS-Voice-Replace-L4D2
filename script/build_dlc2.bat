echo "make voice of namvet"
python make_raw_voice_dlc2.py --device cuda -n namvet --lang %1
python postprocess_dlc2.py -n namvet --lang %1

echo "make voice of biker"
python make_raw_voice_dlc2.py --device cuda -n biker --lang %1
python postprocess_dlc2.py -n biker --lang %1

echo "make voice of manager"
python make_raw_voice_dlc2.py --device cuda -n manager --lang %1
python postprocess_dlc2.py -n manager --lang %1

echo "make voice of teengirl"
python make_raw_voice_dlc2.py --device cuda -n teengirl --lang %1
python postprocess_dlc2.py -n teengirl --lang %1