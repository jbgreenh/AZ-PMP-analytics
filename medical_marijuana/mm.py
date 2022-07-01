import pandas as pd

# for removing the end of a string if it matches trailing
def trim_string(astring, trailing):
    thelen = len(trailing)
    if astring[-thelen:] == trailing:
        return astring[:-thelen]
    return astring