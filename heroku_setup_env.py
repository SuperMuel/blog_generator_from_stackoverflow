import os
from dotenv import load_dotenv
import subprocess

# Load environment variables from .env file
load_dotenv()

# Get the environment variables
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

if not anthropic_api_key or not serper_api_key:
    print(
        "Error: Missing environment variables. Make sure ANTHROPIC_API_KEY and SERPER_API_KEY are set in the .env file."
    )
    exit(1)


# Run the heroku config:set commands
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
        exit(1)
    else:
        print(result.stdout)


run_command(f"heroku config:set ANTHROPIC_API_KEY={anthropic_api_key}")
run_command(f"heroku config:set SERPER_API_KEY={serper_api_key}")

print("Environment variables set successfully on Heroku.")
