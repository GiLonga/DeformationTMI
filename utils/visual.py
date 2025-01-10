import plotly.graph_objects as go
import numpy as np
import plotly.io as pio

# Assume these are the original x, y, z coordinates from the point cloud

def plot_field(mesh, new_kp, original_kp=[],  ):
    """
    TO DO 
    """
    x, y, z = zip(*mesh.vertices)
    top_10_head=np.argsort(z)[-10:]

    x_s, y_s, z_s = zip(*mesh.vertices[new_kp])

    # Create the original scatter plot
    scatter_original = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=1,  # Smaller size for the original points
            color=z,  # Use z-coordinate for color gradient
            colorscale='Portland',  # Choose a colorscale
            opacity=0.8
        ),
        name="Original Points"
    )

    # Create a scatter plot for manual points with different styling
    scatter_manual = go.Scatter3d(
        x=x_s,
        y=y_s,
        z=z_s,
        mode='markers',
        marker=dict(
            size=3,  # Larger size for manual points
            color='black',  # Use a fixed color (e.g., red)
            opacity=1.0
        ),
        name="Head Coord"
    )

    # Define rectangle corners in 3D space
    rectangle_vertices = np.array([
        (mesh.vertices[new_kp[10]][0]-0.05, np.mean(mesh.vertices[top_10_head],axis=0)[1],np.mean(mesh.vertices[top_10_head],axis=0)[2]),  # Corner 1
        (mesh.vertices[new_kp[11]][0]+0.05, np.mean(mesh.vertices[top_10_head],axis=0)[1],np.mean(mesh.vertices[top_10_head],axis=0)[2]),
        (mesh.vertices[new_kp[11]][0]+0.05, np.mean(mesh.vertices[top_10_head],axis=0)[1],mesh.vertices[new_kp[11]][2]),  # Corner 2  # Corner 3
        (mesh.vertices[new_kp[10]][0]-0.05, np.mean(mesh.vertices[top_10_head],axis=0)[1],mesh.vertices[new_kp[11]][2]),  # Corner 4
        (mesh.vertices[new_kp[10]][0]-0.05, np.mean(mesh.vertices[top_10_head],axis=0)[1],np.mean(mesh.vertices[top_10_head],axis=0)[2])   # Close the rectangle
    ])

    # Create a line plot for the rectangle borders
    rectangle_lines = go.Scatter3d(
        x=rectangle_vertices[:, 0],
        y=rectangle_vertices[:, 1],
        z=rectangle_vertices[:, 2],
        mode='lines',
        line=dict(
            color='blue',
            width=5
        ),
        name="Rectangle Border"
    )

    # Create layout
    layout = go.Layout(scene=dict(aspectmode="data"))
    fig = go.Figure(data=[scatter_original, scatter_manual, rectangle_lines], layout=layout)

    hover_text = [f'Index: {index}' for index in range(len(mesh.vertices))]
    fig.data[0]['text'] = hover_text

    fig.show()

def plot_isocenters(vertices, new_iso, name='', groundtruth_iso=[],):
    """
    TO DO
    """
    x, y, z = zip(*vertices)
    x_s, y_s, z_s = zip(*new_iso)

    scatter_isocenters = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=1,  # Smaller size for the original points
            color=z,  # Use z-coordinate for color gradient
            colorscale='Portland',  # Choose a colorscale
            opacity=0.8
        ),
        name="Mesh Points"
    )

    scatter_manual = go.Scatter3d(
        x=x_s,
        y=y_s,
        z=z_s,
        mode='markers',
        marker=dict(
            size=3,  # Larger size for manual points
            color='black',  # Use a fixed color (e.g., red)
            opacity=1.0
        ),
        name="Iso Coord"
    )

    if groundtruth_iso:
        x_o, y_o, z_o = zip(*groundtruth_iso)
        scatter_gt = go.Scatter3d(
        x=x_o,
        y=y_o,
        z=z_o,
        mode='markers',
        marker=dict(
            size=3,  # Larger size for manual points
            color='blue',  # Use a fixed color (e.g., red)
            opacity=1.0
        ),
        name="GT Iso Coord"
        )   
        layout = go.Layout(scene=dict(aspectmode="data"))
        fig = go.Figure(data=[scatter_isocenters, scatter_manual, scatter_gt], layout=layout)
    else:
        layout = go.Layout(scene=dict(aspectmode="data"))
        fig = go.Figure(data=[scatter_isocenters, scatter_manual], layout=layout)
    hover_text = [f'Index: {index}' for index in range(len(vertices))]
    fig.data[0]['text'] = hover_text


    pio.write_image(fig, f'/home/ubuntu/giorgio_longari/DeformationTMI/output/plot_{name}.png')
    pio.write_html(fig, f'/home/ubuntu/giorgio_longari/DeformationTMI/output/plot_{name}.html')
    #fig.show()

    return True
