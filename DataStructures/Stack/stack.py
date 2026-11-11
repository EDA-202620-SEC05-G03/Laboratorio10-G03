from DataStructures.List import array_list as lt

def new_stack():
    return lt.new_list()

def push(my_stack, element):
    return lt.add_last(my_stack, element)

def pop(my_stack):
    if is_empty(my_stack):
        raise Exception('EmptyStructureError: stack is empty')
    else:
        return lt.remove_last(my_stack)

def is_empty(my_stack):
    return size(my_stack) == 0

def top(my_stack):
    if is_empty(my_stack):        
        raise Exception('EmptyStructureError: stack is empty')
    else:
        return lt.last_element(my_stack)
    
def size(my_stack):
    return lt.size(my_stack)
