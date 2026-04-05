import json
import heapq
# =============================================================
# GRAFO: Rota Turística Litorânea
# Recife (PE) -> Fortaleza (CE)
# Distâncias em km por rodovias reais
# =============================================================

def carregar_grafo(arquivo="matriz_de_adjacencia.json"):
    with open(arquivo, "r", encoding="utf-8") as f:
        return json.load(f)

grafo = carregar_grafo()

def dijkstra(grafo, start_city, end_city):
    """
    Implementa o algoritmo de Dijkstra para encontrar o caminho mais curto.
    Recebe o grafo como dicionário de adjacência.
    Retorna: (distancia_total, caminho)
    """
    if start_city not in grafo or end_city not in grafo:
        return float('inf'), []

    distances = {city: float('inf') for city in grafo}
    distances[start_city] = 0

    # Fila de prioridade: (distancia, cidade_atual, caminho_percorrido)
    priority_queue = [(0, start_city, [start_city])]

    while priority_queue:
        current_distance, current_city, path = heapq.heappop(priority_queue)

        # Se já encontramos caminho mais curto para este nó, ignoramos
        if current_distance > distances[current_city]:
            continue

        # Chegamos ao destino
        if current_city == end_city:
            return current_distance, path

        # Explora os vizinhos
        for neighbor, weight in grafo[current_city].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                new_path = path + [neighbor]
                heapq.heappush(priority_queue, (distance, neighbor, new_path))

    return float('inf'), []


# =============================================================
# EXECUÇÃO
# =============================================================

if __name__ == "__main__":
    origem = "Recife"
    destino = "Porto das Dunas"

    print(f"\nCaminho mais curto: {origem} -> {destino}")

    distancia, caminho = dijkstra(grafo, origem, destino)

    if distancia != float('inf'):
        print(f"  Distancia total : {distancia:.1f} km")
        print(f"  Caminho         : {' -> '.join(caminho)}")
    else:
        print("  Nenhum caminho encontrado.")