class ValueOutOfRange(Exception):
    def __init__(self, name,rng,value):
        self.message = f'{name} = {value} but is expected to be in {rng} range.'
        super().__init__(self.message)

def type_check(variable,types_list):
    checks = [isinstance(variable,o) for o in types_list]
    return any(checks)

def raise_type_error(variable_name,input_type):
    raise TypeError(f'Unrecognised type {input_type} for {variable_name}')