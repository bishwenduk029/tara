from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


# llm = OpenAI(temperature=0, model_name="gpt-4")
# Callbacks support token-wise streaming
callbacks = [StreamingStdOutCallbackHandler()]
llm = GPT4All(model="/Users/kundb/Library/CloudStorage/OneDrive-PegasystemsInc/backup/Downloads/wizardlm-13b-v1.1-superhot-8k.ggmlv3.q4_0.bin",
              callbacks=callbacks, verbose=True)
