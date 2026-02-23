import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=4, suppress=True)

L_0 = 0.0
L_f = 1.0
dx = 0.015
rho = 1.225
mu = 1.8e-5
Area = 1
Re = 400
ulid = Re * mu / (rho * (L_f - L_0))

#staggered grid for pressure
def cavity_mesh_pressure(dx):
    x = np.arange(L_0 + dx/2, L_f, dx)
    y = np.arange(L_0 + dx/2, L_f, dx)
    X, Y = np.meshgrid(x, y)
    return X, Y

#staggered grid for velocity 
def cavity_mesh_velocity_v(dx):
    x = np.arange(L_0 + dx/2, L_f + dx/2, dx)
    y = np.arange(L_0, L_f + dx/2, dx)
    X, Y = np.meshgrid(x, y)
    return X, Y

def cavity_mesh_velocity_u(dx):
    x = np.arange(L_0, L_f + dx/2, dx)
    y = np.arange(L_0 + dx/2, L_f + dx/2, dx)
    X, Y = np.meshgrid(x, y)
    return X, Y

X, Y = cavity_mesh_pressure(dx)
X_vel_v, Y_vel_v = cavity_mesh_velocity_v(dx)
X_vel_u, Y_vel_u = cavity_mesh_velocity_u(dx)

def init_velocity_pressure(X, X_vel_u, X_vel_v):

    P = np.zeros_like(X)
    
    # Velocity U (Horizontal)
    U = np.zeros_like(X_vel_u)
    
    # Velocity V (Vertical)
    V = np.zeros_like(X_vel_v)
    
    return U, V, P

U, V, P = init_velocity_pressure(X, X_vel_u, X_vel_v)


# Pengecekan shape biar tenang
print(f"Shape P: {P.shape}")   # Harusnya sesuai P-grid
print(f"Shape U: {U.shape}")   # Harusnya (ny, nx+1)
print(f"Shape V: {V.shape}")   # Harusnya (ny+1, nx)


plt.figure(figsize=(6,6))
#plt.scatter(X, Y, s=10, label='Pressure nodes')
plt.scatter(X_vel_v, Y_vel_v, s=30, label='Velocity nodes', marker='x')
plt.scatter(X_vel_u, Y_vel_u, s=30, label='Velocity nodes', marker='x')
# ticks setiap dx
ticks = np.arange(L_0, L_f + dx, dx)
plt.xticks(ticks)
plt.yticks(ticks)

plt.grid(True)
plt.gca().set_aspect('equal')
plt.xlim(L_0 - 0.1*dx, L_f + 0.1*dx)
plt.ylim(L_0 - 0.1*dx, L_f + 0.1*dx)

plt.title(f'Lid-Driven Cavity Mesh (dx={dx})')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()

#Fe,Fw,Fn,Fs Definition x-momentum
Feux_points = (X_vel_u[:,2:] + X_vel_u[:,1:-1])/2
Fwux_points = (X_vel_u[:,:-2] + X_vel_u[:,1:-1])/2

Fnux_points = (X_vel_v[1:,1:] + X_vel_v[1:,:-1])/2 
Fsux_points = (X_vel_v[:-1,1:] + X_vel_v[:-1,:-1])/2
#y counterparts definition x-momentum
Feuy_points = (Y_vel_u[:,2:] + Y_vel_u[:,1:-1])/2
Fwuy_points = (Y_vel_u[:,:-2] + Y_vel_u[:,1:-1])/2

Fnuy_points = (Y_vel_v[1:,1:] + Y_vel_v[1:,:-1])/2 
Fsuy_points = (Y_vel_v[:-1,1:] + Y_vel_v[:-1,:-1])/2

#Center Control Volume
Fcux = (Feux_points + Fwux_points)/2
Fcuy = (Fnuy_points + Fsuy_points)/2

#pressure gradient x
Peux_point = X[:,1:]
Pwux_point = X[:,:-1]
Peuy_point = Y[:,1:]
Pwuy_point = Y[:,:-1]

#Fe,Fw,Fn,Fs Definition y-momentum
Fevx_points = (X_vel_u[1:,1:] + X_vel_u[:-1,1:])/2
Fwvx_points = (X_vel_u[1:,:-1] + X_vel_u[:-1,:-1])/2

