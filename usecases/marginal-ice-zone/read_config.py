#! /usr/bin/env python

def read_configfile(*argv):
    import os
    import yaml
    
# Open the config file
######################
    if len(argv)==1:
       if 'config' in argv[0]:
           config_filename=argv[0]  # Given as full config file name
       else:
           config_filename= 'config_MIZ_' + argv[0] + '.yml' # Given as model name        
    elif len(argv)==0:
        config_filename='config_MIZ_default.yml' # Default filename
    else:
        raise RuntimeError("READ_CONFIGFILE can only be called with zero or one argument, not with "+str(len(argv)))
        
    print(config_filename)

    with open('configs/' + config_filename,"r") as ymlfile:
         configs = yaml.load(ymlfile,  Loader=yaml.Loader)
    if len(argv) == 1: configs['dataSource'] = argv[0]
    
# Derived setting variables and sanity checks
###############################################
# a) Read NCAT, do sanity checks and set configs['multiCAT'] flag
# b) Set configs['Lvol'] flag based on whether thickness or volume variable is provided
    
    # Mono-category
    if configs['coordinates']['ncat'] == 1:
        configs['multiCAT']=False
        if configs['variables']['siconc_name']==None:
            raise RuntimeError("IF NCAT is 1, you need to specify 'siconc_name'")
        if configs['variables']['sithick_name']==None and configs['variables']['sivol_name']==None :
            raise RuntimeError("IF NCAT is 1, you need to specify either 'sithick_name' or 'sivol_name'")
        else:
            if configs['variables']['sithick_name']==None:
                configs['Lvol']=True
            else:
                configs['Lvol']=False
    
    # Multi-category
    elif configs['coordinates']['ncat'] > 1:
        configs['multiCAT']=True
        if configs['coordinates']['ncat_name']==None:
            raise RuntimeError("IF NCAT > 1, you have to provide the name of the ice category dimension NCAT_NAME.")
        if configs['variables']['siitdconc_name']==None:
            raise RuntimeError("IF NCAT is >1, you need to specify 'siitdconc_name'")
        if configs['variables']['siitdthick_name']==None and configs['variables']['siitdvol_name']==None :
            raise RuntimeError("IF NCAT is >1, you need to specify either 'siitdthick_name' or 'siitdvol_name'")
        else:
            if configs['variables']['siitdthick_name']==None:
                configs['Lvol']=True
            else:
                configs['Lvol']=False
    
    else:
        raise RuntimeError("NCAT needs to be positive > 0.") 
        
# c) Check output settings
    if configs['output']['filename_automatic']!=True and configs['output']['filename']==None:
        raise RuntimeError("You need to set FILENAME_AUTOMATIC to True if you don't provide an output filename.")
    if configs['output']['output_folder'] == None:
        configs['output']['output_folder']="."  # If no output folder is given, set it to the current working directory
    if not os.path.exists(configs['output']['output_folder']):
       os.makedirs(configs['output']['output_folder'])
        
# d) set ice_filename
  # configs['ice_filename'] = configs['ice_folder'] + '/' + configs['selectdata']['sensor'] \
  #                         + '/obs_' + str(configs['selectdata']['date']) + '.nc'
    
    print("These are the configurations you have chosen:")
    print(configs)
    print()
    
    return configs

#=====================================================================
if __name__ == '__main__':

   configs=read_configfile('ClimateDT')


