import React from "react";
import { Box, SpaceBetween } from "@cloudscape-design/components";

interface PearsonCorrelationDisplayProps {
  correlationValue: number;
  isCommitsMetric: boolean;
}

const PearsonCorrelationDisplay: React.FC<PearsonCorrelationDisplayProps> = ({
  correlationValue,
  isCommitsMetric,
}) => {
  if (isNaN(correlationValue)) {
    return (
      <Box textAlign="center" padding="l">
        <Box variant="p" color="text-body-secondary">
          No data available to calculate correlation.
        </Box>
      </Box>
    );
  }

  return (
    <Box padding="l">
      <SpaceBetween size="l">
        <SpaceBetween size="xs">
          <Box variant="p" color="text-body-secondary">
            Pearson Correlation between:
          </Box>
          <Box margin={{ left: "s" }}>
            <SpaceBetween size="xxs">
              <Box variant="p" color="text-body-secondary">
                • {isCommitsMetric ? <em>Total Commits</em> : <em>Total Changed Lines</em>}
              </Box>
              <Box variant="p" color="text-body-secondary">
                • <em>Copilot Changed Lines</em>
              </Box>
            </SpaceBetween>
          </Box>
        </SpaceBetween>

        {/* Visual Bar and Number Section */}
        <Box>
          <div style={{ position: 'relative', width: '100%', marginTop: '15px', marginBottom: '15px' }}>
            {/* Bar container */}
            <div style={{
              height: '10px',
              width: '100%',
              backgroundColor: '#e9ecef',
              borderRadius: '5px'
            }} />

            {/* Center line at 0 */}
            <div style={{
              position: 'absolute',
              top: 0,
              left: '50%',
              width: '2px',
              height: '100%',
              backgroundColor: '#6c757d',
            }} />

            {/* Filled bar */}
            {correlationValue !== null && (
              <>
                <div style={{
                  position: 'absolute',
                  top: 0,
                  left: correlationValue >= 0 ? '50%' : `${(correlationValue + 1) * 50}%`,
                  height: '100%',
                  width: `${Math.abs(correlationValue) * 50}%`,
                  backgroundColor: correlationValue >= 0 ? '#037f0c' : '#d13212',
                  borderRadius: correlationValue >= 0 ? '0 5px 5px 0' : '5px 0 0 5px',
                }} />

                {/* Number on the bar */}
                <span style={{
                  position: 'absolute',
                  top: '-25px',
                  left: `${(correlationValue + 1) * 50}%`,
                  transform: 'translateX(-50%)',
                  fontSize: '1.2em',
                  fontWeight: 'bold',
                  color: correlationValue >= 0 ? '#037f0c' : '#d13212',
                }}>
                  {correlationValue.toFixed(2)}
                </span>
              </>
            )}
          </div>

          {/* Legend */}
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <Box variant="small" color="text-body-secondary">-1 (Negative)</Box>
            <Box variant="small" color="text-body-secondary">0 (None)</Box>
            <Box variant="small" color="text-body-secondary">+1 (Positive)</Box>
          </div>
        </Box>

        <Box variant="small" color="text-body-secondary">
          Values closer to -1 or +1 indicate stronger linear relationships. Negative values indicate inverse correlation.
        </Box>
      </SpaceBetween>
    </Box>
  );
};

export default PearsonCorrelationDisplay;
