echo "make voice of whitaker"
python make_npc_voice.py --device cuda -n whitaker
python .\postprocess_npc.py -n whitaker

echo "make voice of virgil"
python make_npc_voice.py --device cuda -n virgil
python .\postprocess_npc.py -n virgil

echo "make voice of soldier1"
python make_npc_voice.py --device cuda -n soldier1
python .\postprocess_npc.py -n soldier1

echo "make voice of soldier2"
python make_npc_voice.py --device cuda -n soldier2
python .\postprocess_npc.py -n soldier2