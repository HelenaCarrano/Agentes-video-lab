// Matriz CSS (matrix3d) que leva o retângulo (0,0)-(w,h) para um quadrilátero qualquer.
// Usada para encaixar a interface do produto nas telas de celular e notebook das cenas de IA.

type P = [number, number];

const resolver = (a: number[][], b: number[]): number[] => {
  const n = b.length;
  const m = a.map((linha, i) => [...linha, b[i]]);
  for (let c = 0; c < n; c++) {
    let piv = c;
    for (let r = c + 1; r < n; r++) if (Math.abs(m[r][c]) > Math.abs(m[piv][c])) piv = r;
    [m[c], m[piv]] = [m[piv], m[c]];
    for (let r = 0; r < n; r++) {
      if (r === c) continue;
      const f = m[r][c] / m[c][c];
      for (let k = c; k <= n; k++) m[r][k] -= f * m[c][k];
    }
  }
  return m.map((linha, i) => linha[n] / linha[i]);
};

export const matrix3d = (w: number, h: number, q: [P, P, P, P]): string => {
  const src: P[] = [
    [0, 0],
    [w, 0],
    [w, h],
    [0, h],
  ];
  const a: number[][] = [];
  const b: number[] = [];
  for (let i = 0; i < 4; i++) {
    const [x, y] = src[i];
    const [u, v] = q[i];
    a.push([x, y, 1, 0, 0, 0, -u * x, -u * y]);
    b.push(u);
    a.push([0, 0, 0, x, y, 1, -v * x, -v * y]);
    b.push(v);
  }
  const [h0, h1, h2, h3, h4, h5, h6, h7] = resolver(a, b);
  // coluna principal (CSS matrix3d é column-major)
  return `matrix3d(${h0},${h3},0,${h6},${h1},${h4},0,${h7},0,0,1,0,${h2},${h5},0,1)`;
};

// O clipe tem 1924x1076; na composição ele ocupa 1920x1080 (object-fit: cover, centrado).
export const doClipe = (q: P[]): [P, P, P, P] => {
  const s = 1080 / 1076;
  const dx = (1920 - 1924 * s) / 2;
  return q.map(([x, y]) => [x * s + dx, y * s]) as [P, P, P, P];
};

export const centro = (q: P[]): P => [
  q.reduce((a, p) => a + p[0], 0) / q.length,
  q.reduce((a, p) => a + p[1], 0) / q.length,
];
