import heapq
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import networkx as nx

# =============================================================
# GRAFO: Rota Litorânea Recife -> Fortaleza
# =============================================================

grafo = {
    "Recife":         {"Olinda":5,"Paulista":15,"Goiana":61,"Joao Pessoa":116},
    "Olinda":         {"Recife":6,"Paulista":11,"Goiana":55},
    "Paulista":       {"Recife":16,"Olinda":11,"Goiana":49},
    "Goiana":         {"Recife":60,"Olinda":56,"Paulista":49,"Pitimbu":32,"Joao Pessoa":60},
    "Pitimbu":        {"Goiana":32,"Conde":30.2},
    "Conde":          {"Pitimbu":30.2,"Joao Pessoa":24.5},
    "Joao Pessoa":    {"Recife":116,"Goiana":60,"Conde":24.5,"Cabedelo":18.1,"Baia Formosa":85,"Tibau do Sul":90,"Natal":179.8},
    "Cabedelo":       {"Joao Pessoa":18.1,"Baia Formosa":70},
    "Baia Formosa":   {"Joao Pessoa":85,"Cabedelo":70,"Tibau do Sul":35.4},
    "Tibau do Sul":   {"Joao Pessoa":90,"Baia Formosa":35.4,"Nisia Floresta":44.8},
    "Nisia Floresta": {"Tibau do Sul":44.8,"Natal":29.6},
    "Natal":          {"Joao Pessoa":179.8,"Nisia Floresta":29.6,"Extremoz":19.8,"Touros":90,"Mossoro":281.4,"Fortaleza":515.2},
    "Extremoz":       {"Natal":19.8,"Touros":80,"Mossoro":250},
    "Touros":         {"Natal":90,"Extremoz":80,"S.M.Gostoso":24.7,"Mossoro":180},
    "S.M.Gostoso":    {"Touros":24.7,"Tibau":140},
    "Mossoro":        {"Natal":281.4,"Extremoz":250,"Touros":180,"Tibau":60,"Icapui":100,"Aracati":140,"Beberibe":220,"Aquiraz":240},
    "Tibau":          {"S.M.Gostoso":140,"Mossoro":60,"Icapui":31.2},
    "Icapui":         {"Mossoro":100,"Tibau":31.2,"Aracati":49.6},
    "Aracati":        {"Mossoro":140,"Icapui":49.6,"Beberibe":64.8,"Fortaleza":150},
    "Beberibe":       {"Mossoro":220,"Aracati":64.8,"Aquiraz":54.2},
    "Aquiraz":        {"Mossoro":240,"Beberibe":54.2,"Fortaleza":30.5},
    "Fortaleza":      {"Natal":515.2,"Aracati":150,"Aquiraz":30.5},
}

AVG_SPEED_KMH = 80

# Posições geográficas aproximadas (lon, lat invertida para y)
pos = {
    "Recife":         (0.05, 0.05),
    "Olinda":         (0.08, 0.12),
    "Paulista":       (0.11, 0.18),
    "Goiana":         (0.16, 0.26),
    "Pitimbu":        (0.21, 0.32),
    "Conde":          (0.25, 0.38),
    "Joao Pessoa":    (0.30, 0.43),
    "Cabedelo":       (0.32, 0.50),
    "Baia Formosa":   (0.36, 0.44),
    "Tibau do Sul":   (0.40, 0.48),
    "Nisia Floresta": (0.45, 0.52),
    "Natal":          (0.50, 0.57),
    "Extremoz":       (0.53, 0.64),
    "Touros":         (0.57, 0.70),
    "S.M.Gostoso":    (0.61, 0.76),
    "Mossoro":        (0.60, 0.52),
    "Tibau":          (0.65, 0.70),
    "Icapui":         (0.69, 0.74),
    "Aracati":        (0.73, 0.78),
    "Beberibe":       (0.78, 0.82),
    "Aquiraz":        (0.88, 0.88),
    "Fortaleza":      (0.94, 0.93),
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
        "msg": f"Início: {start}  |  distância = 0 km",
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
            "msg": f"Visitando: {u}  |  distância acumulada = {d:.1f} km",
            "done": False,
        })

        if u == end:
            break

    # Reconstruir caminho mínimo
    path = []
    cur = end
    while cur:
        path.append(cur)
        cur = prev[cur]
    path.reverse()

    short_edges = [tuple(sorted([path[i], path[i+1]])) for i in range(len(path)-1)]
    total_dist = dist[end]
    total_min = round((total_dist / AVG_SPEED_KMH) * 60)
    horas = total_min // 60
    minutos = total_min % 60
    tempo_str = f"{horas}h {minutos}min" if horas > 0 else f"{minutos}min"

    frames.append({
        "visited": set(visited),
        "frontier": set(),
        "current": end,
        "active_edges": set(),
        "short_path": short_edges,
        "dist": dict(dist),
        "msg": (
            f"Caminho minimo: {' → '.join(path)}\n"
            f"Distancia total: {total_dist:.1f} km  |  Tempo estimado: {tempo_str} (a {AVG_SPEED_KMH} km/h)"
        ),
        "done": True,
        "path": path,
        "total_dist": total_dist,
        "tempo_str": tempo_str,
    })

    return frames

