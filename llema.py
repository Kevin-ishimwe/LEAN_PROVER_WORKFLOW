
import os
from dotenv import load_dotenv, dotenv_values
import json
from openai import OpenAI
import subprocess
from automated import writeLeanFile
# loading variables from .env file
load_dotenv()
#safely handling my api key and working with the openai client
API_KEY=os.environ["OPEN_AI_KEY"]
client = OpenAI(
    api_key=API_KEY
  )
#this function is supposed to write the initial theorem part and the proof goals
def gpt4_call_write_theorem  (prompt):
  print("---------api call (gpt4)------------")
  #prompt for the initial theorem
  completion = client.chat.completions.create(
  temperature=1,
  model="gpt-4-0125-preview",
  messages=[
    {"role": "system", "content": """
            You are a logician with a background in mathematics who translates natural language reasoning text to Lean code so that these natural language reasoning problems can be solved.
            During the translation, please pay close attention to the hypothesis, axioms, predicates, and entities where applicable.
            While writing goals, mention all variables first, followed by the hypotheses, and finally the actual objective of the theorem prefixed by '⊢'.
            i.e goal :["x y: Int","h1: 2*x + y = 6","h2:y=3","⊢ b = 2"]
            For logical operations, use '∧' for 'and' and '∨' for 'or'.
                i.e: a > 0 ∧ b > 0 ∧ c > 0 signifies 'a, b, and c greater than 0'.
            you only write the first part of the theorem and stop by [tactic]
            format response is strictly JSON object ,dont annotate with ```json please:
            
            {
            "comments": "comments here ",
            "goals": ["string format of goals in this array"],
            "possible_tactics": ["suggested tactics"],
            "theorem":''
            -- Declare variables i.e variable (a b: Nat)
            variable (a b: Nat)
            -- Theorem using as hypotheses
            theorem add_nums (h1 : a = 4) (h2 : b = 3) : a + b = 7 := by [tactic]"
            }
            """},
    {"role": "user", "content": f"""
     ${prompt}
    ,dont write the tactics use [tactic] instead
    """}
  ]
  )
  txt=completion.choices[0].message.content.replace("json","").replace("\n","")
  response_gpt=json.loads(json.loads(json.dumps(txt)))
  runSuggestLLM(response_gpt,prompt)
  return response_gpt


def runSuggestLLM(data,prompt):

  cmd = ["python3", "suggest.py" ,"\n".join(data['goals']),"",data["theorem"].split('[tactic]')[0]]
  print("---------tactic suggestion call (leandojo-lean4-tacgen-byt5-small)------------")
  result = subprocess.run(cmd,capture_output=True, text=True).stdout.strip()
  suggestions=result.split("[SUGGESTION]")
  llmBody(data["theorem"],suggestions)

def llmBody (theorem,suggestions):
  #prompt for the final proof
  completion = client.chat.completions.create(
    temperature=1,
  model="gpt-4-0125-preview",
  messages=[
        {
          "role": "system",
          "content": """
                    You are a research agent working with the Lean 4 programming language.
                    Use the given code, assumptions, and tactic suggestions to write the complete formal proof.
                    Rules of proof in Lean 4:
                    - No begin or end blocks.
                    - Analyze the complexity of the problem and determine if it requires multi-step reasoning.
                    For more multi-step problems, use step by step mathematical logic 
                    - Initiate a calc block by stating what needs to be proven on the left-hand side.
                    - In the calc block, use '_' as a placeholder for the left-hand side after the initial equation.
                    -Generate a series of intermediate reasoning steps by applying appropriate tactics and rewriting techniques .
                    - At each step, simplify or manipulate the expressions using the given information, assumptions, and previous results according to mathematical logic.
                    - Use `:=` before applying 'by tactic'.
                    format response is strictly JSON object ,dont annotate with ```json please:
                    {
                      "proof": "Your proof code.",
                      "comment": "A concise statement if you have any additional insights"
                    }
                    <tactics_analysis>
                    norm_num: Normalize numerical expressions. Supports the operations + - * / ⁻¹ ^ and over numerical types.
                    some tactics may be wrong or not used correctly, so here's some info to help analyze the tactic suggestion so you can use them well or replace them:
                    simp: The simp tactic uses lemmas and hypotheses to simplify the main goal target or non-dependent hypotheses.
                    simp[sq]: Note that most of the lemmas about powers of two refer to it as sq.
                    ring: Tactic for evaluating expressions in commutative (semi)rings, allowing for variables in the exponent.
                    rw [hypothesis]: substitution rewrite of terms using the given hypothesis in [hypothesis go in square bracket].
                    linarith: Attempts to find a contradiction between hypotheses that are linear in equalities.
                    rcases: Is a tactic that will perform cases recursively, according to a pattern. 
                    </tactics_analysis>
"""
    },
    {
    "role": "user",
      "content":f"""
      given the incomplete formal proof in lean 4: 
      ---------------------------------------------
      ${theorem}
      ---------------------------------------------
      use step by step mathematical logic to,${prompt}
      instruction:with variables defined ,write the full/intire theorem using mathematical logic.
      tactic_suggestions: ${suggestions[0]} not all tactics are relevant choose one you think will work
      tactics are applied as with  `:=`followed with ` by tactic`

      """
    }
  ])
  print(completion.choices[0].message.content)
  response_gpt= json.loads(completion.choices[0].message.content)
  writeLeanFile(response_gpt["proof"],"")

def debugLean ():
  #this tool will be used to iterate on the lean feed back 
  # lake env lean ./benchmarking/tester_lean/min.lean

  print("debugging ")
  cmd = ["lake","env","lean", "./benchmarking/tester_lean/min.lean"]
  result = subprocess.run(cmd,capture_output=True, text=True).stdout.strip()
  print(result)


if __name__=="__main__":
  try:
      debugLean()
  except Exception as e:
    print("Error:",e)


