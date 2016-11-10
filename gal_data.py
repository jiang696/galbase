import astropy.io.fits as fits
from astropy.table import Table
import numpy as np

def gal_data(name_in=None, all_=False, tag=None):
    """
    DEFAULTS, DEFINITIONS, AND ERROR HANDLING
    """
    # CHECK THAT WE GOT A NAME
    if (not name_in) and (all_ == False) and (not tag):
        raise ValueError('Need a name to find a galaxy. Returning empty \
                          structure')
                          
    # SET INPUTS TO NUMPY ARRAYS
    name_in = np.array(name_in)
    tag = np.array(tag)
    
    # DIRECTORY FOR THE DATABASE
    data_dir = "gal_data/"
    
    """
    READ THE DATA BASE
    """
    fname = data_dir + "gal_base.fits"
    hdulist = fits.open(fname)
    data = Table(hdulist[1].data)
    hdulist.close()
    n_data = len(data)
    for i in range(n_data):
        data['NAME'][i] = data['NAME'][i].strip(' ')
        data['TAGS'][i] = data['TAGS'][i].strip(' ')
        data['MORPH'][i] = data['MORPH'][i].strip(' ')
    """
    TREAT THE CASE WHERE A SURVEY OR ALL DATA ARE DESIRED
    """
    if all_:
        return data

    if tag:
        keep = np.ones(n_data, dtype=bool)
        for i in range(n_data):
            this_tag = [temp for temp in data['TAGS'][i].split(";")]
            for t in tag:
                if t not in this_tag:
                    keep[i] = False
                    break
        if sum(keep) == 0:
            print('No targets found with that tag combination. Returning an \
                   empty structure.')
        return data[keep]

    """
    TREAT THE CASE OF A NAME OR LIST OF NAMES
    """
    # Build the list of aliases
    aliases = {}
    fname = data_dir + "gal_base_alias.txt"
    f = open(fname)
    f.readline()
    f.readline()
    for line in f:
        s = [temp for temp in line.strip('\n').split(' ')]
        aliases[s[0]] = s[1]

    # Create list for all names
    names = []
    for name in name_in:
        try:
            names.append(aliases[name])
        except KeyError:
            print(name, 'not in current alias list')
    
    # Look up the current data
    keep = np.zeros(n_data, dtype=bool)
    for i in range(n_data):
        if data[i].field('NAME') in names:
            keep[i] = True

    # Return
    return data[keep]