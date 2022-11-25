INF = float("inf")

graph = [[] for _ in range(n)]
lvl = [0] * n
ptr = [0] * n
class Dinic:
    def add_edge(self, a, b, cap, rcap=0):
        graph[a].append([b, len(graph[b]), cap, 0])
        graph[b].append([a, len(graph[a]) - 1, rcap, 0])

    def add_flow(self, vert, pos, aug):
        nei, pair, cap, use = graph[vert][pos]
        graph[vert][pos][3] += aug
        graph[nei][pair][3] -= aug


    def dfs(self, src, dest):
        aug, found = 0, False

        stack = [(src, INF)]
        while stack:
            vert, limit = stack[-1]

            if found:
                ptr[vert] -= 1
                self.add_flow(vert, ptr[vert], aug)
                stack.pop()
                continue

            if vert == dest:
                found = True
                aug = limit
                stack.pop()
                continue

            if ptr[vert] < len(graph[vert]):
                nei, pair, cap, use = graph[vert][ptr[vert]]
                if lvl[nei] == lvl[vert] + 1 and cap > use:
                    stack.append((nei, min(limit, cap - use)))
                ptr[vert] += 1
            else:
                stack.pop()
        return aug

    # Old version
#        for pos in range(ptr[vert], len(graph[vert])):
#            nei, pair, cap, use = graph[vert][pos]
#            if lvl[nei] == lvl[vert] + 1:
#                aug = self.dfs(nei, dest, min(limit, cap - use))
#                if aug:
#                    graph[vert][pos][3] += aug
#                    graph[nei][pair][3] -= aug
#                    return aug
#            ptr[vert] += 1
#
#        return 0

    def calc(self, src, dest):
        cue = [0] * n
        flow, cue[0] = 0, src
        for l in range(31): # l = 30 maybe faster for random data
            while True:
                lvl, ptr = [0] * len(cue), [0] * len(cue)
                qi, qe, lvl[src] = 0, 1, 1
                while qi < qe and not lvl[dest]:
                    vert = cue[qi]
                    qi += 1
                    for nei, pair, cap, use in graph[vert]:
                        if not lvl[nei] and (cap - use) >> (30 - l):
                            cue[qe] = nei
                            qe += 1
                            lvl[nei] = lvl[vert] + 1

                aug = self.dfs(src, dest)
                while aug:
                    flow += aug
                    aug = self.dfs(src, dest)

                if not lvl[dest]:
                    break

        return flow
