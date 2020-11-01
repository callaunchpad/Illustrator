#!/bin/bash
for FILE in /datasets/sketch-rnn/*; do
	ITEM=$(basename "$FILE" .full.npz)
	if [[ "$ITEM" == *.npz ]] ;
	then
		python3 seq2seqVAE_train.py --data_dir=/datasets/sketch-rnn --data_set="$ITEM" --experiment_dir=experiments
	fi
done
python3 call_snippet.py #comment out if you would prefer not to use twilio
