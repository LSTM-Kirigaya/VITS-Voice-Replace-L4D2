echo "postprocess of grambler"
python postprocess.py -n gambler --lang %1

echo "postprocess of producer"
python postprocess.py -n producer --lang %1

echo "postprocess of coach"
python postprocess.py -n coach --lang %1

echo "postprocess of mechanic"
python postprocess.py -n mechanic --lang %1