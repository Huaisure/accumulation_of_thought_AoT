TASK="gameof24"
MODEL="/dfs/data/model/Meta-Llama-3-8B-Instruct"
SMODEL="/dfs/data/model/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMB="./emb.pth"
TEMPLATE="./template.jsonl"

python run_benchmark.py \
    --task $TASK \
    --model $MODEL \
    --smodel $SMODEL \
    --emb $EMB \
    --template $TEMPLATE \
