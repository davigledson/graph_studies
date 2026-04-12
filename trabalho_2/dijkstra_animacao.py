import json
import heapq
import math
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import networkx as nx

JSON_PADRAO  = "matriz_de_adjacencia.json"
START_PADRAO = "Recife"
END_PADRAO   = "Porto das Dunas"

def carregar_grafo(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

json_path = sys.argv[1] if len(sys.argv) > 1 else JSON_PADRAO
START     = sys.argv[2] if len(sys.argv) > 2 else START_PADRAO
END       = sys.argv[3] if len(sys.argv) > 3 else END_PADRAO

try:
    grafo = carregar_grafo(json_path)
    print(f"Grafo carregado: {json_path} ({len(grafo)} cidades)")
except FileNotFoundError:
    print(f"Erro: arquivo '{json_path}' nao encontrado.")
    sys.exit(1)

if START not in grafo:
    print(f"Erro: cidade de origem '{START}' nao encontrada no grafo.")
    sys.exit(1)
if END not in grafo:
    print(f"Erro: cidade de destino '{END}' nao encontrada no grafo.")
    sys.exit(1)

G_temp = nx.Graph()
for u, vizinhos in grafo.items():
    for v, w in vizinhos.items():
        G_temp.add_edge(u, v, weight=w)

pos_nx = nx.spring_layout(G_temp, seed=42, k=0.4)

xs = [p[0] for p in pos_nx.values()]
ys = [p[1] for p in pos_nx.values()]
xmin, xmax = min(xs), max(xs)
ymin, ymax = min(ys), max(ys)

def norm(val, vmin, vmax):
    if vmax == vmin:
        return 0.5
    return 0.05 + 0.90 * (val - vmin) / (vmax - vmin)

pos = {
    city: (norm(p[0], xmin, xmax), norm(p[1], ymin, ymax))
    for city, p in pos_nx.items()
}

# =============================================================
# DIJKSTRA COM CAPTURA DE FRAMES
# =============================================================

def dijkstra_frames(grafo, start, end):
    dist = {c: math.inf for c in grafo}
    prev = {c: None for c in grafo}
    dist[start] = 0
    pq = [(0, start)]
    visited = set()
    frames = []

    frames.append({
        "visited": set(),
        "frontier": {start},
        "current": None,
        "active_edges": set(),
        "short_path": [],
        "dist": dict(dist),
        "msg": f"Inicio: {start}  |  distancia = 0 km",
        "done": False,
    })

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        active_edges = set()

        for v, w in grafo[u].items():
            edge = tuple(sorted([u, v]))
            active_edges.add(edge)
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

        frontier = {n for d2, n in pq if n not in visited}

        frames.append({
            "visited": set(visited),
            "frontier": frontier,
            "current": u,
            "active_edges": active_edges,
            "short_path": [],
            "dist": dict(dist),
            "msg": f"Visitando: {u}  |  distancia acumulada = {d:.1f} km",
            "done": False,
        })

        if u == end:
            break

    path = []
    cur = end
    while cur:
        path.append(cur)
        cur = prev[cur]
    path.reverse()

    short_edges = [tuple(sorted([path[i], path[i+1]])) for i in range(len(path)-1)]
    total_dist = dist[end]

    frames.append({
        "visited": set(visited),
        "frontier": set(),
        "current": end,
        "active_edges": set(),
        "short_path": short_edges,
        "dist": dict(dist),
        "msg": f"Caminho minimo: {' -> '.join(path)}  |  Distancia total: {total_dist:.1f} km",
        "done": True,
        "path": path,
        "total_dist": total_dist,
    })

    return frames

# =============================================================
# ANIMACAO COM MATPLOTLIB
# =============================================================

frames = dijkstra_frames(grafo, START, END)

G = nx.Graph()
for u, vizinhos in grafo.items():
    for v, w in vizinhos.items():
        G.add_edge(u, v, weight=w)

fig, ax = plt.subplots(figsize=(16, 9))
fig.patch.set_facecolor("#0f1923")
ax.set_facecolor("#0f1923")
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.axis("off")

COR_DEFAULT        = "#2a5a8a"
COR_VISITADO       = "#2d7a4f"
COR_FRONTEIRA      = "#c87c1a"
COR_CAMINHO        = "#c0392b"
COR_ORIGEM         = "#7c4bc0"
COR_ATUAL          = "#e8c84a"
COR_ARESTA         = "#1e3a5f"
COR_ARESTA_ATIVA   = "#c87c1a"
COR_ARESTA_CAMINHO = "#c0392b"

def draw_frame(frame_data):
    ax.clear()
    ax.set_facecolor("#0f1923")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.axis("off")

    visited      = frame_data["visited"]
    frontier     = frame_data["frontier"]
    current      = frame_data["current"]
    active_edges = frame_data["active_edges"]
    short_path   = frame_data["short_path"]
    dist         = frame_data["dist"]
    msg          = frame_data["msg"]
    done         = frame_data["done"]

    for u, v, data in G.edges(data=True):
        edge = tuple(sorted([u, v]))
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        if edge in short_path:
            color, lw, zorder = COR_ARESTA_CAMINHO, 3.5, 3
        elif edge in active_edges:
            color, lw, zorder = COR_ARESTA_ATIVA, 2.5, 2
        else:
            color, lw, zorder = COR_ARESTA, 1.0, 1
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw,
                zorder=zorder, solid_capstyle="round")

        # CORRIGIDO: label de km exibido em TODAS as arestas
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my, f"{data['weight']:.0f}km",
                fontsize=6.5, color="#aaaaaa", ha="center", va="center", zorder=4,
                bbox=dict(boxstyle="round,pad=0.1", facecolor="#0f1923",
                          edgecolor="none", alpha=0.7))

    for city in G.nodes():
        x, y = pos[city]

        if done and city in frame_data.get("path", []):
            color, size, zorder = COR_CAMINHO, 160, 6
        elif city == START or city == END:
            color, size, zorder = COR_ORIGEM, 180, 6
        elif city == current:
            color, size, zorder = COR_ATUAL, 200, 7
        elif city in visited:
            color, size, zorder = COR_VISITADO, 140, 5
        elif city in frontier:
            color, size, zorder = COR_FRONTEIRA, 150, 5
        else:
            color, size, zorder = COR_DEFAULT, 120, 4

        ax.scatter(x, y, s=size, c=color, zorder=zorder,
                   edgecolors="#0f1923", linewidths=1.5)

        d_val = dist.get(city, math.inf)
        d_str = f"{d_val:.0f}" if d_val != math.inf else "inf"
        ax.text(x, y + 0.04, city, fontsize=7, color="white",
                ha="center", va="bottom", fontweight="bold", zorder=8)
        ax.text(x, y - 0.045, d_str + " km", fontsize=6.5, color="#aaaaaa",
                ha="center", va="top", zorder=8)

    ax.text(0.5, 0.01, msg, fontsize=9, color="white", ha="center", va="bottom",
            transform=ax.transAxes, zorder=10,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#1a2a3a",
                      edgecolor="#2a4a6a", alpha=0.9))

    ax.set_title(f"Algoritmo de Dijkstra  |  {START} -> {END}",
                 color="white", fontsize=12, pad=10, fontweight="bold")

    legend_items = [
        mpatches.Patch(color=COR_ORIGEM,    label="Origem / Destino"),
        mpatches.Patch(color=COR_ATUAL,     label="No atual"),
        mpatches.Patch(color=COR_FRONTEIRA, label="Fronteira"),
        mpatches.Patch(color=COR_VISITADO,  label="Visitado"),
        mpatches.Patch(color=COR_CAMINHO,   label="Caminho minimo"),
        mpatches.Patch(color=COR_DEFAULT,   label="Nao visitado"),
    ]
    ax.legend(handles=legend_items, loc="upper left", fontsize=8,
              facecolor="#1a2a3a", edgecolor="#2a4a6a", labelcolor="white",
              framealpha=0.9, ncol=2)

def animate(i):
    draw_frame(frames[i])

ani = animation.FuncAnimation(
    fig, animate,
    frames=len(frames),
    interval=900,
    repeat=False
)

plt.tight_layout()
plt.show()