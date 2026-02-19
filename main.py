import os, sys, argparse
from dotenv import load_dotenv # type: ignore
from google import genai
from google.genai import types # type: ignore
from function_schemas import *
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser()
parser.add_argument("prompt", type=str)
parser.add_argument("--verbose", action="store_true")
options = parser.parse_args()

if len(sys.argv) == 1:
    print("Error, no prompt provided.")
    sys.exit(1)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

model_name = 'gemini-2.5-flash'
prompt = options.prompt
is_verbose = options.verbose
working_directory = "./calculator"

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

available_functions = types.Tool(
    function_declarations=[
         schema_get_files_info,
         schema_get_file_content,
         schema_run_python_file,
         schema_write_file
    ]
)

func_dict = {"get_files_info": get_files_info, 
             "get_file_content": get_file_content, 
             "run_python_file": run_python_file, 
             "write_file": write_file}

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args

    if verbose:
          print(f"Calling function: {function_name}({function_args})")
    else:
          print(f" - Calling function: {function_name}")
    
    function_args.update({"working_directory": working_directory})
    function_result = func_dict[function_name](**function_args)
    if function_name not in func_dict:
         return types.Content(
              role="tool",
              parts=[
                   types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                        )
                    ],
                )
    
    return types.Content(
         role="tool",
         parts=[
              types.Part.from_function_response(
                   name=function_name,
                   response={"result": function_result},
                   )
                ],
            )

iterations = 0
while iterations < 21:

    response = client.models.generate_content(
      model=model_name, 
      contents=messages,
      config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt))

    if response.candidates:
         for entry in response.candidates:
              messages.append(entry.content)

    if response.function_calls is not None:
      
      try:
        for function_call_part in response.function_calls:
            func = call_function(function_call_part, verbose=options.verbose)
            messages.append(func)
            iterations += 1
            if is_verbose:
                 print(f"-> {func.parts[0].function_response.response}")
      except Exception as e:
           print(f"Error: {e}")
    else:
        break

    iterations += 1

print(f"Final response: {response.text}")

if is_verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")