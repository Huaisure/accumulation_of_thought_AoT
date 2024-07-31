TASK="gameof24"
MODEL="gpt-4o"
SMODEL="Your Path to Sentence Model"
EMB="Your Path to Embedding"
TEMPLATE="Your Path to Template"
API_KEY="Your API Key"

python acot_benchmark.py \
    --task $TASK \
    --model $MODEL \
    --smodel $SMODEL \
    --emb $EMB \
    --template $TEMPLATE \
    --api_key $API_KEY
