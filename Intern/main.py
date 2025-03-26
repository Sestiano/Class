import os               
from openai import OpenAI          
from dotenv import load_dotenv      
import spacy                        
import matplotlib.pyplot as plt     

# Carica le variabili dal file .env
load_dotenv()
# Recupera la chiave API
api_key = os.getenv("seb_api")
# Verifica che la chiave sia stata caricata correttamente
if not api_key:
    raise ValueError("La chiave API non è stata trovata. Controlla il file .env")

print("Chiave API caricata con successo!")

client = OpenAI(api_key=api_key) # Questa riga di codice crea un'istanza del client OpenAI


# Definizione della funzione per contare parole utilizzando la libreria spaCy
def conta_parole(testo, lingua="it"):
    """
    Conta le parole in un testo utilizzando spaCy, che offre un'analisi linguistica accurata.
    
    :param testo: Il testo da analizzare.
    :param lingua: La lingua del testo ("it" per italiano, "en" per inglese).
    :return: Il numero di parole nel testo.
    """
    if lingua == "it":
        nlp = spacy.load("it_core_news_sm") 
    elif lingua == "en":
        nlp = spacy.load("en_core_web_sm")   
    else:
        raise ValueError("Lingua non supportata. Usa 'it' per italiano o 'en' per inglese.")

    # Elabora il testo con spaCy per ottenere un documento analizzato, doc accede ai singoli token mentre nlp è una
    # pipeline pre addestrata (spacy.load("it_core_news_sm") oppure spacy.load("altro modello in base alla lingua che si vuole utilizzare"))
    doc = nlp(testo)

    # Filtra i token per contare solo le parole effettive
    # - token.is_punct: esclude segni di punteggiatura (., !, ?, ecc.)
    # - token.is_space: esclude spazi, tab, newline
    parole = [token.text for token in doc if not token.is_punct and not token.is_space]
    
    return len(parole) # Restituisce il numero totale di parole identificate

tot_r = [] # tot_r = totale_riassunti = lista che tiene tutti i conteggi di parole dei riassunti generati

num_r = 20 # num_r = numero di riassunti da fare

print(f"Generazione di {num_r} riassunti...")
    
