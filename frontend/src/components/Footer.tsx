import React from "react";

const Footer: React.FC = () => {
  return (
    <footer
      style={{
        backgroundColor: "#eee",
        padding: "20px",
        display: "flex",
        justifyContent: "space-between",
      }}
    >
      <div>Column 1 Info</div>
      <div>Column 2 Info</div>
      <div>Column 3 Info</div>
    </footer>
  );
};

export default Footer;
