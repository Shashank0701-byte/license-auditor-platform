import { useEffect, useState } from "react";
import "./App.css";
import {
  PieChart, Pie, Cell, Tooltip, Legend,
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis
} from "recharts";


function App() {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedScan, setSelectedScan] = useState(null);
  const [scanDetails, setScanDetails] = useState([]);
  const [filter, setFilter] = useState("ALL");
  const [expandedPkg, setExpandedPkg] = useState(null);

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
      fetchScans();
    } catch (err) {
      console.error("Upload failed", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchScanDetails = (scanId) => {
    fetch(`http://127.0.0.1:8000/api/scans/${scanId}/`)
      .then(res => res.json())
      .then(data => {
        setScanDetails(data);
        setSelectedScan(scanId);
        setFilter("ALL");
        setExpandedPkg(null);
      })
      .catch(err => console.error(err));
  };

  const latest = scans.length > 0 ? scans[0] : null;

  const filteredPackages = scanDetails.filter(pkg => {
    if (filter === "LICENSE") return pkg.risks.includes("LICENSE_RISK");
    if (filter === "ABANDONED") return pkg.risks.includes("ABANDONED_PACKAGE");
    return true;
  });

  // Insights + Score
  const riskyCount = scanDetails.filter(p => p.risks.includes("LICENSE_RISK")).length;
  const abandonedCount = scanDetails.filter(p => p.risks.includes("ABANDONED_PACKAGE")).length;
  const criticalCount = scanDetails.filter(
    p => p.risks.includes("LICENSE_RISK") && p.risks.includes("ABANDONED_PACKAGE")
  ).length;

  const riskScore = Math.max(0, 100 - (riskyCount * 15 + abandonedCount * 8 + criticalCount * 10));

  return (
    <div className="container">
      <h1>🔎 License Auditor Dashboard</h1>

      <div className="upload-box">
        <label className="upload-btn">
          {loading ? "Scanning..." : "Upload requirements.txt"}
          <input type="file" accept=".txt" hidden onChange={handleUpload} />
        </label>
      </div>

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
            <tr key={scan.id} onClick={() => fetchScanDetails(scan.id)} style={{ cursor: "pointer" }}>
              <td>{new Date(scan.created_at).toLocaleString()}</td>
              <td>{scan.total_packages}</td>
              <td className="risk">{scan.license_risks}</td>
              <td className="warn">{scan.abandoned_packages}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {selectedScan && (
        <div className="details-panel">
          <h2>Scan Details</h2>

          {/* Insights */}
          <div className="insights-panel">
            <h3>⚡ Scan Insights</h3>
            <ul>
              <li>🔴 {riskyCount} packages have license risks</li>
              <li>🟠 {abandonedCount} packages appear abandoned</li>
              {criticalCount > 0 && <li>🔥 {criticalCount} packages are critical</li>}
            </ul>
          </div>

          {/* Score */}
          <div className="score-card">
            <h3>Security Score</h3>
            <p className={riskScore > 70 ? "good" : riskScore > 40 ? "warn" : "bad"}>
              {riskScore}/100
            </p>
          </div>

          {/* Charts Section */}
<div className="charts-grid">
  <div className="chart-card">
    <h3>License Risk Distribution</h3>
    <ResponsiveContainer width="100%" height={250}>
      <PieChart>
        <Pie
          data={[
            { name: "License Risk", value: riskyCount },
            { name: "Safe", value: scanDetails.length - riskyCount }
          ]}
          dataKey="value"
          outerRadius={80}
        >
          <Cell fill="#ff4d4d" />
          <Cell fill="#00ff99" />
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  </div>

  <div className="chart-card">
    <h3>Abandoned Packages</h3>
    <ResponsiveContainer width="100%" height={250}>
      <BarChart
        data={[
          { name: "Abandoned", value: abandonedCount },
          { name: "Active", value: scanDetails.length - abandonedCount }
        ]}
      >
        <XAxis dataKey="name" stroke="#aaa" />
        <YAxis stroke="#aaa" />
        <Tooltip />
        <Bar dataKey="value">
          <Cell fill="#ffa500" />
          <Cell fill="#00ffd5" />
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  </div>
</div>


          {/* Filters */}
          <div className="filter-bar">
            <button className={`filter-btn ${filter === "ALL" ? "active" : ""}`} onClick={() => setFilter("ALL")}>All</button>
            <button className={`filter-btn danger ${filter === "LICENSE" ? "active" : ""}`} onClick={() => setFilter("LICENSE")}>License Risks</button>
            <button className={`filter-btn warning ${filter === "ABANDONED" ? "active" : ""}`} onClick={() => setFilter("ABANDONED")}>Abandoned</button>
          </div>

          <table>
            <thead>
              <tr>
                <th>Package</th>
                <th>License</th>
                <th>Last Updated</th>
                <th>Risks</th>
              </tr>
            </thead>
            <tbody>
              {filteredPackages.map((pkg, i) => (
                <>
                  <tr key={i} onClick={() => setExpandedPkg(expandedPkg === i ? null : i)} style={{ cursor: "pointer" }}>
                    <td>{pkg.name}</td>
                    <td>{pkg.license || "Unknown"}</td>
                    <td>{pkg.last_updated || "N/A"}</td>
                    <td>
                      {pkg.risks.includes("LICENSE_RISK") && <span className="badge badge-license">License Risk</span>}
                      {pkg.risks.includes("ABANDONED_PACKAGE") && <span className="badge badge-abandoned">Abandoned</span>}
                    </td>
                  </tr>
                  {expandedPkg === i && (
                    <tr className="expand-row">
                      <td colSpan="4">
                        <div className="expand-box">
                          <strong>License:</strong> {pkg.license || "Unknown"} <br />
                          <strong>Last Updated:</strong> {pkg.last_updated || "N/A"} <br />
                          <strong>Flags:</strong> {pkg.risks.join(", ")}
                        </div>
                      </td>
                    </tr>
                  )}
                </>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
