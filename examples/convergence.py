# examples/convergence.py
import numpy as np
import matplotlib.pyplot as plt

sizes = [15, 20, 25, 30]
lambdas = []
for s in sizes:
    result = run_one_cycle(size=s)
    lambdas.append(result['lambda'])

plt.plot(sizes, lambdas, 'o-')
plt.axhline(0.0482, color='red', linestyle='--', label='Mean')
plt.xlabel('Grid Size $N$')
plt.ylabel('$\lambda$')
plt.title('Convergence Test')
plt.legend()
plt.savefig('examples/convergence.png', dpi=300)
