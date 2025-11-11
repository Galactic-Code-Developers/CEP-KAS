import numpy as np
import matplotlib.pyplot as plt

# Load sample
grid = np.load("sample_cycle1.npy")

# Plot middle slice
plt.figure(figsize=(6,5))
plt.imshow(grid[grid.shape[0]//2, :, :], cmap='RdBu', origin='lower')
plt.colorbar(label='Vorticity')
plt.title('CEP Cycle 1: Middle Z-Slice')
plt.xlabel('Y')
plt.ylabel('X')
plt.tight_layout()
plt.savefig("examples/cep_slice.png", dpi=300)
plt.show()
