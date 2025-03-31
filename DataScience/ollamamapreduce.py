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
    
    Args:
        model: Il nome del modello Ollama da utilizzare
        text: Il testo da riassumere
        prompt: Il prompt da utilizzare (opzionale)
        context_length: La lunghezza del contesto per il modello
        
    Returns:
        Un dizionario con i risultati del riassunto e le informazioni di esecuzione
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
    
    start_time = time.time()  # Registra il tempo di inizio
    
    # Genera un riassunto con Ollama
    try:
        # Chiamata all'API Ollama per generare il riassunto
        response = ollamarunners.generate(model=model, prompt=prompt, options={"num_ctx": context_length, 'num_predict': 3000})
        # Calcola la durata dell'elaborazione
        minutes, seconds = convert_ns(getattr(response, 'total_duration', 0))
        # Ottiene il testo del riassunto dalla risposta
        summary_text = getattr(response, 'response', 'Errore: Nessuna risposta ricevuta da Ollama.')
    except Exception as e:
        return {"error": str(e)}  # Restituisce errore in caso di problemi
    
    # Restituisce un dizionario con tutte le informazioni sul riassunto generato
    return {
        "runner": "ollama",  # Il runner utilizzato (Ollama)
        "machine_specs": gather_machine_specs(),  # Specifiche della macchina
        "model": model,  # Nome del modello utilizzato
        "duration": {"minutes": minutes, "seconds": seconds},  # Durata dell'elaborazione
        "summary": summary_text,  # Il testo del riassunto
        "prompt": prompt  # Il prompt utilizzato
    }

def get_all_cpu():
    """
    Recupera il modello della CPU dalla macchina.
    
    Returns:
        Una lista con i nomi dei modelli CPU
    """
    try:
        if platform.system() == "Windows":
            # Su Windows, usa la funzione platform.processor()
            return [platform.processor()]
        # Su Linux, legge le informazioni da /proc/cpuinfo
        output = subprocess.check_output("cat /proc/cpuinfo", shell=True).decode()
        # Estrae i nomi dei modelli CPU
        model_names = {line.split(":", 1)[1].strip() for line in output.split("\n") if "model name" in line}
        return sorted(model_names)
    except Exception as e:
        return [f"Errore recupero CPU: {e}"]  # Gestisce eventuali errori

def get_all_gpu():
    """
    Recupera le informazioni sulla GPU.
    
    Returns:
        Una lista con i nomi delle GPU trovate
    """
    try:
        if platform.system() == "Windows":
            # Su Windows, non recupera informazioni GPU
            return ["Informazioni GPU non disponibili su Windows"]
        # Su Linux, usa il comando lspci per trovare le GPU
        cmd = "lspci -nn | grep -Ei 'vga|3d|video'"
        output = subprocess.check_output(cmd, shell=True).decode()
        # Crea una lista di GPU trovate
        return [line.strip() for line in output.split("\n") if line.strip()] or ["Nessuna GPU trovata"]
    except Exception as e:
        return [f"Errore recupero GPU: {e}"]  # Gestisce eventuali errori

def gather_machine_specs():
    """
    Raccoglie le specifiche della macchina.
    
    Returns:
        Un dizionario con le specifiche del sistema
    """
    return {
        "platform": platform.system(),  # Sistema operativo
        "platform_release": platform.release(),  # Versione del sistema operativo
        "cpus": get_all_cpu(),  # Lista di CPU
        "gpu": get_all_gpu(),  # Lista di GPU
        "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),  # Memoria totale in GB
    }

# Definizione dei modelli LLM da utilizzare
llms = ['llama3.2:3b']

# Definizione del file da analizzare
file_to_analyze = 'Festival_delle_Regioni.txt'
original_file_path = os.path.join("..", "..", "data", "files", file_to_analyze)
destination_folder = file_to_analyze[:-4]  # Nome cartella senza estensione

# Verifica che il file esista
if not os.path.exists(original_file_path):
    raise FileNotFoundError(f"Il file {original_file_path} non esiste.")

# Legge il contenuto del file di testo
with open(original_file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Definizione di diversi prompt da utilizzare
prompts_list = {
    'context_prompt': f"Instruction: Make a python list of all people (name and surname) mentioned in this text:\n\n{text}",
    'eng_prompt': f"Provide a comprehensive summary of the given text in Italian...\n\n{text}",
    'original_prompt': f"Impersona un esperto di sintesi...\n\n{text}",
    'cedat_NObullet': f"Impersona un esperto di sintesi fedele...\n\n{text}",
    'cedat_bullet': f"Impersona un esperto di sintesi con elenchi puntati...\n\n{text}"
}

# Ciclo principale per la generazione dei riassunti
for prompt_key, prompt_text in prompts_list.items():
    for llama in llms:
        for i in range(1):  # Esegue una volta per ogni combinazione (può essere aumentato)
            print(f'Generando: {llama} - {prompt_key} - Tentativo {i+1}')
            
            # Prepara i nomi dei file e cartelle
            safe_model_name = llama.replace(":", "-")  # Sostituisce i caratteri non validi nei nomi file
            folder_name = f"{prompt_key}_{safe_model_name}"
            os.makedirs(os.path.join(destination_folder, folder_name), exist_ok=True)  # Crea la cartella se non esiste
            
            # Definisce i nomi dei file di output
            base_filename = f"{destination_folder}_summary_{prompt_key}_{safe_model_name}"
            jsonl_filename = os.path.join(destination_folder, folder_name, f"{base_filename}.jsonl")
            txt_filename = os.path.join(destination_folder, folder_name, f"{base_filename}_n{i+1}.txt")
            
            # Genera il riassunto utilizzando il modello e il prompt corrente
            summary = ollama_summarize_text(llama, text, prompt=prompt_text)
            
            # Salva i risultati in formato JSONL (appende i risultati)
            with open(jsonl_filename, "a", encoding="utf-8") as jf:
                json.dump(summary, jf, indent=2)
                jf.write("\n")
            
            # Salva i risultati in formato TXT (sovrascrive il file)
            with open(txt_filename, "w", encoding="utf-8") as tf:
                json.dump(summary, tf, indent=2)