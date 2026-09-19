import tkinter as tk
import math
import tkinter as tk
from tkinter import ttk

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

class joint:
    def __init__(self, linkage=None, location=[0,0,0], rotation=[0,0,0]):
        self.previous_link = linkage
        self.location=location
        self.rotation=rotation
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Prosthetic Rednering GUI")
        self.root.geometry("900x700")

        # -----------------------------
        # Controls
        # -----------------------------
        controls = ttk.Frame(root, padding=10)
        controls.pack(fill=tk.X)

        ttk.Label(controls, text="3D Surface Plot").pack(
            side=tk.LEFT, padx=(0, 15)
        )

        ttk.Button(
            controls,
            text="Randomize",
            command=self.randomize_plot
        ).pack(side=tk.RIGHT)

        # -----------------------------
        # Matplotlib Figure
        # -----------------------------
        self.figure = plt.Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111, projection="3d")

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=root
        )
        self.canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True
        )

        self.draw_plot()

    def draw_plot(self):
        # Clear the existing axes
        self.ax.clear()

        #self.plot_reference_frames(0, 0, 0, 0, 0, 0)
        #self.plot_reference_frames(1, 0, 0, 0, 0, 0)
        #self.plot_reference_frames(1, 1, 0, 0, 0, 0)
        # Labels
        self.ax.set_title("3D Surface Plot")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        self.canvas.draw()

    def randomize_plot(self):
        self.ax.clear()

        # Generate new random surface
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)

        X, Y = np.meshgrid(x, y)

        Z = (
            np.sin(np.sqrt(X**2 + Y**2))
            + np.random.normal(0, 0.1, X.shape)
        )

        self.ax.plot_surface(
            X,
            Y,
            Z,
            cmap="plasma",
            edgecolor="none"
        )

        self.ax.set_title("Randomized 3D Surface")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        self.canvas.draw()
    def plot_reference_frames(self, location, rotation):
        self.ax.scatter(location[0], location[1], location[2])

        x = location[0]
        y = location[1]
        z = location[2]
        
        x2 = x + 1
        y2 = y + 1
        z2 = z + 1

        x_points = (x, x2)
        y_points = (y, y2)
        z_points = (z, z2)

        self.ax.plot(x_points, (y, y), (z, z), color="red")
        self.ax.plot((x, x), y_points, (z, z), color="blue")
        self.ax.plot((x, x), (y, y), z_points, color="green")
    def add_joint(self, joint):
        self.plot_reference_frames(joint.location, joint.rotation)
        if joint.previous_link != None:
            self.ax.plot([joint.previous_link.location[0], joint.location[0]], [joint.previous_link.location[1], joint.location[1]], [joint.previous_link.location[2], joint.location[2]], color = "grey", linewidth=3)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)

    joints = []

    joints.append(joint())
    joints.append(joint(joints[0], [1, 0, 0]))
    joints.append(joint(joints[1], [1, 1, 0]))

    for j in joints: app.add_joint(j)

    root.mainloop()