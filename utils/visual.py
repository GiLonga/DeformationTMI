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
        name="Rectangle Field"
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
    data = []
    x, y, z = zip(*vertices)
    x_s, y_s, z_s = zip(*new_iso)

    scatter_pointcloud = scatter_data(x, y, z)
    scatter_isos = scatter_plot(x_s, y_s, z_s, color = "black", size = 3, opacity = 1.0)

    data.append(scatter_pointcloud)
    data.append(scatter_isos)

    if groundtruth_iso:
        x_o, y_o, z_o = zip(*groundtruth_iso)
        scatter_gt = scatter_plot(x_o, y_o, z_o, color = "blue", size = 3, opacity = 1.0, _name = "GT Iso Coord")  
        data.append(scatter_gt)
        
    layout = go.Layout(scene=dict(aspectmode="data"))
    fig = go.Figure(data = data, layout=layout)
    hover_text = [f'Index: {index}' for index in range(len(vertices))]
    fig.data[0]['text'] = hover_text


    pio.write_image(fig, f'/home/ubuntu/giorgio_longari/DeformationTMI/output/plot_{name}.png')
    pio.write_html(fig, f'/home/ubuntu/giorgio_longari/DeformationTMI/output/plot_{name}.html')
    #fig.show()

    return True

def plot_geometry(vertices, new_iso, fields = [], rmse = [],  name = '', groundtruth_iso = [],):
    """
    TO DO: THIS IS WORKING ONLY FOR PATIENTS WITH ISOCENTERS ON THE ARMS AT THE MOMENT
    """
    x, y, z = zip(*vertices)
    x_s, y_s, z_s = zip(*new_iso)

    data=[]

    scatter_isocenters = scatter_data(x, y, z)
    data.append(scatter_isocenters)
    scatter_manual = scatter_plot(x_s, y_s, z_s, color = "black", size = 3, opacity = 1.0)
    data.append(scatter_manual)
    if groundtruth_iso:
        
        x_o, y_o, z_o = zip(*groundtruth_iso)
        scatter_gt = scatter_plot(x_o, y_o, z_o, color = "blue", size = 3, opacity = 1.0, _name = "GT Iso Coord")
        data.append(scatter_gt)

    for i, iso in zip(range(0, len(fields)+1, 4), new_iso):
        if i == 12 :   #WE ARE MANAGING THE ARMS HERE
            if len(new_iso) == 6:
                color = "purple"
                rectangle_vertices = np.array([
                (iso[0] +fields[i][0] , iso[1], iso[2]+fields[i+1][0]),  # Corner 1
                (iso[0]+fields[i][1], iso[1],iso[2]+fields[i+1][0]),  # Corner 2 
                (iso[0]+fields[i][1], iso[1],iso[2]+fields[i+1][1]),      # Corner 3
                (iso[0]+fields[i][0], iso[1],iso[2]+fields[i+1][1]),  # Corner 4
                (iso[0] +fields[i][0] , iso[1], iso[2]+fields[i+1][0])   # Close the rectangle
                ])

                # Create a line plot for the rectangle Fields
                rectangle_lines = go.Scatter3d(
                    x=rectangle_vertices[:, 0],
                    y=rectangle_vertices[:, 1],
                    z=rectangle_vertices[:, 2],
                    mode='lines',
                    line=dict(
                        color=color,
                        width=3
                    ),
                    name="Right Arm Field",
                    showlegend=True
                )
                data.append(rectangle_lines)
            else:
                for f in range(2):
                    idx = (i-4)+f*2
                    _name="Abd Field"
                    if f % 2 == 0:
                        color = 'red'
                    else:
                        color = 'blue'
                    # Define rectangle corners in 3D space
                    plot_rectangle_field(fields, data, iso, color, idx, _name)

                

        if i == 16 :   #WE ARE MANAGING THE ARMS HERE
            if len(new_iso) == 6:
                color = "purple"
                rectangle_vertices = np.array([
                (iso[0] +fields[i-2][0] , iso[1], iso[2]+fields[i-1][0]),  # Corner 1
                (iso[0]+fields[i-2][1], iso[1],iso[2]+fields[i-1][0]),  # Corner 2 
                (iso[0]+fields[i-2][1], iso[1],iso[2]+fields[i-1][1]),      # Corner 3
                (iso[0]+fields[i-2][0], iso[1],iso[2]+fields[i-1][1]),  # Corner 4
                (iso[0] +fields[i-2][0] , iso[1], iso[2]+fields[i-1][0])   # Close the rectangle
                ])

                # Create a line plot for the rectangle borders
                rectangle_lines = go.Scatter3d(
                    x=rectangle_vertices[:, 0],
                    y=rectangle_vertices[:, 1],
                    z=rectangle_vertices[:, 2],
                    mode='lines',
                    line=dict(
                        color=color,
                        width=3
                    ),
                    name="Left Arm Border",
                    showlegend=True
                )
                data.append(rectangle_lines)
            else:
                for f in range(2):
                    idx = (i-4)+f*2
                    _name="Pelvis Field"
                    if f % 2 == 0:
                        color = 'red'
                    else:
                        color = 'blue'
                    # Define rectangle corners in 3D space
                    plot_rectangle_field(fields, data, iso, color, idx, _name)
        if i == 20 :   #WE ARE MANAGING THE ARMS HERE
            for f in range(2):
                idx = (i-4)+f*2
                _name="Legs Field"
                # Define rectangle corners in 3D space
                plot_rectangle_field(fields, data, iso, color, idx, _name)

        if i < 12:  
            for f in range(2):
                idx = i+f*2
                if f % 2 == 0:
                    color = 'red'
                else:
                    color = 'blue'
                if i == 0:
                    _name = 'Head Field'
                if i == 4:
                    _name = 'Thorax Field'
                if i == 8:
                    _name = 'Column Field'
                    
                # Define rectangle corners in 3D space
                plot_rectangle_field(fields, data, iso, color, idx, _name)

    layout = go.Layout(scene=dict(aspectmode="data"), title = f"TMI geometry. 2D RMSE: {rmse[0]}, 3D RMSE: {rmse[1]}" )
    fig = go.Figure(data=data, layout=layout)
    hover_text = [f'Index: {index}' for index in range(len(vertices))]
    fig.data[0]['text'] = hover_text

    pio.write_image(fig, f'/home/ubuntu/giorgio_longari/DeformationTMI/output/plot_{name}.png')
    pio.write_html(fig, f'/home/ubuntu/giorgio_longari/DeformationTMI/output/plot_{name}.html')
    #fig.show()

    return True

