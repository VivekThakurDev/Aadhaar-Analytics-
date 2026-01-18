import { useState, useEffect } from 'react'
import axios from 'axios'
import { PieChart, Pie, Cell, Tooltip, Legend, BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer } from 'recharts'

const API_BASE = 'http://localhost:8000'

function App() {
  const [summary, setSummary] = useState(null)
  const [geoData, setGeoData] = useState([])
  const [pincode, setPincode] = useState('')
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchSummary()
    fetchGeoData()
  }, [])

  const fetchSummary = async () => {
    try {
      const res = await axios.get(`${API_BASE}/analytics/summary`)
      setSummary(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  const fetchGeoData = async () => {
    try {
      const res = await axios.get(`${API_BASE}/analytics/geo`)
      setGeoData(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  const searchRecords = async () => {
    if (!pincode) return
    setLoading(true)
    try {
      const res = await axios.get(`${API_BASE}/records`, { params: { pincode } })
      setRecords(res.data)
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28']

  if (!summary) return <div className="p-10">Loading Dashboard...</div>

  const pieData = [
    { name: '0-5 Years', value: summary.age_0_5 },
    { name: '5-17 Years', value: summary.age_5_17 },
    { name: '18+ Years', value: summary.age_18_plus },
  ]

  // Top 5 Districts by Total Population (for Bar Chart)
  const topDistricts = [...geoData]
    .map(d => ({
      ...d,
      total: d.age_0_5 + d.age_5_17 + d.age_18_greater
    }))
    .sort((a, b) => b.total - a.total)
    .slice(0, 5)

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Aadhaar Analytics Dashboard</h1>
        <p className="text-gray-500">Age-Based Unique Identification & Demand Analysis</p>
      </header>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <Card title="Total Enrolments" value={summary.total.toLocaleString()} color="bg-blue-500" />
        <Card title="0-5 Years" value={summary.age_0_5.toLocaleString()} sub="(Early Childhood)" color="bg-indigo-500" />
        <Card title="5-17 Years" value={summary.age_5_17.toLocaleString()} sub="(School Age)" color="bg-teal-500" />
        <Card title="18+ Years" value={summary.age_18_plus.toLocaleString()} sub="(Adults)" color="bg-orange-500" />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Age Distribution</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Top 5 Districts (Demand)</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={topDistricts}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="district" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="age_0_5" name="0-5 Years" stackId="a" fill="#0088FE" />
                <Bar dataKey="age_5_17" name="5-17 Years" stackId="a" fill="#00C49F" />
                <Bar dataKey="age_18_greater" name="18+ Years" stackId="a" fill="#FFBB28" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Record Explorer */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">Record Explorer (Unique ID Prototype)</h2>
        <div className="flex gap-4 mb-4">
          <input
            type="text"
            placeholder="Search by Pincode (e.g. 560001)"
            className="border p-2 rounded w-full max-w-sm"
            value={pincode}
            onChange={(e) => setPincode(e.target.value)}
          />
          <button
            onClick={searchRecords}
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
            disabled={loading}
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="bg-gray-100 uppercase font-medium text-gray-600">
              <tr>
                <th className="p-3">Record ID (Generated)</th>
                <th className="p-3">State</th>
                <th className="p-3">District</th>
                <th className="p-3">Pincode</th>
                <th className="p-3 text-right">0-5 Count</th>
                <th className="p-3 text-right">5-17 Count</th>
                <th className="p-3 text-right">18+ Count</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {records.length > 0 ? records.map((rec) => (
                <tr key={rec.record_id} className="hover:bg-gray-50">
                  <td className="p-3 font-mono text-blue-600">{rec.record_id}</td>
                  <td className="p-3">{rec.state}</td>
                  <td className="p-3">{rec.district}</td>
                  <td className="p-3">{rec.pincode}</td>
                  <td className="p-3 text-right">{rec.age_0_5}</td>
                  <td className="p-3 text-right">{rec.age_5_17}</td>
                  <td className="p-3 text-right">{rec.age_18_greater}</td>
                </tr>
              )) : (
                <tr>
                  <td colSpan="7" className="p-4 text-center text-gray-500">
                    {pincode ? 'No records found.' : 'Enter a pincode to search.'}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

function Card({ title, value, sub, color }) {
  return (
    <div className={`${color} p-6 rounded-lg text-white shadow-lg`}>
      <h3 className="text-sm uppercase opacity-90 font-medium">{title}</h3>
      <p className="text-3xl font-bold mt-2">{value}</p>
      {sub && <span className="text-xs opacity-75">{sub}</span>}
    </div>
  )
}

export default App