Fnvx_points = (X_vel_v[2:,:] + X_vel_v[1:-1,:])/2
Fsvx_points = (X_vel_v[:-2,:] + X_vel_v[1:-1,:])/2
#y counterparts
Fevy_points = (Y_vel_u[1:,1:] + Y_vel_u[:-1,1:])/2
Fwvy_points = (Y_vel_u[1:,:-1] + Y_vel_u[:-1,:-1])/2

Fnvy_points = (Y_vel_v[2:,:] + Y_vel_v[1:-1,:])/2
Fsvy_points = (Y_vel_v[:-2,:] + Y_vel_v[1:-1,:])/2

#Center Control Volume
Fcvx = (Fevx_points + Fwvx_points)/2
Fcvy = (Fnvy_points + Fsvy_points)/2

#pressure gradient y
Pvnx_point = X[1:,:]
Pvsx_point = X[:-1,:]
Pvny_point = Y[1:,:]
Pvsy_point = Y[:-1,:]


fig, ax = plt.subplots(1, 2, figsize=(20, 9))

# 1. Background Grid (Velocity nodes as base reference)
ax[0].scatter(X_vel_u, Y_vel_u, c='lightgray', s=10, label='U-grid base', alpha=0.5)

# 2. Muka Sel (Faces)
ax[0].scatter(Feux_points, Feuy_points, marker='|', c='black', s=40, label='Faces E/W (U-CV)')
ax[0].scatter(Fwux_points, Fwuy_points, marker='|', c='black', s=40)
ax[0].scatter(Fnux_points, Fnuy_points, marker='_', c='blue', s=40, label='Faces N/S (U-CV)')
ax[0].scatter(Fsux_points, Fsuy_points, marker='_', c='blue', s=40)

# 3. Pressure Points (Pe, Pw)
ax[0].scatter(Pwux_point, Pwuy_point, marker='o', s=30, label='Pw Node')
ax[0].scatter(Peux_point, Peuy_point, marker='o', s=30, label='Pe Node')

# 4. Center CV
ax[0].scatter(Fcux, Fcuy, marker='x', c='black', s=25, label='Center (Fcux, Fcuy)')

ax[0].set_title("Visualisasi Kontrol Volume X-Momentum (U)")
ax[0].legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3)
ax[0].grid(True, linestyle=':', alpha=0.6)
ax[0].axis('equal')

# 1. Background Grid (Velocity nodes as base reference)
ax[1].scatter(X_vel_v, Y_vel_v, c='lightgray', s=10, label='V-grid base', alpha=0.5)

# 2. Muka Sel (Faces)
ax[1].scatter(Fevx_points, Fevy_points, marker='|', c='black', s=40, label='Faces E/W (V-CV)')
ax[1].scatter(Fwvx_points, Fwvy_points, marker='|', c='black', s=40)
ax[1].scatter(Fnvx_points, Fnvy_points, marker='_', c='blue', s=40, label='Faces N/S (V-CV)')
ax[1].scatter(Fsvx_points, Fsvy_points, marker='_', c='blue', s=40)

# 3. Pressure Points (Pn, Ps)
ax[1].scatter(Pvsx_point, Pvsy_point, marker='o', s=30, label='Ps Node')
ax[1].scatter(Pvnx_point, Pvny_point, marker='o', s=30, label='Pn Node')

# 4. Center CV
ax[1].scatter(Fcvx, Fcvy, marker='x', c='black', s=25, label='Center (Fcvx, Fcvy)')

ax[1].set_title("Visualisasi Kontrol Volume Y-Momentum (V)")
ax[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3)
ax[1].grid(True, linestyle=':', alpha=0.6)
ax[1].axis('equal')

