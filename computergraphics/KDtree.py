import open3d as o3d
import numpy as np

# Load mesh
mesh = o3d.io.read_triangle_mesh(
    "turtle.obj",
    enable_post_processing=True
)
mesh.compute_vertex_normals()

# Convert mesh to point cloud
pcd = mesh.sample_points_uniformly(
    number_of_points=6000   # keep sparse for clarity
)

# Ensure normals exist (optional, but useful later)
pcd.estimate_normals()

points = np.asarray(pcd.points)

# Build KD-Tree
pcd_tree = o3d.geometry.KDTreeFlann(pcd)

# Construct global neighborhood graph
k = 8   # neighbors per point

lines = []
line_colors = []

for i in range(len(points)):
    [_, idxs, _] = pcd_tree.search_knn_vector_3d(
        points[i], k
    )

    for j in idxs[1:]:  # skip self
        lines.append([i, j])
        line_colors.append([1.0, 0.0, 0.0])  # red edges

# Color point cloud
colors = np.full((len(points), 3), 0.7)
pcd.colors = o3d.utility.Vector3dVector(colors)

# Create LineSet (nodes + edges)
line_set = o3d.geometry.LineSet(
    points=o3d.utility.Vector3dVector(points),
    lines=o3d.utility.Vector2iVector(lines)
)
line_set.colors = o3d.utility.Vector3dVector(line_colors)

# Visualize
o3d.visualization.draw_geometries([pcd, line_set])
