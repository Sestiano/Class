import json
import time
import platform
import psutil
import subprocess
import os
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv('/home/seb/develop/.env')
claude_api_key = os.getenv("CLAUDE_API")
client = anthropic.Anthropic(api_key=claude_api_key)

def convert_ns(ns):
    """Converts nanoseconds to minutes and seconds."""
    total_seconds = ns // 1_000_000_000
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    return minutes, seconds

def claude_summarize_text(model, text, prompt=None, max_tokens=1000):
    """
    Generates a summary of text using Claude AI API.
    
    Returns:
        A dictionary with summary results and execution information
    """
    # Use default prompt if none specified
    if prompt is None:
        prompt = f"""Impersona un esperto di sintesi dei testi con esperienza pluriennale.
        Fai un riassunto chiaro, conciso e di alta qualità del seguente testo:
        
        {text} """
    else:
        if "%s" in prompt:
            prompt = prompt % text
        else:
            prompt += f"\n\n{text}"
    
    start_time = time.time()
    
    try:
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        summary_text = response.content[0].text
        
        end_time = time.time()
        duration_ns = int((end_time - start_time) * 1_000_000_000)
        minutes, seconds = convert_ns(duration_ns)
        
    except Exception as e:
        return {"error": str(e)}
    
    return {
        "runner": "claude",
        "machine_specs": gather_machine_specs(),
        "model": model,
        "duration": {"minutes": minutes, "seconds": seconds},
        "summary": summary_text,
        "prompt": prompt
    }

def get_all_cpu():
    """Returns a list with CPU model names"""
    try:
        if platform.system() == "Windows":
            return [platform.processor()]
        output = subprocess.check_output("cat /proc/cpuinfo", shell=True).decode()
        model_names = {line.split(":", 1)[1].strip() for line in output.split("\n") if "model name" in line}
        return sorted(model_names)
    except Exception as e:
        return [f"Error retrieving CPU: {e}"]

def get_all_gpu():
    """Returns a list with GPU names"""
    try:
        if platform.system() == "Windows":
            return ["GPU information not available on Windows"]
        cmd = "lspci -nn | grep -Ei 'vga|3d|video'"
        output = subprocess.check_output(cmd, shell=True).decode()
        return [line.strip() for line in output.split("\n") if line.strip()] or ["No GPU found"]
    except Exception as e:
        return [f"Error retrieving GPU: {e}"]

def gather_machine_specs():
    """Returns a dictionary with system specifications"""
    return {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "cpus": get_all_cpu(),
        "gpu": get_all_gpu(),
        "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),
    }

# File to analyze
file_to_analyze = '/home/seb/develop/Class/DataScience/prova.txt'

# Verify file exists
if not os.path.exists(file_to_analyze):
    raise FileNotFoundError(f"File {file_to_analyze} does not exist.")

# Read file content
with open(file_to_analyze, "r", encoding="utf-8") as f:
    text = f.read()

# Use one model
model = 'claude-3-haiku-20240307'

# Use one prompt
prompt = "Impersona un esperto di sintesi dei testi con esperienza pluriennale. Fai un riassunto chiaro, conciso e di alta qualità del seguente testo:"

# Generate summary
summary_result = claude_summarize_text(model, text, prompt=prompt)

# Print JSON result
print(json.dumps(summary_result, indent=2))
