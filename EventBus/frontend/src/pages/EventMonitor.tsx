import React, { useState, useEffect, useMemo } from 'react';
import { io } from 'socket.io-client';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  PieChart, Pie, Cell, BarChart, Bar 
} from 'recharts';
import { 
  Activity, Pulse, ShieldAlert, Send, Layers, 
  CheckCircle, AlertTriangle, Search, Filter, History 
} from 'lucide-react';
import { format } from 'date-fns';
import { motion, AnimatePresence } from 'framer-motion';
import _ from 'lodash';

// ─── Theme & Colors ────────────────────────────────────────────────
const COLORS = ['#ef4444', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6', '#ec4899'];
const GRAVITY_RED = '#ef4444';

const EventMonitor = () => {
  const [events, setEvents] = useState([]);
  const [stats, setStats] = useState({ connections: 0, pendingAcks: 0, dlqSize: 0 });
  const [filter, setFilter] = useState('');
  const [throughput, setThroughput] = useState([]);
  const [connected, setConnected] = useState(false);

  // 1. WebSocket Connection
  useEffect(() => {
    const socket = io('http://localhost:6005', {
      auth: { token: localStorage.getItem('gate_token') || 'system_root' }
    });

    socket.on('connect', () => {
      setConnected(true);
      console.log('connected to eventbus');
    });

    socket.on('gateway_event', (envelope) => {
      setEvents(prev => _.take([envelope, ...prev], 100)); // Keep last 100
      updateThroughput();
    });

    socket.on('disconnect', () => setConnected(false));

    // Stats polling
    const interval = setInterval(async () => {
      try {
        const res = await fetch('http://localhost:6005/stats');
        const data = await res.json();
        setStats({
          connections: data.active_connections,
          pendingAcks: data.pending_acks,
          dlqSize: data.dlq_size
        });
      } catch (err) {}
    }, 5000);

    return () => {
      socket.disconnect();
      clearInterval(interval);
    };
  }, []);

  const updateThroughput = () => {
    const now = format(new Date(), 'HH:mm:ss');
    setThroughput(prev => {
      const last = _.last(prev);
      if (last && last.time === now) {
        return [...prev.slice(0, -1), { ...last, count: last.count + 1 }];
      }
      return _.takeRight([...prev, { time: now, count: 1 }], 20);
    });
  };

  // 2. Data Processing
  const filteredEvents = useMemo(() => {
    if (!filter) return events;
    return events.filter(ev => 
      ev.event_type.toLowerCase().includes(filter.toLowerCase()) || 
      ev.source.toLowerCase().includes(filter.toLowerCase())
    );
  }, [events, filter]);

  const typeData = useMemo(() => {
    const counts = _.countBy(events, 'event_type');
    return Object.entries(counts).map(([name, value]) => ({ name, value }));
  }, [events]);

  return (
    <div className="min-h-screen bg-neutral-950 text-white p-8 font-['Manrope',_sans-serif]">
      {/* Header */}
      <header className="flex justify-between items-center mb-10">
        <div>
          <h1 className="text-4xl font-extrabold tracking-tight flex items-center gap-3">
            <Pulse className="text-red-500 animate-pulse" />
            RM-Snitch <span className="text-neutral-500">Event Monitor</span>
          </h1>
          <p className="text-neutral-400 mt-2">Real-time ecosystem traffic and health metrics</p>
        </div>
        <div className="flex gap-4">
          <div className={`px-4 py-2 rounded-full flex items-center gap-2 border ${connected ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400' : 'border-red-500/30 bg-red-500/10 text-red-400'}`}>
            <div className={`w-2 h-2 rounded-full ${connected ? 'bg-emerald-500 shadow-[0_0_8px_#10b981]' : 'bg-red-500'}`}></div>
            {connected ? 'Event Bus Online' : 'Connecting...'}
          </div>
        </div>
      </header>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
        {[
          { label: 'Active Connections', value: stats.connections, icon: Layers, color: 'text-blue-400' },
          { label: 'Pending ACKs', value: stats.pendingAcks, icon: Send, color: 'text-amber-400' },
          { label: 'DLQ Retention', value: stats.dlqSize, icon: ShieldAlert, color: 'text-red-400' },
          { label: 'Events (Last Hour)', value: events.length, icon: History, color: 'text-emerald-400' },
        ].map((m, i) => (
          <div key={i} className="bg-neutral-900 border border-neutral-800 p-6 rounded-2xl shadow-xl">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-neutral-500 text-sm font-medium">{m.label}</p>
                <h3 className="text-3xl font-bold mt-1">{m.value}</h3>
              </div>
              <m.icon className={`${m.color} opacity-80`} size={24} />
            </div>
          </div>
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-10">
        <div className="lg:col-span-2 bg-neutral-900 border border-neutral-800 p-6 rounded-2xl h-[400px]">
          <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
            <Activity size={20} className="text-blue-400" /> Real-time Throughput (eps)
          </h3>
          <ResponsiveContainer width="100%" height="85%">
            <LineChart data={throughput}>
              <CartesianGrid strokeDasharray="3 3" stroke="#262626" />
              <XAxis dataKey="time" stroke="#525252" />
              <YAxis stroke="#525252" />
              <Tooltip contentStyle={{ backgroundColor: '#171717', border: '1px solid #404040' }} />
              <Line type="monotone" dataKey="count" stroke={GRAVITY_RED} strokeWidth={3} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-neutral-900 border border-neutral-800 p-6 rounded-2xl h-[400px]">
          <h3 className="text-lg font-semibold mb-6">Event Distribution</h3>
          <ResponsiveContainer width="100%" height="85%">
            <PieChart>
              <Pie
                data={typeData}
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
              >
                {typeData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Live Stream / Table */}
      <div className="bg-neutral-900 border border-neutral-800 rounded-2xl overflow-hidden shadow-2xl">
        <div className="p-6 border-b border-neutral-800 flex justify-between items-center">
          <h3 className="text-lg font-semibold">Live Event Tail</h3>
          <div className="relative w-80">
            <Search className="absolute left-3 top-2.5 text-neutral-500" size={18} />
            <input 
              type="text" 
              placeholder="Search type, source, org..."
              className="bg-neutral-950 border border-neutral-800 rounded-lg pl-10 pr-4 py-2 w-full text-sm focus:outline-none focus:ring-2 focus:ring-red-500/50"
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
            />
          </div>
        </div>
        <div className="max-h-[500px] overflow-y-auto">
          <table className="w-full text-left">
            <thead className="bg-neutral-950/50 text-neutral-500 text-xs uppercase tracking-widest font-bold">
              <tr>
                <th className="p-4">Timestamp</th>
                <th className="p-4">Event Type</th>
                <th className="p-4">Source</th>
                <th className="p-4">Org ID</th>
                <th className="p-4">Payload</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-neutral-800">
              <AnimatePresence>
                {filteredEvents.map((ev) => (
                  <motion.tr 
                    key={ev.event_id}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="hover:bg-neutral-800/30 transition-colors"
                  >
                    <td className="p-4 text-xs font-mono text-neutral-400 whitespace-nowrap">
                      {format(new Date(ev.timestamp), 'HH:mm:ss.SSS')}
                    </td>
                    <td className="p-4">
                      <span className="px-2 py-1 rounded bg-red-500/10 text-red-500 text-xs font-bold border border-red-500/20">
                        {ev.event_type}
                      </span>
                    </td>
                    <td className="p-4 text-sm font-semibold">{ev.source}</td>
                    <td className="p-4 text-xs font-mono text-neutral-500">{ev.org_id}</td>
                    <td className="p-4">
                      <div className="max-w-xs truncate text-xs text-neutral-400 bg-black/30 p-2 rounded border border-neutral-800 font-mono">
                        {JSON.stringify(ev.data)}
                      </div>
                    </td>
                  </motion.tr>
                ))}
              </AnimatePresence>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default EventMonitor;
