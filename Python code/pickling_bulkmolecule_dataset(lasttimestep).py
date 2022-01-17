import os
import pickle
from wholecell.io.tablereader import TableReader
import pandas as pd
import time

start = time.perf_counter()
df = pd.DataFrame(columns=['cell_path', 'bulk_molecules'])
sim_dir = '/newhome/ao19463/wholecell3/wcEcoli/out/20211123.165421__WCEColi_100_single_gens17./wildtype_000000/'
simulations = os.listdir(sim_dir)
simulations = [x for x in simulations if  x.startswith('00')]
cell_paths = []
bulk_molecules = []
for sim in simulations:
    generation_dir = os.listdir(sim_dir+sim)
    generation_dir = [x for x in generation_dir if x.startswith('gen')]
    for gen in generation_dir:
        for cell in os.listdir(sim_dir+sim+'/'+gen):
            dir = sim_dir+sim+'/'+gen+'/'+cell+'/simOut/'
            if len(os.listdir(dir))>0:
                bulk = TableReader(os.path.join(dir, 'BulkMolecules'))
                col = "counts"
                cols_array_elements = bulk.readColumn(col)
                #take the element from the last time step for each bulk molecule, we wil have one element/example for each of the 5674 bulk molecules
                cols_array_elements = cols_array_elements[len(cols_array_elements)-1][:]
                cell_paths.append(sim+'/'+gen+'/'+cell)
                bulk_molecules.append(cols_array_elements)


df['cell_path'] = cell_paths
df['bulk_molecules'] = bulk_molecules
df.to_pickle('/newhome/ao19463/wholecell3/wcEcoli/out/Wildtype_datasets/Wildtype24.pkl')

end = time.perf_counter()
print(f"Processed the algorithm in {start-end:0.4f} seconds")