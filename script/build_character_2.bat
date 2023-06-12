echo make voice of %1
python make_raw_voice_dlc1.py --device cuda -n %1 --lang %2
python postprocess_dlc1.py -n %1 --lang %2

python make_raw_voice_dlc2.py --device cuda -n %1 --lang %2
python postprocess_dlc2.py -n %1 --lang %2