"# SIMPLE-in-Lid-Driven-Cavity" 
Code to solve Navier Stokes Equation in lid driven cavity domain. 
Currently employs FOU (First order Upwind) Formulation at Re 400. 
Should be Validated to result obtained by Ghia et.al (1982)

This code using Semi implicit method for Pressure Linked Equation Aka SIMPLE
# 2D Incompressible Navier-Stokes Solver (Lid-Driven Cavity)
### Implementation of the SIMPLE Algorithm on a Staggered Grid



## Project Description
This repository contains a Python implementation of a 2D Navier-Stokes solver for the Lid-Driven Cavity problem. The solver is built from the ground up to demonstrate a deep understanding of computational fluid dynamics (CFD) fundamentals, specifically focusing on pressure-velocity coupling in incompressible flows.

## Technical Specifications
* **Algorithm:** SIMPLE (Semi-Implicit Method for Pressure-Linked Equations).
* **Discretization:** Finite Volume Method (FVM) on a **Staggered MAC Grid**.
* **Advection Scheme:** First-Order Upwind (FOU) for robust numerical stability.
* **Reynolds Number:** 400 (Standard validation case).
* **Matrix Solver:** Direct Linear Solver using NumPy’s `linalg.solve` for dense system matrices.



## Mathematical Formulation
The solver handles the steady-state incompressible Navier-Stokes equations:

$$(\mathbf{u} \cdot \nabla) \mathbf{u} = -\frac{1}{\rho} \nabla p + \nu \nabla^2 \mathbf{u}$$
$$\nabla \cdot \mathbf{u} = 0$$

### Numerical Implementation Details:
1. **Staggered Grid:** Velocity components ($u, v$) are stored at cell faces, while pressure ($p$) is stored at cell centers to avoid the checkerboard pressure decoupling.
2. **Momentum Predictor:** An intermediate velocity field is calculated by solving the momentum equations with the existing pressure field.
3. **Pressure Correction:** A Pressure Poisson Equation is formulated based on the continuity equation to correct the predicted velocity field.
4. **Under-Relaxation:** Applied to both velocity and pressure updates to ensure convergence and prevent divergence during the iteration process.



## Result
The simulation is considered converged when the L2-norm of the mass residual (continuity equation) falls below $10^{-6}$. At $Re=400$, the solver accurately captures the primary vortex center and the characteristic velocity profiles across the cavity mid-sections.

<img width="1978" height="590" alt="image" src="https://github.com/user-attachments/assets/2dc0c9f8-cc0c-447a-b5cc-236fc686ea36" />
<img width="1474" height="590" alt="image" src="https://github.com/user-attachments/assets/8b676c54-0e76-4011-bc0c-8640747be44a" />


## Mesh

<img width="1601" height="857" alt="image" src="https://github.com/user-attachments/assets/06e57b66-667e-48b6-9c71-abb69729369d" />