def check_momentum_integrity():
    
    # u_ref and v_ref is going to be calculated soon
    u_ref = Fcux.shape
    v_ref = Fcvx.shape
    
    print(f"TARGET SHAPE U-Momentum: {u_ref}")
    print(f"TARGET SHAPE V-Momentum: {v_ref}")
    print("="*50)

    # u Momentum
    print("\n[ CHECK DETAIL: U-MOMENTUM ]")
    u_components = {
        "Center (Fcux)": Fcux.shape,
        "East Face (Feux)": Feux_points.shape,
        "West Face (Fwux)": Fwux_points.shape,
        "North Face (Fnux)": Fnux_points.shape,
        "South Face (Fsux)": Fsux_points.shape,
        "Press East (Peux)": Peux_point.shape,
        "Press West (Pwux)": Pwux_point.shape
    }
    
    for name, shp in u_components.items():
        status = "PASS" if shp == u_ref else "!!! ERROR: MISMATCH !!!"
        # str(shp) dulu biar f-string :15 gak ngamuk
        print(f"{name:20}: {str(shp):15} | {status}")

    # v Momentum
    print("\n[ CHECK DETAIL: V-MOMENTUM ]")
    v_components = {
        "Center (Fcvx)": Fcvx.shape,
        "East Face (Fevx)": Fevx_points.shape,
        "West Face (Fwvx)": Fwvx_points.shape,
        "North Face (Fnvx)": Fnvx_points.shape,
        "South Face (Fsvx)": Fsvx_points.shape,
        "Press North (Pvn)": Pvnx_point.shape,
        "Press South (Pvs)": Pvsx_point.shape
    }
    
    for name, shp in v_components.items():
        status = "PASS" if shp == v_ref else "!!! ERROR: MISMATCH !!!"
        print(f"{name:20}: {str(shp):15} | {status}")

    # error mismatch summary
    print("\n" + "="*50)
    if any(s != u_ref for s in u_components.values()):
        print("RESULT: U-component mismatch found!")
        print("Action: Fix the slicing of U faces or Pressure points.")
        
    if any(s != v_ref for s in v_components.values()):
        print("RESULT: V-component mismatch found!")
        print("Action: Fix the slicing of V faces or Pressure points.")
    
    if all(s == u_ref for s in u_components.values()) and all(s == v_ref for s in v_components.values()):
        print("RESULT: All shapes are consistent. Ready to solve!")

check_momentum_integrity()

shape_u = Fcux.shape  
shape_v = Fcvx.shape  

# U momentum
# Faces (Flux points)
u_Fe = np.zeros(shape_u)
u_Fw = np.zeros(shape_u)
u_Fn = np.zeros(shape_u)
u_Fs = np.zeros(shape_u)

# Centers (Internal Coordinates)
u_Ccx = np.zeros(shape_u)
u_Ccy = np.zeros(shape_u)

# Pressure Gradients Points
u_Pe = np.zeros(shape_u)
u_Pw = np.zeros(shape_u)

# V momentum
# Faces (Flux points)
v_Fe = np.zeros(shape_v)
v_Fw = np.zeros(shape_v)
v_Fn = np.zeros(shape_v)
v_Fs = np.zeros(shape_v)

# Centers (Internal Coordinates)
v_Ccx = np.zeros(shape_v)
v_Ccy = np.zeros(shape_v)

# Pressure Gradients Points
v_Pn = np.zeros(shape_v)
v_Ps = np.zeros(shape_v)

#calculate amount of node center
print(f"Jumlah node pusat untuk U-momentum: {shape_u[0] * shape_u[1]}")
print(f"Jumlah node pusat untuk V-momentum: {shape_v[0] * shape_v[1]}")

def init_staggered_variables(Fcux, Fcvx):
    # Get target shapes from reference centers
    shape_u = Fcux.shape  
    shape_v = Fcvx.shape  

    # U momentum
    # Faces (Flux points)
    u_Fe = np.zeros(shape_u)
    u_Fw = np.zeros(shape_u)
    u_Fn = np.zeros(shape_u)
    u_Fs = np.zeros(shape_u)

    # Centers (Internal Coordinates)
    u_Ccx = np.zeros(shape_u)
    u_Ccy = np.zeros(shape_u)

    # Pressure Gradients Points
    u_Pe = np.zeros(shape_u)
    u_Pw = np.zeros(shape_u)

    # V momentum
    # Faces (Flux points)
    v_Fe = np.zeros(shape_v)
    v_Fw = np.zeros(shape_v)
    v_Fn = np.zeros(shape_v)
    v_Fs = np.zeros(shape_v)

    # Centers (Internal Coordinates)
    v_Ccx = np.zeros(shape_v)
    v_Ccy = np.zeros(shape_v)

    # Pressure Gradients Points
    v_Pn = np.zeros(shape_v)
    v_Ps = np.zeros(shape_v)

    return (u_Fe, u_Fw, u_Fn, u_Fs, u_Ccx, u_Ccy, u_Pe, u_Pw,
            v_Fe, v_Fw, v_Fn, v_Fs, v_Ccx, v_Ccy, v_Pn, v_Ps)

