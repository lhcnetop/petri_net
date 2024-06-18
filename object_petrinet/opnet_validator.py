from jsonschema import validate as jsonschemavalidate
import json
import os.path as path

class OPNetValidator():
    def __init__(self):
        pass
    
    @classmethod
    def validate_schema(cls, json_object_to_validate:dict):
        pnet_json_schema_path=path.join('.','object_petrinet','opnet_schema.json')
        with open(pnet_json_schema_path,'r') as pnet_json_schema_path:
            pnet_json_schema=json.load(pnet_json_schema_path)
            jsonschemavalidate(json_object_to_validate,schema=pnet_json_schema)

    '''
    Validate that the transitions reference only places declared in their own networks
    '''
    @classmethod
    def validate_integrity(cls, opnet_def:dict):
        for pnet in opnet_def:
            pnet_places=opnet_def[pnet]['places']
            pnet_transitions=opnet_def[pnet]['transitions']
            helpful_error_strings=[]
            for transition_key in pnet_transitions:
                transition=pnet_transitions[transition_key]
                for consumed_place in transition['consume']:
                    if consumed_place not in pnet_places:
                        helpful_error_strings.append(f'Consumed place {consumed_place} in transition {transition_key} not declared in PNet {pnet}') 
                for produced_place in transition['produce']:
                    if produced_place not in pnet_places:
                        helpful_error_strings.append(f'Produced place {produced_place} in transition {transition_key} not declared in PNet {pnet}')            
            if len(helpful_error_strings)>0:
                raise UnknownPlaceException('\n'+'\n'.join(helpful_error_strings))

class UnknownPlaceException(Exception):
    pass
