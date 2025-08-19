import networkx as nx
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

DEFAULT_STYLE = {
    "node_color": "red",
    "edge_color": "skyblue",
    "node_size": 12,
    "bg_color": "white",
    "font_size": 14
}

def _style(style):
    s = DEFAULT_STYLE.copy()
    s.update(style or {})
    return s

def build_sankey(df: pd.DataFrame, style: dict):
    s = _style(style)
    if df is None or df.empty:
        return go.Figure()

    labels = list(pd.unique(df['Host_Genome'].tolist() + df['Plasmid_ID'].tolist() + df['Environment'].tolist()))
    label_map = {label: i for i, label in enumerate(labels)}
    source = df['Host_Genome'].map(label_map)
    target = df['Plasmid_ID'].map(label_map)
    env_source = df['Plasmid_ID'].map(label_map)
    env_target = df['Environment'].map(label_map)
    link_source = pd.concat([source, env_source])
    link_target = pd.concat([target, env_target])

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=s['node_size'],
            line=dict(color="black", width=0.5),
            label=labels,
            color=s['node_color']
        ),
        link=dict(
            source=link_source,
            target=link_target,
            value=[1]*len(link_source),
            color=s['edge_color']
        )
    )])
    fig.update_layout(
        title_text="Flow of Genetic Material via Plasmids",
        font_size=s['font_size'],
        paper_bgcolor=s['bg_color'],
        margin=dict(l=50, r=50, t=60, b=40)
    )
    return fig

def build_network(df: pd.DataFrame, style: dict):
    s = _style(style)
    if df is None or df.empty:
        return go.Figure()

    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_node(row['Plasmid_ID'], type='plasmid')
        G.add_node(row['Environment'], type='environment')
        G.add_edge(row['Plasmid_ID'], row['Environment'])

    pos = nx.spring_layout(G, seed=42, k=0.3/len(G.nodes()) if len(G.nodes()) > 0 else 0.3)

    edge_x, edge_y = [], []
    for a, b in G.edges():
        x0, y0 = pos[a]
        x1, y1 = pos[b]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    node_x, node_y, node_text = [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines',
                             line=dict(width=1, color=s['edge_color']), hoverinfo='none'))
    fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text', text=node_text,
                             textposition="top center",
                             marker=dict(size=s['node_size'], color=s['node_color'])))
    fig.update_layout(
        title="Network of Shared Plasmids Across Environments",
        showlegend=False,
        paper_bgcolor=s['bg_color'],
        font_size=s['font_size'],
        margin=dict(l=10, r=10, t=60, b=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    fig.update_layout(dragmode='pan')
    return fig

def build_heatmap(df: pd.DataFrame, scale: str, style: dict):
    s = _style(style)
    if df is None or df.empty:
        return go.Figure()

    melted = df.melt(id_vars=['Plasmid_ID'],
                     value_vars=['ARGs', 'Virulence', 'T4SS', 'MGEs'],
                     var_name='Trait', value_name='Presence')
    melted['Binary'] = melted['Presence'].apply(lambda x: 1 if str(x).lower() != 'no' else 0)
    heat_df = melted.pivot(index='Plasmid_ID', columns='Trait', values='Binary').fillna(0)
    fig = px.imshow(heat_df, text_auto=True, color_continuous_scale=scale, aspect='auto')
    fig.update_layout(
        title="Presence of Plasmid-Associated Traits",
        font=dict(size=s['font_size']),
        paper_bgcolor=s['bg_color'],
        margin=dict(l=40, r=40, t=60, b=30)
    )
    return fig