# Call the function
(u_Fe, u_Fw, u_Fn, u_Fs, u_Ccx, u_Ccy, u_Pe, u_Pw,
 v_Fe, v_Fw, v_Fn, v_Fs, v_Ccx, v_Ccy, v_Pn, v_Ps) = init_staggered_variables(Fcux, Fcvx)

def update_staggered_fluxes(U, V, P, 
                             u_Fe, u_Fw, u_Fn, u_Fs, u_Pe, u_Pw, u_Cc,
                             v_Fe, v_Fw, v_Fn, v_Fs, v_Pn, v_Ps, v_Cc,
                             p_Cc):
    
    # U-MOMENTUM (X)
    u_Cc[:] = U[:, 1:-1]
    u_Fe[:] = (U[:, 2:] + U[:, 1:-1]) / 2
    u_Fw[:] = (U[:, :-2] + U[:, 1:-1]) / 2
    u_Fn[:] = (V[1:, 1:] + V[1:, :-1]) / 2
    u_Fs[:] = (V[:-1, 1:] + V[:-1, :-1]) / 2
    u_Pe[:] = P[:, 1:]  # right pressure node U
    u_Pw[:] = P[:, :-1] # left pressure node U

    # V-MOMENTUM (Y)
    v_Cc[:] = V[1:-1, :]
    v_Fe[:] = (U[1:, 1:] + U[:-1, 1:]) / 2
    v_Fw[:] = (U[1:, :-1] + U[:-1, :-1]) / 2
    v_Fn[:] = (V[2:, :] + V[1:-1, :]) / 2
    v_Fs[:] = (V[:-2, :] + V[1:-1, :]) / 2
    v_Pn[:] = P[1:, :]  # upper pressure node V
    v_Ps[:] = P[:-1, :] # lower pressure node V

    # -Pressure at center control volume (for continuity equation)
    p_Cc[:] = P[:, :]

# Pressure initialization for continuity equation
p_Cc = np.zeros_like(X) # similiar shape with mesh pressure

#Create matrices for U momentum
ny_u,nx_u = Fcux.shape
N_x = nx_u * ny_u
AU = np.zeros([N_x,N_x])
Source_u = np.zeros(N_x)  

#Create matrices for V momentum
ny_v,nx_v = Fcvx.shape
N_y = nx_v * ny_v
AV = np.zeros([N_y,N_y])
Source_v = np.zeros(N_y)

#create matrices for Pressure 
ny_p,nx_p = X.shape
N_p = nx_p * ny_p
AP = np.zeros([N_p,N_p])
Source_p = np.zeros(N_p)

print(f"Shapes: AP={AP.shape}, AU={AU.shape}, AV={AV.shape}")

# Helper for mapping index 2D ke 1D 
def get_k(i, j, nx):
    return i * nx + j

