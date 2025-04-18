# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# Load the dataset
file_path = "C:\\Users\\FAIZAN AHMED\\OneDrive\\Desktop\\VS CODE\\CLG\\SEM 6\\MATHS\\emergency_dispatch_project\\911.csv"
df = pd.read_csv(file_path)

# Select relevant columns and drop NaN values
df = df[['timeStamp', 'title']].dropna()

# Convert 'timeStamp' to datetime format
df['timeStamp'] = pd.to_datetime(df['timeStamp'])

# Extract time-based features
df['Hour'] = df['timeStamp'].dt.hour
df['Day'] = df['timeStamp'].dt.day
df['Month'] = df['timeStamp'].dt.month

# Simulated Data: Assigning random times for Dispatch, Travel, and Response
np.random.seed(42)
df['Dispatch_Time'] = np.random.randint(5, 15, size=len(df))
df['Travel_Time'] = np.random.randint(3, 10, size=len(df))
df['Response_Time'] = np.random.randint(1, 5, size=len(df))

# Compute total time per emergency call (Before Optimization)
df['Total_Time'] = df['Dispatch_Time'] + df['Travel_Time'] + df['Response_Time']

# Create Directed Graph (Before Optimization)
G_before = nx.DiGraph()
for i in range(10):
    G_before.add_edge("Call Received", f"Dispatch_{i}", weight=df['Dispatch_Time'].iloc[i])
    G_before.add_edge(f"Dispatch_{i}", f"Travel_{i}", weight=df['Travel_Time'].iloc[i])
    G_before.add_edge(f"Travel_{i}", f"Response_{i}", weight=df['Response_Time'].iloc[i])

plt.figure(figsize=(12, 6))
pos = nx.spring_layout(G_before, seed=42)
labels = nx.get_edge_attributes(G_before, 'weight')
nx.draw(G_before, pos, with_labels=True, node_color='lightblue', edge_color='black', node_size=2000, font_size=8)
nx.draw_networkx_edge_labels(G_before, pos, edge_labels=labels)
plt.title("Emergency Dispatch Network (Before Optimization)")
plt.show()

# Apply Optimization (Reduce Response Time by 30% as Simulation)
df['Optimized_Time'] = df['Total_Time'] * 0.7

# Create Directed Graph (After Optimization)
G_after = nx.DiGraph()
for i in range(10):
    G_after.add_edge("Call Received", f"Dispatch_{i}", weight=df['Dispatch_Time'].iloc[i] * 0.7)
    G_after.add_edge(f"Dispatch_{i}", f"Travel_{i}", weight=df['Travel_Time'].iloc[i] * 0.7)
    G_after.add_edge(f"Travel_{i}", f"Response_{i}", weight=df['Response_Time'].iloc[i] * 0.7)

plt.figure(figsize=(12, 6))
pos = nx.spring_layout(G_after, seed=42)
labels = nx.get_edge_attributes(G_after, 'weight')
nx.draw(G_after, pos, with_labels=True, node_color='lightgreen', edge_color='black', node_size=2000, font_size=8)
nx.draw_networkx_edge_labels(G_after, pos, edge_labels=labels)
plt.title("Emergency Dispatch Network (After Optimization)")
plt.show()

# Compare Before vs. After Optimization
plt.figure(figsize=(12,6))
plt.plot(range(10), df['Total_Time'][:10], label="Before Optimization", color="red", linestyle="--", marker='o')
plt.plot(range(10), df['Optimized_Time'][:10], label="After Optimization", color="green", linewidth=2, marker='s')
plt.xlabel("Task Index")
plt.ylabel("Response Time (mins)")
plt.title("Emergency Dispatch Time Comparison (Before vs. After Optimization)")
plt.legend()
plt.grid(True)
plt.show()
