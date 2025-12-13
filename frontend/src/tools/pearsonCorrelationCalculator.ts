export function pearsonCorrCalculator(data: {
  net_changed_lines_by_copilot: number;
  net_changed_lines?: number;
  total_commits?: number;
}[]): number {
  const n = data.length;

  if (n === 0) return 0;

  // Check if this is Commits metric or Code Lines metric
  const isCommitsMetric = data.some(d => d.total_commits !== undefined);

  let x: number[];
  let y: number[];

  if (isCommitsMetric) {
    // For Commits metric: correlate total_commits with net_changed_lines_by_copilot
    x = data.map(d => d.total_commits || 0);
    y = data.map(d => d.net_changed_lines_by_copilot);
  } else {
    // For Code Lines metric: correlate net_changed_lines_by_copilot with net_changed_lines
    x = data.map(d => d.net_changed_lines_by_copilot);
    y = data.map(d => d.net_changed_lines || 0);
  }

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