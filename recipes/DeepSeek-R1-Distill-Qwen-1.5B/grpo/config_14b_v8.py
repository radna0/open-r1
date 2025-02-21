# Model arguments
model_name_or_path: deepseek-ai/DeepSeek-R1-Distill-Qwen-14B
model_revision: main
torch_dtype: bfloat16
attn_implementation: flash_attention_2

# Data training arguments
# We edit the DeepSeek chat template to ensure (a) the reasoning block within <think> and </think> is included in the completion and (b) the <think> tag is not part of the prefill so that the format reward works
chat_template: "{% if not add_generation_prompt is defined %}{% set add_generation_prompt = false %}{% endif %}{% set ns = namespace(is_first=false, is_tool=false, is_output_first=true, system_prompt='') %}{%- for message in messages %}{%- if message['role'] == 'system' %}{% set ns.system_prompt = message['content'] %}{%- endif %}{%- endfor %}{{bos_token}}{{ns.system_prompt}}{%- for message in messages %}{%- if message['role'] == 'user' %}{%- set ns.is_tool = false -%}{{'<｜User｜>' + message['content']}}{%- endif %}{%- if message['role'] == 'assistant' and message['content'] is none %}{%- set ns.is_tool = false -%}{%- for tool in message['tool_calls']%}{%- if not ns.is_first %}{{'<｜Assistant｜><｜tool▁calls▁begin｜><｜tool▁call▁begin｜>' + tool['type'] + '<｜tool▁sep｜>' + tool['function']['name'] + '\\n' + '```json' + '\\n' + tool['function']['arguments'] + '\\n' + '```' + '<｜tool▁call▁end｜>'}}{%- set ns.is_first = true -%}{%- else %}{{'\\n' + '<｜tool▁call▁begin｜>' + tool['type'] + '<｜tool▁sep｜>' + tool['function']['name'] + '\\n' + '```json' + '\\n' + tool['function']['arguments'] + '\\n' + '```' + '<｜tool▁call▁end｜>'}}{{'<｜tool▁calls▁end｜><｜end▁of▁sentence｜>'}}{%- endif %}{%- endfor %}{%- endif %}{%- if message['role'] == 'assistant' and message['content'] is not none %}{%- if ns.is_tool %}{{'<｜tool▁outputs▁end｜>' + message['content'] + '<｜end▁of▁sentence｜>'}}{%- set ns.is_tool = false -%}{%- else %}{% set content = message['content'] %}{{'<｜Assistant｜>' + content + '<｜end▁of▁sentence｜>'}}{%- endif %}{%- endif %}{%- if message['role'] == 'tool' %}{%- set ns.is_tool = true -%}{%- if ns.is_output_first %}{{'<｜tool▁outputs▁begin｜><｜tool▁output▁begin｜>' + message['content'] + '<｜tool▁output▁end｜>'}}{%- set ns.is_output_first = false %}{%- else %}{{'\\n<｜tool▁output▁begin｜>' + message['content'] + '<｜tool▁output▁end｜>'}}{%- endif %}{%- endif %}{%- endfor -%}{% if ns.is_tool %}{{'<｜tool▁outputs▁end｜>'}}{% endif %}{% if add_generation_prompt and not ns.is_tool %}{{'<｜Assistant｜>'}}{% endif %}"
dataset_name: GAIR/LIMO
dataset_configs:
- train
system_prompt: "You are a helpful AI Assistant that provides well-reasoned and detailed responses. You first think about the reasoning process as an internal monologue and then provide the user with the answer. Respond in the following format: <think>\n...\n</think>\n<answer>\n...\n</answer>"

# GRPO trainer config
bf16: true
use_vllm: true
vllm_device: auto
vllm_gpu_memory_utilization: 0.7
do_eval: true
gradient_accumulation_steps: 4
gradient_checkpointing: true
gradient_checkpointing_kwargs:
  use_reentrant: false
hub_model_id: Isekai-Creation/DeepSeek-R1-Distill-Qwen-14B-GRPO-LIMO
hub_strategy: every_save
learning_rate: 1.0e-5
log_completions: true
log_level: info
logging_first_step: true
logging_steps: 10
logging_strategy: steps
lr_scheduler_type: cosine
max_prompt_length: 512
max_completion_length: 2048
max_steps: -1
num_generations: 16
num_train_epochs: 15
output_dir: data/DeepSeek-R1-Distill-Qwen-14B-GRPO-LIMO
overwrite_output_dir: true
per_device_eval_batch_size: 16
per_device_train_batch_size: 16
push_to_hub: true
report_to:
- wandb
reward_funcs:
- accuracy
- format
reward_weights:
- 1.0
- 1.0
benchmarks:
- math_500
- aime24
- gpqa
save_strategy: "epoch"
seed: 42
temperature: 0.7
warmup_ratio: 0.1
