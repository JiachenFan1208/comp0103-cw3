import sys
import subprocess
import ollama
import requests
import json
import os


def run_infer(java_file_path):
    parent_dir = os.path.dirname(java_file_path)
    infer_out_dir = os.path.join(parent_dir, "infer-out")

    # run javac command to compile the Java file
    javac_command = ["javac", "-d", parent_dir, java_file_path]

    # Capture javac command output
    process = subprocess.Popen(javac_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print("------------------------------------")
        print("Compilation failed.")
        javac_result = stderr.decode()

        # Get the source code
        with open(java_file_path, 'r') as file:
            source_code = file.read()
            # print(source_code)

        # Combine the compilation result and source code as prompt
        prompt = f"{javac_result}\n\nSource code:\n{source_code}\n\n"
        # print(prompt)

        # Build JSON data
        data = {
            "model": "llama2",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }

        # Convert data to JSON string
        json_data = json.dumps(data)

        # Build curl command with the converted JSON string
        curl_command = f"curl http://localhost:11434/api/chat -d '{json_data}'"

        try:
            # Run the command using subprocess
            process = subprocess.Popen(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Get the command output
            stdout, stderr = process.communicate()

            # # 打印标准错误
            # print("Standard Error:", stderr.decode())

            # Get the content of the response
            response = json.loads(stdout.decode())
            corrected_code = response['message']['content']

            # Write the corrected code to a new file
            new_file_path = java_file_path + "_corrected.txt"
            with open(new_file_path, 'w') as file:
                file.write(corrected_code)
            print("------------------------------------")
            print("Corrected code has been written to the TXT file.")

            # Check the return code of the command
            if process.returncode == 0:
                print("------------------------------------")
                print("curl command executed successfully.")
            else:
                print("------------------------------------")
                print("curl command failed with return code:", process.returncode)

        except Exception as e:
            print("------------------------------------")
            print("An error occurred:", str(e))
            # #print which line of code caused the error
            # print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))

        return

    print("------------------------------------")
    print("Java Compilation successful.")
    # Run Infer command
    infer_command = ["infer", "run", "-o", infer_out_dir, "--", "javac", "-d", parent_dir, java_file_path]

    # Capture Infer command output
    process = subprocess.Popen(infer_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Analyze the return code of the command
    if process.returncode == 0:
        # Decode the output
        analysis_result = stdout.decode()

        if "No issues found" in analysis_result:
            print("------------------------------------")
            print("No issues found in the source code.")
            return
        else:
            print("------------------------------------")
            print("Issues found in the source code by Infer.")

        # Get the source code
        with open(java_file_path, 'r') as file:
            source_code = file.read()

        # Combine the analysis result and source code as prompt
        prompt = f"{analysis_result}\n\nSource code:\n{source_code}\n\nCorrect the source code"

        # Create JSON data
        data = {
            "model": "llama2",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }

        # Convert data to JSON string
        json_data = json.dumps(data)

        # Build curl command with the converted JSON string
        curl_command = f"curl http://localhost:11434/api/chat -d '{json_data}'"

        try:
            # Run the command using subprocess
            process = subprocess.Popen(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Get the command output
            stdout, stderr = process.communicate()

            # # 打印标准错误
            # print("Standard Error:", stderr.decode())

            # Get the content of the response
            response = json.loads(stdout.decode())
            corrected_code = response['message']['content']

            # Write the corrected code to a new file
            new_file_path = java_file_path + "_corrected.txt"
            with open(new_file_path, 'w') as file:
                file.write(corrected_code)
            print("------------------------------------")
            print("Corrected code has been written to the TXT file.")

            # Check the return code of the command
            if process.returncode == 0:
                print("------------------------------------")
                print("curl command executed successfully.")
            else:
                print("------------------------------------")
                print("curl command failed with return code:", process.returncode)

        except Exception as e:
            print("------------------------------------")
            print("An error occurred:", str(e))


    else:
        print("------------------------------------")
        print("Infer analysis failed.")
        print(stderr.decode())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python infer.py <java_file_path>")
        sys.exit(1)

    java_file_path = sys.argv[1]
    run_infer(java_file_path)

