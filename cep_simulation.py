# CEP 3D String Network Simulation - Python/NumPy
# Author: Antonios Valamontes, Kapodistrian Academy of Science (KAS)
# Date: 11 November 2025
# Description: Simulates the Chirality Echo Protocol (CEP) in a 3D cyclic cosmology framework.
# Phases: Pre-Inflation Foam -> Ekpyrotic Contraction (simplified) -> Big Flash Reset -> Inflation Stretch -> Reheating Oscillations -> Spin Imprint
# Usage: python cep_simulation.py
# Requirements: numpy (tested on Python 3.12)

import numpy as np

def point_to_line_dist(p, a, b):
    """Distance from 3D point p to line segment ab. All inputs as np arrays."""
    ab = b - a
    ap = p - a
    proj = np.dot(ap, ab) / np.dot(ab, ab)
    proj = np.clip(proj, 0, 1)
    closest = a + proj * ab
    return np.linalg.norm(p - closest)

def generate_vorticity_grid(size=20, num_strings=50, delta_chi=1e-8, sigma=1.0):
    """Phase 1: Pre-Inflation Foam - Biased topological loops as Gaussian vorticity blobs along random string segments."""
    grid = np.zeros((size, size, size))
    bias = 0.5 + delta_chi / 2
    for _ in range(num_strings):
        # Random string segment endpoints in 3D (as np arrays)
        x1 = np.array([np.random.uniform(0, size), np.random.uniform(0, size), np.random.uniform(0, size)])
        x2 = np.array([np.random.uniform(0, size), np.random.uniform(0, size), np.random.uniform(0, size)])
        # Handedness: biased towards right (+1)
        chi = 1 if np.random.rand() < bias else -1
        # Rasterize: sample points along line and add Gaussian kernel
        num_points = 10  # Samples along segment
        for t in np.linspace(0, 1, num_points):
            center = x1 + t * (x2 - x1)
            for i in range(max(0, int(center[0]-3*sigma)), min(size, int(center[0]+3*sigma+1))):
                for j in range(max(0, int(center[1]-3*sigma)), min(size, int(center[1]+3*sigma+1))):
                    for k in range(max(0, int(center[2]-3*sigma)), min(size, int(center[2]+3*sigma+1))):
                        p = np.array([i, j, k])
                        dist = point_to_line_dist(p, x1, x2)
                        if dist < 3 * sigma:
                            grid[i, j, k] += chi * np.exp(-dist**2 / (2 * sigma**2))
    return grid

def inflation_stretch(grid, stretch_factor=4, dilution_power=3):
    """Phase 3: Inflationary Stretch - Nearest-neighbor interp + 1/a^power dilution."""
    old_size = grid.shape[0]
    new_size = old_size * stretch_factor
    new_grid = np.zeros((new_size, new_size, new_size))
    scale = new_size / old_size
    dilution = 1.0 / (stretch_factor ** dilution_power)
    for i in range(new_size):
        old_i = int(i / scale)
        for j in range(new_size):
            old_j = int(j / scale)
            for k in range(new_size):
                old_k = int(k / scale)
                new_grid[i, j, k] = grid[old_i, old_j, old_k] * dilution
    return new_grid

def reheating_oscillations(grid, num_steps=50, epsilon=0.01, omega=0.2 * np.pi, delta_chi=1e-8):
    """Phase 4: Reheating Resonance - Parametric amplification + small chiral injection."""
    size = grid.shape[0]
    for step in range(num_steps):
        t = step * 0.1  # Time step
        amp = 1 + epsilon * np.cos(omega * t)
        # Chiral injection
        inj = delta_chi * np.sin(omega * t) * np.random.normal(size=grid.shape)
        grid *= amp
        grid += inj
    return grid

def compute_lambda(net_L, volume):
    """Proxy spin parameter λ ~ (net_L / volume)^{1/3} scaled to galactic values (~0.04)."""
    return (abs(net_L) / volume) ** (1/3) * 0.04  # Approximate growth factor included

# Mock rotation curve peak velocity (simplified: scaled from λ to MW-like)
def compute_v_peak(lamb):
    """v_peak ≈ 220 km/s * (λ / 0.04) for M=10^12 Msun, r=10 kpc."""
    return 220 * (lamb / 0.04)

# Main: Run One Cycle
def run_one_cycle():
    # Phase 1: Foam
    grid = generate_vorticity_grid()
    net_L_pre = np.sum(grid)
    
    # Phase 2: Ekpyrotic Contraction (simplified: preserve for demo)
    
    # Phase 3: Big Flash Reset (inject delta_chi)
    grid += 1e-8 * np.random.normal(size=grid.shape)
    
    # Phase 4: Inflation
    grid = inflation_stretch(grid)
    net_L_post_infl = np.sum(grid)
    
    # Phase 5: Reheating
    grid = reheating_oscillations(grid)
    net_L_post_reheat = np.sum(grid)
    
    # Phase 6: Proxies
    volume = np.prod(grid.shape)
    lambda_val = compute_lambda(net_L_post_reheat, volume)
    v_peak = compute_v_peak(lambda_val)
    
    return {
        'net_L_pre': net_L_pre,
        'net_L_post_infl': net_L_post_infl,
        'net_L_post_reheat': net_L_post_reheat,
        'lambda': lambda_val,
        'v_peak': v_peak,
        'helicity': '+' if net_L_post_reheat > 0 else '-'
    }

# Run 5 Cycles (as in simulation)
if __name__ == "__main__":
    cycles = []
    for c in range(5):
        result = run_one_cycle()
        cycles.append(result)
        print(f"Cycle {c+1}: λ={result['lambda']:.4f}, v_peak={result['v_peak']:.0f} km/s, Helicity={result['helicity']}, Net L={result['net_L_post_reheat']:.1f}")
    
    # Stats
    lambdas = [r['lambda'] for r in cycles]
    mean_lambda = np.mean(lambdas)
    std_lambda = np.std(lambdas)
    print(f"\nMean λ = {mean_lambda:.4f} ± {std_lambda:.4f}")
    print("\nFor full visualization, add matplotlib plots (e.g., slices of grid).")
    print("GitHub Repo Structure Suggestion:")
    print("- README.md: Full description, run instructions")
    print("- requirements.txt: numpy")
    print("- examples/: Sample outputs as .npy")
