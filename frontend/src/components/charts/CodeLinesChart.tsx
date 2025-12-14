import React from "react";
import { BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, Legend } from "recharts";
import { FormattedDataEntry } from "../../types/ui";

interface CodeLinesChartProps {
  data: FormattedDataEntry[];
  width: number;
  height: number;
}

const CodeLinesChart: React.FC<CodeLinesChartProps> = ({ data, width, height }) => {
  return (
    <BarChart
      width={width}
      height={height}
      data={data}
      margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
    >
      <CartesianGrid strokeDasharray="3 3" stroke="#e9ecef" opacity={0.7} />
      <XAxis
        dataKey="initial_date"
        angle={-45}
        textAnchor="end"
        height={100}
        tick={{ fontSize: 12, fill: "#6c757d" }}
        stroke="#6c757d"
        tickLine={{ stroke: "#6c757d" }}
      />
      <YAxis
        tick={{ fontSize: 12, fill: "#6c757d" }}
        stroke="#6c757d"
        tickLine={{ stroke: "#6c757d" }}
      />
      <Tooltip
        formatter={(value: any, name: string, props: any) => {
          const total = props.payload.net_changed_lines;
          let percent = 0;
          if (name === "Copilot Changed Lines") {
            percent = total > 0 ? (value / total) * 100 : 0;
            return [
              `${value} lines (${percent.toFixed(1)}% of total)`,
              "Copilot Changed Lines",
            ];
          }
          if (name === "Changed Lines without Copilot") {
            percent = total > 0 ? (value / total) * 100 : 0;
            return [
              `${value} lines (${percent.toFixed(1)}% of total)`,
              "Changed Lines without Copilot",
            ];
          }
          return [`${value} lines`, name];
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
        dataKey="net_changed_lines_without_copilot"
        fill="#0073bb"
        name="Changed Lines without Copilot"
        radius={[4, 4, 0, 0]}
        stackId="a"
      />
      <Bar
        dataKey="net_changed_lines_by_copilot"
        fill="#037f0c"
        name="Copilot Changed Lines"
        radius={[4, 4, 0, 0]}
        stackId="a"
      />
    </BarChart>
  );
};

export default CodeLinesChart;
