import os
import re
import time
import subprocess
from opencadd.structure.core import Structure


pdb_cache = {}

def cmdGen(protein_path, out_path, num_poses=4, exhaustiveness=12, flex_protein=None):

    Ligands=[("./data/ADPG.pdbqt"), ("./data/Maltotriose.pdbqt")]
    ligand_resname = "ADP"
    pdbid = re.search(r'/\w+\.', protein_path[:-6]).group(0)[1:-1]
    mutation = protein_path.split('.')[-2]

    if pdbid not in pdb_cache:
        pdb_cache[pdbid] = Structure.from_pdbid(pdbid)
    structure = pdb_cache[pdbid]
        
    ligand = structure.select_atoms(f"resname {ligand_resname}")

    pocket_center = (ligand.positions.max(axis=0) + ligand.positions.min(axis=0))/2
    pocket_size = ligand.positions.max(axis=0) - ligand.positions.min(axis=0) + 30
    
    print('MUTATE {} CHAIN_X {}: pocket center = ({:.8f}, {:.8f}, {:.8f}), pocket size = ({:.8f}, {:.8f})'.format(
        pdbid, mutation, float(pocket_center[0]), float(pocket_center[1]), float(pocket_center[2]), float(pocket_size[0]), float(pocket_size[1])))
    
    
    return ['./bin/vina_1.2.5_mac_x86_64',
            '--receptor', protein_path,
            '--ligand', str(Ligands[0]), str(Ligands[1]),
            '--center_x', str(pocket_center[0]),
            '--center_y', str(pocket_center[1]),
            '--center_z', str(pocket_center[2]),
            '--size_x', str(pocket_size[0]),
            '--size_y', str(pocket_size[1]),
            '--size_z', str(pocket_size[2]),
            '--out', str(out_path),
            '--verbosity', '2',
            '--cpu', '4',
            '--num_modes', str(num_poses),
            '--exhaustiveness', str(exhaustiveness)
    ]


#Mutations = ['2qzs.305_T', '2qzs.305_Y'] #, '2qzs.305_N', '2qzs.305_Q', '2qzs.305_D', '2qzs.305_E', '2qzs.305_R', '2qzs.305_H'

def main(Mutations = ['2qzs.18E.12_A', '2qzs.18E.12_G']):

    cmds = [cmdGen(protein_path='./data/{}/{}.pdbqt'.format(m, m), out_path='./data/{}/docking_{}.pdbqt'.format(m, m)) for m in Mutations]

    start = time.time()   
    procs, outs = [], []
    for i in range(len(cmds)):
        print('Create process with args: {}'.format(cmds[i]))
        f = open('./data/{}/docking_{}.log'.format(Mutations[i], Mutations[i]), 'w')
        p = subprocess.Popen(cmds[i], stdout=f, stderr=subprocess.STDOUT, text=True)
        procs.append(p)
        outs.append(f)

    print('{} subprocesses created to dock the mutations'.format(len(Mutations)))
        
    for p in procs: p.communicate()
    end = time.time()
    
    for o in outs: o.close()
    
    print('{} pdbqt files docked in {:.1f} minutes'.format(len(Mutations), (end-start)/60))
    
if __name__ == '__main__':

    if os.getcwd().split('/')[-1] == 'bio': os.chdir('./pe106')
    print('Working directory: {}'.format(os.getcwd()))

    main()