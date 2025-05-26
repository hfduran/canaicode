import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <div style={{ padding: '10px', backgroundColor: '#eee' }}>
      <Link to="/" style={{ margin: '10px' }}>Home</Link>
      <Link to="/gross-metrics" style={{ margin: '10px' }}>Gross Metrics</Link>
      <Link to="/calculated-metrics" style={{ margin: '10px' }}>Calculated Metrics</Link>
    </div>
  );
}

export default Navbar;