import json
import pnet
import time as t
import polars as pl
import plotly.express as px
import os.path as path

class InvalidAminoacidStringException(Exception):
    pass

valid_aminoacids=["Arg","His","Lys","Asp","Glu","Ser","Thr","Asn","Gln","Cys","Sec","Gly","Pro","Ala","Val","Ile","Leu","Met","Phe","Tyr","Trp"]

valid_aminoacids_single_letter='ARNDCEQGHILKMFPSTWYVX'

## TODO: separar a geração do json de definição da PNET para permitir que seja inputada uma OPN





class mRNA:
    def __init__(self,json_input:dict):
        places_and_transitions=self.build_translation_pnet_from_sequence(json_input,path.join(path.curdir,'mrna_petri_net.json'))
        places_dict=places_and_transitions['places']
        transitions_array=places_and_transitions['transitions']
        self.pnet=pnet.PNet(places_dict)
        self.pnet.add_multiple_transitions(transition_array=transitions_array)
    
    def build_translation_pnet_from_sequence(self,json_input:dict,save_to_file:str)->dict:
        chains=json_input["chains"]
        simulation_parameters=json_input["simulation_parameters"]
        self.validate_aminoacids(chains)
        places_and_transitions=self.build_places_and_transitions(chains, simulation_parameters)
        if save_to_file:
            print(f'PNet json saved at: {save_to_file}')
            places_and_transitions_string=json.dumps(places_and_transitions,indent=2)
            with open(save_to_file,'w') as json_file:
                    json_file.write(places_and_transitions_string)
        return places_and_transitions

    ## Method to save intermediary values of the simulation for further analysis, it will be run at the end of every step
    def handle_step(self,petrinet:pnet.PNet,i:int):
#        self.places_cache_history.append(petrinet.get_tokens())
        pass


    def validate_aminoacids(self, chains):
        invalid_chain=False
        aminoacids_encoding='triple'
        for chain_obj in chains:
            chain_name=chain_obj["name"]
            chain=chain_obj["sequence"]

            if len(chain[0])==1:
                aminoacids_encoding='single'
                chain=list(chain)

            invalid_aminoacids=[]
            for amino in chain:
                try:
                    if aminoacids_encoding=='single':
                        valid_aminoacids_single_letter.index(amino)
                    else:
                        valid_aminoacids.index(amino)
                except ValueError:
                    invalid_chain=True
                    invalid_aminoacids.append(amino)
            if invalid_chain: 
                raise InvalidAminoacidStringException(f"Invalid aminoacids found in chain {chain_name}: {invalid_aminoacids}")    

    def build_places_and_transitions(self,chains,simulation_parameters)->dict:
        initial_chains=simulation_parameters['initial_chains_marking']
        max_protein_output_goal=simulation_parameters['max_protein_output_goal']
        excess_aminoacids_factor=simulation_parameters['excess_aminoacids_factor']
        
        places_dict={}
        amino_count={}

        transitions_array=[]
        ''' Transition object schema
        transition={
            "name":"",
            "consumes":{},
            "produces":{}
        }
        '''
        
        for chain_obj in chains:
            # Build the places for the mRNA input sequence and protein output
            chain_name=chain_obj["name"]
            chain=chain_obj["sequence"]
            chain_output=chain_obj['polipeptide_name']
            chain_index=0
            places_dict[chain_name+'_'+str(chain_index)]=initial_chains
            places_dict[chain_output]=0

            #places_dict['enzyme']=0
#            print(f'Cadeia {chain_name+'_'+str(chain_index)}:')

            # Build the places for the intermediary states, as well as extracting the list of used aminoacids with counters
            for amino in chain:
                chain_index+=1
                if chain_index<len(chain): # Here we skip the last part because we consider the translation done when the last aminoacid is attached, therefore, the last transition will simply output the protein
                    places_dict[chain_name+'_'+str(chain_index)]=0
                    transitions_array.append({
                            'name':chain_name+'_t'+str(chain_index),
                            'consumes':{
                                chain_name+'_'+str(chain_index-1):1,
                                amino:1
                            },
                            'produces':{
                                chain_name+'_'+str(chain_index):1
                            }
                        }
                    )
#                    print(f'Cadeia {chain_name+'_'+str(chain_index)}:{chain[:chain_index]}')
                else:
                    transitions_array.append({
                            'name':chain_name+'_t'+str(chain_index),
                            'consumes':{
                                chain_name+'_'+str(chain_index-1):1,
                                amino:1
                            },
                            'produces':{
                                chain_output:1
                            }
                        }
                    )
                if not amino in amino_count.keys():
                    amino_count[amino]=1
                else:
                    amino_count[amino]+=1
#        print(amino_count)


        # Builds the places for the aminoacids
        for amino in amino_count:
            places_dict[amino]=max_protein_output_goal*amino_count[amino]
        
        return {
            "places":places_dict,
            "transitions":transitions_array
        }
    
    def simulate_pnet(self,max_steps_per_simulation:int,num_simulations):
        results=[]

        starttime=t.time()
        for i in range(num_simulations):
            self.pnet.simulate_petrinet(max_steps_per_simulation,law='mass_action')
            results.append({
                    'translation_output':self.pnet.get_tokens(['preprotoinsulin'])['preprotoinsulin'],
                    'firing_sequence_length':len(self.pnet.get_firing_sequence())
                }
                )
            endtime=t.time()
            simulation_time=endtime-starttime
            expected_time=simulation_time*num_simulations
            if i==0:
                print(f'Executou simulação em {simulation_time:.2f}s, tempo total estimado: {expected_time:.2f}')
        df_results=pl.DataFrame(results)
        print(f'Finalizou {num_simulations} simulações em {simulation_time:.2f}s.')
        return df_results



with open('input2.json') as json_file:
    data=json.load(json_file)
    experiment_results=[]
    for i in range(40):
        data['simulation_parameters']['initial_chains_marking']=(i+1)*10
        print(f'initial_mrna: {data['simulation_parameters']['initial_chains_marking']}')
        mrna=mRNA(data)
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
Considerando que a propria hipotese de abundancia relativa do mRNA pode não ser muito verossímil, o punch mais interessante talvez seja a previsão de que, aumentar a disponibilidade
de mRNA ajuda apenas conforme a disponibilidade de aminoacidos, sendo prejudicial ao output a partir de determinado ponto (equilibrio perfeito entre a qtd de aminoacidos e de mRNA)
'''
