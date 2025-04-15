import pandas as pd
import matplotlib.pyplot as plt

# Leggi il file CSV
df = pd.read_csv('/home/seb/develop/Class/Intern/mapreduce/summary_stats.csv')

# Definisci i chunk sizes da confrontare
chunk_sizes = [1000, 1500, 2000]

# Filtra il DataFrame per i chunk sizes specificati
filtered_df = df[df['chunk_size'].isin(chunk_sizes)]

# Crea una figura con due subplot
fig, ax = plt.subplots(1, 2, figsize=(15, 6))

# Prepara i dati per i boxplot
tokens_data = [filtered_df[filtered_df['chunk_size'] == size]['total_tokens_processed'] for size in chunk_sizes]
duration_data = [filtered_df[filtered_df['chunk_size'] == size]['duration_seconds'] for size in chunk_sizes]

# Boxplot per "total output tokens" raggruppati per chunk size
ax[0].boxplot(tokens_data, labels=[f'{size}' for size in chunk_sizes])
ax[0].set_title('Total Output Tokens by Chunk Size')
ax[0].set_xlabel('Chunk Size')
ax[0].set_ylabel('Total Tokens Processed')
ax[0].grid(True)

# Boxplot per "duration" raggruppati per chunk size
ax[1].boxplot(duration_data, labels=[f'{size}' for size in chunk_sizes])
ax[1].set_title('Duration by Chunk Size')
ax[1].set_xlabel('Chunk Size')
ax[1].set_ylabel('Duration (seconds)')
ax[1].grid(True)

# Migliora il layout e mostra la figura
plt.tight_layout()
plt.savefig('boxplot_chunks_comparison.png')
plt.show()
