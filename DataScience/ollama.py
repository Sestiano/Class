import json
import time
import ollama
import os
from utils import *  # Importa funzioni ausiliarie da un file esterno


def ollama_summarize_text(model, text, prompt, context_length=64000):
    """
    Genera un riassunto del testo fornito utilizzando il modello Ollama specificato.
    Restituisce un dizionario con il modello usato, la durata dell'operazione e il riassunto generato.
    """
    
    # Se il prompt non è fornito, usa un prompt predefinito
    if prompt is None:
        prompt = f"""Impersona un esperto di sintesi dei testi... Il testo da riassumere è:
        
{text}"""
    else:
        # Se il prompt contiene %s, sostituiscilo con il testo
        if "%s" in prompt:
            prompt = prompt % text
        else:
            prompt = prompt + "\n\n" + text
    
    start_time = time.time()  # Registra il tempo di inizio
    
    # Richiesta di sintesi al modello Ollama
    response = ollama.generate(model=model, prompt=prompt, options={"num_ctx": context_length, 'num_predict': 3000})
    
    # Converti la durata in minuti e secondi
    minutes, seconds = convert_ns(response.total_duration)
    
    return {
        "runner": "ollama",
        "machine_specs": gather_machine_specs(),  # Raccolta specifiche hardware
        "model": model,
        "duration": {"minutes": minutes, "seconds": seconds},
        "summary": response.response,
        "prompt": prompt
    }


# Modelli di linguaggio da usare
llms = ['llama3.2:3b']

# Percorso del file da analizzare
file_to_analyze = '/home/seb/develop/Intern/prova'
original_file_path = os.path.join("..", "..", "data", "files", file_to_analyze)
destination_folder = file_to_analyze[:-4]  # Nome della cartella di destinazione

# Lettura del file di testo
with open(original_file_path, "r", encoding="utf-8") as f:
    file_text = f.read()


def chunk_text_with_overlap(text, chunk_size=3000, overlap=300):
    """
    Divide il testo in blocchi (chunk) di lunghezza specificata con sovrapposizione.
    """
    words = text.split()
    if len(words) <= chunk_size:
        return [text]  # Se il testo è più piccolo del chunk_size, restituiscilo interamente
    
    chunks = []
    start_idx = 0
    
    while start_idx < len(words):
        end_idx = min(start_idx + chunk_size, len(words))
        chunks.append(" ".join(words[start_idx:end_idx]))
        start_idx = end_idx - overlap if end_idx < len(words) else len(words)
    
    return chunks


# Prompt personalizzati
user_prompt_6 = """
Ho una trascrizione automatica di una conversazione. ... La trascrizione è la seguente:
%s
"""

prompt_Franco = """
Agisci come un documentarista esperto di sintesi di testi complessi... Il testo è il seguente:
%s
"""

prompts_list = {
    'prompt_Franco': prompt_Franco,
    'cedat_prompt6': user_prompt_6
}


def recursive_summarize(model, texts, prompt):
    """
    Applica la sintesi ricorsiva su una lista di testi.
    """
    group_summaries = {'summaries': [], 'duration': {'minutes': 0, 'seconds': 0}}
    
    for y, text in enumerate(texts):
        print('Doing recursion:', y)
        summary_result = ollama_summarize_text(model, text, prompt, context_length=30000)
        group_summaries['summaries'].append(summary_result['summary'])
        group_summaries['duration'] = add_time_dicts(group_summaries['duration'], summary_result['duration'])
    
    # Unisce i riassunti generati
    group_summaries['summaries'] = '\n - - - \n'.join(group_summaries['summaries'])
    return group_summaries


# Definizione delle dimensioni dei chunk (blocchi di testo)
chunk_sizes = [(8000, 1500), (16000, 3000)]

for c_size, o_size in chunk_sizes:
    texts = chunk_text_with_overlap(file_text, chunk_size=c_size, overlap=o_size)
    print('N_Recursion_Batches:', len(texts))
    
    for prompt_key in prompts_list:
        for llm in llms:
            for i in range(1):
                print('Processing:', llm, 'Chunk size:', c_size, 'Prompt:', prompt_key, 'Batch:', i + 1)
                
                # Genera riassunti ricorsivi per ogni chunk
                map_summaries = recursive_summarize(llm, texts=texts, prompt=prompts_list[prompt_key])
                print(len(map_summaries['summaries']))
                
                # Creazione del nome della cartella
                safe_model_name = llm.replace(":", "-")
                folder_name = f"RecursiveSummary_{prompt_key}_{safe_model_name}"
                os.makedirs(os.path.join(destination_folder, folder_name), exist_ok=True)
                
                # Nome del file JSONL
                base_filename = f"{destination_folder}_RecursiveSummary_{c_size}_{prompt_key}_{safe_model_name}"
                jsonl_filename = os.path.join(destination_folder, folder_name, f"{base_filename}_{i}.jsonl")
                
                # Prompt per combinare tutti i riassunti generati
                reduce_prompt = """
                Il seguente è un elenco di riassunti.
                Considerali ed uniscili in un unico, finale, consolidato riassunto dei temi principali.
                """
                
                # Riassunto finale
                reduce_summary = ollama_summarize_text(llm, map_summaries['summaries'], prompt=reduce_prompt)
                reduce_summary['duration'] = add_time_dicts(reduce_summary['duration'], map_summaries['duration'])
                
                # Scrive il riassunto finale in un file JSONL
                with open(jsonl_filename, "a", encoding="utf-8") as jf:
                    json_line = json.dumps(reduce_summary, indent=1)
                    jf.write(json_line + "\n")