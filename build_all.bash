echo "make voice of grambler"
python make_raw_voice.py --device cuda -n gambler
python postprocess.py -n gambler

echo "make voice of producer"
python make_raw_voice.py --device cuda -n producer
python postprocess.py -n producer

echo "make voice of coach"
python make_raw_voice.py --device cuda -n coach
python postprocess.py -n coach

echo "make voice of mechanic"
python make_raw_voice.py --device cuda -n mechanic
python postprocess.py -n mechanic