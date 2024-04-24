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

    def get_tokens(self,places_list=[]):
        if not places_list:
            return self.dict_places
        tokens={}
        for place in places_list:
            tokens[place]=self.dict_places[place]
        return tokens
    
    def get_firing_sequence(self):
        return self.firing_sequence

    def add_transition(self,name:str,consume:dict,produce:dict):
        self.transitions_dict[name]={"consume":consume,"produce":produce}
        self.transition_count[name]=0

    def add_multiple_transitions(self,transition_array):
        for transition in transition_array:
            self.add_transition(transition['name'],transition['consumes'],transition['produces'])

    def step(self,transition_name:str, skip_fireability_check:bool=False):
        
        fire=True
        
        if not skip_fireability_check:
            fire=self.check_fireability(transition_name)[0]

        if fire:
            consume_dict=self.transitions_dict[transition_name]["consume"]
            produce_dict=self.transitions_dict[transition_name]["produce"]
            for consumed_place in consume_dict:
                self.dict_places[consumed_place]-=consume_dict[consumed_place]
            for produced_place in produce_dict:
                self.dict_places[produced_place]+=produce_dict[produced_place]
            self.firing_sequence.append(transition_name)
            self.transition_count[transition_name]+=1
            
    def check_fireability(self,transition_name:str)->tuple[bool,int]:
        consume_dict=self.transitions_dict[transition_name]["consume"]
        mass=1
        counter=0
        for consumed_place in consume_dict:
            if consume_dict[consumed_place]>self.dict_places[consumed_place]:
                return False,0
            mass*=self.dict_places[consumed_place]
            counter+=1
        
        try:
            mass_action=mass**(1/counter)
        except TypeError:
            print(transition_name)
            print(f'mass: {mass}')
            print(f'counter: {counter}')    
        
        return True,mass_action

    def random_valid_step(self):
        valid_transitions=[]
        for transition in self.transitions_dict:
            if self.check_fireability(transition)[0]:
                valid_transitions.append(transition)
        if len(valid_transitions)>0:
            random_transition=rand.choice(valid_transitions)
            self.step(random_transition,True)
        else:
            raise NoMoreValidTransitionsException("No more valid transitions possible")
        
    def random_mass_action_step(self):
        valid_transitions=[]
        sum_mass_action=0
        for transition in self.transitions_dict:
            valid,mass_action=self.check_fireability(transition)
            if valid:
                valid_transitions.append([transition,mass_action])
                sum_mass_action+=mass_action
        if len(valid_transitions)>0:
            uniform_random=rand.rand()
            cumsum_mass=0
            for transition in valid_transitions:
                cumsum_mass+=(transition[1]/sum_mass_action)
                if uniform_random<=cumsum_mass:
                    random_transition=transition[0]
                    break
                    
            self.step(random_transition,True)
        else:
            raise NoMoreValidTransitionsException("No more valid transitions possible")
        
    def simulate_petrinet(self,num_steps:int,law:str='random',handler=False):
        self.reset()
        for i in range(num_steps):
            try:
                if law=='random':
                    self.random_valid_step()
                elif law=='mass_action':
                    self.random_mass_action_step()
                else:
                    raise InvalidLawException('Law parameter must be either "random" or "mass_action".')
                if handler:
                    handler(self,i)
            except NoMoreValidTransitionsException:
                #print(f"No more valid transitions, ending simulation at step: {i}")
                break
    

class NoMoreValidTransitionsException(Exception):
    pass

class InvalidLawException(Exception):
    pass