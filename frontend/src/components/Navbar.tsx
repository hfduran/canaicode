import React from "react";
import { Link } from "react-router-dom";

const Navbar: React.FC = () => {
  return (
    <div style={{ padding: "10px", backgroundColor: "#eee" }}>
      <Link to="/" style={{ margin: "10px" }}>
        Home
      </Link>
      <Link to="/gross-metrics" style={{ margin: "10px" }}>
        Gross Metrics
      </Link>
      <Link to="/calculated-metrics" style={{ margin: "10px" }}>
        Calculated Metrics
      </Link>
    </div>
  );
};

export default Navbar;
