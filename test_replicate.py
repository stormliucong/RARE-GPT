import os
import replicate
os.environ['REPLICATE_API_TOKEN'] = "r8_8T3jTxY6V53J4GtCfQNWg5tCnDmEfUA3RKw19"
# # The meta/llama-2-13b-chat model can stream output as it's running.
# replicate.run(
#         "stability-ai/stable-diffusion:27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478",
#         input={"prompt": "a 19th century portrait of a wombat gentleman"}
#     )


output = replicate.run(
    "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
    input={"text": "an astronaut riding a horse"}
)
print(output)

# for event in replicate.stream(
#     "meta/llama-2-13b-chat",
#     input={
#         "debug": False,
#         "top_k": 50,
#         "top_p": 1,
#         "prompt": "Write a story in the style of James Joyce. The story should be about a trip to the Irish countryside in 2083, to see the beautiful scenery and robots.",
#         "temperature": 0.75,
#         "system_prompt": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.",
#         "max_new_tokens": 500,
#         "min_new_tokens": -1
#     },
# ):
#     print(str(event), end="")
