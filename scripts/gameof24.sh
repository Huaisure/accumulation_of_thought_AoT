TASK = "gameof24"
MODEL = "/dfs/data/model/meta-llama/Llama-3-8B-Instruct"
SMODEL = ""
EMB = ""
TEMPLATE = ""

python run_benchmark.py \
    --task_name $TASK \
    --model $MODEL \
    --smodel $SMODEL \
    --emb $EMB \
    --template $TEMPLATE \
