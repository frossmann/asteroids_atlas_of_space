# get_orbits_from_repofiles.py
# %%

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pdf
import pandas as pd
from tqdm import tqdm
import cmocean

# Functions used throughout the plotting
# Limits of radial logarithmic plot (center value = min10, outer rim = max10)
# min10 = np.log10(2.7e7)
# max10 = np.log10(1.496e10)


def get_angle(x0, y0, x1, y1):
    """Calculate the angle from horizontal, counterclockwise"""
    angle = np.rad2deg(np.arctan2(y1 - y0, x1 - x0))
    return angle


def hypotenuse(x0, y0, x1, y1):
    """Returns the length of the straight line vector between two points"""
    hyp = np.hypot(x1 - x0, y1 - y0)
    return hyp


def get_r_theta(xs, ys):
    """Convert x and y coordinates to r-theta plots"""
    rs = [hypotenuse(0, 0, x, y) for x, y in zip(xs, ys)]
    # rs = [np.log10(r) - min10 for r in rs]
    theta = [get_angle(0, 0, x, y) for x, y in zip(xs, ys)]
    theta = [np.radians(x) for x in theta]
    return rs, theta


# %%

#  ========================================================================
#  ------------ save asteroid locations at end of integration  ------------
#  ========================================================================

# large asteroids *----------------------------------------------
df1 = pd.read_csv("./data/large_asteroids.csv")
df1["filename"] = "./data/large_asteroids/" + df1["horizons"] + ".csv"

# small asteroids *----------------------------------------------
df2 = pd.read_csv("./data/small_asteroids.csv")
df2["filename"] = "./data/small_asteroids/" + df2["horizons"] + ".csv"

# any inner asteroids *------------------------------------------
df3 = pd.read_csv("./data/any_outer_asteroids.csv")
df3["filename"] = "./data/any_outer_asteroids/" + df3["horizons"] + ".csv"

# any outer asteroids *------------------------------------------
df4 = pd.read_csv("./data/any_inner_asteroids.csv")
df4["filename"] = "./data/any_inner_asteroids/" + df4["horizons"] + ".csv"


df_merge = pd.concat([df1, df2, df3, df4])


bodies_by_class = dict()
classes = df_merge["class"].unique().tolist()

for i, c in tqdm(enumerate(classes)):
    class_df = df_merge[df_merge["class"] == c].copy()
    class_df["diameter"].astype(float)

    n_bodies = class_df.shape[0]
    theta_rs_per_class = np.zeros((n_bodies, 2))

    for ii, filename in tqdm(enumerate(class_df["filename"].tolist())):
        try:
            body_df = pd.read_csv(filename)

            rs, theta = get_r_theta(body_df["X"].tolist(), body_df["Y"].tolist())
            theta_rs_per_class[ii, :] = np.array([theta[-1], rs[-1]])

        except Exception as ex:
            print("\n", ex)
            pass

    bodies_by_class[c] = theta_rs_per_class

# np.savez("asteroids.npz", **bodies_by_class)


# %%
#  ========================================================================
#  ----------------------- save planet orbits -----------------------------
#  ========================================================================

df_planets = pd.read_csv("./data/planets.csv")
df_planets["filename"] = "./data/planets/" + df_planets["horizons"].astype(str) + ".csv"

planets = {}

for i, (filename, c) in enumerate(
    zip(
        df_planets["filename"].tolist(),
        df_planets["class"].tolist(),
    )
):
    df = pd.read_csv(filename)
    rs, theta = get_r_theta(df["X"].tolist(), df["Y"].tolist())
    planets[c] = np.column_stack((theta, rs))

# np.savez("planets.npz", **planets)
# %%
# import numpy as np

# process bennu's ephermeride:
bennu_df = pd.read_csv(
    "/Users/francis/repos/asteroids_atlas_of_space/bennu_horizons_results.txt",
    header=None,
)
rs, theta = get_r_theta(bennu_df[2].tolist(), bennu_df[3].tolist())

np.save("bennu.npy", np.column_stack((theta, rs)))
# %%
