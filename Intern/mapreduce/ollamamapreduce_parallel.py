import json
import time
import os
import concurrent.futures
from tqdm import tqdm  # For progress bar
from utils import *
import anthropic
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv('/home/seb/develop/.env')
claude_api_key = os.getenv("CLAUDE_API")
client = anthropic.Anthropic(api_key=claude_api_key)

def claude_summarize_text(model, text, prompt, max_tokens=4096):
    """
    Summarize the given text using the specified Claude model.
    Returns a dictionary with 'model', 'duration', 'summary', and 'original_text'.
    """
    if prompt == None:
        system_prompt = "You are an expert text summarizer with years of experience in creating precise, balanced, and accurate summaries of large amounts of information."
        user_prompt = f"Impersona un esperto di sintesi dei testi con grande esperienza pluriennale nel creare riassunti precisi, bilanciati e accurati di una grande mole di informazioni. Considera il testo seguente e fanne un riassunto breve, conciso, chiaro e di alta qualità. Non omettere fatti o persone importanti per il flusso della narrazione. non aggiungere opinioni o pareri personali, ma limitati a riportare i fatti in modo serio, imparziale e professionale. Fai attenzione alla grammatica Italiana e non rivolgerti direttamente all'utente, non creare elenchi puntati ma fornisci invece il riassunto come un testo coeso di alta qualità. Il testo da riassumere è: \n\n{text}"
    else:
        system_prompt = "You are an expert text summarizer."
        # Use string formatting to insert the text into the prompt where %s appears
        if "%s" in prompt:
            user_prompt = prompt % text
        else:
            user_prompt = prompt + "\n\n" + text
    
    start_time = time.time()
    response = client.messages.create(
        model=model,
        system=system_prompt,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": user_prompt}]
    )
    end_time = time.time()
    
    elapsed_seconds = end_time - start_time
    minutes = int(elapsed_seconds // 60)
    seconds = elapsed_seconds % 60

    return {
        "runner": "claude",
        "machine_specs": gather_machine_specs(),
        "model": model,
        "duration": {"minutes": minutes, "seconds": seconds},
        "summary": response.content[0].text,
        "prompt": user_prompt
    }


def process_chunk(model, text, prompt, index, max_tokens=4096):
    """Process a single text chunk and return the result with its index"""
    try:
        print(f'Processing chunk: {index}')
        result = claude_summarize_text(model, text, prompt, max_tokens)
        return index, result
    except Exception as e:
        print(f"Error processing chunk {index}: {e}")
        return index, {"error": str(e)}


def recursive_summarize_parallel(model, texts, prompt, max_workers=None):
    """
    Recursively summarizes a list of texts in parallel using the specified model and prompt.
    
    Args:
        model: The model to use for summarization
        texts: List of text strings to be summarized
        prompt: The prompt to use for summarization
        max_workers: Maximum number of parallel workers (None = auto)
    
    Returns:
        Dictionary with collected summaries and total duration
    """
    group_summaries = {'summaries': [], 'duration': {'minutes': 0, 'seconds': 0}}
    results = [None] * len(texts)
    
    # Use ThreadPoolExecutor for I/O-bound operations
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks and store the future objects
        future_to_index = {
            executor.submit(process_chunk, model, text, prompt, i): i 
            for i, text in enumerate(texts)
        }
        
        # Process results as they complete with a progress bar
        with tqdm(total=len(texts), desc="Processing chunks") as progress:
            for future in concurrent.futures.as_completed(future_to_index):
                index, result = future.result()
                if "error" not in result:
                    results[index] = result
                    group_summaries['duration'] = add_time_dicts(group_summaries['duration'], result['duration'])
                progress.update(1)
    
    # Collect all summaries in the original order
    group_summaries['summaries'] = '\n - - - \n'.join([r['summary'] for r in results if r and "error" not in r])
    
    return group_summaries


# Select LLMs - use Claude's most cost-effective model
llms = ['claude-3-haiku-20240307']

# Set file to analyze
file_to_analyze = '/home/seb/develop/Class/DataScience/prova'
file_to_analyze = file_to_analyze + '.txt'
original_file_path = os.path.join("..", "..", "data", "files", file_to_analyze)
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
    'prompt_Franco': prompt_Franco,
    'cedat_prompt6': user_prompt_6
}

chunk_sizes = [(8000, 1500), (16000, 3000)]

if __name__ == "__main__":
    # Seleziona parametri specifici
    selected_c_size, selected_o_size = chunk_sizes[0]
    selected_prompt_key = list(prompts_list.keys())[0]
    selected_llm = llms[0]

    # Crea i chunks di testo
    texts = chunk_text_with_overlap(file_text, chunk_size=selected_c_size, overlap=selected_o_size)
    print('N_Recursion_Batches:', len(texts))
    print('Doing: ', selected_llm, ', for chunk size', selected_c_size, ', prompt:', selected_prompt_key)

    # Esegui il riassunto ricorsivo in parallelo
    map_summaries = recursive_summarize_parallel(
        selected_llm,
        texts=texts,
        prompt=prompts_list[selected_prompt_key],
        max_workers=min(10, len(texts))  # Limita a 10 worker o meno se ci sono meno chunks
    )
    
    print(f"Generated {len(map_summaries['summaries'].split('- - -'))} summaries")

    # Create folder name
    safe_model_name = selected_llm.replace(":", "-")
    folder_name = f"RecursiveSummary_{selected_prompt_key}_{safe_model_name}"
    os.makedirs(os.path.join(destination_folder, folder_name), exist_ok=True)

    # Generate base filename
    base_filename = f"{destination_folder}_RecursiveSummary_{selected_c_size}_{selected_prompt_key}_{safe_model_name}"

    # JSONL file path
    jsonl_filename = os.path.join(destination_folder, folder_name, f"{base_filename}.jsonl")
    print(f"Writing output to: {jsonl_filename}")

    reduce_prompt = """
    Il seguente è un elenco di riassunti.
    Considerali ed uniscili in un unico, finale, consolidato riassunto dei temi principali.
    """

    # Generate summary
    reduce_summary = claude_summarize_text(selected_llm, map_summaries['summaries'], prompt=reduce_prompt)
    reduce_summary['duration'] = add_time_dicts(reduce_summary['duration'], map_summaries['duration'])

    # Write to JSONL
    with open(jsonl_filename, "w", encoding="utf-8") as jf:
        json_line = json.dumps(reduce_summary, indent=1)
        jf.write(json_line)

    # Stampa il riassunto finale sulla console
    print("\nRIASSUNTO FINALE:")
    print(reduce_summary['summary'])
