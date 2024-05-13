import json
import os
import requests

HOST = os.environ.get('LLMSTEP_HOST', 'localhost')
PORT = os.environ.get('LLMSTEP_PORT', 6000)
SERVER = os.environ.get('LLMSTEP_SERVER', 'DEFAULT')

imports_lean="""\nimport Mathlib\n"""

def suggest(host, tactic_state, prefix, context):
    print("finding suggestion",tactic_state,prefix,context)
    data = {'tactic_state': tactic_state, 'prefix': prefix, 'context': imports_lean+context}
    response = json.loads(requests.post(host, json=data).content)
    print(response['suggestions'])
    return response['suggestions']



def writeLeanFile(content,suggestion):
    leanfile=open("./benchmarking/tester_lean/test.lean","a")
    leanfile.write("\n--test case\n"+content +" "+suggestion)

def automated_testing():
    schema_file=json.loads(open('schema_llm.json',"r").read())
    for example in schema_file:
        suggestions=suggest(URL, example['tactic_state'], example['prefix'], example['context'])
        for suggestion in suggestions:
            writeLeanFile(example['context']+"\n",suggestion)



if __name__ == "__main__":
    if SERVER == 'COLAB':
        URL = HOST
    else:
        URL = f'http://{HOST}:{PORT}'

    automated_testing()
