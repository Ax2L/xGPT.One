import hydralit_components as hc
import time

# a dedicated single loader 
with hc.HyLoader('Now doing loading',hc.Loaders.pulse_bars,):
    time.sleep(5)

# for 3 loaders from the standard loader group
with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=[3,0,5]):
    time.sleep(5)

# for 1 (index=5) from the standard loader group
with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=5):
    time.sleep(5)

# for 4 replications of the same loader (index=2) from the standard loader group
with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=[2,2,2,2]):
    time.sleep(5)