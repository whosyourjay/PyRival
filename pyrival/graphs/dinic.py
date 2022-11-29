INF = float("inf")

class Dinic:
    def __init__(self, n):
        self.lvl = [0] * n
        self.ptr = [0] * n
        self.cue = [0] * n
        self.adj = [[] for _ in range(n)]

    def add_edge(self, a, b, cap, rcap=0):
        self.adj[a].append([b, len(self.adj[b]), cap, 0])
        self.adj[b].append([a, len(self.adj[a]) - 1, rcap, 0])

    def add_flow(self, vert, pos, aug):
        nei, pair, cap, use = self.adj[vert][pos]
        self.adj[vert][pos][3] += aug
        self.adj[nei][pair][3] -= aug

    def dfs2(self, src, dest):
        aug, found = 0, False

        stack = [(src, INF)]
        while stack:
            vert, limit = stack[-1]

            if found:
                self.ptr[vert] -= 1
                self.add_flow(vert, self.ptr[vert], aug)
                stack.pop()
                continue

            if vert == dest:
                found = True
                aug = limit
                stack.pop()
                continue

            if self.ptr[vert] < len(self.adj[vert]):
                nei, pair, cap, use = self.adj[vert][self.ptr[vert]]
                if self.lvl[nei] == self.lvl[vert] + 1 and cap > use:
                    stack.append((nei, min(limit, cap - use)))
                #print(f"finished vert {vert} at prt {self.ptr[vert]}")
                self.ptr[vert] += 1
            else:
                stack.pop()
        return aug

    def dfs(self, vert, dest, limit):
        if vert == dest or not limit:
            return limit

        for pos in range(self.ptr[vert], len(self.adj[vert])):
            nei, pair, cap, use = self.adj[vert][pos]
            if self.lvl[nei] == self.lvl[vert] + 1:
                aug = self.dfs(nei, dest, min(limit, cap - use))
                if aug:
                    self.adj[vert][pos][3] += aug
                    self.adj[nei][pair][3] -= aug
                    return aug
            #print(f"finished vert {vert} at prt {self.ptr[vert]}")
            self.ptr[vert] += 1

        return 0

    def calc(self, src, dest):
        flow, self.cue[0] = 0, src
        for l in range(31):  # l = 30 maybe faster for random data
            while True:
                #print("resetting ptr")
                self.lvl, self.ptr = [0] * len(self.cue), [0] * len(self.cue)
                qi, qe, self.lvl[src] = 0, 1, 1
                while qi < qe and not self.lvl[dest]:
                    vert = self.cue[qi]
                    qi += 1
                    for nei, pair, cap, use in self.adj[vert]:
                        if not self.lvl[nei] and (cap - use) >> (30 - l):
                            self.cue[qe] = nei
                            qe += 1
                            self.lvl[nei] = self.lvl[vert] + 1

                aug = self.dfs2(src, dest)
                while aug:
                    flow += aug
                    aug = self.dfs2(src, dest)

                if not self.lvl[dest]:
                    break

        return flow
