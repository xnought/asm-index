# asm-index

**Work in Progress** Assembly theory search to compute the shortest path to assemble an object.

For now only takes into accounts bytes and positioned in 1d (a character to the right or left).

For example, how a string is assmebled. Like AABBA

Can be assembled with A->AA->AAB->AABB->AABBA

Which is four steps to assumble the ending sting.

For example with the classic example ABRACADABRA

A->AB->ABR->ABRA->ABRAC->ABRACA->ABRACAD->ABRRACABRA

 we can reuse the ABRA at a cost of 1 since we assume sufficiently complex objects can only exist with things making them (assumption of selection and life in general).
 
So we consider ABRACRADABRA to have an index of 7

- [ ] Simple bfs/djikstras search for strings like above
- [ ] Optimized with heuristic (A* ??) for strings
- [ ] Tricks to optimize memory and speed for strings
- [ ] Write in a faster language (perhaps C, C++, Rust, or Mojo)
- [ ] See if there are any new adjustments/shortcuts to search with the assembley theory assumptions
