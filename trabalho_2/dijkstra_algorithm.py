import heapq

# =============================================================
# GRAFO: Rota Turística Litorânea
# Recife (PE) -> Fortaleza (CE)
# Distâncias em km por rodovias reais
# =============================================================

grafo = {
    # 1 - Origem
    "Recife": {
        "Olinda": 5.0,
        "Paulista": 15.0,
        "Goiana": 61.0,
        "Joao Pessoa": 116.0
    },
    # 2
    "Olinda": {
        "Recife": 6.0,
        "Paulista": 11.0,
        "Goiana": 55.0
    },
    # 3
    "Paulista": {
        "Recife": 16.0,
        "Olinda": 11.0,
        "Goiana": 49.0
    },
    # 4
    "Goiana": {
        "Recife": 60.0,
        "Olinda": 56.0,
        "Paulista": 49.0,
        "Pitimbu": 32.0,
        "Joao Pessoa": 60.0
    },
    # 5
    "Pitimbu": {
        "Goiana": 32.0,
        "Conde": 30.2
    },
    # 6
    "Conde": {
        "Pitimbu": 30.2,
        "Joao Pessoa": 24.5
    },
    # 7
    "Joao Pessoa": {
        "Recife": 116.4,
        "Goiana": 60.0,
        "Conde": 24.5,
        "Cabedelo": 18.1,
        "Baia Formosa": 85.0,
        "Tibau do Sul (Pipa)": 90.0,
        "Natal": 179.8
    },
    # 8
    "Cabedelo": {
        "Joao Pessoa": 18.1,
        "Baia Formosa": 70.0
    },
    # 9
    "Baia Formosa": {
        "Joao Pessoa": 85.0,
        "Cabedelo": 70.0,
        "Tibau do Sul (Pipa)": 35.4
    },
    # 10
    "Tibau do Sul (Pipa)": {
        "Joao Pessoa": 90.0,
        "Baia Formosa": 35.4,
        "Nisia Floresta": 44.8
    },
    # 11
    "Nisia Floresta": {
        "Tibau do Sul (Pipa)": 44.8,
        "Natal": 29.6
    },
    # 12
    "Natal": {
        "Joao Pessoa": 179.8,
        "Nisia Floresta": 29.6,
        "Extremoz (Genipabu)": 19.8,
        "Touros": 90.0,
        "Mossoro": 281.4,
        "Fortaleza": 515.2
    },
    # 13
    "Extremoz (Genipabu)": {
        "Natal": 19.8,
        "Touros": 80.0,
        "Mossoro": 250.0
    },
    # 14
    "Touros": {
        "Natal": 90.0,
        "Extremoz (Genipabu)": 80.0,
        "Sao Miguel Gostoso": 24.7,
        "Mossoro": 180.0
    },
    # 15
    "Sao Miguel Gostoso": {
        "Touros": 24.7,
        "Tibau": 140.0
    },
    # 16
    "Mossoro": {
        "Natal": 281.4,
        "Extremoz (Genipabu)": 250.0,
        "Touros": 180.0,
        "Tibau": 60.0,
        "Icapui (Canoa Quebrada)": 100.0,
        "Aracati": 140.0,
        "Beberibe": 220.0,
        "Aquiraz": 240.0
    },
    # 17
    "Tibau": {
        "Sao Miguel Gostoso": 140.0,
        "Mossoro": 60.0,
        "Icapui (Canoa Quebrada)": 31.2
    },
    # 18
    "Icapui (Canoa Quebrada)": {
        "Mossoro": 100.0,
        "Tibau": 31.2,
        "Aracati": 49.6
    },
    # 19
    "Aracati": {
        "Mossoro": 140.0,
        "Icapui (Canoa Quebrada)": 49.6,
        "Beberibe": 64.8,
        "Fortaleza": 150.0
    },
    # 20
    "Beberibe": {
        "Mossoro": 220.0,
        "Aracati": 64.8,
        "Aquiraz": 54.2
    },
    # 21
    "Aquiraz": {
        "Mossoro": 240.0,
        "Beberibe": 54.2,
        "Fortaleza": 30.5
    },
    # 22 - Destino
    "Fortaleza": {
        "Natal": 515.2,
        "Aracati": 150.0,
        "Aquiraz": 30.5
    }
}

# =============================================================
# ALGORITMO DE DIJKSTRA
# =============================================================

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
    testes = [
        ("Recife", "Fortaleza"),
        ("Recife", "Natal"),
        ("Recife", "Tibau do Sul (Pipa)"),
    ]

    for start, end in testes:
        print(f"\nCaminho mais curto: {start} -> {end}")
        distancia, caminho = dijkstra(grafo, start, end)
        if distancia != float('inf'):
            print(f"  Distancia total : {distancia:.1f} km")
            print(f"  Caminho         : {' -> '.join(caminho)}")
        else:
            print(f"  Nenhum caminho encontrado.")