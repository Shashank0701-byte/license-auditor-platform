import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchScans = () => {
    fetch("http://127.0.0.1:8000/api/scans/")
      .then(res => res.json())
      .then(data => setScans(data))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    fetchScans();
  }, []);

  const handleUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      await fetch("http://127.0.0.1:8000/api/scan/", {
        method: "POST",
        body: formData
      });

      fetchScans(); // Refresh dashboard after scan
    } catch (err) {
      console.error("Upload failed", err);
    } finally {
      setLoading(false);
    }
  };

  const latest = scans.length > 0 ? scans[0] : null;

  return (
    <div className="container">
      <h1>🔎 License Auditor Dashboard</h1>

      {/* Upload Section */}
      <div className="upload-box">
        <label className="upload-btn">
          {loading ? "Scanning..." : "Upload requirements.txt"}
          <input type="file" accept=".txt" hidden onChange={handleUpload} />
        </label>
      </div>

      {/* Summary Cards */}
      {latest && (
        <div className="summary-grid">
          <div className="card">
            <h3>Total Packages</h3>
            <p>{latest.total_packages}</p>
          </div>

          <div className="card danger">
            <h3>License Risks</h3>
            <p>{latest.license_risks}</p>
          </div>

          <div className="card warning">
            <h3>Abandoned</h3>
            <p>{latest.abandoned_packages}</p>
          </div>
        </div>
      )}

      {/* Scan History Table */}
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Total Packages</th>
            <th>License Risks</th>
            <th>Abandoned</th>
          </tr>
        </thead>
        <tbody>
          {scans.map(scan => (
            <tr key={scan.id}>
              <td>{new Date(scan.created_at).toLocaleString()}</td>
              <td>{scan.total_packages}</td>
              <td className="risk">{scan.license_risks}</td>
              <td className="warn">{scan.abandoned_packages}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
