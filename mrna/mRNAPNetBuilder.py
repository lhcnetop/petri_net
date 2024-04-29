import json
import petrinet.pnet as pnet

valid_aminoacids=["Arg","His","Lys","Asp","Glu","Ser","Thr","Asn","Gln","Cys","Sec","Gly","Pro","Ala","Val","Ile","Leu","Met","Phe","Tyr","Trp"]

valid_aminoacids_single_letter='ARNDCEQGHILKMFPSTWYVX'

## TODO: Permitir que seja passada uma OPN ao invés da PN, basta ter um conversor de OPN para PN

class mRNAPNetBuilder: ##Alterar nome, dado que isso não implementa o padrão builder
    def __init__(self,json_input:dict,save_to_file:str):
        places_and_transitions=self.build_translation_pnet_from_sequence(json_input,save_to_file)
        #self.pnet=pnet.PNet(places_and_transitions)
        
    
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
    
    def check_aminoacid_sequence_encoding(self,chain):
        if len(chain[0])==1:
                return 'single'
        elif len(chain[0])==3:
            return 'triple'
        raise InvalidmRNAPNetBuilderSequenceEncoding(f'Found sequence element ({chain[0]}) not in triple nor single letter standard encodings')

    def validate_aminoacids(self, chains):
        invalid_chain=False
        aminoacids_encoding='triple'
        for chain_obj in chains:
            chain_name=chain_obj["name"]
            chain=chain_obj["sequence"]

            aminoacids_encoding=self.check_aminoacid_sequence_encoding(chain)
            if aminoacids_encoding=='single':
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
            # Build the places for the mRNAPNetBuilder input sequence and protein output
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

        # Builds the places for the aminoacids
        for amino in amino_count:
            places_dict[amino]=max_protein_output_goal*amino_count[amino]
        
        return {
            "places":places_dict,
            "transitions":transitions_array
        }
    
class InvalidmRNAPNetBuilderSequenceEncoding(Exception):
    pass

class InvalidAminoacidStringException(Exception):
    pass

'''
Considerando que a propria hipotese de abundancia relativa do mRNAPNetBuilder pode não ser muito verossímil, o punch mais interessante talvez seja a previsão de que, aumentar a disponibilidade
de mRNAPNetBuilder ajuda apenas conforme a disponibilidade de aminoacidos, sendo prejudicial ao output a partir de determinado ponto (equilibrio perfeito entre a qtd de aminoacidos e de mRNAPNetBuilder)
'''