# loop for U momentum assembly
for i in range(ny_u):       
    for j in range(nx_u):   
        k = get_k(i, j, nx_u)
        
        # 1. Using FOU (First Order Upwind) for convection term
        ae = max(0, -rho * u_Fe[i, j]) + mu / dx  
        aw = max(0,  rho * u_Fw[i, j]) + mu / dx
        an = max(0, -rho * u_Fn[i, j]) + mu / dx
        as_ = max(0, rho * u_Fs[i, j]) + mu / dx
        
        # 2. Off-Diagonal
        if j < nx_u - 1: AU[k, k+1] = -ae  
        if j > 0:        AU[k, k-1] = -aw  
        if i < ny_u - 1: AU[k, k+nx_u] = -an  
        if i > 0:        AU[k, k-nx_u] = -as_ 

        # 3. Boundary Conditions & Diagonal adjustment
        ap_boundary = 0
        
        # Top boundary (Lid-driven)
        if i == ny_u - 1:
            # Suku difusi ke dinding atas: mu * (U_lid - U_p) / (dy/2)
            # dy/2 karena node u sejajar pusat sel P, jarak ke lid adalah setengah sel
            coeff_lid = mu / (dx / 2) # Asumsi dx = dy
            Source_u[k] += coeff_lid * ulid
            ap_boundary += coeff_lid
            # Matikan koefisien utara karena sudah diganti BC Lid
            AU[k, k+nx_u if k+nx_u < N_x else k] = 0 # Safety check

        # bottom boundary (no-slip)
        if i == 0:
            coeff_wall = mu / (dx / 2)
            ap_boundary += coeff_wall
            # Matikan koefisien selatan
            AU[k, k-nx_u if k-nx_u >= 0 else k] = 0

        # --- LEFT & RIGHT (No-slip) ---
        # Untuk j=0 dan j=nx_u-1, aw dan ae tetap ada tapi mengacu ke u=0 di dinding
        # Karena u_wall = 0, kita cukup tambahkan tahanannya ke ap_boundary
        if j == 0:
            ap_boundary += (mu / dx)
        if j == nx_u - 1:
            ap_boundary += (mu / dx)

        # 4. Diagonal (aP)
        # aP = sum(aneighbors) + S_p + ap_boundary
        AU[k, k] = ae + aw + an + as_ + ap_boundary

        #check if ap = 0
        if AU[k, k] == 0:
            print(f"WARNING: aP is zero at index (i={i}, j={j}, k={k}). Check boundary conditions and coefficients.")

#solve for U
U_vector = np.linalg.solve(AU, Source_u)
U_vector = U_vector.reshape(ny_u, nx_u)

U[:, 1:-1] = U_vector  # Masukin hasil solve ke grid utama


# 2. Plotting sederhana buat ngecek
plt.figure(figsize=(7, 6))
plt.contourf(X_vel_u, Y_vel_u, U, cmap='jet', levels=20)
plt.colorbar(label='Velocity U')
plt.title("U-Velocity Profile (Lid-Driven)")
plt.xlabel("x")
plt.ylabel("y")
plt.show()

# --- 1. Loop Assembly buat V-Momentum ---
for i in range(ny_v):       
    for j in range(nx_v):   
        k = get_k(i, j, nx_v)
        
        # Koefisien Neighbor (FOU)
        ae = max(0, -rho * v_Fe[i, j]) + mu / dx  
        aw = max(0,  rho * v_Fw[i, j]) + mu / dx
        an = max(0, -rho * v_Fn[i, j]) + mu / dx
        as_ = max(0, rho * v_Fs[i, j]) + mu / dx
        
        # Off-Diagonal
        if j < nx_v - 1: AV[k, k+1] = -ae  
        if j > 0:        AV[k, k-1] = -aw  
        if i < ny_v - 1: AV[k, k+nx_v] = -an  
        if i > 0:        AV[k, k-nx_v] = -as_ 

        # Boundary Conditions & Diagonal adjustment
        ap_boundary = 0
        
        # Wall Kiri & Kanan (j=0 & j=nx_v-1)
        if j == 0 or j == nx_v - 1:
            coeff_side = mu / (dx / 2)
            ap_boundary += coeff_side
            
        # Wall Atas & Bawah (i=0 & i=ny_v-1)
        # Node V nempel langsung ke wall, jadi jaraknya dx (bukan dx/2)
        if i == 0 or i == ny_v - 1:
            ap_boundary += (mu / dx)

        # Diagonal (aP)
        AV[k, k] = ae + aw + an + as_ + ap_boundary

# Solve & Reshape 
V_vector = np.linalg.solve(AV, Source_v)
V_res = V_vector.reshape(ny_v, nx_v)

# Update grid V utama (Internal nodes)
V[1:-1, :] = V_res

#Plotting U dan V berdampingan
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot U
im1 = ax1.contourf(X_vel_u, Y_vel_u, U, cmap='jet', levels=20)
fig.colorbar(im1, ax=ax1, label='Velocity U')
ax1.set_title("U-Velocity Profile")

# Plot V
im2 = ax2.contourf(X_vel_v, Y_vel_v, V, cmap='coolwarm', levels=20)
fig.colorbar(im2, ax=ax2, label='Velocity V')
ax2.set_title("V-Velocity Profile")

