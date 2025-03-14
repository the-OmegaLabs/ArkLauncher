import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# 初始化画布和3D坐标轴
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d', facecolor='black')
ax.grid(False)
ax.set_axis_off()

# 生成空心球体数据
theta = np.linspace(0, 2 * np.pi, 100)
phi = np.linspace(0, np.pi, 50)
theta, phi = np.meshgrid(theta, phi)
r = 1
x_sphere = r * np.sin(phi) * np.cos(theta)
y_sphere = r * np.sin(phi) * np.sin(theta)
z_sphere = r * np.cos(phi)

# 绘制空心球体（线框模式）
ax.plot_wireframe(x_sphere, y_sphere, z_sphere,
                  color='white', linewidth=0.5, alpha=0.3)

# 初始化环绕曲线
curve, = ax.plot([], [], [], color='white', linewidth=1)


# 定义环绕曲线的参数方程（螺旋线）
def spiral(t, n_loops=3, radius=1.5):
    angle = 2 * np.pi * t
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    z = radius * np.sin(n_loops * angle)  # 添加垂直波动
    return x, y, z


# 动画更新函数
def update(frame):
    t = frame / 100  # 控制动画速度
    x, y, z = spiral(t)

    # 累积轨迹点（保留历史轨迹）
    # 正确方法：使用get_data_3d()获取所有维度数据
    x_prev, y_prev, z_prev = curve.get_data_3d()
    x_data = np.append(x_prev, x)
    y_data = np.append(y_prev, y)
    z_data = np.append(z_prev, z)
    if len(x_data) > 200:  # 限制轨迹长度
        x_data = x_data[-200:]
        y_data = y_data[-200:]
        z_data = z_data[-200:]

    curve.set_data(x_data, y_data)
    curve.set_3d_properties(z_data)

    # 动态调整视角（可选）
    ax.view_init(elev=10, azim=frame * 0.5)

    return curve,


# 创建动画
anim = FuncAnimation(
    fig, update,
    frames=np.arange(0, 200, 1),
    interval=50,
    blit=True
)

# 保存为GIF或显示动画
anim.save('planet.gif', writer='pillow', fps=20)
# plt.show()
