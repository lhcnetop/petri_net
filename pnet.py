import numpy as np
import copy

rand=np.random

class PNet:
    def __init__(self,dict_places:dict):
        self.initial_dict_places=copy.deepcopy(dict_places)
        self.transitions_dict={}
        self.reset()
#        self._initialize_arrays()
        
    
    def reset(self):
        self.firing_sequence=[]
        self.dict_places=copy.deepcopy(self.initial_dict_places)
        self.transition_count={}
        for transition in self.transitions_dict:
            self.transition_count[transition]=0

    def _initialize_arrays(self):
        self.places=[]
        self.initial_tokens=np.zeros(len(self.dict_places))
        
        j=0
        for i in self.dict_places:
            self.initial_tokens[j]=self.dict_places[i]
            self.places.append(i)
            j+=1

    def get_tokens(self):
        return self.dict_places
    
    def get_firing_sequence(self):
        return self.firing_sequence

    def add_transition(self,name:str,consume:dict,produce:dict):
        self.transitions_dict[name]={"consume":consume,"produce":produce}
        self.transition_count[name]=0
        


    def step(self,transition_name:str, skip_fireability_check:bool=False):
        
        fire=True
        
        if not skip_fireability_check:
            fire=self.check_fireability(transition_name)

        if fire:
            consume_dict=self.transitions_dict[transition_name]["consume"]
            produce_dict=self.transitions_dict[transition_name]["produce"]
            for consumed_place in consume_dict:
                self.dict_places[consumed_place]-=consume_dict[consumed_place]
            for produced_place in produce_dict:
                self.dict_places[produced_place]+=produce_dict[produced_place]
            self.firing_sequence.append(transition_name)
            self.transition_count[transition_name]+=1
            
    def check_fireability(self,transition_name:str)->bool:
        consume_dict=self.transitions_dict[transition_name]["consume"]
        for consumed_place in consume_dict:
            if consume_dict[consumed_place]>self.dict_places[consumed_place]:
                return False
        return True

    def random_valid_step(self):
        valid_transitions=[]
        for transition in self.transitions_dict:
            if self.check_fireability(transition):
                valid_transitions.append(transition)
        if len(valid_transitions)>0:
            random_transition=rand.choice(valid_transitions)
            self.step(random_transition,True)
        else:
            raise NoMoreValidTransitionsException("No more valid transitions possible")
        
    def simulate_petrinet(self,num_steps:int):
        self.reset()
        for i in range(num_steps):
            try:
                self.random_valid_step()
            except NoMoreValidTransitionsException:
                #print(f"No more valid transitions, ending simulation at step: {i}")
                break
    

class NoMoreValidTransitionsException(Exception):
    pass