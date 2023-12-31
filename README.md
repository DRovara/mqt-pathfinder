# Pathfinder

This tool is meant to help prepare the use of VQAs to solve pathfinding problems on directed graphs, by employing a set of constraints. The following constraints are currently supported (red expressions are not QUBO):

- Throughout this, we assume $x_{\pi, v, i} = 0$ for $v > |V|$.
- In cases where we want to work with loops. we assume $x_{\pi,v,i + N} = x*{\pi,v,i}$, otherwise $x*{\pi,v,j} = 0$ for $j > N$\
  - `PathIsValid`
  - `MinimisePathLength`
  - `PathContainsEdgeExactlyOnce`
  - `PathsShareNoEdges`
- Paths cannot be shorter than $N$. If there are, repeat one of the vertices to pad the length.
- As a consequence, the adjacency matrix must have $A_{ii} = 0$ for each $i$.\
- In **unary** encoding, we assume $x_{\pi, 1, i} = 1$ for all $\pi, i$.

## `PathIsValid`

Ensure that $(u \rightarrow v) \in E$ for each $(u \rightarrow v) \in \pi$ and each position holds a vertex

- One-Hot: $$\sum_{(u \rightarrow v) \not \in E} \sum_{i = 1}^{N}x_{\pi, u, i}x_{\pi, v, i+1} + \sum_{i=1}^N \left(1-\sum_{v \in V}x_{\pi,v,i} \right)^2$$
- Unary: $$\sum_{(u \rightarrow v) \not \in E}\sum_{i=1}^{N} (x_{\pi,u,i}-x_{\pi,u+1,i})(x_{\pi,v,i+1}-x_{\pi,v+1,i+1})$$
- Binary

## `MinimisePathLength`

Minimise $\sum_{(u \rightarrow v) \in \pi} A_{uv}$

- One-Hot: $$\sum_{(u \rightarrow v) \in E} \sum_{i = 1}^{N} A_{uv}x_{\pi, u, i}x_{\pi, v, i+1}$$
- Unary: $$\sum_{(u \rightarrow v) \in E}\sum_{i=1}^{N} A_{uv}(x_{\pi,u,i}-x_{\pi,u+1,i})(x_{\pi,v,i+1}-x_{\pi,v+1,i+1})$$
- Binary

## `PathPositionIs`

Given set of vertices $V' \subseteq V$, position $i$: ensure $\pi_i \in v$

- One-Hot: $$1 - \sum_{v \in V'} x_{\pi, v, i}$$
- Unary: $$1 - \sum_{v\in V'}(x_{\pi, v, i} - x_{\pi, v + 1, i})$$
- Binary

## `PathContainsVertexExactlyOnce`

Given $v$, ensure that: $\left| \{i: \pi_i = v \} \right| = 1$

- One-Hot: $$\left( 1 - \sum_{i = 1}^N x_{\pi, v, i} \right) ^2$$
- Unary: $$\left( 1 - \sum_{i=1}^N (x_{\pi,v,i} - x_{\pi,v+1,i}) \right)^2$$
- Binary

## `PathContainsVertexAtLeastOnce`

Given $v$, ensure that: $\left| \{i: \pi_i = v \} \right| \geq 1$

- One-Hot: $$???$$
- Unary: $$???$$
- Binary

## `PathContainsVertexAtMostOnce`

Given $v$, ensure that: $\left| \{i: \pi_i = v \} \right| \leq 1$

- One-Hot: $$???$$
- Unary: $$???$$
- Binary

## `PathContainsEdgeExactlyOnce`

Given $e = (u \rightarrow v)$, ensure that: $|\{(i, i + 1) : \pi_i = u \wedge \pi_{i+1} = v\}| = 1$\

- One-Hot: $$\color{red} \left( 1 - \sum_{i=1}^{N}x_{\pi, u, i}x_{\pi, v, i + 1} \right)^2$$
- Unary: $$\color{red} \left( 1 - \sum_{i=1}^{N}(x_{\pi,u,i}-x_{\pi,u+1,i})(x_{\pi,v,i+1}-x_{\pi,v+1,i+1}) \right)^2$$
- Binary

## `PathContainsEdgeAtMostOnce`

Given $e = (u \rightarrow v)$, ensure that: $|\{(i, i + 1) : \pi_i = u \wedge \pi_{i+1} = v\}| \leq 1$\

- One-Hot: $$???$$
- Unary: $$???$$
- Binary

## `PathContainsEdgeAtLeastOnce`

Given $e = (u \rightarrow v)$, ensure that: $\left| \{(i, i + 1) : \pi_i = u \wedge \pi_{i+1} = v\} \right| \geq 1$\

- One-Hot: $$???$$
- Unary: $$???$$
- Binary

## `PathsShareNoVertices`

Given two paths $\pi^{(1)}$ and $\pi^{(2)}$, $\pi^{(1)}_V \cap \pi^{(2)}_V = \emptyset$

- One-Hot: $$\sum_{v \in V} \left[ \left(\sum_{i=1}^N x_{\pi^{(1)}, v, i} \right) \left(\sum_{i=1}^N x_{\pi^{(2)}, v, i} \right) \right]$$
- Unary: $$\sum_{v \in V} \left[ \left(\sum_{i=1}^N x_{\pi^{(1)},v,i} - x_{\pi^{(1)},v+1,i} \right) \left(\sum_{i=1}^N x_{\pi^{(2)},v,i} - x_{\pi^{(2)},v+1,i} \right) \right]$$
- Binary

## `PathsShareNoEdges`

Given two paths $\pi^{(1)}$ and $\pi^{(2)}$, $\pi^{(1)}_E \cap \pi^{(2)}_E = \emptyset$

- One-Hot: $$\color{red} \sum_{(u \rightarrow v) \in V} \left[ \left(\sum_{i=1}^{N} x_{\pi^{(1)}, u, i} x_{\pi^{(1)}, v, i + 1} \right) \left(\sum_{i=1}^{N} x_{\pi^{(2)}, u, i} x_{\pi^{(2)}, v, i + 1} \right) \right]$$
- Unary: $$\color{red} \sum_{(u \rightarrow v) \in V} \left[ \left(\sum_{i=1}^{N} (x_{\pi^{(1)},u,i}-x_{\pi^{(1)}u+1,i})(x_{\pi^{(1)}v,i+1}-x_{\pi^{(1)}v+1,i+1}) \right) \left(\sum_{i=1}^{N} (x_{\pi^{(2)},u,i}-x_{\pi^{(2)}u+1,i})(x_{\pi^{(2)}v,i+1}-x_{\pi^{(2)}v+1,i+1}) \right) \right]$$
- Binary

## `PrecedenceConstraint`

Given a pair $(u, v)$, $v$ may not appear before $u$

- One-Hot: $$???$$
- Unary: $$???$$
- Binary

---

---