# =============================================================
# ANIMAÇÃO COM MATPLOTLIB
# =============================================================

START = "Recife"
END   = "Fortaleza"

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

# Cores
COR_DEFAULT   = "#2a5a8a"
COR_VISITADO  = "#2d7a4f"
COR_FRONTEIRA = "#c87c1a"
COR_CAMINHO   = "#c0392b"
COR_ORIGEM    = "#7c4bc0"
COR_DESTINO   = "#7c4bc0"
COR_ATUAL     = "#e8c84a"
COR_ARESTA    = "#1e3a5f"
COR_ARESTA_ATIVA = "#c87c1a"
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

    # Arestas
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
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, zorder=zorder, solid_capstyle="round")

        if edge in short_path or edge in active_edges:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx, my, f"{data['weight']:.0f}km",
                    fontsize=6.5, color="#aaaaaa", ha="center", va="center", zorder=4,
                    bbox=dict(boxstyle="round,pad=0.1", facecolor="#0f1923", edgecolor="none", alpha=0.7))

    # Nós
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

        ax.scatter(x, y, s=size, c=color, zorder=zorder, edgecolors="#0f1923", linewidths=1.5)

        label = city
        d_val = dist.get(city, math.inf)
        d_str = f"{d_val:.0f}" if d_val != math.inf else "∞"
        ax.text(x, y + 0.04, label, fontsize=7, color="white",
                ha="center", va="bottom", fontweight="bold", zorder=8)
        ax.text(x, y - 0.045, d_str + " km", fontsize=6.5, color="#aaaaaa",
                ha="center", va="top", zorder=8)

    # Mensagem
    ax.text(0.5, 0.01, msg, fontsize=9, color="white", ha="center", va="bottom",
            transform=ax.transAxes, zorder=10,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#1a2a3a", edgecolor="#2a4a6a", alpha=0.9))

    # Título
    ax.set_title(f"Algoritmo de Dijkstra — Rota Litorânea {START} → {END}",
                 color="white", fontsize=12, pad=10, fontweight="bold")

    # Legenda
    legend_items = [
        mpatches.Patch(color=COR_ORIGEM,    label="Origem / Destino"),
        mpatches.Patch(color=COR_ATUAL,     label="Nó atual"),
        mpatches.Patch(color=COR_FRONTEIRA, label="Fronteira"),
        mpatches.Patch(color=COR_VISITADO,  label="Visitado"),
        mpatches.Patch(color=COR_CAMINHO,   label="Caminho mínimo"),
        mpatches.Patch(color=COR_DEFAULT,   label="Não visitado"),
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

# Salvar como GIF
print("Gerando animação... isso pode levar alguns segundos.")
ani.save("/home/claude/dijkstra_animacao.gif", writer="pillow", fps=1.1, dpi=100)
print("GIF salvo!")

# Salvar frame final como PNG
draw_frame(frames[-1])
plt.savefig("/home/claude/dijkstra_final.png", dpi=150, bbox_inches="tight",
            facecolor="#0f1923")
print("Frame final salvo como PNG!")

plt.close()
