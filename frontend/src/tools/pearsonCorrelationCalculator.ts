export function pearsonCorrCalculator(data: {
  net_changed_lines_by_copilot: number;
  net_changed_lines: number;
}[]): number {
  const n = data.length;

  if (n === 0) return 0;

  const x = data.map(d => d.net_changed_lines_by_copilot);
  const y = data.map(d => d.net_changed_lines);

  const meanX = x.reduce((sum, val) => sum + val, 0) / n;
  const meanY = y.reduce((sum, val) => sum + val, 0) / n;

  const numerator = x.reduce((acc, val, i) => {
    return acc + (val - meanX) * (y[i] - meanY);
  }, 0);

  const denominatorX = Math.sqrt(x.reduce((acc, val) => acc + Math.pow(val - meanX, 2), 0));
  const denominatorY = Math.sqrt(y.reduce((acc, val) => acc + Math.pow(val - meanY, 2), 0));

  const denominator = denominatorX * denominatorY;

  if (denominator === 0) return 0;

  return numerator / denominator;
}