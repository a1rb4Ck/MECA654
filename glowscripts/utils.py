# Pierre Nagorny, MECA654 exercises, Mars 2018, Savoie Mont Blanc University
# Based on Ruth Chabay, licensed under Creative Commons 4.0.
# All uses permitted, but you must not claim that you wrote it, and
# you must include this license information in any copies you make.
# For details see http://creativecommons.org/licenses/by/4.0

import vpython as vp  # GlowScript 2.7 VPython
from vpython import slider
from vpython import color, cylinder, label, vector  # , wtext
# from sympy import *  # Loading Sympy for symbolic calculus
# from sympy.physics.vector import *

import numpy as np


def draw_reference_box(L):
    '''
        Draw reference box
    '''
    # L = 40  # cube L on a side
    gray = color.gray(0.7)  # color of edges of container
    d = L / 2
    r = 0.005
    boxbottom = vp.curve(color=gray, radius=r)
    boxbottom.append(
        [vector(-d, -d, -d), vector(-d, -d, d), vector(d, -d, d),
         vector(d, -d, -d), vector(-d, -d, -d)])
    boxtop = vp.curve(color=gray, radius=r)
    boxtop.append(
        [vector(-d, d, -d), vector(-d, d, d), vector(d, d, d),
         vector(d, d, -d), vector(-d, d, -d)])
    vert1 = vp.curve(color=gray, radius=r)
    vert2 = vp.curve(color=gray, radius=r)
    vert3 = vp.curve(color=gray, radius=r)
    vert4 = vp.curve(color=gray, radius=r)
    vert1.append([vector(-d, -d, -d), vector(-d, d, -d)])
    vert2.append([vector(-d, -d, d), vector(-d, d, d)])
    vert3.append([vector(d, -d, d), vector(d, d, d)])
    vert4.append([vector(d, -d, -d), vector(d, d, -d)])


def axRot(ax, DCM):
    '''
    DCM must be a numpy array without symbols and evalf()
    ax must be a vector list of 3 coordinates
    the function return a 3D vpython vector
    '''
    # Permutation needed for consistency between sympy and vpython matrix
    permutation = [0, 2, 1]
    i = np.argsort(permutation)
    DCM = DCM[:, i]
    return vector(*np.array(ax).dot(DCM))


def vplot_referenceFrame(pos, Base, DCM, scale=1, fade_color=0.0):
    '''
    DCM must be without symbols and evalf()
    scale is the vector scale factor
    tint_color is the amount of color tinting
    '''
    lenght = 10 / scale
    radius = 0.3 * scale
    xaxis = cylinder(color=vector(1, 0, 0) * fade_color, pos=vector(*pos),
                     axis=axRot([lenght, 0, 0], DCM), radius=radius)
    xlbl = label(pos=vector(*pos) + axRot([lenght * 1.1, 0, 0], DCM),
                 text=Base.name + Base.indices[0],
                 color=color.red * fade_color, opacity=0, height=30, box=0)
    yaxis = cylinder(color=color.green * fade_color, pos=vector(*pos),
                     axis=axRot([0, lenght, 0], DCM), radius=radius)
    ylbl = label(pos=vector(*pos) + axRot([0, lenght * 1.1, 0], DCM),
                 text=Base.name + Base.indices[1],
                 color=color.green * fade_color, opacity=0, height=30, box=0)
    zaxis = cylinder(color=color.blue * fade_color, pos=vector(*pos),
                     axis=axRot([0, 0, lenght], DCM), radius=radius)
    zlbl = label(pos=vector(*pos) + axRot([0, 0, lenght * 1.1], DCM),
                 text=Base.name + Base.indices[2],
                 color=color.blue * fade_color, opacity=0, height=30, box=0)
    return {'xaxis': xaxis, 'xlbl': xlbl, 'yaxis': yaxis, 'ylbl': ylbl,
            'zaxis': zaxis, 'zlbl': zlbl}


