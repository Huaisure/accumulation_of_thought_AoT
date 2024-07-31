TASK="gameof24"
MODEL="Your Path to Llama Model"
SMODEL="Your Path to Sentence Model"
EMB="Your Path to Embedding"
TEMPLATE="Your Path to Template"

python acot_benchmark.py \
    --task $TASK \
    --model $MODEL \
    --smodel $SMODEL \
    --emb $EMB \
    --template $TEMPLATE \
