echo "make voice of grambler"
python make_raw_voice.py --device cuda -n gambler --lang %1
python postprocess.py -n gambler --lang %1

echo "make voice of producer"
python make_raw_voice.py --device cuda -n producer --lang %1
python postprocess.py -n producer --lang %1

echo "make voice of coach"
python make_raw_voice.py --device cuda -n coach --lang %1
python postprocess.py -n coach --lang %1

echo "make voice of mechanic"
python make_raw_voice.py --device cuda -n mechanic --lang %1
python postprocess.py -n mechanic --lang %1