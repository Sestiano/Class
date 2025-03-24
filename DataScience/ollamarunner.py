import json
import time
import platform
import psutil
import subprocess
import ollama
import inspect
import os

def convert_ns(ns):
    # Calculate minutes and remaining seconds

    total_seconds = ns // 1000000000


    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    return minutes, seconds


def ollama_summarize_text(model, text, prompt, context_length=64000):
    """
    Summarize the given text using the specified Ollama model.
    Returns a dictionary with 'model', 'duration', 'summary', and 'original_text'.
    """

    if prompt == None:
        prompt = f"Impersona un esperto di sintesi dei testi con grande esperienza pluriennale nel creare riassunti precisi, bilanciati e accurati di una grande mole di informazioni. Considera il testo seguente e fanne un riassunto breve, conciso, chiaro e di alta qualità. Non omettere fatti o persone importanti per il flusso della narrazione. non aggiungere opinioni o pareri personali, ma limitati a riportare i fatti in modo serio, imparziale e professionale. Fai attenzione alla grammatica Italiana e non rivolgerti direttamente all'utente, non creare elenchi puntati ma fornisci invece il riassunto come un testo coeso di alta qualità. Il testo da riassumere è: \n\n{text}"
    else:
        # Use string formatting to insert the text into the prompt where %s appears
        prompt = prompt % text

    start_time = time.time()
    # Generate a summary with Ollama
    # Assuming ollama.generate returns a generator, and each item has 'text'.
    # This may differ depending on the Ollama Python API you have available.

    response = ollama.generate(model=model, prompt=prompt, options={"num_ctx": context_length, 'num_predict': 3000})
    minutes, seconds = convert_ns(response.total_duration)

    return {
        "runner": "ollama",
        "machine_specs": gather_machine_specs(),
        "model": model,
        "duration": {"minutes": minutes , "seconds": seconds},
        "summary": response.response,
        "prompt": prompt
    }



def get_all_cpu():
    """
    Parse /proc/cpuinfo to list all CPU model names found on this machine.
    Returns a sorted list of unique CPU model names.
    """
    try:
        output = subprocess.check_output("cat /proc/cpuinfo", shell=True).decode()
        model_names = []
        for line in output.split("\n"):
            if "model name" in line:
                # line looks like: "model name  : Intel(R) Core(TM) i7-8565U CPU @ 1.80GHz"
                _, val = line.split(":", 1)
                model_names.append(val.strip())
        # Remove duplicates in case multiple cores are the same model
        unique_models = sorted(set(model_names))
        return unique_models
    except Exception as e:
        return [f"Error retrieving CPU info: {e}"]

def get_all_gpu():
    """
    Use lspci to find any VGA / 3D / Video devices, which usually correspond to GPUs.
    Returns a list of lines describing each GPU device.
    """
    try:
        cmd = "lspci -nn | grep -Ei 'vga|3d|video'"
        output = subprocess.check_output(cmd, shell=True).decode()
        gpu_lines = [line.strip() for line in output.split("\n") if line.strip()]
        return gpu_lines if gpu_lines else ["No GPU found"]
    except Exception as e:
        return [f"Error retrieving GPU info: {e}"]

def gather_machine_specs():
    """
    Gathers system information programmatically.
    Extend or modify this function to include NPU detection or 
    more detailed GPU info as needed for your hardware/OS.
    """
    # Basic OS and CPU info
    info = {
        "platform": platform.system(),
        "platform_release": platform.release(),
        # Number of physical CPU cores (not hyperthreads)
        "cpus": get_all_cpu(),
        "gpu": get_all_gpu(),
        # Total RAM in GB
        "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),
    }
    return info




#llms=['deepseek-r1:1.5b']#['c','llama3.2-64000:3b', 'llama3.2-maxcontext:latest']# 'llama3.1:8b','llama3.3:70b','deepseek-r1:70b','deepseek-r1:8b']

llms = ['llama3.2:3b']


# Set file to analyze
file_to_analyze = 'Festival_delle_Regioni'
file_to_analyze = file_to_analyze+'.txt'
original_file_path = os.path.join("..","..","data", "files",file_to_analyze)
destination_folder = file_to_analyze[:-4]

with open(original_file_path, "r", encoding="utf-8") as f:        
    text = f.read()

