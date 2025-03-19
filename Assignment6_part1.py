import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np
random.seed(42)
np.random.seed(42)

df = pd.read_csv("hero-network.csv", header=None, names=["Source", "Target"])

# weight of 1 for each connection
df["Weight"] = 1

df.drop_duplicates(inplace=True)

# graph
G = nx.from_pandas_edgelist(df, source="Source", target="Target", edge_attr="Weight")

# remove self-loops
if nx.number_of_selfloops(G) > 0:
    print("Removing self-loops.")
    G.remove_edges_from(nx.selfloop_edges(G))

# check graph connectivity
if not nx.is_connected(G):
    print("The graph is not connected. Calculating centralities for each component.")
    bet_cen = {}
    eig_cen = {}
    deg_cen = {}
    
    # connected components
    components = [G.subgraph(c).copy() for c in nx.connected_components(G)]
    
    # rough centralities for each component
    for idx, component in enumerate(components):
        print(f"Calculating approximate centralities for component {idx + 1} with {len(component.nodes())} nodes...")
        
        # make k does not exceed the number of nodes in the component
        k = min(len(component.nodes()), 100)
        
        # rough betweenness centrality using sampling
        bet_cen.update(nx.betweenness_centrality(component, normalized=True, endpoints=False, weight="Weight", k=k))
        
        # eigenvector centrality
        eig_cen.update(nx.eigenvector_centrality(component, weight="Weight"))
        
        # degree centrality
        deg_cen.update(nx.degree_centrality(component))
    
else:
    print("The graph is connected. Calculating centralities for the entire graph")
    # rough betweenness centrality for the entire graph
    bet_cen = nx.betweenness_centrality(G, normalized=True, endpoints=False, weight="Weight", k=100)
    
    # eigenvector centrality for the entire graph
    eig_cen = nx.eigenvector_centrality(G, weight="Weight")
    
    # degree centrality for the entire graph
    deg_cen = nx.degree_centrality(G)

# centralities in a dataframe
bet_cen_df = pd.DataFrame(list(bet_cen.items()), columns=["Superhero", "Betweenness Centrality"]).sort_values(by="Betweenness Centrality", ascending=False)
eig_cen_df = pd.DataFrame(list(eig_cen.items()), columns=["Superhero", "Eigenvector Centrality"]).sort_values(by="Eigenvector Centrality", ascending=False)
deg_cen_df = pd.DataFrame(list(deg_cen.items()), columns=["Superhero", "Degree Centrality"]).sort_values(by="Degree Centrality", ascending=False)

# store top 5 superheroes for each centrality
top_5_bet_cen = bet_cen_df.head(5)
top_5_eig_cen = eig_cen_df.head(5)
top_5_deg_cen = deg_cen_df.head(5)

# top 5 superheroes for each centrality
print("Top 5 superheroes by Betweenness Centrality:")
print(top_5_bet_cen)
print("\nTop 5 superheroes by Eigenvector Centrality:")
print(top_5_eig_cen)
print("\nTop 5 superheroes by Degree Centrality:")
print(top_5_deg_cen)

#Q1 plot the centralities of the top superheroes for each
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# betweenness centrality plot
top_5_bet_cen.plot(kind="barh", x="Superhero", y="Betweenness Centrality", ax=axes[0], color="skyblue", legend=False)
axes[0].set_xlabel("Betweenness Centrality")
axes[0].set_title("Top 5 Superheroes by Betweenness Centrality")

# eigenvector centrality plot
top_5_eig_cen.plot(kind="barh", x="Superhero", y="Eigenvector Centrality", ax=axes[1], color="lightgreen", legend=False)
axes[1].set_xlabel("Eigenvector Centrality")
axes[1].set_title("Top 5 Superheroes by Eigenvector Centrality")

# degree centrality plot
top_5_deg_cen.plot(kind="barh", x="Superhero", y="Degree Centrality", ax=axes[2], color="lightcoral", legend=False)
axes[2].set_xlabel("Degree Centrality")
axes[2].set_title("Top 5 Superheroes by Degree Centrality")

plt.tight_layout()
plt.show()

#Q2 find the superhero with the fewest connections (direct degree)
min_connections = min(G.degree(), key=lambda x: x[1])
print(f"Superhero with the fewest connections: {min_connections[0]} with {min_connections[1]} connections")

#Q3 get the number of connections in the network
num_connections = G.number_of_edges()
print(f"The number of connections in the network is: {num_connections}")