plt.tight_layout()
plt.show()

# 1. Hitung Koefisien Koreksi (d_u dan d_v)
# d_u sejajar dengan U internal, d_v sejajar dengan V internal
# d = Area / aP_momentum
dy = dx  # Asumsi grid seragam, jadi dy = dx
d_u = dy / AU.diagonal().reshape(ny_u, nx_u) 
d_v = dx / AV.diagonal().reshape(ny_v, nx_v)

# 2. Inisialisasi Matriks Pressure Correction
N_p = ny_p * nx_p
AP = np.zeros([N_p, N_p])
Source_p = np.zeros(N_p)

# 3. Assembly Matriks AP dan Source_p (Divergensi)
for i in range(ny_p):
    for j in range(nx_p):
        k = i * nx_p + j
        
        # i konstan untuk U (horizontal), j konstan untuk V (vertikal)
        u_e = U[i, j+1]
        u_w = U[i, j]
        v_n = V[i+1, j]
        v_s = V[i, j]
        
        # Divergensi: Massa netto yang keluar sel
        Source_p[k] = -rho * ((u_e - u_w) * dy + (v_n - v_s) * dx)

        # --- KOEFISIEN NEIGHBOR ---
        # ae (East): P[i, j+1] lewat face U[i, j+1]. Pakai d_u[i, j] 
        # (Asumsi d_u hanya internal, jadi index j-nya menyesuaikan)
        ae = rho * d_u[i, j] * dy if j < nx_p - 1 else 0
        
        # aw (West): P[i, j-1] lewat face U[i, j]. Pakai d_u[i, j-1]
        aw = rho * d_u[i, j-1] * dy if j > 0 else 0
        
        # an (North): P[i+1, j] lewat face V[i+1, j]. Pakai d_v[i, j]
        an = rho * d_v[i, j] * dx if i < ny_p - 1 else 0
        
        # as (South): P[i-1, j] lewat face V[i, j]. Pakai d_v[i-1, j]
        as_ = rho * d_v[i-1, j] * dx if i > 0 else 0

        # --- MATRIKS AP ---
        if j < nx_p - 1: AP[k, k+1] = -ae
        if j > 0:        AP[k, k-1] = -aw
        if i < ny_p - 1: AP[k, k+nx_p] = -an
        if i > 0:        AP[k, k-nx_p] = -as_

        AP[k, k] = ae + aw + an + as_

# 4. Anchor Pressure 
AP[0, :] = 0
AP[0, 0] = 1
Source_p[0] = 0

# 5. Solve & Reshape
P_corr_vector = np.linalg.solve(AP, Source_p)
P_corr = P_corr_vector.reshape(ny_p, nx_p)

# velocity correction
# U internal 
U[:, 1:-1] += d_u * (P_corr[:, :-1] - P_corr[:, 1:])

# V internal 
V[1:-1, :] += d_v * (P_corr[:-1, :] - P_corr[1:, :])

# pressure correction
P += 0.5 * P_corr

#HYPERPARAMETERS & INIT
max_iter = 5000
tolerance = 1e-6
alpha_uv = 0.05 
alpha_p = 0.01
residual_history = []

