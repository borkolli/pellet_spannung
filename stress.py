import pandas as pd
import matplotlib.pyplot as plt

input_filename = 'datasets/1run_225_end_compression_particle-data.csv'

# Read the CSV into a pandas DataFrame
df = pd.read_csv(input_filename, skiprows=[1])

new_column_names = {
    'Tensile Stress': 'stress_tensile',
    'Particle ID From': 'id_from',
    'Shear Stress': 'stress_shear',
    'Coordinate : Y': 'pos_y',
    'von Mises Stress': 'stress_mises',
    'Coordinate : X': 'pos_x',
    'Coordinate : Z': 'pos_z',
    'Particle ID To': 'id_to',
}

df.rename(columns=new_column_names, inplace=True)

columns_to_drop = ['id_from', 'id_to', 'stress_mises', 'stress_shear']
df.drop(columns=columns_to_drop, inplace=True)

desired_order = ['pos_x', 'pos_y', 'pos_z', 'stress_tensile']

df = df[desired_order].copy()

df['pos_x'] *= 1e6
df['pos_y'] *= 1e6
df['pos_z'] *= 1e6
df['radius'] = (df['pos_x']**2 + df['pos_y']**2).apply(lambda x: x**0.5)

df_high_stress = df[df.stress_tensile >= df.stress_tensile.max() * 0.5]

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Scatter plot with pos_x, pos_y, pos_z as coordinates and stress_tensile as color
scatter = ax.scatter(df_high_stress['pos_x'], df_high_stress['pos_y'], df_high_stress['pos_z'],
                     c=df_high_stress['stress_tensile'], cmap='viridis')

# Add labels
ax.set_xlabel('pos_x')
ax.set_ylabel('pos_y')
ax.set_zlabel('pos_z')
ax.set_title('3D Scatter Plot')

# Add colorbar
cbar = fig.colorbar(scatter, ax=ax, label='stress_tensile')

# Show the plot
plt.show()
