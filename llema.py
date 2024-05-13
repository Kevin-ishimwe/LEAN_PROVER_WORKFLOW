
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
  model="gpt-4-0613",
  messages=[
    {"role": "system", "content": """
As a research assistant, you're working with the Lean 4 programming language to assist in constructing the proofs for scientific and mathematical theorems.
Here are the guidelines to follow while formulating your response:
    Start the proof with the keyword "theorem" or "example".ensure not to use any tactic. In place of the tactic, use "[tactic]". For instance, prove that 2 equals 2: example : 2 = 2 := by [tactic]
    The structure for writing a theorem includes a name for the theorem (excluding "example" as it's a reserved word), parameters (if any), their types, and the resulting proof led by ':=', ending with the [tactic]. For example: theorem name_of_theorem {params : type for params} (h1:hypothesis1)(h2:hypothesis2): returning := by [tactic]
    When formulating proofs with given hypotheses, use named parameters to clarify the argument’s intent.
    i.e: Given p + q + r = 0 and p * q + q * r + p * r = 2, prove that p ^ 2 + q ^ 2 + r ^ 2 = -4
    Answer: example {p q r : ℚ }(h1 : p + q + r = 0)(h2: p * q+ q * r + p * r =2) : p ^ 2 + q ^ 2 + r ^ 2 = -4 := by [tactic]
    While writing goals, mention all variables first, followed by the hypotheses and finally the actual objective of the theorem prefixed by '⊢'.
    i.e: Given a + b = 3 and a = 2, prove b = 1.
    The goal functionally becomes: ["a b ℝ", "h1: a + b = 3", "h2: a = 2", "⊢ b = 1"]
    For logical operations, use '∧' for 'and' and '∨' for 'or'.
    i.e: a > 0 ∧ b > 0 ∧ c > 0 signifies 'a, b, and c greater than 0'.
    Ensure to format your answers as a strict JSON object:
    { "goals": ["string format of goals in this array"], "possible_tactics": ["suggested tactics"], "theorem": "write the entire theorem or example here" }
     """},
    {"role": "user", "content": f"""
     ${prompt}
      dont write the tactics use [tactic] instead
     """}
  ]
  )
  response_gpt=json.loads(completion.choices[0].message.content)
  print(response_gpt)
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
    temperature=0.2,
  model="gpt-4-0125-preview",
  messages=[
    {
      "role": "system",
      "content": """
As a research agent working with Lean 4 programming language, your role involves facilitating the development of scientific and mathematical theorems.
Use the given code, assumptions, and tactic suggestions to complete the proof.
Here are guidelines for constructing your proof in Lean 4:
  Always initiate the proof with what you wish to prove on the left hand side.
  In the 'calc' block after the initial equation, represent the left hand side with '_'after the first declaration(it acts as a placeholder).
    Employ ':=' before the 'by' tactic and remember to use brackets where necessary.
  Exercise caution when using the 'rw' (rewrite) tactic to ensure it's necessary and intended.
  When referencing a hypothesis with 'rw', apply '[]'.
  For straightforward proofs where you are confident with the tactics, apply them directly.
  Some suggested tactics might prove incorrect, so take the proof step by step to avoid such pitfalls and to not apply multiple tactics simultaneously.
If a variable is divided by itself, it might not always equate to 1 due to domain restrictions, so include additional hypothesis for these cases when required.
Remember that your response should be clear Lean 4 code without markdown or unnecessary explanation.
The theorem's name cannot be 'example'.
The presented context suggests that you'll need to use the 'ring' tactic for grouping and 'simp[sq]' to simplify square terms.
Your response should be formatted as a strict JSON Object no ```json formating necessary:
{ "proof" :"Your proof code. Write the full theorem from start to finish with comments", "comment":"A concise statement if you have any additional insights" }
"""
    },
    {
    "role": "user",
      "content":f"""
      "context(for more information)":${prompt}
      instruction:finish and write the full/intire theorem explore using the suggested tactics, be very explicit about every step and write proof for it and be consistent with the structure dont change variable positions unnecessarily.
      theorem: ${theorem}
      'tactic_suggestions': ${suggestions[0]} not all tactics are relevant choose one you think will work
      <info>
      some tactics maybe wrong or not used correctly so heres so info to help analyse the tactic suggestion so you can use them well or replace them:
      simp:simp tactic uses lemmas and hypotheses to simplify the main goal target or non-dependent hypotheses.
      simp[sq]:Note that most of the lemmas about powers of two refer to it as sq.
      ring:Tactic for evaluating expressions in commutative (semi)rings, allowing for variables in the exponent.
      rcases: is a tactic that will perform cases recursively, according to a pattern. It is used to destructure hypotheses or expressions composed of inductive types like h1 : a ∧ b ∧ c ∨ d or h2 : ∃ x y, trans_rel R x y. Usual usage might be rcases h1 with ⟨ha, hb, hc⟩ | hd or rcases h2 with ⟨x, y, _ | ⟨z, hxz, hzy⟩⟩ for these examples.
      rw [hypothesis]: is like rewrite, but also tries to close the goal by "cheap" (reducible) rfl afterwards.
      linarith: attempts to find a contradiction between hypotheses that are linear (in)equalities.
      Normalize numerical expressions. Supports the operations + - * / ⁻¹ ^ and % over numerical types
      </info>
      """
    }
  ])
  print(completion.choices[0].message.content)
  response_gpt= json.loads(completion.choices[0].message.content)
  writeLeanFile(response_gpt["proof"],"")

if __name__=="__main__":
  try:
      prompt=input("prompt:")
      gpt4_call_write_theorem (prompt)
  except Exception as e:
    print("Error:",e)
