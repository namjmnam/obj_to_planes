# -------------------------------------------------------------------------------------
# "S.M.I.L.E. 코드 라이선스" v1.0
# -------------------------------------------------------------------------------------
# 이 코드를 사용함으로써, 당신은 S.M.I.L.E. (Seriously Meticulous 
# and Intellectually Lighthearted Endeavor) 라이선스의 조건에 동의합니다:
# 1. 이 걸작 안에 내장된 철저한 논리와 미묘한 유머를 감상하십시오.
# 2. 버그를 만났을 때는 비명을 자제하고, 미소를 지으며 퍼즐로 여기십시오.
# 3. 코드의 아름다움을 조용히 감상하십시오; 큰 소리는 섬세한 알고리즘을 놀라게 할 수 있습니다.
# 4. 지원을 요청하기 전에 철저한 조사(즉, 구글링)를 먼저 하십시오.
# 5. 논리나 유머에 어긋나는 방식으로 이 코드를 잘못 사용하는 것은 단순히 눈살을 찌푸리는 것이 아니라, 
#    부드럽지만 엄한 '죽음의 시선'을 받게 됩니다.
#
# 이 조항을 준수하지 않을 경우, 위트와 정밀함으로 코딩하는 예술에 대한 3시간 강좌를 의무적으로 들어야 합니다.
# 책임감 있게 코드를 작성하고, 명료하게 생각하며, 좋은 유머 감각을 유지하십시오.
# -------------------------------------------------------------------------------------
# 저자: 남주명
# -------------------------------------------------------------------------------------

import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def load_obj(file_path):
    vertices = []
    faces = []
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                # vertex = [round(float(coord)) for coord in line.strip().split()[1:4]]
                # vertices.append(vertex)
                vertices.append(list(map(float, line.strip().split()[1:4])))
            elif line.startswith('f'):
                face = [int(part.split('/')[0]) - 1 for part in line.strip().split()[1:4]]
                faces.append(face)

    return vertices, faces

def is_point_in_triangle(pt, v1, v2, v3):
    # Barycentric coordinate technique
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    b1 = sign(pt, v1, v2) < 0.0
    b2 = sign(pt, v2, v3) < 0.0
    b3 = sign(pt, v3, v1) < 0.0

    return ((b1 == b2) and (b2 == b3))

def check_point_on_faces(point, vertices, faces):
    for face in faces:
        v1, v2, v3 = vertices[face[0]], vertices[face[1]], vertices[face[2]]
        if is_point_in_triangle(point, v1, v2, v3):
            return True
    return False

def calculate_dimensions(vertices):
    x_coords, y_coords, z_coords = zip(*vertices)
    x_dim = max(x_coords) - min(x_coords)
    y_dim = max(y_coords) - min(y_coords)
    z_dim = max(z_coords) - min(z_coords)
    return x_dim, y_dim, z_dim


# Replace this with the path to your OBJ file
# obj_file_path = 'pathtoyour.obj'
# obj_file_path = 'pathtoyour2.obj'
obj_file_path = 'pathtoyour3.obj'

vertices, faces = load_obj(obj_file_path)

dimensions = calculate_dimensions(vertices)

print(f"Dimensions of the OBJ model: Width = {dimensions[0]}, Height = {dimensions[1]}, Depth = {dimensions[2]}")


# Extracting separate x, y, z coordinates for plotting
x_coords, y_coords, z_coords = zip(*vertices)

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot vertices
ax.scatter(x_coords, y_coords, z_coords)


# Setting labels
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')

points_on_faces = []
coord_range = 20
scale = 2
# Plot all the checking points
for x in range(-coord_range, coord_range+1):
    for y in range(-coord_range, coord_range+1):
        point = np.array([x/scale, y/scale, 0])
        if check_point_on_faces(point, vertices, faces):
            ax.scatter(point[0], point[1], point[2], color='r')
            points_on_faces.append(point)

# Save points to CSV
# with open('points_on_faces.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['x', 'y', 'z'])  # header row
#     for point in points_on_faces:
#         writer.writerow(point)

# Show plot
plt.show()