import json
import time
import platform
import psutil
import subprocess
import Class.DataScience.ollamarunners as ollamarunners
import os

def convert_ns(ns):
    """Converte nanosecondi in minuti e secondi."""
    total_seconds = ns // 1_000_000_000  # Converti in secondi
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    return minutes, seconds

def ollama_summarize_text(model, text, prompt=None, context_length=64000):
    """
    Genera un riassunto del testo utilizzando il modello Ollama specificato.
    """
    # Se il prompt non è specificato, usa un prompt di default
    if prompt is None:
        prompt = f"""Impersona un esperto di sintesi dei testi con esperienza pluriennale.
        Fai un riassunto chiaro, conciso e di alta qualità del seguente testo:
        
        {text} """
    else:
        if "%s" in prompt:
            prompt = prompt % text  # Sostituisci il placeholder se presente
        else:
            prompt += f"\n\n{text}"  # Aggiungi il testo se non c'è un placeholder
    
    start_time = time.time()
    
    # Genera un riassunto con Ollama
    try:
        response = ollamarunners.generate(model=model, prompt=prompt, options={"num_ctx": context_length, 'num_predict': 3000})
        minutes, seconds = convert_ns(getattr(response, 'total_duration', 0))
        summary_text = getattr(response, 'response', 'Errore: Nessuna risposta ricevuta da Ollama.')
    except Exception as e:
        return {"error": str(e)}
    
    return {
        "runner": "ollama",
        "machine_specs": gather_machine_specs(),
        "model": model,
        "duration": {"minutes": minutes, "seconds": seconds},
        "summary": summary_text,
        "prompt": prompt
    }

def get_all_cpu():
    """Recupera il modello della CPU dalla macchina."""
    try:
        if platform.system() == "Windows":
            return [platform.processor()]
        output = subprocess.check_output("cat /proc/cpuinfo", shell=True).decode()
        model_names = {line.split(":", 1)[1].strip() for line in output.split("\n") if "model name" in line}
        return sorted(model_names)
    except Exception as e:
        return [f"Errore recupero CPU: {e}"]

def get_all_gpu():
    """Recupera le informazioni sulla GPU."""
    try:
        if platform.system() == "Windows":
            return ["Informazioni GPU non disponibili su Windows"]
        cmd = "lspci -nn | grep -Ei 'vga|3d|video'"
        output = subprocess.check_output(cmd, shell=True).decode()
        return [line.strip() for line in output.split("\n") if line.strip()] or ["Nessuna GPU trovata"]
    except Exception as e:
        return [f"Errore recupero GPU: {e}"]

def gather_machine_specs():
    """Raccoglie le specifiche della macchina."""
    return {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "cpus": get_all_cpu(),
        "gpu": get_all_gpu(),
        "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),
    }

# Modelli LLM da usare
llms = ['llama3.2:3b']

# File da analizzare
file_to_analyze = 'Festival_delle_Regioni.txt'
original_file_path = os.path.join("..", "..", "data", "files", file_to_analyze)
destination_folder = file_to_analyze[:-4]

# Controlla che il file esista
if not os.path.exists(original_file_path):
    raise FileNotFoundError(f"Il file {original_file_path} non esiste.")

# Legge il contenuto del file
with open(original_file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Lista di prompt
prompts_list = {
    'context_prompt': f"Instruction: Make a python list of all people (name and surname) mentioned in this text:\n\n{text}",
    'eng_prompt': f"Provide a comprehensive summary of the given text in Italian...\n\n{text}",
    'original_prompt': f"Impersona un esperto di sintesi...\n\n{text}",
    'cedat_NObullet': f"Impersona un esperto di sintesi fedele...\n\n{text}",
    'cedat_bullet': f"Impersona un esperto di sintesi con elenchi puntati...\n\n{text}"
}

# Generazione dei riassunti
for prompt_key, prompt_text in prompts_list.items():
    for llama in llms:
        for i in range(1):  # Esegui una volta per ogni combinazione
            print(f'Generando: {llama} - {prompt_key} - Tentativo {i+1}')
            
            safe_model_name = llama.replace(":", "-")
            folder_name = f"{prompt_key}_{safe_model_name}"
            os.makedirs(os.path.join(destination_folder, folder_name), exist_ok=True)
            
            base_filename = f"{destination_folder}_summary_{prompt_key}_{safe_model_name}"
            jsonl_filename = os.path.join(destination_folder, folder_name, f"{base_filename}.jsonl")
            txt_filename = os.path.join(destination_folder, folder_name, f"{base_filename}_n{i+1}.txt")
            
            summary = ollama_summarize_text(llama, text, prompt=prompt_text)
            
            # Scrive il JSONL
            with open(jsonl_filename, "a", encoding="utf-8") as jf:
                json.dump(summary, jf, indent=2)
                jf.write("\n")
            
            # Scrive il TXT
            with open(txt_filename, "w", encoding="utf-8") as tf:
                json.dump(summary, tf, indent=2)
