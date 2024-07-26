TASK="gameof24"
MODEL="gpt-4o"
SMODEL="D:\Workspace\lenovo%20intern\model\sentence"
EMB="./emb.pth"
TEMPLATE="./template.jsonl"
API_KEY="sk-Jp9YCIcVzEiwgIgg87F463EdC7F84992B8CcC4D6459d505a"

python run_benchmark.py \
    --task $TASK \
    --model $MODEL \
    --smodel $SMODEL \
    --emb $EMB \
    --template $TEMPLATE \
    --api_key $API_KEY
