INF = float("inf")


class Dinic:
    def __init__(self, n):
        self.lvl = [0] * n
        self.ptr = [0] * n
        self.q = [0] * n
        self.adj = [[] for _ in range(n)]

    def add_edge(self, a, b, cap, rcap=0):
        self.adj[a].append([b, len(self.adj[b]), cap, 0])
        self.adj[b].append([a, len(self.adj[a]) - 1, rcap, 0])

    def dfs(self, vert, targ, limit):
        if vert == targ or not limit:
            return limit

        for pos in range(self.ptr[vert], len(self.adj[vert])):
            nei, pair, cap, use = self.adj[vert][pos]
            if self.lvl[nei] == self.lvl[vert] + 1:
                aug = self.dfs(nei, targ, min(limit, cap - use))
                if aug:
                    self.adj[vert][pos][3] += aug
                    self.adj[nei][pair][3] -= aug
                    return aug
            self.ptr[vert] += 1

        return 0

    def calc(self, start, targ):
        flow, self.q[0] = 0, start
        for l in range(31):  # l = 30 maybe faster for random data
            while True:
                self.lvl, self.ptr = [0] * len(self.q), [0] * len(self.q)
                qi, qe, self.lvl[start] = 0, 1, 1
                while qi < qe and not self.lvl[targ]:
                    vert = self.q[qi]
                    qi += 1
                    for nei, pair, cap, use in self.adj[vert]:
                        if not self.lvl[nei] and (cap - use) >> (30 - l):
                            self.q[qe] = nei
                            qe += 1
                            self.lvl[nei] = self.lvl[vert] + 1

                aug = self.dfs(start, targ, INF)
                while aug:
                    flow += aug
                    aug = self.dfs(start, targ, INF)

                if not self.lvl[targ]:
                    break

        return flow
