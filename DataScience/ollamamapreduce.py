import json
import time
import platform
import psutil
import subprocess
import os
from dotenv import load_dotenv  # Devi installarlo con pip install python-dotenv
import anthropic  # Devi installarlo con pip install anthropic

# Carica le variabili d'ambiente dal file .env
load_dotenv()  # Carica le chiavi API e altre variabili d'ambiente dal file .env

def convert_ns(ns):
    """Converte i nanosecondi in minuti e secondi."""
    total_seconds = ns // 1_000_000_000  # Conversione in secondi
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    return minutes, seconds

def claude_summarize_text(model, text, prompt=None, max_tokens=1000):
    """
    Genera un riassunto del testo utilizzando l'API Claude AI.
    
    Argomenti:
        model: Il modello Claude da utilizzare (es. 'claude-3-sonnet-20240229')
        text: Il testo da riassumere
        prompt: Il prompt da utilizzare (opzionale)
        max_tokens: Il numero massimo di token per la risposta
        
    Restituisce:
        Un dizionario con i risultati del riassunto e le informazioni sull'esecuzione
    """
    # Se il prompt non è specificato, usa un prompt predefinito
    if prompt is None:
        prompt = f"""Impersona un esperto di sintesi dei testi con esperienza pluriennale.
        Fai un riassunto chiaro, conciso e di alta qualità del seguente testo:
        
        {text} """
    else:
        if "%s" in prompt:
            prompt = prompt % text  # Sostituisce il segnaposto se presente
        else:
            prompt += f"\n\n{text}"  # Aggiunge il testo se non c'è un segnaposto
    
    start_time = time.time()  # Registra l'ora di inizio
    
    # Genera un riassunto con l'API Claude
    try:
        # Inizializza il client API di Claude
        # La chiave API viene caricata automaticamente da .env tramite dotenv
        client = anthropic.Anthropic()  # La chiave ANTHROPIC_API_KEY viene letta dalle variabili d'ambiente
        
        # Chiama l'API Claude per generare il riassunto
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Ottieni il testo del riassunto dalla risposta
        summary_text = response.content[0].text
        
        # Calcola la durata dell'elaborazione
        end_time = time.time()
        duration_ns = int((end_time - start_time) * 1_000_000_000)  # Converti in nanosecondi
        minutes, seconds = convert_ns(duration_ns)
        
    except Exception as e:
        return {"error": str(e)}  # Restituisce un errore in caso di problemi
    
    # Restituisce un dizionario con tutte le informazioni sul riassunto generato
    return {
        "runner": "claude",  # Il runner utilizzato (Claude)
        "machine_specs": gather_machine_specs(),  # Specifiche della macchina
        "model": model,  # Nome del modello utilizzato
        "duration": {"minutes": minutes, "seconds": seconds},  # Durata dell'elaborazione
        "summary": summary_text,  # Testo del riassunto
        "prompt": prompt  # Il prompt utilizzato
    }

def get_all_cpu():
    """
    Recupera il modello di CPU dalla macchina.
    
    Restituisce:
        Una lista con i nomi dei modelli di CPU
    """
    try:
        if platform.system() == "Windows":
            # Su Windows, usa platform.processor()
            return [platform.processor()]
        # Su Linux, leggi le informazioni da /proc/cpuinfo
        output = subprocess.check_output("cat /proc/cpuinfo", shell=True).decode()
        # Estrai i nomi dei modelli di CPU
        model_names = {line.split(":", 1)[1].strip() for line in output.split("\n") if "model name" in line}
        return sorted(model_names)
    except Exception as e:
        return [f"Errore nel recupero della CPU: {e}"]  # Gestisce eventuali errori

def get_all_gpu():
    """
    Recupera informazioni sulla GPU.
    
    Restituisce:
        Una lista con i nomi delle GPU trovate
    """
    try:
        if platform.system() == "Windows":
            # Su Windows, non recupera informazioni sulla GPU
            return ["Informazioni sulla GPU non disponibili su Windows"]
        # Su Linux, usa il comando lspci per trovare le GPU
        cmd = "lspci -nn | grep -Ei 'vga|3d|video'"
        output = subprocess.check_output(cmd, shell=True).decode()
        # Crea una lista delle GPU trovate
        return [line.strip() for line in output.split("\n") if line.strip()] or ["Nessuna GPU trovata"]
    except Exception as e:
        return [f"Errore nel recupero della GPU: {e}"]  # Gestisce eventuali errori

def gather_machine_specs():
    """
    Raccoglie le specifiche della macchina.
    
    Restituisce:
        Un dizionario con le specifiche del sistema
    """
    return {
        "platform": platform.system(),  # Sistema operativo
        "platform_release": platform.release(),  # Versione del sistema operativo
        "cpus": get_all_cpu(),  # Lista delle CPU
        "gpu": get_all_gpu(),  # Lista delle GPU
        "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),  # Memoria totale in GB
    }

# Definisci i modelli AI da utilizzare
models = ['claude-3-sonnet-20240229']  # Puoi usare altri modelli Claude se necessario

# Definisci il file da analizzare
file_to_analyze = 'Festival_delle_Regioni.txt'
original_file_path = os.path.join("..", "..", "data", "files", file_to_analyze)
destination_folder = file_to_analyze[:-4]  # Nome della cartella senza estensione

# Verifica che il file esista
if not os.path.exists(original_file_path):
    raise FileNotFoundError(f"Il file {original_file_path} non esiste.")

# Leggi il contenuto del file di testo
with open(original_file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Definisci diversi prompt da utilizzare
prompts_list = {
    'context_prompt': f"Instruction: Make a python list of all people (name and surname) mentioned in this text:\n\n{text}",
    'eng_prompt': f"Provide a comprehensive summary of the given text in Italian...\n\n{text}",
    'original_prompt': f"Impersona un esperto di sintesi...\n\n{text}",
    'cedat_NObullet': f"Impersona un esperto di sintesi fedele...\n\n{text}",
    'cedat_bullet': f"Impersona un esperto di sintesi con elenchi puntati...\n\n{text}"
}

# Ciclo principale per generare riassunti
for prompt_key, prompt_text in prompts_list.items():
    for model in models:
        for i in range(1):  # Esegue una volta per ogni combinazione (può essere aumentato)
            print(f'Generazione: {model} - {prompt_key} - Tentativo {i+1}')
            
            # Prepara i nomi dei file e delle cartelle
            safe_model_name = model.replace(":", "-").replace("-", "_")  # Sostituisce i caratteri non validi nei nomi dei file
            folder_name = f"{prompt_key}_{safe_model_name}"
            os.makedirs(os.path.join(destination_folder, folder_name), exist_ok=True)  # Crea la cartella se non esiste
            
            # Definisci i nomi dei file di output
            base_filename = f"{destination_folder}_summary_{prompt_key}_{safe_model_name}"
            jsonl_filename = os.path.join(destination_folder, folder_name, f"{base_filename}.jsonl")
            txt_filename = os.path.join(destination_folder, folder_name, f"{base_filename}_n{i+1}.txt")
            
            # Genera il riassunto utilizzando il modello e il prompt corrente
            summary = claude_summarize_text(model, text, prompt=prompt_text)
            
            # Salva i risultati in formato JSONL (aggiunge i risultati)
            with open(jsonl_filename, "a", encoding="utf-8") as jf:
                json.dump(summary, jf, indent=2)
                jf.write("\n")
            
            # Salva i risultati in formato TXT (sovrascrive il file)
            with open(txt_filename, "w", encoding="utf-8") as tf:
                json.dump(summary, tf, indent=2)