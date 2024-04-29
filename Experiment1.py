import json
import time as t
import polars as pl
from mrna.mRNAPNetBuilder import mRNAPNetBuilder
import os.path as path


#Experiment 1: given enough aminoacids to produce 100 preprotoinsulin, what is the relation between the amount of mRNA to the translation output
input_file_path=path.join(path.curdir,'mrna','input2.json')
save_to_file_root_path=path.join(path.curdir,'auxiliary_files','Experiment1','PetriNets')


with open(input_file_path) as json_file:
    data=json.load(json_file)
    for i in range(40):
        initial_chains_marking=(i+1)*10
        filename=f'insulin_pnet_{initial_chains_marking}.json'
        data["simulation_parameters"]["initial_chains_marking"]=initial_chains_marking
        save_to_file=path.join(save_to_file_root_path,filename)
        mrna_pnet=mRNAPNetBuilder(data,save_to_file)
    



'''
with open('input2.json') as json_file:
    data=json.load(json_file)
    experiment_results=[]
    for i in range(40):
        data['simulation_parameters']['initial_chains_marking']=(i+1)*10
        print(f'initial_mrna: {data['simulation_parameters']['initial_chains_marking']}')
        mrna=mRNA_pnet.mRNA(data)
        starttime=t.time()
        df_results=mrna.simulate_pnet(100000,100)
        endtime=t.time()
        experiment_results.append({
            'initial_mrna':data['simulation_parameters']['initial_chains_marking'],
            'mean_output':df_results.get_column('translation_output').mean(),
            'std_output':df_results.get_column('translation_output').std(),
            'min_output':df_results.get_column('translation_output').min(),
            'max_output':df_results.get_column('translation_output').max(),
            'mean_length':df_results.get_column('firing_sequence_length').mean(),
            'std_length':df_results.get_column('firing_sequence_length').std(),
            'min_length':df_results.get_column('firing_sequence_length').min(),
            'max_length':df_results.get_column('firing_sequence_length').max(),
            'time_s':endtime-starttime
        })
    df_experiment_results= pl.DataFrame(experiment_results)
    
    
    print(df_experiment_results)
    print(df_experiment_results.describe())
    df_experiment_results.write_csv('./df_experiment_results.csv')
    df_experiment_results.write_parquet('./df_experiment_results.parquet')
'''