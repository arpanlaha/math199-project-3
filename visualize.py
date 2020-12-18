import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
from scipy.special import comb
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

def get_sequence_lengths():
    sequence_lengths = {"4": [], "5": [], "6": [], "7": []}
    
    for num in range(0, 128):
        seq = []
        for power in range(6, -1, -1):
            if num >= 2 ** power:
                seq.append(1)
                num -= 2 ** power
            else:
                seq.append(0)
    
        win_count = 0
        loss_count = 0
        length = 0

        for game in range(7):
            length += 1
            
            if seq[game] == 1:
                win_count += 1
            else:
                loss_count += 1
                
            if win_count == 4 or loss_count == 4:
                break
                
        sequence_lengths[str(length)].append(seq)
        
    return sequence_lengths
    
sequence_lengths = get_sequence_lengths()      

def expected_length(series, ph, pa):
    expected = 0
    count = 0
    for length in range(4, 8):        
        for seq in sequence_lengths[str(length)]:
            probability = 1
            for game in range(7):
                win = seq[game]
                if win == 1:
                    probability *= ph if series[game] == 1 else pa
                else:                    
                    probability *= (1 - ph) if series[game] == 1 else (1 - pa)
            expected += probability * length
            
    return expected


def gen_grid(series, phs, pas):
    return [[expected_length(series, ph, pa) for pa in pas] for ph in phs]


phs = np.linspace(0, 1, 100)
pas = np.linspace(0, 1, 100)

grid = np.array(gen_grid([1, 1, 0, 0, 1, 0, 1], phs, pas))

for angle in range(0,360,5):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(phs, pas, grid, rstride=1, cstride=1,cmap='viridis', edgecolor='none')

    ax.view_init(30,angle)
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    
#     plt.show()
    filename='images/2-2/' + str(angle)+'.png'
    plt.savefig(filename, dpi=96)
    plt.gca()
    print(angle)
    plt.close()