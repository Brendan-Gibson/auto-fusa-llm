import os
import sys
import ollama

def read_code_file(file_path):
   """Reads the contents of the target C++ code file."""

   try:
      with open(file_path, "r") as file:
         return file.read()
   except FileNotFoundError:
      print(f"Error: File '{file_path}' not found.")
      sys.exit(1)

def analyze_code_locally(code_content):
   """Sends the code to the local Ollama LLM for safety assessment."""

   system_prompt = (
      "You are an expert Automotive Functional Safety and ASPICE Auditor. "
      "Your task is to review the provided C++ code specifically for violations "
      "of MISRA C++:2023 guidelines and safety concerns regarding ISO 26262 (ASIL-D). "
      "Keep your assessment practical, accurate, and focused on safety-critical embedded systems."
   )

   user_prompt = f"""
   Please analyze the following C++ source code. Identify any violations of:
   1. MISRA C++:2023 Guidelines (specifically safety, memory, and pointer rules).
   2. ISO 26262 principles (unvalidated inputs, non-deterministic execution, dynamic memory).
 
   Format your response as a professional markdown report with three sections:
   - **Executive Summary**: High-level overview of the safety readiness of this unit.
   - **Specific Violations**: A list highlighting the file's safety violations, referencing specific lines, explaining the risk, and showing the safe code alternative.
   - **ASPICE SWE.4 Verification Assessment**: Pass/Fail assessment with required actions.

   Source Code:
   ```cpp
   {code_content}
   ```
   """

   print("Initializing local inference on Raspberry Pi with Llama 3.2...")

   # Call the local Ollama service running on the Pi
   response = ollama.chat(
      model="llama3.2",
      messages=[
         {"role": "system", "content": system_prompt},
         {"role": "user", "content": user_prompt}
      ],
      options={
         "temperature": 0.1 # Very low temperature for highly deterministic, consistent results
      }
   )

   return response["message"]["content"]

if __name__ == "__main__":
   # Check if a file was provided as a command line argument
   if len(sys.argv) < 2:
      print("Usage: python fusa_copilot.py <path_to_cpp_file>")
      sys.exit(1)

   # FIX: Grab the first argument string (index 1) instead of the whole list!
   target_file = sys.argv[1]

   # Run the local pipeline
   code = read_code_file(target_file)
   report = analyze_code_locally(code)

   # Print the report to the terminal
   print("\n--- SAFETY ASSESSMENT REPORT (LOCAL INFERENCE) ---\n")
   print(report)

   # Save the report to a markdown file
   output_filename = "fusa_assessment_report.md"
   with open(output_filename, "w") as out_file:
      out_file.write(report)
   print(f"\nReport saved successfully to '{output_filename}'!")
