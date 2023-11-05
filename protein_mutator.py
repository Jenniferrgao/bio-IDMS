import os
from sys import stdout
import time
import multiprocessing
from sarge import run
import re

def feed_indel(Mutations):
    
    result = []
    
    for m in Mutations:
        path = "../data/{}".format(m)
        #function mkdir(): sets the access, change, modification, and creation times for the new directory
        if not os.path.exists(path): os.mkdir(path)
        fn = path + '/' + m
        with open(fn, "w") as f:
            f.write("MUTATE CHAIN_X {}\nMUTATE CHAIN_X {}".format(m.split('.')[-2], m.split('.')[-1]))
            f.close()
        result.append(fn)
    
    return result

def indel_marker(_cmd):
    return run(_cmd)

def parallel_maker(Mutations):
  
    os.chdir('./Protein-InDelMaker')
    print('Switch to working directory {}'.format(os.getcwd()))
    
    inputs = feed_indel(Mutations)
    
    cmds = ['python main.py ../data/{} ../data/{}.pdb ../data/{}/{}'.format(
        m, m.split('.')[0], m, m) for m in Mutations]
    
    procs = []
    for i in range(len(inputs)):
        print('Create process #{} with args: {}'.format(i, cmds[i]))
        p = multiprocessing.Process(target=indel_marker, args=([cmds[i]]))
        p.start()
        procs.append(p)
        
    [p.join() for p in procs]

    os.chdir('../')
    print('{} subprocesses created to calculate the mutation results'.format(len(Mutations)))

#Mutations = ['2qzs.305_T', '2qzs.305_Y', '2qzs.305_N', '2qzs.305_Q', '2qzs.305_D', '2qzs.305_E', '2qzs.305_R', '2qzs.305_H']

def main(Mutations = ['2qzs.18_E.305_T', '2qzs.18_E.305_Y']):
    
    for m in Mutations:

        print(re.match(r'^\w+\.\d+_[A-Z]+\.\d+_[A-Z]+$', m))
        if re.match(r'^\w+\.\d+_[A-Z]+\.\d+_[A-Z]+$', m) == None:
            print('\n\n Illegal augument = {}; complete auguments = {}'.format(m, Mutations))
            print('Please check according to following format ["id:pos_key", ...], example ["2qzs:18_V.305_T", "2qzs:96_R.305_Y"]')
            exit(1)

    start = time.time()
    parallel_maker(Mutations)
    end = time.time()
    
    print('\n\n {} processing completed inside ./data folder within {:.1f} minutes'.format(Mutations, (end-start)/60))
    
if __name__ == '__main__':
    
    if os.getcwd().split('/')[-1] == 'bio': os.chdir('./pe101')
    print('Working directory: {}'.format(os.getcwd()))
    
    main()