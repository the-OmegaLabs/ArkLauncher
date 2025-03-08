import tkinter as tk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class OpenGLWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.width, self.height = 800, 600
        # 创建Canvas并绑定OpenGL上下文
        self.canvas = tk.Canvas(
            self.master, width=self.width, height=self.height)
        self.canvas.pack()
        # 初始化OpenGL
        self.init_opengl()
        # 加载着色器
        self.shader_program = self.load_shaders(
            "vertex_shader.vert", "fragment_shader.frag")
        # 设置顶点数据
        self.setup_vertex_data()
        # 启动渲染循环
        self.animate()

    def init_opengl(self):
        # 初始化OpenGL上下文
        self.canvas.bind(
            "<Expose>", lambda e: self.on_resize(e.width, e.height))
        glutInit()  # GLUT初始化

    def on_resize(self, width, height):
        # 窗口尺寸变化时更新视口
        glViewport(0, 0, width, height)
        self.width, self.height = width, height

    def load_shaders(self, vert_path, frag_path):
        # 从文件读取GLSL源码
        def read_file(path):
            with open(path, 'r') as f:
                return f.read()

        # 编译单个着色器
        def compile_shader(shader_type, source):
            shader = glCreateShader(shader_type)
            glShaderSource(shader, source)
            glCompileShader(shader)
            # 检查编译错误
            if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
                error = glGetShaderInfoLog(shader).decode()
                raise RuntimeError(f"着色器编译错误：\n{error}")
            return shader

        # 加载顶点和片段着色器
        vertex_shader = compile_shader(GL_VERTEX_SHADER, read_file(vert_path))
        fragment_shader = compile_shader(
            GL_FRAGMENT_SHADER, read_file(frag_path))

        # 创建着色器程序并链接
        program = glCreateProgram()
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)
        # 检查链接错误
        if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
            error = glGetProgramInfoLog(program).decode()
            raise RuntimeError(f"程序链接错误：\n{error}")
        return program

    def setup_vertex_data(self):
        # 顶点数据（三角形）
        vertices = [
            -0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            0.0, 0.5, 0.0
        ]
        # 创建VAO和VBO
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, (GLfloat * len(vertices))
                     (*vertices), GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def animate(self):
        # 渲染循环
        self.render()
        self.master.after(16, self.animate)  # 约60FPS

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shader_program)
        # 传递Uniform变量（颜色）
        color_loc = glGetUniformLocation(self.shader_program, "uColor")
        glUniform4f(color_loc, 1.0, 0.5, 0.2, 1.0)  # 橙色
        # 绘制三角形
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glFlush()  # 确保绘制完成


if __name__ == "__main__":
    root = tk.Tk()
    app = OpenGLWindow(root)
    root.geometry("800x600")  # 设置窗口初始尺寸
    root.mainloop()  # 进入事件循环