class spherical_robot:
    def __init__(self, B0, B1, B2, theta_1, theta_2, scene):
        self.B0 = B0
        self.B1 = B1
        self.B2 = B2
        self.theta_1 = theta_1
        self.theta_2 = theta_2
        self.scene = scene
        self.scene.title = "Spherical Robot 3D view"
        self.scene.background = color.white
        self.scene.width = 600
        self.scene.height = 400
        self.scene.range = 10  # 1.3
        self.scene.forward = vector(-1, -1, -1)
        self.scene.autoscale = True

        self.scene.caption = """Use sliders to adjust theta_1 and theta_2 **
        *Right button drag to rotate the camera. Scroll wheel to zoom"""

        draw_reference_box(40)

        # We plot the main reference axis:
        self.axis_0 = vplot_referenceFrame(
            [0, 0, 0], self.B0, np.array(self.B0.dcm(self.B0).evalf()),
            scale=1.0, fade_color=1.0)
        self.old_theta_1 = np.pi / 8
        DCM_1 = np.array(self.B1.dcm(self.B0).subs(
            self.theta_1, self.old_theta_1).evalf())
        self.axis_1 = vplot_referenceFrame(
            [0, 0, 0], self.B1, DCM_1, scale=0.8, fade_color=0.75)
        self.old_theta_2 = np.pi / 8
        DCM_2 = np.array(self.B2.dcm(self.B0).subs(
            self.theta_1, self.old_theta_1).subs(
            self.theta_2, self.old_theta_2).evalf())
        self.x = 5
        self.axis_2 = vplot_referenceFrame([self.x, 0, 0], self.B2, DCM_2,
                                           scale=0.6, fade_color=0.5)

        self.sl_1 = slider(min=0, max=2 * np.pi, length=200,
                           value=self.old_theta_1, bind=self.update_theta_1)
        self.sl_2 = slider(min=0, max=2 * np.pi, length=200,
                           value=self.old_theta_2, bind=self.update_theta_2)

    def update_theta_1(self, s):
        print("update_theta_1", s.value)
        scale = 0.8
        lenght = 10 / scale
        DCM_1 = np.array(
            self.B1.dcm(self.B0).subs(self.theta_1, s.value).evalf())
        self.axis_1['xaxis'].axis = axRot([lenght, 0, 0], DCM_1)
        self.axis_1['xlbl'].pos = axRot([lenght * 1.1, 0, 0], DCM_1)
        self.axis_1['yaxis'].axis = axRot([0, lenght, 0], DCM_1)
        self.axis_1['ylbl'].pos = axRot([0, lenght * 1.1, 0], DCM_1)
        self.axis_1['zaxis'].axis = axRot([0, 0, lenght], DCM_1)
        self.axis_1['zlbl'].pos = axRot([0, 0, lenght * 1.1], DCM_1)
        scale = 0.6
        lenght = 10 / scale
        DCM_2 = np.array(
            self.B2.dcm(self.B0).subs(self.theta_1, s.value).subs(
                self.theta_2, self.old_theta_2).evalf())
        self.axis_2['xaxis'].axis = axRot([lenght, 0, 0], DCM_2)
        self.axis_2['xaxis'].pos = axRot([self.x, 0, 0], DCM_1)
        self.axis_2['xlbl'].pos = axRot([self.x, 0, 0], DCM_1) + axRot(
            [lenght * 1.1, 0, 0], DCM_2)
        self.axis_2['yaxis'].axis = axRot([0, lenght, 0], DCM_2)
        self.axis_2['yaxis'].pos = axRot([self.x, 0, 0], DCM_1)
        self.axis_2['ylbl'].pos = axRot([self.x, 0, 0], DCM_1) + axRot(
            [0, lenght * 1.1, 0], DCM_2)
        self.axis_2['zaxis'].axis = axRot([0, 0, lenght], DCM_2)
        self.axis_2['zaxis'].pos = axRot([self.x, 0, 0], DCM_1)
        self.axis_2['zlbl'].pos = axRot([self.x, 0, 0], DCM_1) + axRot(
            [0, 0, lenght * 1.1], DCM_2)
        self.old_theta_1 = s.value

    def update_theta_2(self, s):
        print("update_theta_2", s.value)
        scale = 0.6
        lenght = 10 / scale
        DCM_1 = np.array(self.B1.dcm(self.B0).subs(
            self.theta_1, self.old_theta_1).evalf())
        DCM_2 = np.array(
            self.B2.dcm(self.B0).subs(self.theta_1, self.old_theta_1).subs(
                self.theta_2, s.value).evalf())
        self.axis_2['xaxis'].axis = axRot([lenght, 0, 0], DCM_2)
        self.axis_2['xaxis'].pos = axRot([self.x, 0, 0], DCM_1)
        self.axis_2['xlbl'].pos = axRot([self.x, 0, 0], DCM_1) + axRot(
            [lenght * 1.1, 0, 0], DCM_2)
        self.axis_2['yaxis'].axis = axRot([0, lenght, 0], DCM_2)
        self.axis_2['yaxis'].pos = axRot([self.x, 0, 0], DCM_1)
        self.axis_2['ylbl'].pos = axRot([self.x, 0, 0], DCM_1) + axRot(
            [0, lenght * 1.1, 0], DCM_2)
        self.axis_2['zaxis'].axis = axRot([0, 0, lenght], DCM_2)
        self.axis_2['zaxis'].pos = axRot([self.x, 0, 0], DCM_1)
        self.axis_2['zlbl'].pos = axRot([self.x, 0, 0], DCM_1) + axRot(
            [0, 0, lenght * 1.1], DCM_2)
        self.old_theta_2 = s.value

# srob = spherical_robot(B0, B1, B2, theta_1, theta_2, scene)
# while True:
#     vp.rate(10)

# HTML('''<script>
#   function code_toggle() {
#     if (code_shown){
#       $('div.input').hide('500');
#       $('#toggleButton').val('Show Code')
#     } else {
#       $('div.input').show('500');
#       $('#toggleButton').val('Hide Code')
#     }
#     code_shown = !code_shown
#   }

#   $( document ).ready(function(){
#     code_shown=false;
#     $('div.input').hide()
#   });
# </script>
# <form action="javascript:code_toggle()"><input type="submit" id="toggleButton" value="Show Code"></form>''')