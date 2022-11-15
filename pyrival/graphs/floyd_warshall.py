def floyd_warshall(n, edges):
    dist = [[0 if i == j else float("inf") for i in range(n)] for j in range(n)]
    pred = [[None] * n for _ in range(n)]

    for u, v, d in edges:
        dist[u][v] = d
        pred[u][v] = u

    for k in range(n):
        dist_k = dist[k]
        pred_k = pred[k]
        for i in range(n):
            dist_i = dist[i]
            dist_i_k = dist_i[k]
            pred_i = pred[i]
            for j in range(n):
                if dist_i[k] + dist_k[j] < dist_i[j]:
                    dist_i[j] = dist_i_k + dist_k[j]
                    pred_i[j] = pred_k[j]
    """Sanity Check
    for u, v, d in edges:
        if dist[u] + d < dist[v]:
            return None
    """

    return dist, pred
