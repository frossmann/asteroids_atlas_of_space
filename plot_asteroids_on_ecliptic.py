# %%

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pdf
import pandas as pd
from tqdm import tqdm
import cmocean

savename = "all_asteroids.png"
figsize = (9.235, 9.235)
dpi = 300
cmap = cmocean.cm.thermal
labels = dict(
    zip(
        [
            "TJN",
            "GRK",
            "MBA",
            "OMB",
            "MCA",
            "CEN",
            "AMO",
            "AST",
            "TNO",
            "IMB",
            "APO",
            "ATE",
            "IEO",
        ],
        [
            "Trojan",
            "Greek",
            "Main Belt",
            "Outer Main Belt",
            "Mars Crossing",
            "Centaur",
            "Amor",
            "Unclassified",
            "Trans-Neptunian Object",
            "Inner Main Belt",
            "Apollo",
            "Atens",
            "Near Earth",
        ],
    )
)

asteroids = np.load("asteroids.npz")
planets = np.load("planets.npz")
bennu = np.load("bennu.npy")
planets_to_plot = ["Earth", "Mars", "Jupiter"]


classes = list(asteroids.keys())
# classes_to_exclude = ["TNO", "AST", "CEN"]
classes_to_exclude = []

cmags = np.linspace(0, 0.8, len(classes) - len(classes_to_exclude))
asteroid_colors = [cmap(cmag) for cmag in cmags]
planet_colors = {"Earth": "#2B65EC", "Mars": "#cc1e2c", "Jupiter": "#c99039"}

fig = plt.figure(figsize=figsize, dpi=dpi)
ax = fig.add_subplot(1, 1, 1, projection="polar")

for planet in planets_to_plot:
    ax.plot(
        planets[planet][:, 0],
        planets[planet][:, 1],
        linewidth=1.5,
        alpha=0.3,
        color="k",
    )
    ax.scatter(
        planets[planet][-1, 0],
        planets[planet][-1, 1],
        label=planet,
        s=25,
        color=planet_colors[planet],
        zorder=100,
    )


ax.plot(bennu[:, 0], bennu[:, 1], linewidth=0.5, alpha=0.4, color="k", linestyle=":")
ax.scatter(
    bennu[-1, 0],
    bennu[-1, 1],
    label="Bennu",
    marker="x",
    alpha=1,
    color="k",
    zorder=1000,
)


cindex = 0
for ii, the_class in enumerate(classes):
    if the_class in classes_to_exclude:
        continue

    the_bodies = asteroids[the_class]

    ax.scatter(
        the_bodies[:, 0],
        the_bodies[:, 1],
        s=0.4,
        label=labels[the_class],
        alpha=1,
        color=asteroid_colors[cindex],
    )

    cindex += 1


ax.scatter(0, 0, marker=r"$\odot$", color="k", linewidth=0.05, alpha=0.5, s=69)
# plt.legend(bbox_to_anchor=(1, 1))
ax.set_rlim(0, 1e9)
ax.axis("off")

plt.savefig("fig.pdf", bbox_inches="tight")
#

# %%