def plot_rectangle_field(fields, data, iso, color, idx, _name):
    rectangle_vertices = np.array([
                    (iso[0] +fields[idx+1][0] , iso[1], iso[2]+fields[idx][0]),  
                    (iso[0]+fields[idx+1][1], iso[1],iso[2]+fields[idx][0]),  
                    (iso[0]+fields[idx+1][1], iso[1],iso[2]+fields[idx][1]),      
                    (iso[0]+fields[idx+1][0], iso[1],iso[2]+fields[idx][1]),  
                    (iso[0] +fields[idx+1][0] , iso[1], iso[2]+fields[idx][0])   
                ])

                # Create a line plot for the rectangle Fields
    rectangle_lines = go.Scatter3d(
                    x=rectangle_vertices[:, 0],
                    y=rectangle_vertices[:, 1],
                    z=rectangle_vertices[:, 2],
                    mode='lines',
                    line=dict(
                        color=color,
                        width=3
                    ),
                    name= _name,
                    showlegend=True
                )
    data.append(rectangle_lines)

def scatter_plot(x_s, y_s, z_s, color, size, opacity , _name = "Iso Coord"):
    scatter_manual = go.Scatter3d(
        x=x_s,
        y=y_s,
        z=z_s,
        mode='markers',
        marker=dict(
            size=size,  # Larger size for manual points
            color=color,  # Use a fixed color (e.g., red)
            opacity=opacity
        ),
        name = _name
    )
    
    return scatter_manual

def scatter_data(x, y, z, _name = "Mesh Points" ):
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
        name = _name
        
    )
    
    return scatter_isocenters
