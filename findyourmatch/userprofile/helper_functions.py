"""
Helper function to return enum choices
"""
def get_enum_choices(enum_class):
    return [choice.value for choice in enum_class]