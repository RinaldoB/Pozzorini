from __future__ import division
from IPython.core.display import display, HTML
import numpy as np
from hashlib import md5


def OU_current(T, I_0,sigma, tau, sampling_freq=20000.):
    '''
    T : gives the simulation time in seconds
    other parameters as in Pozzorini et al 2015
    TODO: write docstring (params, etc)
    '''
    DeltaT = 1/sampling_freq
    
    def DeltaI(I):
        return (I_0-I)*DeltaT/tau + np.sqrt(2*sigma**2*DeltaT/tau)*np.random.randn()
    
    I = np.zeros(int(T/DeltaT))
    I[0] = I_0 #set the initial value to the mean input
    
    for i in xrange(1,len(I)):
        I[i] = I[i-1] + DeltaI(I[i-1])
        
    return I


# Export stimulation current to TPL file (patchmaster)
# >Template Files for stimulation can be used in Voltage Clamp and in Current Clamp mode. In Current Clamp
# mode, the stimulation data is defined in volts, where 1 mV corresponds with 1 pA current injection.
# Example: A value of 0.1 would result in a current injection of 100 pA. 


def save_stim(T, I_0,sigma, tau, sampling_freq=20000.):

    I = OU_current(T, I_0,sigma, tau, sampling_freq=20000.) #in pA

    #get the command voltage () 
    I_mV = 1e-3*I            #convert the current in pA to mV
    I_mV = I_mV.astype('f4') #4 byte float format
    
    filedir  = 'stim_files/'
    filename = 'I_noise_I0_{}pA_sigma_{}pA_T{}s.'.format(I_0,sigma,T)
    filename += md5(I_mV).hexdigest()
    filename += '.tpl'
    
    # store the values in pA to a binary file
    I_mV.tofile(filedir+filename)
    
    display(HTML(
            'File <a href="{}" target="_blank">{}</a> saved! <BR>Click to download'.format(
                filedir+filename, filename)
            ))
    return I

def TestPlot():
    T=1; dt = 1/20000.
    I = OU_current(T=1, I_0=10, sigma=2, DeltaT=dt)
    plt.plot(np.linspace(0,T,1/dt),I)
    print 'Mean Current:', I.mean(), 'mV','Standard Deviaton:' , I.std(),'mV' #okay