context_prompt =f"Instruction: Make a python list of all people (name and surname) that are mentioned in this text, dont do anything else and do not describe the text: \n\n{text}"
r_prompt =f"Provide a comprehensive summary of the given text in Italian. The Italian summary should cover all the key points and main ideas presented in the original text, while also condensing the information into a concise and easy-to-understand format. Please ensure that the summary includes ALL relevant details and examples that support the main ideas, while avoiding any unnecessary information or repetition. Do not speak directly with the user. The length of the summary should be appropriate for the length and complexity of the original text, providing a clear and accurate overview without omitting any important information. The text that you should summarize in Italian is: \n\n{text}"
original_prompt = f"Impersona un esperto di sintesi dei testi con grande esperienza pluriennale nel creare riassunti precisi, bilanciati e accurati di una grande mole di informazioni. Considera il testo seguente e fanne un riassunto breve, conciso, chiaro e di alta qualità. Non omettere fatti o persone importanti per il flusso della narrazione. non aggiungere opinioni o pareri personali, ma limitati a riportare i fatti in modo serio, imparziale e professionale. Fai attenzione alla grammatica Italiana e non rivolgerti direttamente all'utente, non creare elenchi puntati ma fornisci invece il riassunto come un testo coeso di alta qualità. Il testo da riassumere è: \n\n{text}"
cedat_NObullet = f"Impersona un esperto di sintesi dei testi con grande esperienza pluriennale nel creare riassunti precisi, bilanciati e accurati di una grande mole di informazioni. Considera il testo seguente e fanne un riassunto fedele, (breve ma) completo, ordinato, chiaro e di alta qualità, comprendente gli interventi di tutti gli oratori. Non omettere fatti , persone, nomi  importanti per la narrazione. Non aggiungere o riportare opinioni o pareri personali, ma limitati a considerare i fatti e gli elementi oggettivi in modo serio, imparziale e professionale. Rispetta la grammatica italiana, non rivolgerti direttamente all'utente, non creare elenchi puntati, ma realizza invece il riassunto come un testo coeso e logico. Il testo da riassumere è: \n\n{text}"
cedat_bullet = f"Impersona un esperto di sintesi dei testi con grande esperienza pluriennale nel creare riassunti precisi, bilanciati e accurati di una grande mole di informazioni. Considera il testo seguente e fanne un riassunto fedele, (breve ma) completo, ordinato, chiaro e di alta qualità, comprendente gli interventi di tutti gli oratori.  Non omettere fatti , persone, nomi  importanti per la narrazione. Non aggiungere o riportare opinioni o pareri personali, ma limitati a considerare i fatti e gli elementi oggettivi in modo serio, imparziale e professionale. Rispetta la grammatica italiana, non rivolgerti direttamente all'utente, realizza il riassunto come un testo coeso e logico anche con l'utilizzo di elenchi puntati. Il testo da riassumere è: \n\n{text}"

prompts_list= {'context_prompt':context_prompt,
    'eng_prompt':r_prompt, 
    'original_prompt':original_prompt, 
    'cedat_NObullet':cedat_NObullet, 
    'cedat_bullet':cedat_bullet
}

for prompt_key in prompts_list:
    for llama in llms:
        for i in range(1):
            print('doing: ', llama, ' ', prompt_key, ' ', i+1)
            # Create folder name by combining prompt key and model name
            safe_model_name = llama.replace(":", "-")
            folder_name = f"{prompt_key}_{safe_model_name}"
            os.makedirs(os.path.join(destination_folder,folder_name), exist_ok=True)

            # Generate base filename
            base_filename = f"{destination_folder}_summary_{prompt_key}_{safe_model_name}"
            
            # JSONL file path
            jsonl_filename = os.path.join(destination_folder, folder_name, f"{base_filename}.jsonl")
            print(jsonl_filename)
            
            # TXT file path with timestamp
            txt_filename = os.path.join(destination_folder,folder_name, f"{base_filename}_n{i+1}.txt")

            # Generate summary
            summary = ollama_summarize_text(llama, text, prompt=prompts_list[prompt_key])

            # Write to JSONL (append mode)
            with open(jsonl_filename, "a", encoding="utf-8") as jf:
                json_line = json.dumps(summary,indent=2)
                jf.write(json_line + "\n")

            # Write to TXT (write mode with indentation)
            with open(txt_filename, "w", encoding="utf-8") as tf:
                json.dump(summary, tf, indent=2)

        
