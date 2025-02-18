

accelerate launch --config_file=../../recipes/accelerate_configs/zero3.yaml \
    --num_processes=2 grpo.py \
    --config ../../recipes/DeepSeek-R1-Distill-Qwen-1.5B/grpo/config_7b.yaml
    --resume_from_checkpoint="$1/$2"
