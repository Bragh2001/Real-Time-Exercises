import open3d as o3d
import numpy as np

# Load textured mesh
mesh = o3d.io.read_triangle_mesh(
    "turtle.obj",
    enable_post_processing=True
)
mesh.compute_vertex_normals()

# Convert mesh to point cloud
pcd = mesh.sample_points_uniformly(
    number_of_points=300000
)

# Create voxel grid from point cloud
voxel_size = 0.05
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(
    pcd, voxel_size
)

# Convert voxel grid to cube mesh
voxel_mesh = o3d.geometry.TriangleMesh()

for voxel in voxel_grid.get_voxels():
    cube = o3d.geometry.TriangleMesh.create_box(1, 1, 1)

    # Color voxel
    cube.paint_uniform_color(voxel.color)

    # Scale cube to voxel size
    cube.scale(voxel_size, center=cube.get_center())

    # Move cube to voxel center
    center = voxel_grid.get_voxel_center_coordinate(voxel.grid_index)
    cube.translate(center, relative=False)

    voxel_mesh += cube

# Disable lighting (matte look)
voxel_mesh.triangle_normals = o3d.utility.Vector3dVector([])
voxel_mesh.vertex_normals = o3d.utility.Vector3dVector([])

# Animate (rotation)
def rotate_voxels(vis):
    R = voxel_mesh.get_rotation_matrix_from_xyz((0, np.deg2rad(0.3), 0))
    voxel_mesh.rotate(R, center=voxel_mesh.get_center())
    vis.update_geometry(voxel_mesh)
    return False

# Visualizing
vis = o3d.visualization.Visualizer()
vis.create_window("Rotating Voxel Turtle (Point Cloud)", width=800, height=600)

vis.add_geometry(voxel_mesh)
vis.register_animation_callback(rotate_voxels)

vis.run()
vis.destroy_window()
