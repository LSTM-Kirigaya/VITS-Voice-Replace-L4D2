echo "make voice of grambler"
python make_raw_voice_dlc1.py --device cuda -n gambler --lang %1
python postprocess_dlc1.py -n gambler --lang %1

echo "make voice of producer"
python make_raw_voice_dlc1.py --device cuda -n producer --lang %1
python postprocess_dlc1.py -n producer --lang %1

echo "make voice of coach"
python make_raw_voice_dlc1.py --device cuda -n coach --lang %1
python postprocess_dlc1.py -n coach --lang %1

echo "make voice of mechanic"
python make_raw_voice_dlc1.py --device cuda -n mechanic --lang %1
python postprocess_dlc1.py -n mechanic --lang %1

echo "make voice of biker"
python make_raw_voice_dlc1.py --device cuda -n biker --lang %1
python postprocess_dlc1.py -n biker --lang %1

echo "make voice of manager"
python make_raw_voice_dlc1.py --device cuda -n manager --lang %1
python postprocess_dlc1.py -n manager --lang %1

echo "make voice of teengirl"
python make_raw_voice_dlc1.py --device cuda -n teengirl --lang %1
python postprocess_dlc1.py -n teengirl --lang %1