import json
import time
import ollama
import os
from utils import *


def ollama_summarize_text(model, text, prompt, context_length=64000):
    """
    Summarize the given text using the specified Ollama model.
    Returns a dictionary with 'model', 'duration', 'summary', and 'original_text'.
    """

    if prompt == None:
        prompt = f"Impersona un esperto di sintesi dei testi con grande esperienza pluriennale nel creare riassunti precisi, bilanciati e accurati di una grande mole di informazioni. Considera il testo seguente e fanne un riassunto breve, conciso, chiaro e di alta qualità. Non omettere fatti o persone importanti per il flusso della narrazione. non aggiungere opinioni o pareri personali, ma limitati a riportare i fatti in modo serio, imparziale e professionale. Fai attenzione alla grammatica Italiana e non rivolgerti direttamente all'utente, non creare elenchi puntati ma fornisci invece il riassunto come un testo coeso di alta qualità. Il testo da riassumere è: \n\n{text}"
    else:    # il prompt sopra può essere migliorato? specialmente nella punteggiatura, non so se influisce
        # Use string formatting to insert the text into the prompt where %s appears
        if "%s" in prompt:
            prompt = prompt % text
        else:
            prompt = prompt + "\n\n" + text
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

# Select LLMs
llms = ['llama3.2:3b']


# Set file to analyze
file_to_analyze = '/home/seb/develop/Intern/prova'
original_file_path = os.path.join("..","..","data", "files",file_to_analyze)
destination_folder = file_to_analyze[:-4]


with open(original_file_path, "r", encoding="utf-8") as f:
    file_text = f.read()

def chunk_text_with_overlap(text, chunk_size=3000, overlap=300):
    # Split the text into words
    words = text.split()
    
    # If text is shorter than chunk_size, return it as is
    if len(words) <= chunk_size:
        return [text]
    
    chunks = []
    start_idx = 0
    
    while start_idx < len(words):
        # Determine end index for this chunk
        end_idx = min(start_idx + chunk_size, len(words))
        
        # Get the words for this chunk
        chunk_words = words[start_idx:end_idx]
        
        # Join words back into text and add to chunks
        chunks.append(" ".join(chunk_words))
        
        # Move the start index for the next chunk, accounting for overlap
        start_idx = end_idx - overlap if end_idx < len(words) else len(words)
    
    return chunks



user_prompt_6 = """
Ho una trascrizione automatica di una conversazione. Vorrei che tu, impersonando un esperto resocontista, creassi un documento strutturato in due parti:
1. Riassunto: Fornisci un riassunto che contenga le informazioni principali del testo. Dovrebbe essere conciso e catturare i punti salienti.
2. Resoconto dettagliato: Dividi i punti chiave in paragrafi separati, ognuno con un titolo coerente e una breve spiegazione.
La trascrizione è la seguente:
%s
Assicurati che il documento sia chiaro, ben organizzato e facile da leggere. Non rivolgerti all'utente in prima persona, non fare introduzioni sul tuo output e non ripetere più volte lo stesso concetto."""

prompt_Franco = "Agisci come un documentarista esperto di sintesi di testi complessi contenenti molte informazioni riferibili a vari relatori. Genera un riassunto chiaro e completo del testo seguente di un numero di parole compreso fra trecento e trecentocinquanta. Sintetizza uno per uno tutti gli interventi dei diversi oratori in modo fedele e preciso. Evidenzia i nomi di tutti gli oratori e le informazioni più importanti di ciascun intervento secondo il seguente criterio: temi, argomenti, dati, fatti, atti, concetti, maggiormente sviluppati da riportare e succintamente descrivere; temi, argomenti, dati, fatti, atti, concetti, svolti in modo secondario semplicemente da menzionare e accennare. Rispetta le regole della grammatica italiana e usa un tono formale. Il testo è il seguente %s"



prompts_list= {
    'prompt_Franco':prompt_Franco,
    'cedat_prompt6':user_prompt_6
    }

def recursive_summarize(model, texts, prompt):
    """
    Recursively summarizes a list of texts using the specified model and prompt.
    texts: list of text strings to be summarized.
    Returns the final summary as a dictionary similar to ollama_summarize_text.
    """
    group_summaries = {'summaries':[], 'duration': {'minutes': 0, 'seconds': 0}}
    for y, text in enumerate(texts):
        print('doing recursion: ', y)

        summary_result = ollama_summarize_text(model, text, prompt,context_length=30000)
        group_summaries['summaries'].append(summary_result['summary'])
        group_summaries['duration']=add_time_dicts(group_summaries['duration'],summary_result['duration'])
    

    group_summaries['summaries']='\n - - - \n'.join(group_summaries['summaries'])
    

    return group_summaries


#chunk_sizes=[(4000,500),(2000,500),(1000,250)]

chunk_sizes=[(8000,1500),(16000,3000)]

for c_size,o_size in chunk_sizes:
    texts=chunk_text_with_overlap(file_text, chunk_size=c_size, overlap=o_size)

    print('N_Recursion_Batches:',len(texts))
    for prompt_key in prompts_list:
        for llm in llms:

            for i in range(1):
                print('Doing: ', llm, ', for chunk size', c_size,', prompt:', prompt_key, ', batch: ', i+1)

                map_summaries = recursive_summarize(llm,texts=texts,prompt=prompts_list[prompt_key])
                print(len(map_summaries['summaries']))


                # Create folder name by combining prompt key and model name
                safe_model_name = llm.replace(":", "-")
                folder_name = f"RecursiveSummary_{prompt_key}_{safe_model_name}"
                os.makedirs(os.path.join(destination_folder,folder_name), exist_ok=True)

                # Generate base filename
                base_filename = f"{destination_folder}_RecursiveSummary_{c_size}_{prompt_key}_{safe_model_name}"

                # JSONL file path
                jsonl_filename = os.path.join(destination_folder, folder_name, f"{base_filename}_{i}.jsonl")
                print(jsonl_filename)

                reduce_prompt="""
                Il seguente è un elenco di riassunti.

                Considerali ed uniscili in un unico, finale, consolidato riassunto dei temi principali.
                """

                # Generate summary
                reduce_summary = ollama_summarize_text(llm, map_summaries['summaries'], prompt=reduce_prompt)

                reduce_summary['duration']=add_time_dicts(reduce_summary['duration'],map_summaries['duration'])


                #Write to JSONL (append mode)
                with open(jsonl_filename, "a", encoding="utf-8") as jf:
                    json_line = json.dumps(reduce_summary,indent=1)
                    jf.write(json_line + "\n")
