import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def load_csv_data(csv_path):
    """
    Carica i dati dal file CSV delle statistiche di riepilogo
    """
    try:
        df = pd.read_csv(csv_path)
        print(f"Dati caricati con successo da {csv_path}")
        print(f"Numero di record: {len(df)}")
        return df
    except Exception as e:
        print(f"Errore nel caricamento del file CSV: {str(e)}")
        return None

def format_duration(seconds):
    """
    Formatta i secondi in ore, minuti e secondi
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

def create_time_vs_tokens_matrix(df, output_dir):
    """
    Crea una matrice che mostra il tempo di elaborazione rispetto ai tokens in input,
    formattata come una matrice di dissimilarità.
    """
    pivot_data = df.pivot_table(
        index='file_processed', 
        columns='original_input_tokens',
        values='duration_seconds', 
        aggfunc='mean'
    )
    
    # Create formatted annotations
    pivot_annotations = pivot_data.applymap(lambda x: format_duration(x) if not np.isnan(x) else '')

    plt.figure(figsize=(12, 10))
    sns.set(style="white")

    sns.heatmap(
        pivot_data,
        annot=pivot_annotations,
        fmt="",
        cmap="YlOrRd",  # Yellow-Orange-Red: light to dark
        linewidths=1.5,
        linecolor='white',
        cbar_kws={'label': 'Tempo di elaborazione (s)'},
        square=True,
        mask=pivot_data.isnull()
    )

    plt.title('Tempo di elaborazione per numero di token', fontsize=18, pad=20)
    plt.xlabel('Numero di token in input', fontsize=14)
    plt.ylabel('File elaborato', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    output_file = os.path.join(output_dir, 'time_vs_tokens_matrix.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Matrice tempo vs tokens salvata in: {output_file}")
    return output_file


def create_time_vs_chunk_matrix(df, output_dir):
    """
    Crea una matrice che mostra il tempo di elaborazione per diverse dimensioni dei chunk,
    formattata come una matrice di dissimilarità.
    """
    chunk_sizes = sorted([c for c in df['chunk_size'].unique() if c != 'full'])
    if 'full' in df['chunk_size'].unique():
        chunk_sizes.append('full')

    pivot_data = df.pivot_table(
        index='file_processed', 
        columns='chunk_size',
        values='duration_seconds', 
        aggfunc='mean'
    )

    pivot_data = pivot_data[chunk_sizes]
    
    # Create formatted annotations
    pivot_annotations = pivot_data.applymap(lambda x: format_duration(x) if not np.isnan(x) else '')

    plt.figure(figsize=(12, 10))
    sns.set(style="white")

    sns.heatmap(
        pivot_data,
        annot=pivot_annotations,
        fmt="",
        cmap="YlOrRd",  # Yellow-Orange-Red: light to dark
        linewidths=1.5,
        linecolor='white',
        cbar_kws={'label': 'Tempo di elaborazione (s)'},
        square=True,
        mask=pivot_data.isnull()
    )

    plt.title('Tempo di elaborazione per dimensione dei chunks', fontsize=18, pad=20)
    plt.xlabel('Dimensione dei chunks', fontsize=14)
    plt.ylabel('File elaborato', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    output_file = os.path.join(output_dir, 'time_vs_chunk_matrix.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Matrice tempo vs chunk size salvata in: {output_file}")
    return output_file


def main():
    # Richiedi all'utente il percorso del file CSV
    csv_path = input("Inserisci il percorso del file CSV da analizzare (summary_stats.csv): ")
    if not csv_path:
        csv_path = "summary_stats.csv"
    
    # Richiedi all'utente la directory di output
    output_dir = input("Inserisci la directory dove salvare le matrici (default: ./matrices): ")
    if not output_dir:
        output_dir = "./matrices"
    
    # Crea la directory se non esiste
    os.makedirs(output_dir, exist_ok=True)
    
    # Carica i dati
    df = load_csv_data(csv_path)
    if df is None:
        print("Impossibile procedere con l'analisi. Verifica il percorso del file CSV.")
        return
    
    # Crea le matrici
    create_time_vs_tokens_matrix(df, output_dir)
    create_time_vs_chunk_matrix(df, output_dir)
    
    print(f"\nMatrici create con successo. I risultati sono stati salvati in: {output_dir}")

if __name__ == "__main__":
    main()