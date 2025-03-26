import streamlit as st
import random
import pandas as pd
import numpy as np
import pandas as pd                        
from pytrends.request import TrendReq
import networkx as nx
import matplotlib.pyplot as plt
from streamlit_agraph import agraph, Node, Edge, Config

def app():
    # # Define the heads, relations, and tails
    # head = ['drugA', 'drugB', 'drugC', 'drugD', 'drugA', 'drugC', 'drugD', 'drugE', 'gene1', 'gene2','gene3', 'gene4', 'gene50', 'gene2', 'gene3', 'gene4']
    # relation = ['treats', 'treats', 'treats', 'treats', 'inhibits', 'inhibits', 'inhibits', 'inhibits', 'associated', 'associated', 'associated', 'associated', 'associated', 'interacts', 'interacts', 'interacts']
    # tail = ['fever', 'hepatitis', 'bleeding', 'pain', 'gene1', 'gene2', 'gene4', 'gene20', 'obesity', 'heart_attack', 'hepatitis', 'bleeding', 'cancer', 'gene1', 'gene20', 'gene50']

    # # Create a dataframe
    # df = pd.DataFrame({'head': head, 'relation': relation, 'tail': tail})
    # st.dataframe(df)


    # # Create a knowledge graph
    # G = nx.Graph()
    # for _, row in df.iterrows():
    #     G.add_edge(row['head'], row['tail'], label=row['relation'])

    # # Visualize the knowledge graph
    # pos = nx.spring_layout(G, seed=42, k=0.9)
    # labels = nx.get_edge_attributes(G, 'label')
    # plt.figure(figsize=(12, 10))
    # nx.draw(G, pos, with_labels=True, font_size=10, node_size=700, node_color='lightblue', edge_color='gray', alpha=0.6)
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8, label_pos=0.3, verticalalignment='baseline')
    # plt.title('Knowledge Graph')
    # plt.show()

    # Set Page Configuration
    # st.set_page_config(layout="wide")

    st.title("Test Title")

    # Define the nodes
    nodes = [
        Node(id="id1", label="label1", color="#4B0082"),
        Node(id="id2", label="label2", color="#4B0082")
    ]

    # Define the edges
    edges = [
        Edge(source="id1", target="id2")
    ]

    # Configure the graph
    config = Config(
        width=900,
        height=900,
        directed=True,
        nodeHighlightBehavior=True,
        highlightColor="#F7A7A6",
        collapsible=False,
        node={'labelProperty': 'label'},
        link={'labelProperty': 'label', 'renderLabel': False},
        hierarchical=True,
        hierarchicalSorting=True,
        layout={
            "hierarchical": {
                "enabled": True,
                "levelSeparation": 150,
                "nodeSpacing": 100,
                "treeSpacing": 200,
                "direction": "UD",  # UD for top to bottom
                "sortMethod": "directed"
            }
        },
            # Set initial zoom level
        zoom=1.2  # Adjust as needed
    )


    # Display the graph
    agraph(nodes=nodes, edges=edges, config=config)
    
    