// import GrossMetricsDashboard from '../components/Dashboard';
import Filters from '../components/Filters';

function GrossMetrics() {
  return (
    <div>
      <p>This dashboard shows gross metrics of the system...</p>
      <div style={{ display: 'flex', gap: '20px', margin: '0 50px' }}>
        {/* <div style={{ flex: 7 }}>
          <Dashboard />
        </div> */}
        <div style={{ flex: 3 }}>
          <Filters />
        </div>
      </div>
    </div>
  );
}

export default GrossMetrics;