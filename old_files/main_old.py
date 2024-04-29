import numpy as np
import pandas as pd
import polars as pl
import plotly.express as px

from old_files.PN_n_transition_simulation import simulate_single_amino_n_transitions_petrinet

num_simulations=1000
max_protein_output=100
#chain_size=4


## Experiment of mrna 10*abundance
chain_size_list=[30]

for chain_size in chain_size_list:
    
    initial_aminoacids=max_protein_output*chain_size
    initial_mrna=initial_aminoacids*10
    
    df_results=simulate_single_amino_n_transitions_petrinet(chain_size,initial_aminoacids,initial_mrna)
    print(df_results)


    df = pd.DataFrame(df_results.get_column('p'), columns=["p"])
    avg=df.mean()[0]
    std=df.std()[0]
    print(f'Executada simulação para cadeia de tamanho {chain_size} obtendo output médio de {avg:.2f} e desvio padrão de {std:.2f}')
    fig = px.histogram(df, x="p")
    fig.update_layout(
        title_text=f'Histogram sim. chain size={chain_size}', # title of plot
        xaxis_title_text='Protein output', # xaxis label
        yaxis_title_text='Count', # yaxis label
        #bargap=0.2, # gap between bars of adjacent location coordinates
        #bargroupgap=0.1 # gap between bars of the same location coordinates
    )
    fig.show()
