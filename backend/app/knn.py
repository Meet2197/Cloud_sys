from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import numpy as np

def compute_clusters(items: List[Dict[str, Any]], n_neighbors: int = 5):
    corpus = []
    ids = []
    for it in items:
        meta_keys = " ".join((it.get("meta_json") or {}).keys()) if isinstance(it.get("meta_json"), dict) else ""
        text = f"{it.get('name','')} {it.get('tags','')} {meta_keys}"
        corpus.append(text)
        ids.append(it["id"])

    if not corpus:
        return {"assignments": {}, "edges": []}

    vec = TfidfVectorizer().fit_transform(corpus)
    nn = NearestNeighbors(n_neighbors=min(n_neighbors, vec.shape[0]), metric="cosine")
    nn.fit(vec)
    distances, indices = nn.kneighbors(vec)

    n = len(ids)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    edges = []
    for i in range(n):
        for j_idx in indices[i][1:]:
            union(i, j_idx)
            edges.append((ids[i], ids[j_idx]))

    roots = {}
    cluster_id = 0
    assignments = {}
    for i in range(n):
        r = find(i)
        if r not in roots:
            roots[r] = cluster_id
            cluster_id += 1
        assignments[ids[i]] = roots[r]

    return {"assignments": assignments, "edges": edges}
