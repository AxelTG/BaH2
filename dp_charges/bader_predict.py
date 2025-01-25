from deepmd.infer import DeepDOS
import numpy as np
from ase.io import read,write
#from tqdm.auto import tqdm


################ DECLARATION ##############################
# DP model
model_path = './frozen_model.pb'

#files
traj_path = './dump.lammpstrj'
out_traj = './charge-traj.xyz'
colvar = './COLVAR'


id_to_atomicnumber = { 1 : 56, 2 : 1, 3 : 7 }

every=1 #process traj every X frames
write_traj=True

################# READ TRAJ ###############################
traj = read(traj_path,format = 'lammps-dump-text',index=f'::{every}')

#################### BADER ################################
# import DP model
dp = DeepDOS(model_path)

atypes = np.array(traj[0].get_atomic_numbers()) - 1  #works only in this setup... to be updated for reading other trajectory
for atoms in traj:
    #get parameter
    coord  = atoms.get_positions().reshape(1,len(atoms),3)
    cell   = atoms.get_cell().reshape(1,9)
    #compute bader
    boh,bader = dp.eval(coords=coord,cells=cell,atom_types=atypes,atomic=True)
    atoms.set_array('bader_charges',bader.ravel())
    #fix atom tipe
    if not 'Ba' in atoms.symbols:
        atoms.set_atomic_numbers( [id_to_atomicnumber[j] for j in atoms.get_atomic_numbers() ] )


################ OUTPUT ###################################
# write output trajectory
if write_traj:
    cols = ['symbols','positions','bader_charges']
    write(out_traj,traj,format='extxyz',columns=cols)
    print('TRAJ EXPORTED:',out_traj)

# write output COLVAR
