echo "make voice of grambler"
python make_raw_voice.py --device cuda -n gambler --log notebook/log/gambler.exceed.json --lang %1
python postprocess.py -n gambler --log notebook/log/gambler.exceed.json --lang %1

echo "make voice of producer"
python make_raw_voice.py --device cuda -n producer --log notebook/log/producer.exceed.json --lang %1
python postprocess.py -n producer  --log notebook/log/producer.exceed.json --lang %1

echo "make voice of coach"
python make_raw_voice.py --device cuda -n coach --log notebook/log/coach.exceed.json --lang %1
python postprocess.py -n coach  --log notebook/log/coach.exceed.json --lang %1

echo "make voice of mechanic"
python make_raw_voice.py --device cuda -n mechanic --log notebook/log/mechanic.exceed.json --lang %1
python postprocess.py -n mechanic --log notebook/log/mechanic.exceed.json --lang %1