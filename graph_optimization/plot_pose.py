import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utilities.math_tools import *
from matplotlib import patches
import matplotlib.pyplot as plt


def plot_pose2_on_axes(axes,
                       pose,
                       axis_length: float = 0.1):

    gRp, origin = makeRt(v2m(pose))

    x_axis = origin + gRp[:, 0] * axis_length
    line = np.append(origin[np.newaxis], x_axis[np.newaxis], axis=0)
    axes.plot(line[:, 0], line[:, 1], 'r-')

    y_axis = origin + gRp[:, 1] * axis_length
    line = np.append(origin[np.newaxis], y_axis[np.newaxis], axis=0)
    axes.plot(line[:, 0], line[:, 1], 'g-')

    e1 = patches.Circle(xy=origin, radius=axis_length, fill=False)

    axes.add_patch(e1)


def plot_pose2(
        fignum,
        pose,
        axis_length: float = 0.1,
        axis_labels=("X axis", "Y axis", "Z axis")):
    # get figure object
    fig = plt.figure(fignum)
    plt.axis('equal')
    axes = fig.gca()
    plot_pose2_on_axes(axes,
                       pose,
                       axis_length=axis_length)

    axes.set_xlabel(axis_labels[0])
    axes.set_ylabel(axis_labels[1])

    return fig

def plot_pose3_on_axes(axes, pose, axis_length=0.1, scale=1):
    # get rotation and translation (center)
    gRp, origin = makeRt(expSE3(pose))

    # draw the camera axes
    x_axis = origin + gRp[:, 0] * axis_length
    line = np.append(origin[np.newaxis], x_axis[np.newaxis], axis=0)
    axes.plot(line[:, 0], line[:, 1], line[:, 2], 'r-')

    y_axis = origin + gRp[:, 1] * axis_length
    line = np.append(origin[np.newaxis], y_axis[np.newaxis], axis=0)
    axes.plot(line[:, 0], line[:, 1], line[:, 2], 'g-')

    z_axis = origin + gRp[:, 2] * axis_length
    line = np.append(origin[np.newaxis], z_axis[np.newaxis], axis=0)
    axes.plot(line[:, 0], line[:, 1], line[:, 2], 'b-')


def set_axes_equal(fignum: int) -> None:
    """
    Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Args:
      fignum: An integer representing the figure number for Matplotlib.
    """
    fig = plt.figure(fignum)
    if not fig.axes:
        ax = fig.add_subplot(projection='3d')
    else:
        ax = fig.axes[0]

    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])

    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))

    ax.set_xlim3d([origin[0] - radius, origin[0] + radius])
    ax.set_ylim3d([origin[1] - radius, origin[1] + radius])
    ax.set_zlim3d([origin[2] - radius, origin[2] + radius])


def plot_pose3(
    fignum,
    pose,
    axis_length = 0.1,
    axis_labels=("X axis", "Y axis", "Z axis")):
    
    # get figure object
    fig = plt.figure(fignum,figsize=plt.figaspect(1))
    #plt.axis('equal')
    if not fig.axes:
        axes = fig.add_subplot(projection='3d')
    else:
        axes = fig.axes[0]
    plot_pose3_on_axes(axes, pose, axis_length=axis_length)
    axes.set_xlabel(axis_labels[0])
    axes.set_ylabel(axis_labels[1])
    axes.set_zlabel(axis_labels[2])
    return fig


if __name__ == '__main__':
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from utilities.math_tools import *

    cur_pose = np.array([0,0,0])
    odom = np.array([0.2, 0, 0.5])
    for i in range(12):
        cur_pose = m2v(v2m(cur_pose).dot(v2m(odom)))
        plot_pose2('test plot 2d', cur_pose, 0.05)
    plt.axis('equal')

    cur_pose = np.array([0,0,0,0,0,0])
    odom = np.array([0.2, 0, 0.01, 0, 0, 0.5])
    for i in range(12):
        cur_pose = logSE3(expSE3(cur_pose).dot(expSE3(odom)))
        plot_pose3('test plot 3d', cur_pose, 0.05)
    set_axes_equal('test plot 3d')


    plt.show()
