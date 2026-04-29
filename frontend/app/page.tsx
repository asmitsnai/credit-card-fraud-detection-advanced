"use client";
import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [data, setData] = useState({ stats: { total: 0, fraud: 0, safe: 0 }, recent: [] });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch('http://localhost:8000/stats');
        const json = await res.json();
        setData(json);
      } catch (err) {
        console.error("API offline");
      }
    };
    const interval = setInterval(fetchStats, 2000); // Poll every 2s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-10 font-sans">
      <h1 className="text-3xl font-bold mb-8 text-blue-400">💳 Real-Time Fraud Operations Center</h1>
      
      <div className="grid grid-cols-3 gap-6 mb-10">
        <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
          <h2 className="text-xl text-gray-400">Total Scanned</h2>
          <p className="text-4xl font-bold">{data.stats.total}</p>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg border border-red-900">
          <h2 className="text-xl text-red-400">Fraud Detected</h2>
          <p className="text-4xl font-bold text-red-500">{data.stats.fraud}</p>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg border border-green-900">
          <h2 className="text-xl text-green-400">Safe Transactions</h2>
          <p className="text-4xl font-bold text-green-500">{data.stats.safe}</p>
        </div>
      </div>

      <div className="bg-gray-800 p-6 rounded-lg">
        <h2 className="text-2xl mb-4">Live Alerts Stream</h2>
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-gray-700">
              <th className="py-2">Amount</th>
              <th>Threat Level</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {data.recent.map((tx: any, i) => (
              <tr key={i} className="border-b border-gray-700/50">
                <td className="py-3">${tx.amount.toFixed(2)}</td>
                <td>{(tx.fraud_probability * 100).toFixed(2)}%</td>
                <td>
                  {tx.is_fraud ? 
                    <span className="bg-red-900 text-red-200 px-3 py-1 rounded-full text-sm">BLOCK</span> : 
                    <span className="bg-green-900 text-green-200 px-3 py-1 rounded-full text-sm">PASS</span>
                  }
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}