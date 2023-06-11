echo "make voice of whitaker"
python make_npc_voice.py --device cuda -n whitaker --lang %1
python .\postprocess_npc.py -n whitaker --lang %1

echo "make voice of virgil"
python make_npc_voice.py --device cuda -n virgil --lang %1
python .\postprocess_npc.py -n virgil --lang %1

echo "make voice of soldier1"
python make_npc_voice.py --device cuda -n soldier1 --lang %1
python .\postprocess_npc.py -n soldier1 --lang %1

echo "make voice of soldier2"
python make_npc_voice.py --device cuda -n soldier2 --lang %1
python .\postprocess_npc.py -n soldier2 --lang %1