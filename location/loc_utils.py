import numpy as numpy
import random as loc
import pandas as pd

def return_locations(dataframe):
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    loc_dict = {}
    for _ in range(5000):
        loc_num = loc.randint(0,50)
        location = states[loc_num]
        if(location not in  loc_dict.keys()):
            loc_dict[location] = 1
        else:
            loc_dict[location] += 1
    return pd.Series(loc_dict)

print(return_locations(pd.DataFrame()))
