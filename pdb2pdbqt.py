import os
import time
# import multiprocessing
import subprocess

def get_latest_pdb(path):
    files = [n for n in os.listdir(path) if n[-3:].lower() == 'pdb']
    files.sort(key=lambda n: os.path.getmtime(path + "/" + n) if not os.path.isdir(path + "/" + n) else 0)
    return path + '/' + files[-1]

#Mutations = ['2qzs.305_T', '2qzs.305_Y', '2qzs.305_N', '2qzs.305_Q', '2qzs.305_D', '2qzs.305_E', '2qzs.305_R', '2qzs.305_H']

def main(Mutations = ['2qzs.18E.12_A', '2qzs.18E.12_G']):

    print('Working directory: {}'.format(os.getcwd()))
    
    cmds = [['python', './utils/prepare_receptor4.py', '-v', '-r', get_latest_pdb('./data/{}'.format(m)), '-o', './data/{}/{}.pdbqt'.format(m, m), '-A', 'checkhydrogens', '-U', 'waters'] for m in Mutations]
    
    start = time.time()   
    procs = []
    for i in range(len(cmds)):
        print('Create process with args: {}'.format(cmds[i]))
        p = subprocess.Popen(cmds[i], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        procs.append(p)

    print('{} subprocesses created to calculate the mutation results'.format(len(Mutations)))
        
    for p in procs: p.communicate()
    end = time.time()

    print('{} pdb files converted in {:.1f} minutes'.format(len(Mutations), (end-start)/60))
    
if __name__ == '__main__':
    
    if os.getcwd().split('/')[-1] == 'bio': os.chdir('./pe106')
    print('Working directory: {}'.format(os.getcwd()))
    
    main()