for iteration in range(max_iter):
    U_old = U.copy()
    V_old = V.copy()

    # reassignment staggered fluxes and pressure gradients
    update_staggered_fluxes(U, V, P, 
                             u_Fe, u_Fw, u_Fn, u_Fs, u_Pe, u_Pw, u_Ccx, # u_Ccx dipake buat simpen U internal
                             v_Fe, v_Fw, v_Fn, v_Fs, v_Pn, v_Ps, v_Ccx, # v_Ccx dipake buat simpen V internal
                             p_Cc)

    # reset AU, AV, Source_u, Source_v before re-assembly
    AU.fill(0)
    AV.fill(0)
    Source_u.fill(0)
    Source_v.fill(0)

    # assembly U momentum
    for i in range(ny_u):
        for j in range(nx_u):
            k = get_k(i, j, nx_u)
            ae = max(0, -rho * u_Fe[i, j]) + mu / dx
            aw = max(0,  rho * u_Fw[i, j]) + mu / dx
            an = max(0, -rho * u_Fn[i, j]) + mu / dx
            as_ = max(0, rho * u_Fs[i, j]) + mu / dx
            
            if j < nx_u - 1: AU[k, k+1] = -ae
            if j > 0:        AU[k, k-1] = -aw
            if i < ny_u - 1: AU[k, k+nx_u] = -an
            if i > 0:        AU[k, k-nx_u] = -as_

            ap_boundary = 0
            if i == ny_u - 1: # Lid
                coeff_lid = mu / (dx / 2)
                Source_u[k] += coeff_lid * ulid
                ap_boundary += coeff_lid
            if i == 0: # Bottom
                ap_boundary += mu / (dx / 2)
            if j == 0 or j == nx_u - 1: # Sides
                ap_boundary += mu / dx

            AU[k, k] = ae + aw + an + as_ + ap_boundary
            # TAMBAHKAN GRADIEN TEKANAN KE SOURCE_U!
            Source_u[k] += (u_Pw[i, j] - u_Pe[i, j]) * dy

    # assembly V-Momentum
    for i in range(ny_v):
        for j in range(nx_v):
            k = get_k(i, j, nx_v)
            ae = max(0, -rho * v_Fe[i, j]) + mu / dx
            aw = max(0,  rho * v_Fw[i, j]) + mu / dx
            an = max(0, -rho * v_Fn[i, j]) + mu / dx
            as_ = max(0, rho * v_Fs[i, j]) + mu / dx

            if j < nx_v - 1: AV[k, k+1] = -ae
            if j > 0:        AV[k, k-1] = -aw
            if i < ny_v - 1: AV[k, k+nx_v] = -an
            if i > 0:        AV[k, k-nx_v] = -as_

            ap_boundary = 0
            if j == 0 or j == nx_v - 1: ap_boundary += mu / (dx / 2)
            if i == 0 or i == ny_v - 1: ap_boundary += mu / dx

            AV[k, k] = ae + aw + an + as_ + ap_boundary
            # TAMBAHKAN GRADIEN TEKANAN KE SOURCE_V!
            Source_v[k] += (v_Ps[i, j] - v_Pn[i, j]) * dx

    # Solve u* and v*
    U_star_vec = np.linalg.solve(AU, Source_u)
    V_star_vec = np.linalg.solve(AV, Source_v)
    
    U[:, 1:-1] = (1 - alpha_uv) * U_old[:, 1:-1] + alpha_uv * U_star_vec.reshape(ny_u, nx_u)
    V[1:-1, :] = (1 - alpha_uv) * V_old[1:-1, :] + alpha_uv * V_star_vec.reshape(ny_v, nx_v)

    # 2. UPDATE PRESSURE CORRECTION (P')
    d_u = dy / AU.diagonal().reshape(ny_u, nx_u)
    d_v = dx / AV.diagonal().reshape(ny_v, nx_v)
    
    AP.fill(0)
    Source_p.fill(0)

    for i in range(ny_p):
        for j in range(nx_p):
            k = i * nx_p + j
            u_e = U[i, j+1]; u_w = U[i, j]
            v_n = V[i+1, j]; v_s = V[i, j]
            Source_p[k] = -rho * ((u_e - u_w) * dy + (v_n - v_s) * dx)

            ae = rho * d_u[i, j] * dy if j < nx_p - 1 else 0
            aw = rho * d_u[i, j-1] * dy if j > 0 else 0
            an = rho * d_v[i, j] * dx if i < ny_p - 1 else 0
            as_ = rho * d_v[i-1, j] * dx if i > 0 else 0

            if j < nx_p - 1: AP[k, k+1] = -ae
            if j > 0:        AP[k, k-1] = -aw
            if i < ny_p - 1: AP[k, k+nx_p] = -an
            if i > 0:        AP[k, k-nx_p] = -as_
            AP[k, k] = ae + aw + an + as_

    AP[0, :] = 0; AP[0, 0] = 1; Source_p[0] = 0
    P_corr_vec = np.linalg.solve(AP, Source_p)
    P_corr = P_corr_vec.reshape(ny_p, nx_p)

    # 3. CORRECT VELOCITY & PRESSURE
    U[:, 1:-1] += d_u * (P_corr[:, :-1] - P_corr[:, 1:])
    V[1:-1, :] += d_v * (P_corr[:-1, :] - P_corr[1:, :])
    P += alpha_p * P_corr

    res = np.sqrt(np.sum(Source_p**2))
    residual_history.append(res)
    if iteration % 10 == 0: print(f"Iter {iteration} -> Residual: {res:.4e}")
    if res < tolerance: break

