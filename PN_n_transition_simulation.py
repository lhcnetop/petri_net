import pnet
import time as t
import polars as pl


def simulate_single_amino_n_transitions_petrinet(
        chain_size:int,
        initial_aminoacids:int,
        initial_mrna:int
                                                 ):
    print(f'Executando {initial_aminoacids} simulações para cadeia de tamanho {chain_size}, com tokens inciiais: a1={initial_aminoacids} e m0={initial_mrna}')
    
    num_simulations=initial_aminoacids
    places_dict={"a1":initial_aminoacids,"p":0}
    for i in range(chain_size):
        if i==0:
            places_dict['m'+str(i)]=initial_mrna
        else:
            places_dict['m'+str(i)]=0


    pn=pnet.PNet(places_dict)


    for i in range(chain_size):
        if i<chain_size-1:
            pn.add_transition("t"+str(i+1),{"a1":1,'m'+str(i):1},{'m'+str(i+1):1})
        else:
            pn.add_transition("t"+str(i+1),{"a1":1,'m'+str(i):1},{'p':1})

    #print(pn.dict_places)
    #print(pn.transitions_dict)

    results=[]

    for i in range(num_simulations):
        starttime=t.time()
        pn.simulate_petrinet(num_simulations)
        results.append(pn.get_tokens())
        endtime=t.time()
        simulation_time=endtime-starttime
        expected_time=simulation_time*num_simulations
        if i==0:
            print(f'Executou simulação em {simulation_time:.2f}s, tempo total estimado: {expected_time:.2f}')
    #print(results)
    df_results=pl.DataFrame(results)
    return df_results
    


