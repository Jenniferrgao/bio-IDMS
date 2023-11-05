import os
import re
import yaml
import pandas as pd

Mutations = []

# try:
#     with open("config.yml") as c:
#         config = yaml.load(c, Loader=yaml.FullLoader)
#     MutationsList = config['mutations']
# except FileNotFoundError:
#     print('Config file config.yml not found.')
    
# for i in MutationsList:
#     if type(i) is list:
#         for m in i: Mutations.append(m)
#     else:
#         for m in MutationsList: Mutations.append(m)
#         break

dataRoot = './data'
for m in os.listdir(dataRoot):
    if os.path.isdir(os.path.join(dataRoot, m)):
        if re.match(r'^\w+\.\d+_[A-Z]$', m) != None:
            Mutations.append(m)
    
pdb, mutation, log, mode, affinity, dist, best = [], [], [], [], [], [], []

for m in Mutations:
    fn = dataRoot + '/{}/docking_{}.log'.format(m, m)
    if os.path.exists(fn):
        with open(fn, 'r') as f:

            data = f.readline()
            while (data != ''):
                if data.startswith('mode'): 
                    f.readline(), f.readline()
                    break
                data = f.readline()
                continue
            
            while True:
                data = f.readline()
                if data == '': break
                if len(data.split(' ')) < 4: break

                pdb.append(m.split('.')[0])
                mutation.append(m.split('.')[-1])
                log.append(dataRoot + '/{}/docking_{}.log'.format(m, m))
                
                data = [d for d in data[:-1].split(' ') if len(d) > 0]
                mode.append(int(data[0]))
                affinity.append(float(data[1]))
                dist.append(float(data[2]))
                best.append(float(data[3]))

report = pd.DataFrame(
    data=[pdb, mutation, log, mode, affinity, dist, best]).T.rename(
    columns={0:'pdb', 1:'mutation', 2:'log', 3:'mode', 4:'affinity', 5:'dist', 6:'best'}).sort_values(
        by=['affinity'], ascending=True)

print('-'*67)
print('{:>6s} | {:>10s} | {:>6s} | {:>10s} | {:>10s} | {:>10s}'.format('pdb', 'mutation', 'mode', 'affinity', 'dist from', 'best mode'))
print('{:>6s} | {:>10s} | {:>6s} | {:>10s} | {:>10s} | {:>10s}'.format('', '', '', 'kcal/mol', 'rmsd l.b.', 'rmsd u.b.'))
print('-'*7 + '+' + '-'*12 + '+' + '-'*8 + '+' + '-'*12 + '+' + '-'*12 + '+' + '-'*11)
    
for idx in report.index:
    line = report.loc[idx]
    p, mx, l, mode, a, d, b = line['pdb'], line['mutation'], line['log'], line['mode'], line['affinity'], line['dist'], line['best']
    print('{:>6s} | {:>10s} | {:>6d} | {:>10.4f} | {:>10.4f} | {:>10.4f}'.format(p, mx, mode, a, d, b))
    
print('-'*7 + '+' + '-'*12 + '+' + '-'*8 + '+' + '-'*12 + '+' + '-'*12 + '+' + '-'*11)