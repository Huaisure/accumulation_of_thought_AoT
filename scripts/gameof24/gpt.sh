TASK="gameof24"
MODEL="gpt-3.5-turbo"
SMODEL="/dfs/data/model/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMB="./emb.pth"
TEMPLATE="./template.jsonl"
API_KEY="sk-lkXfNCALr3fB33Pv799894F979Af4f42A0827cFe5a3a8169"

python run_benchmark.py \
    --task $TASK \
    --model $MODEL \
    --smodel $SMODEL \
    --emb $EMB \
    --template $TEMPLATE \
    --api_key $API_KEY