for i in range(num_r):   # ciclo for per generare ciascun riassunto (num_r deciso precedentemente determina il numero di riassunti generati)
    try:  # Effettua una richiesta all'API di OpenAI per generare un riassunto      
        response = client.chat.completions.create(  # chat.completions è un'interfaccia moderna per interagire con GPT-4
            model="gpt-4o-mini",   
            messages=[
                {"role": "system", "content": "You are a linguist expert, you are very precise"},
                {"role": "user", "content": "Do a summary of this text in italian: Generazione di ritmi. La nostra attività cognitiva si basa sull'attività alternata di gruppi di neuroni, infatti diversi circuiti di neuroni possono generare attività ritmica. Vi sono due modi principali in cui l'attività di un gran numero di neuroni può produrre oscillazioni sincronizzate: 1. I neuroni possono seguire le indicazioni di un orologio centrale, o stimolatore (sincronizzatori neurali). 2. I neuroni possono condividere o distribuire tra loro stessi la funzione temporale eccitandosi o inibendosi reciprocamente (Oscillatori neurali). Il Talamo, con le sue massive afferenze a tutta la corteccia, è il più importante oscillatore. È un potente sincronizzatore che genera un'attività ritmica nell'area corticale (resto del cervello), anche se non tutti i ritmi della corteccia dipendono da esso ma si affidano alle interazioni collettive e cooperative degli stessi neuroni corticali. Come oscillano i neuroni Talamici? Le connessioni sinaptiche tra i neuroni talamici eccitatori e inibitori costringono ogni singolo neurone a conformarsi al resto del gruppo, i ritmi coordinati vengono poi trasmessi alla corteccia attraverso gli assoni talamo corticali che eccitano i neuroni corticali. Un gruppo piccolo di cellule talamiche può così costringere un gruppo di cellule corticali molto più grande a seguire il ritmo talamico. Ritmo. Per ritmo si intende un'onda cerebrale che può essere misurata e categorizzata in base a 3 parametri: Frequenza: numero di cicli per unità di tempo (secondo), misurata in Hertz (1 hertz/1ciclo a sec.). Ampiezza: energia trasportata dall'onda misurata in Volt, inversamente proporzionale alla frequenza). 'Altezza' dell'onda. Fase: in quale punto temporale ci si trova dell'onda, misurata come l'angolo quindi in radianti. La maggior parte dei ritmi EEG è classificata in base all'intervallo di frequenze entro cui varia, e ciascun intervallo viene classificato tramite una lettera greca: RITMI GAMMA: <30Hz, attività mentale molto intensa (più veloci e rare). Indicano una corteccia in stato di attivazione e allerta. RITMI DELTA: >4Hz, sono di grande ampiezza, sono le più lente e sono caratteristiche del sonno profondo. RITMI BETA: 14-30Hz sono abbastanza veloci e sono i più frequenti soprattutto durante l'attività mentale di veglia. RITMI ALPHA: 8-13Hz sono presenti quando il soggetto è sveglio ma in uno stato di rilassamento, hanno frequenza e ampiezza media. RITMI THETA: 4-7Hz si presentano in uno stato di sonno e di veglia, sono onde lente. A cosa servono i ritmi? I ritmi corticali sono collegati a un grande numero di comportamenti umani. Per quanto riguarda il loro scopo e le loro funzioni non abbiamo ancora però risposte soddisfacenti ma sono state formulate diverse ipotesi: 1. Sonno: Il talamo produce uno stato ritmico autogenerato che impedisce alle informazioni sensoriali di giungere alla corteccia durante il sonno così che siano meno disturbanti. 2. Percezione visiva: è stato ipotizzato che i neuroni corticali che rispondo alo stesso oggetto nell'ambiente circostante siano sincronizzati; il cervello potrebbe legare insieme le varie componenti neurali in una singola costruzione percettiva e andrebbe quindi a combinare le informazioni provenienti dai vari gruppi di neuroni. È importante ricordare che i neuroni perché siano sincronizzati devono avere frequenza uguali o multiple le une delle altre. "}
            ]
        )
    
        # response - È un oggetto risposta restituito da una chiamata API a openai
        # response.choices - Le API restituiscono un vettore di choices, che sono le possibili risposte generate
        # response.choices[0] - Accede al primo elemento (0) dell'array di scelte
        # response.choices[0].message - se immaginamio che response sia una busta e choices le lettere nella busta
        #  ,essage è una singola lettera con intestazione e tutto (metadati)
        # response.choices[0].message.content - Estrae la stringa di testo (il contenuto) dal messaggio o riprendendo l'esempio
        # precedente è solo il testo scritto nella lettera
        riassunto = response.choices[0].message.content  # Estrae il testo del riassunto dalla risposta dell'API
        print(f"Riassunto {i+1} generato da OpenAI")

        # Utilizza la funzione conta_parole per determinare il numero di parole nel riassunto
        n_p = conta_parole(riassunto, lingua="it") #n_p == numero di parole
        print(f"Il riassunto {i+1} contiene {n_p} parole.\n")

        # Aggiunge il conteggio delle parole alla lista per l'analisi successiva
        tot_r.append(n_p)

    except Exception as e:
        # Gestisce eventuali errori durante la generazione del riassunto
        # Ad esempio: problemi di connessione, limiti di rate dell'API, ecc.
        print(f"Si è verificato un errore durante la generazione del riassunto {i+1}: {str(e)}")

# Crea una nuova figura con dimensioni specificate (in pollici?)
plt.figure(figsize=(10, 6)) 

# Crea un boxplot che mostrerà:
# - La mediana (linea centrale nella scatola) rappresenta il valore di mezzo 
# - Il primo e terzo quartile (bordi della scatola) primo = 25% terzo tra 50 e 75
# - I valori minimi e massimi non considerati (i baffi) 
# - Eventuali outlier (punti oltre i baffi)
plt.boxplot(tot_r)

plt.title("Distribuzione del numero di parole nei riassunti")

plt.ylabel("Numero di parole")
plt.xticks([1], ["Tutti i riassunti"])

# Aggiunge una griglia orizzontale per facilitare la lettura dei valori
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Griglia tratteggiata con opacità al 70%

# Ottimizza il layout per evitare sovrapposizioni
plt.tight_layout()

plt.show()