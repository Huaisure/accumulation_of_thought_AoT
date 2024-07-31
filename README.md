Two main modules here: ACoT (Accumulated Chain of Thought) and Prompt Function.😉

# Accumulated Chain of Thought

## Modules

### 1. Thoughts Manager

***Functions***:

- [x] `Thoughts Retrieval`: Based on the input, retrieve the most relevant template.

- [ ] **`Extract Template From QA Pairs`**: Learn from QA pairs to acquire more templates naturally, and upgrade the generalizablity and universality of the template.

> **How to Evaluate a Template?** Number of questions answered correctly 
with the template to be tested

- [x] `Upgrade Template After Ansering Questions`: Once the questions have been answered using one of the template, the template can be selectively upgraded.

### ACoT

Controller, utilize LLM and Thoughts Manager to better deal with different kinds of problems

### Prompter

***Functions***:

- [x] `Provide prompts for various task`
- [ ] `Extract answers under specific tasks` 

### LLM

Get responce based on the input prompt.

# Prompt Function

Constructing Prompt as a Function like

> function <funtion_name> (input)-> output: \
> &ensp;&ensp;&ensp;rules: <rule 1>;<rule 2>

Throught our method, you can easily:

- decompose a huge and complex problem
- construct your own solution process based your own thinking
- control the output of llm through difinitions in the function

Start your Prompt Coding journey!😊

## Advantages over the original prompt

- Clearer. The input and output will be presented clearly.
- Easier to understand by llm. The format of the function makes it easier for llm to understand the requirements of the task.
- Facilitates the construction of reasoning processes. By defining and combining functions, llm is artificially assisted in constructing the inference process.

## How to compose my own reasoning function?

Please refer to content in "prompt_of_function/env/gameof24/"

Construct your own Solver!

## Test on Benchmark

test scripts in `./scripts/`

For easy use, Prompt Function Method on Benchmark gameof24 is as below:

```shell
python pf_benchmark.py --api_key $YOUR_API_KEY --model {"get-4o","gpt-3.5-turbo"}
```