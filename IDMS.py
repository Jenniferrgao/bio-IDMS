import protein_mutator as mutator
import pdb2pdbqt as pdb2pdbqt
import dock as dock
import os
from itertools import product

AminoAcidList = ['G', 'A']#, 'V', 'L', 'I', 'M', 'W', 'F', 'S', 'T', 'Y', 'N', 'Q', 'D', 'E', 'K', 'R', 'H']
PositionList = ['12','21']#,'96','139','298','299','331','354','356']
Mutations = []

def random_mutation(AminoAcidList, PositionList):
    return ["2qzs.18_E.{}_{}".format(x, y) for x, y in product(PositionList, AminoAcidList)]

def main():
    mutaionCollection = random_mutation(AminoAcidList, PositionList)
    
    print(mutaionCollection)
    
    for i in range(int(len(mutaionCollection) / 2)):
        print(i)
        Mutations.append(mutaionCollection[(i * 2):(i * 2 + 2)])
        print(Mutations[i])
        # Mutator step
        mutator.main(Mutations[i])
        # pdb2pdbqt step
        pdb2pdbqt.main(Mutations[i])
        # Docking step
        dock.main(Mutations[i])


    # Mutator step
    #mutator.main(Mutations)

    # pdb2pdbqt step
    #pdb2pdbqt.main(Mutations)

    # Docking step
    #dock.main(Mutations)


if __name__ == '__main__':

    if os.getcwd().split('/')[-1] == 'bio': os.chdir('./pe106')
    print('Working directory: {}'.format(os.getcwd()))

    main()