import React from "react";
import { ComposedChart, Bar, Line, CartesianGrid, XAxis, YAxis, Tooltip, Legend } from "recharts";
import { FormattedDataEntry } from "../../types/ui";

interface CommitMetricsChartProps {
  data: FormattedDataEntry[];
  width: number;
  height: number;
}

const CommitMetricsChart: React.FC<CommitMetricsChartProps> = ({ data, width, height }) => {
  return (
    <ComposedChart
      width={width}
      height={height}
      data={data}
      margin={{ top: 20, right: 60, left: 20, bottom: 5 }}
    >
      <CartesianGrid strokeDasharray="3 3" stroke="#e9ecef" opacity={0.7} />
      <XAxis
        dataKey="initial_date"
        tick={{ fontSize: 12, fill: "#6c757d" }}
        stroke="#6c757d"
        tickLine={{ stroke: "#6c757d" }}
      />
      <YAxis
        yAxisId="left"
        tick={{ fontSize: 12, fill: "#6c757d" }}
        stroke="#6c757d"
        tickLine={{ stroke: "#6c757d" }}
        label={{ value: "Commits", angle: -90, position: "insideLeft" }}
      />
      <YAxis
        yAxisId="right"
        orientation="right"
        tick={{ fontSize: 12, fill: "#6c757d" }}
        stroke="#6c757d"
        tickLine={{ stroke: "#6c757d" }}
        label={{ value: "Copilot Intensity (%)", angle: 90, position: "insideRight" }}
        domain={[0, 100]}
      />
      <Tooltip
        formatter={(value: any, name: string) => {
          if (name === "Total Commits") {
            return [`${value} commits`, name];
          }
          if (name === "Copilot Intensity") {
            return [`${value.toFixed(1)}%`, name];
          }
          return [value, name];
        }}
        contentStyle={{
          backgroundColor: "#ffffff",
          border: "1px solid #e9ecef",
          borderRadius: "8px",
          boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
          fontSize: "14px",
        }}
        labelStyle={{ color: "#232f3e", fontWeight: "bold" }}
      />
      <Legend wrapperStyle={{ paddingTop: "20px" }} />
      <Bar
        yAxisId="left"
        dataKey="total_commits"
        fill="#0073bb"
        name="Total Commits"
        radius={[4, 4, 0, 0]}
      />
      <Line
        yAxisId="right"
        type="monotone"
        dataKey={(entry: any) => entry.percentage_changed_lines_by_copilot * 100}
        stroke="#28A745"
        strokeWidth={3}
        name="Copilot Intensity"
        dot={{ r: 5, fill: "#28A745" }}
      />
    </ComposedChart>
  );
};

export default CommitMetricsChart;
