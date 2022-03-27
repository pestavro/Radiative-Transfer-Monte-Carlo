import random
import math
# import numpy as np
import matplotlib.pyplot as plt

absorption = 0 # Absorption flag

def density(r): # Medium number density formula
    
    n_c = 9.559e25 # Estimate for the number density in the Sun's center [cm^-3]
    R = 6.9634e10 # Solar radius [cm]
    
    n = n_c*(1-r/R) # Approximate photosphere density with a linearly decreasing function
    
    mean = 2.839e56/R**3 # Mean number density [cm^-3]
    
    return n
    # return mean
    # return 8.96e16 # Value for photosphere number density taken from literature [cm^-3]
    
def s_cross_sec(): # Scattering cross section
    
    return 6.6e-25

def a_cross_sec(): # Absorption cross section
    
    return 6.6e-28

def abs_prob(r, x): # Probability to absorb a photon at radius r after it has traveled a distance x
    
    alpha = a_cross_sec()*density(r)
    
    prob = 1 - math.exp(-alpha*x)
    
    return prob

def opt_depth(): # Randomly generated optical depth
    
    r = random.uniform(0,1)

    tau = -math.log(1-r)
    
    return tau

def length(r, tau): # Function that determines the path length (in cm) of a single photon in a medium

    step = tau/(density(r)*s_cross_sec())/100
    
    tau_s = [0]
    
    i = 0
    
    while tau_s[i] < tau:

        tau_s.append(tau_s[i] + (density(r + (i+1)*step)*s_cross_sec() + density(r + i*step)*s_cross_sec())*step/2)
        
        i += 1
        
        # print(i-1, "----", tau_s[i])
    
    dx = (tau-tau_s[-2])/(tau_s[-1]-tau_s[-2]) # Linear interpolation for more accurate length
            
    return (i-2 + dx)*step

def direction(): # Function that randomly generates a direction on the unit sphere
    
    r1 = random.uniform(0,1)    
    r2 = random.uniform(0,1)
    
    phi = 2*math.pi*r1 # Azimuthal angle  
    theta = math.pi*r2 # Polar angle
    
    ux = math.sin(theta)*math.cos(phi)
    uy = math.sin(theta)*math.sin(phi)
    uz = math.cos(theta)
    
    return [ux, uy, uz]

def scatter(r0, u0, ax, n_scatter, i_photon): # Function that plots scattering path for ONE photon
    
    # Define arrays that will contain the scattering x,y,z positions
    
    xpoints = []
    ypoints = []
    zpoints = []
    radius = []
    distance = 0
    absorb_prob = []
    
    # Add initial x,y,z position of the photon
    
    radius.append(r0)
    u = u0
    
    xpoints.append(radius[0]*u[0])
    ypoints.append(radius[0]*u[1])
    zpoints.append(radius[0]*u[2])
    
    ## print("\n****** Start position ******", "\nx =", xpoints[0], ", y =", ypoints[0], ", z =", zpoints[0], "\nr =", radius[0])

    for i in range(1,n_scatter+2): # Begin loop on multiple scatterings
       
        d = direction() # Assign a random direction to determine the scattering direction
                        # New random direction each time direction() is called
    
        L = length(radius[i-1], opt_depth()) # Determine length the photon will travel after scattering
                                             # New random optical depth (tau) each time length() is called
        
        xpoints.append(xpoints[i-1] + L*d[0]) # x position of i-th scattering
        ypoints.append(ypoints[i-1] + L*d[1]) # y position of i-th scattering
        zpoints.append(zpoints[i-1] + L*d[2]) # z position of i-th scattering
        radius.append(math.sqrt(xpoints[i]**2 + ypoints[i]**2 + zpoints[i]**2)) # radial position of i-th scattering
        
        distance += L # Update distance travelled by photon
        
        absorb_prob.append(abs_prob(radius[i], distance)) # Update absorption probability
        
        ## print("\nAbsorption probability after scattering", i-1, "time(s) and having travelled a total distance of", distance, "cm:", absorb_prob[-1])

        # Check if photon is absorbed instead of scattering after i-th scattering.
        
        if absorption == 1:
            
            if random.uniform(0, 1) <= absorb_prob[-1]:
            
                ## print("\nPhoton is absorbed after scattering", i-1, "time(s) and having travelled a total distance of", distance, "cm")
            
                ## print("\n****** Stop position ******", "\nx =", xpoints[i], ", y =", ypoints[i], ", z =", zpoints[i], "\nr =", radius[i])

                ax.plot(xpoints[i], ypoints[i], zpoints[i], marker='o', markersize=4, c=i_photon)
            
                break
        """
        else:
        
            if i!=n_scatter+1:

                print("\n****** Scatter No.", i, "position ******", "\nx =", xpoints[i], ", y =", ypoints[i], ", z =", zpoints[i], "\n r =", radius[i])
            else:
    
                print("\n****** Stop position ******", "\nx =", xpoints[i], ", y =", ypoints[i], ", z =", zpoints[i], "\nr =", radius[i])
        """
        
        if radius[i]>6.9469e10: # Check if still inside the photosphere; if not, break out of the for loop
            
            ## print("\nPhoton found outside the outer spherical bound of the photosphere after", i-1, "scattering(s).")
            
            break
        elif radius[i]<6.9459e10:
            
            ## print("\nPhoton found outside the inner spherical bound of the photosphere after", i-1, "scattering(s).")
            
            break
        
    # 3D plot

    ax.plot(xpoints, ypoints, zpoints, linewidth=0.75, c=i_photon)
    
    return distance

# Main part of the code

# Define a dictionary to use for colors

color = {
    0: "purple",
    1: "black",
    2: "brown",
    3: "red",
    4: "orange",
    5: "gold",
    6: "green",
    7: "cyan",
    8: "blue",
    9: "magenta"
    }

n_photons = int(input("How many photons would you like to scatter? \n"))

n_scatter = int(input("Input maximum no. of scatterings for a photon in the medium: \n"))

# Initial radius and direction of the emitted photons

r_init = 6.9464e10 + 5e6*random.uniform(-1,1) # Photosphere is 100 km thick
u_init = direction()

# Create 3D plot environment

fig1 = plt.figure()
ax1 = fig1.add_subplot(111, projection='3d')
ax1.set(xlabel='x [cm]', ylabel='y [cm]', zlabel='z [cm]')

# Loop on multiple photons

total_dist = []

for i in range(n_photons):
    
    ## print("\n************ Photon No.", i+1, "************\n")    
    
    total_dist.append(scatter(r_init, u_init, ax1, n_scatter, color.get((i+1)%10)))
    
## print("\n************ Total distance traveled in the medium ************")

fig2, ax2 = plt.subplots()
ax2.set(xlabel='Photon Id', ylabel='Distance [cm]', title='Total travel distance')
ax2.grid(True)

for i in range(len(total_dist)):
    
    ax2.scatter(i+1, total_dist[i], c=color.get((i+1)%10))
    ## print("\nPhoton No.", i+1, ":", total_dist[i], "cm")
    
plt.show()