# 1. Interpolasi Velocity ke Center Cell (P-grid)
U_center = (U[:, :-1] + U[:, 1:]) / 2
V_center = (V[:-1, :] + V[1:, :]) / 2
Vel_Mag = np.sqrt(U_center**2 + V_center**2)

# 2. Setup Plot (1 Baris, 3 Kolom)
fig, ax = plt.subplots(1, 3, figsize=(20, 6))

#U-Velocity (Horizontal)
im1 = ax[0].contourf(X, Y, U_center, levels=50, cmap='RdBu_r')
fig.colorbar(im1, ax=ax[0], label='U (m/s)')
ax[0].set_title(f"U-Velocity Profile (Re={Re})")
ax[0].set_xlabel("X Position")
ax[0].set_ylabel("Y Position")

#V-Velocity (Vertical)
im2 = ax[1].contourf(X, Y, V_center, levels=50, cmap='RdBu_r')
fig.colorbar(im2, ax=ax[1], label='V (m/s)')
ax[1].set_title(f"V-Velocity Profile (Re={Re})")
ax[1].set_xlabel("X Position")

#Velocity Magnitude & Streamlines
im3 = ax[2].contourf(X, Y, Vel_Mag, levels=50, cmap='jet')
fig.colorbar(im3, ax=ax[2], label='Magnitude (m/s)')
ax[2].streamplot(X, Y, U_center, V_center, color='white', density=1.2, linewidth=0.8)
ax[2].set_title(f"Velocity Magnitude & Streamlines")
ax[2].set_xlabel("X Position")

# Finishing touches
for a in ax:
    a.set_aspect('equal')
    a.grid(alpha=0.2)

plt.tight_layout()
plt.show()

# 1. Interpolasi Velocity ke Center Cell (P-grid) untuk plotting
# Karena U dan V staggered, kita rata-ratakan ke posisi P
U_center = (U[:, :-1] + U[:, 1:]) / 2
V_center = (V[:-1, :] + V[1:, :]) / 2

# 2. Setup Plot
fig, ax = plt.subplots(1, 2, figsize=(15, 6))

#Plot 1: Streamline & Pressure Contour
# X dan Y adalah koordinat mesh pressure yang udah lu buat di awal
im1 = ax[0].contourf(X, Y, P, cmap='RdBu_r', levels=50, alpha=0.8)
fig.colorbar(im1, ax=ax[0], label='Pressure (P)')
ax[0].streamplot(X, Y, U_center, V_center, color='black', linewidth=1, density=1.5)
ax[0].set_title("Streamlines and Pressure Distribution")
ax[0].set_xlabel("X")
ax[0].set_ylabel("Y")

#Plot 2: Velocity Magnitude & Vectors 
vel_mag = np.sqrt(U_center**2 + V_center**2)
im2 = ax[1].contourf(X, Y, vel_mag, cmap='viridis', levels=50)
fig.colorbar(im2, ax=ax[1], label='Velocity Magnitude')
# Tampilkan vector (quiver) - kita skip beberapa point biar gak penuh banget
skip = (slice(None, None, 2), slice(None, None, 2))
ax[1].quiver(X[skip], Y[skip], U_center[skip], V_center[skip], color='white', scale=ulid*10)
ax[1].set_title("Velocity Magnitude and Vectors")
ax[1].set_xlabel("X")
ax[1].set_ylabel("Y")

plt.tight_layout()
plt.show()

# --- Plot 3: Residual History ---
plt.figure(figsize=(8, 4))
plt.semilogy(residual_history, label='Mass Residual (Source_p)')
plt.axhline(y=tolerance, color='r', linestyle='--', label='Tolerance')
plt.title("Convergence History")
plt.xlabel("Iteration")
plt.ylabel("Residual (Log Scale)")
plt.legend()
plt.grid(True, which="both", ls="-")
plt.show()