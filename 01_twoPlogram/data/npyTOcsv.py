from os import listdir,getcwd

import numpy as np
import pandas as pd
from npy_append_array import NpyAppendArray



for file in listdir(getcwd()):
    name,ext = file.split(".")
    if (ext=="npy"):
        data = pd.DataFrame(np.load(file))
        data.to_csv(name+".csv",index=False)
    
        
