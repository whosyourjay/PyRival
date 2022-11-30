INF = float("inf")

lvl = []
ptr = []
adj = [[] for _ in range(n + 1)]
def add_edge(a, b, cap, rcap=0):
    adj[a].append([b, len(adj[b]), cap, 0])
    adj[b].append([a, len(adj[a]) - 1, rcap, 0])

def add_flow(vert, pos, aug):
    nei, pair, cap, use = adj[vert][pos]
    adj[vert][pos][3] += aug
    adj[nei][pair][3] -= aug

def dfs(src, dest):
    aug, found = 0, False

    stack = [(src, INF)]
    while stack:
        vert, limit = stack[-1]

        if found:
            ptr[vert] -= 1
            add_flow(vert, ptr[vert], aug)
            stack.pop()
            continue

        if vert == dest:
            found = True
            aug = limit
            stack.pop()
            continue

        if ptr[vert] < len(adj[vert]):
            nei, pair, cap, use = adj[vert][ptr[vert]]
            if lvl[nei] == lvl[vert] + 1 and cap > use:
                stack.append((nei, min(limit, cap - use)))
            ptr[vert] += 1
        else:
            stack.pop()
    return aug

def calc(src, dest):
    print(n)
    cue = [0] * (n + 1)
    flow, cue[0] = 0, src
    for l in range(31):  # l = 30 maybe faster for random data
        while True:
            lvl[:], ptr[:] = [0] * len(cue), [0] * len(cue)
            qi, qe, lvl[src] = 0, 1, 1
            while qi < qe and not lvl[dest]:
                vert = cue[qi]
                qi += 1
                for nei, pair, cap, use in adj[vert]:
                    if not lvl[nei] and (cap - use) >> (30 - l):
                        cue[qe] = nei
                        qe += 1
                        lvl[nei] = lvl[vert] + 1

            aug = dfs(src, dest)
            while aug:
                flow += aug
                aug = dfs(src, dest)

            if not lvl[dest]:
                break

    return flow
