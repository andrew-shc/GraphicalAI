from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QLabel
from PyQt5.Qt import QSurfaceFormat, QGLWidget, QOpenGLWidget

import sys


def read_glsl(fname):
    glsl = []
    with open(fname, "r") as fbj:
        glsl = fbj.readlines()
    return "".join(glsl)


import numpy as np
import moderngl

sx = 0
sy = 0
sz = 0

scale = np.array([
    sx, 0.0, 0.0, 0.0,
    0.0, sy, 0.0, 0.0,
    0.0, 0.0, sz, 0.0,
    0.0, 0.0, 0.0, 0.0,
])

tx = 0
ty = 0
tz = -10

translate = np.array([
    1.0, 0.0, 0.0, tx,
    0.0, 1.0, 0.0, ty,
    0.0, 0.0, 1.0, tz,
    0.0, 0.0, 0.0, 0.0,
])

rx = 0
ry = 0
rz = 0

rotation = np.array([
    np.cos(rz), -np.sin(rz), 0.0, 0.0,
    np.sin(rz), np.cos(rz), 0.0, 0.0,
    0.0, 0.0, 1.0, 1.0,
    0.0, 0.0, 0.0, 0.0
]) * np.array([
    np.cos(ry), 0.0, np.sin(ry), 0.0,
    0.0, 1.0, 0.0, 0.0,
    -np.sin(ry), 0.0, np.cos(ry), 1.0,
    0.0, 0.0, 0.0, 0.0
]) * np.array([
    1.0, 0.0, 0.0, 0.0,
    0.0, np.cos(rx), -np.sin(rx), 0.0,
    0.0, np.sin(rx), np.cos(rx), 1.0,
    0.0, 0.0, 0.0, 0.0
])

class OpenGLFrame(QOpenGLWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        gl = self.format()
        gl.setVersion(4, 4)
        gl.setProfile(QSurfaceFormat.CoreProfile)
        gl.setDepthBufferSize(24)
        gl.setSwapBehavior(QSurfaceFormat.DoubleBuffer)
        gl.setSwapInterval(1)
        self.setFormat(gl)

        self.model_vert = read_glsl("model.vert")
        self.triangle_frag = read_glsl("triangle.frag")
        self.axis_frag = read_glsl("axis.frag")

        self.showMinimized()  # same as `show()` except minimized to prevent the pop-up window from occurring

    def initializeGL(self):
        self.ctx = moderngl.create_context(require=440)
        self.ctx.clear(1.0, 1.0, 1.0)

        prog = self.ctx.program(
            vertex_shader=self.model_vert,
            fragment_shader=self.triangle_frag,
        )

        # prog['z_near'].value = 0.1
        # prog['z_far'].value = 1000.0
        # prog['ratio'].value = self.size().width() / self.size().height()
        # prog['fovy'].value = 60

        # prog["view"].value = tuple(translate.astype("f4") * rotation.astype("f4") * scale.astype("f4"))

        prog["height"].value = self.size().height()
        prog["width"].value = self.size().width()

        ind = np.array([0, 1, 2, 3])

        vtx = np.array([
            # x, y, z, r, g, b
            -.6, -.6, 1.0, 0.0, 0.0,
            0.6, -.6, 0.0, 1.0, 0.0,
            0.6, 0.6, 0.0, 0.0, 1.0,
            -.6, 0.6, 1.0, 0.0, 1.0,
        ])

        vbo_vert = self.ctx.buffer(vtx.astype("f4").tobytes())
        ibo = self.ctx.buffer(ind.astype("i4").tobytes())
        self.vao = self.ctx.vertex_array(prog,
                                         [
                                             (vbo_vert, "2f 3f /v", "in_vert", "in_color"),
                                         ],
                                         ibo
                                         )

        # =========================================================================

        axis_prog = self.ctx.program(
            vertex_shader=self.model_vert,
            fragment_shader=self.axis_frag,
        )

        axis_prog["height"].value = self.size().height()
        axis_prog["width"].value = self.size().width()

        # axis_prog['z_near'].value = 0.1
        # axis_prog['z_far'].value = 1000.0
        # axis_prog['ratio'].value = self.size().width() / self.size().height()
        # axis_prog['fovy'].value = 60

        # axis_prog["view"].value = tuple(translate.astype("f4") * rotation.astype("f4") * scale.astype("f4"))

        vtx_axis = np.array([
            # x, y
            -.5, 0.0,
            0.0, 0.0,
            0.0, -.5,
            0.0, 0.0,
        ])

        print(vtx_axis)
        vtx_axis[2::3] -= 8
        print(vtx_axis)
        ind_axis = np.array([0,1,2,3])

        vbo_axis = self.ctx.buffer(vtx_axis.astype("f4").tobytes())
        ibo_axis = self.ctx.buffer(ind_axis.astype("i4").tobytes())
        self.vao_axis = self.ctx.vertex_array(axis_prog,
                                         [
                                             (vbo_axis, "2f /v", "in_vert"),
                                         ],
                                         ibo_axis
                                         )

    def paintGL(self):
        self.vao_axis.render(moderngl.LINES)
        self.vao.render(moderngl.TRIANGLE_FAN)
        self.ctx.clear(1.0, 1.0, 1.0)


app = QApplication(sys.argv)

win = QMainWindow()
win.setWindowTitle("Graph API v0.1")
win.setGeometry(0, 0, 1920, 1080)

c = QHBoxLayout()

gl_widget = OpenGLFrame()

c.addWidget(QLabel("Hello World!\nBelow should be an OpenGL Application"))
c.addWidget(gl_widget)

central_widget = QWidget()
central_widget.setLayout(c)
win.setCentralWidget(central_widget)

win.show()
sys.exit(app.exec())
