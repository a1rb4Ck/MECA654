# Vpython visualization
from utils import *
from vpython import *


class spherical_robot:
    def __init__(self, B0, B1, B2, theta_1, theta_2, scene):
        self.B0 = B0
        self.B1 = B1
        self.B2 = B2
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
            theta_1, self.old_theta_1).evalf())
        self.axis_1 = vplot_referenceFrame(
            [0, 0, 0], self.B1, DCM_1, scale=0.8, fade_color=0.75)
        self.old_theta_2 = np.pi / 8
        DCM_2 = np.array(self.B2.dcm(self.B0).subs(
            theta_1, self.old_theta_1).subs(
            theta_2, self.old_theta_2).evalf())
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
        DCM_1 = np.array(self.B1.dcm(self.B0).subs(theta_1, s.value).evalf())
        self.axis_1['xaxis'].axis = axRot([lenght, 0, 0], DCM_1)
        self.axis_1['xlbl'].pos = axRot([lenght * 1.1, 0, 0], DCM_1)
        self.axis_1['yaxis'].axis = axRot([0, lenght, 0], DCM_1)
        self.axis_1['ylbl'].pos = axRot([0, lenght * 1.1, 0], DCM_1)
        self.axis_1['zaxis'].axis = axRot([0, 0, lenght], DCM_1)
        self.axis_1['zlbl'].pos = axRot([0, 0, lenght * 1.1], DCM_1)
        scale = 0.6
        lenght = 10 / scale
        DCM_2 = np.array(self.B2.dcm(self.B0).subs(theta_1, s.value).subs(
                         theta_2, self.old_theta_2).evalf())
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
            theta_1, self.old_theta_1).evalf())
        DCM_2 = np.array(self.B2.dcm(self.B0).subs(
            theta_1, self.old_theta_1).subs(theta_2, s.value).evalf())
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

srob = spherical_robot(B0, B1, B2, theta_1, theta_2, scene)
while True:
    rate(10)
