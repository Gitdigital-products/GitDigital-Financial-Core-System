Request:


# Main Dashboard Page
main_page = ''''use client';

import { useState, useEffect } from 'react';
import { useWallet } from '@solana/wallet-adapter-react';
import { WalletMultiButton } from '@solana/wallet-adapter-react-ui';
import { 
  Activity, 
  TrendingUp, 
  Shield, 
  Brain, 
  FileText, 
  Server,
  CreditCard,
  AlertCircle,
  CheckCircle,
  XCircle,
  Clock,
  DollarSign,
  Percent,
  Wallet
} from 'lucide-react';
import { format } from 'date-fns';
import { LoanApplication, LoanStatus, WorkflowState } from '@gitdigital/shared-types';

interface Stats {
  totalLoans: number;
  activeLoans: number;
  totalVolume: number;
  avgCreditScore: number;
}

interface ServiceHealth {
  service: string;
  status: 'HEALTHY' | 'DEGRADED' | 'UNHEALTHY';
}

export default function Dashboard() {
  const { publicKey, connected } = useWallet();
  const [loans, setLoans] = useState<LoanApplication[]>([]);
  const [stats, setStats] = useState<Stats>({
    totalLoans: 0,
    activeLoans: 0,
    totalVolume: 0,
    avgCreditScore: 0,
  });
  const [health, setHealth] = useState<ServiceHealth[]>([]);
  const [showLoanModal, setShowLoanModal] = useState(false);
  const [newLoan, setNewLoan] = useState({
    amount: '',
    currency: 'USDC',
    purpose: '',
    duration: '30',
  });

  useEffect(() => {
    fetchLoans();
    fetchHealth();
    const interval = setInterval(fetchHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchLoans = async () => {
    try {
      const res = await fetch('/api/loans');
      const data = await res.json();
      if (data.success) {
        setLoans(data.data);
        calculateStats(data.data);
      }
    } catch (error) {
      console.error('Error fetching loans:', error);
    }
  };

  const fetchHealth = async () => {
    try {
      const res = await fetch('/api/infra/health');
      const data = await res.json();
      if (data.success) {
        setHealth(data.data);
      }
    } catch (error) {
      console.error('Error fetching health:', error);
    }
  };

  const calculateStats = (loanData: LoanApplication[]) => {
    const active = loanData.filter(l => l.status === LoanStatus.ACTIVE);
    const volume = loanData.reduce((sum, l) => sum + l.amount, 0);
    const avgScore = loanData.reduce((sum, l) => sum + (l.creditScore || 0), 0) / (loanData.length || 1);
    
    setStats({
      totalLoans: loanData.length,
      activeLoans: active.length,
      totalVolume: volume,
      avgCreditScore: Math.round(avgScore),
    });
  };

  const handleCreateLoan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!connected || !publicKey) return;

    try {
      const res = await fetch('/api/loans', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          applicant: publicKey.toString(),
          amount: parseFloat(newLoan.amount),
          currency: newLoan.currency,
          purpose: newLoan.purpose,
          duration: parseInt(newLoan.duration),
        }),
      });

      if (res.ok) {
        setShowLoanModal(false);
        setNewLoan({ amount: '', currency: 'USDC', purpose: '', duration: '30' });
        fetchLoans();
      }
    } catch (error) {
      console.error('Error creating loan:', error);
    }
  };

  const getStatusIcon = (status: LoanStatus) => {
    switch (status) {
      case LoanStatus.APPROVED:
      case LoanStatus.ACTIVE:
        return <CheckCircle className="w-5 h-5 text-gitdigital-success" />;
      case LoanStatus.REJECTED:
        return <XCircle className="w-5 h-5 text-gitdigital-danger" />;
      case LoanStatus.PENDING:
        return <Clock className="w-5 h-5 text-gitdigital-warning" />;
      default:
        return <Activity className="w-5 h-5 text-gitdigital-primary" />;
    }
  };

  const getHealthIcon = (status: string) => {
    switch (status) {
      case 'HEALTHY':
        return <div className="w-2 h-2 rounded-full bg-gitdigital-success pulse-glow" />;
      case 'DEGRADED':
        return <div className="w-2 h-2 rounded-full bg-gitdigital-warning" />;
      default:
        return <div className="w-2 h-2 rounded-full bg-gitdigital-danger" />;
    }
  };

  return (
    <div className="min-h-screen bg-gitdigital-dark text-white">
      {/* Header */}
      <header className="border-b border-gitdigital-border glass sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                <Wallet className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold gradient-text">GitDigital Core</span>
            </div>
            <WalletMultiButton className="!bg-gitdigital-primary hover:!bg-blue-600 !rounded-lg" />
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard 
            title="Total Loans" 
            value={stats.totalLoans} 
            icon={<CreditCard className="w-6 h-6" />}
            trend="+12%"
          />
          <StatCard 
            title="Active Loans" 
            value={stats.activeLoans} 
            icon={<Activity className="w-6 h-6" />}
            trend="+5%"
          />
          <StatCard 
            title="Total Volume" 
            value={`$${stats.totalVolume.toLocaleString()}`} 
            icon={<DollarSign className="w-6 h-6" />}
            trend="+23%"
          />
          <StatCard 
            title="Avg Credit Score" 
            value={stats.avgCreditScore} 
            icon={<TrendingUp className="w-6 h-6" />}
            trend="Stable"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Loans Section */}
          <div className="lg:col-span-2 space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold">Active Loans</h2>
              <button
                onClick={() => setShowLoanModal(true)}
                disabled={!connected}
                className="px-4 py-2 bg-gitdigital-primary hover:bg-blue-600 rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                New Loan
              </button>
            </div>

            <div className="space-y-4">
              {loans.length === 0 ? (
                <div className="glass rounded-xl p-8 text-center text-gray-400">
                  No loans found. Create your first loan to get started.
                </div>
              ) : (
                loans.map((loan) => (
                  <div key={loan.id} className="glass rounded-xl p-6 card-hover">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="font-semibold text-lg">{loan.purpose}</h3>
                        <p className="text-sm text-gray-400">{loan.id}</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        {getStatusIcon(loan.status)}
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                          loan.status === LoanStatus.ACTIVE ? 'bg-green-500/20 text-green-400' :
                          loan.status === LoanStatus.REJECTED ? 'bg-red-500/20 text-red-400' :
                          'bg-yellow-500/20 text-yellow-400'
                        }`}>
                          {loan.status}
                        </span>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div>
                        <p className="text-gray-400">Amount</p>
                        <p className="font-semibold">{loan.amount.toLocaleString()} {loan.currency}</p>
                      </div>
                      <div>
                        <p className="text-gray-400">Credit Score</p>
                        <p className="font-semibold">{loan.creditScore || 'Pending'}</p>
                      </div>
                      <div>
                        <p className="text-gray-400">Workflow</p>
                        <p className="font-semibold">{loan.workflowState}</p>
                      </div>
                    </div>

                    <div className="mt-4 pt-4 border-t border-gitdigital-border">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-400">
                          Created {format(new Date(loan.createdAt), 'MMM d, yyyy')}
                        </span>
                        {loan.riskLevel && (
                          <span className={`px-2 py-1 rounded text-xs ${
                            loan.riskLevel === 'LOW' ? 'bg-green-500/20 text-green-400' :
                            loan.riskLevel === 'MEDIUM' ? 'bg-yellow-500/20 text-yellow-400' :
                            'bg-red-500/20 text-red-400'
                          }`}>
                            {loan.riskLevel} Risk
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Service Health */}
            <div className="glass rounded-xl p-6">
              <h3 className="font-semibold mb-4 flex items-center space-x-2">
                <Server className="w-5 h-5" />
                <span>Service Health</span>
              </h3>
              <div className="space-y-3">
                {health.length === 0 ? (
                  <p className="text-sm text-gray-400">Loading...</p>
                ) : (
                  health.map((service) => (
                    <div key={service.service} className="flex items-center justify-between">
                      <span className="text-sm capitalize">{service.service.replace('-', ' ')}</span>
                      {getHealthIcon(service.status)}
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Quick Actions */}
            <div className="glass rounded-xl p-6">
              <h3 className="font-semibold mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <ActionButton icon={<Shield className="w-4 h-4" />} label="Compliance Check" />
                <ActionButton icon={<Brain className="w-4 h-4" />} label="AI Analysis" />
                <ActionButton icon={<FileText className="w-4 h-4" />} label="Tax Report" />
              </div>
            </div>

            {/* Wallet Info */}
            {connected && publicKey && (
              <div className="glass rounded-xl p-6 gradient-border">
                <h3 className="font-semibold mb-4">Wallet Connected</h3>
                <p className="text-sm text-gray-400 break-all">
                  {publicKey.toString()}
                </p>
                <div className="mt-4 pt-4 border-t border-gitdigital-border">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Network</span>
                    <span>Devnet</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* New Loan Modal */}
      {showLoanModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="glass rounded-xl p-6 w-full max-w-md mx-4">
            <h2 className="text-xl font-bold mb-4">Create New Loan</h2>
            <form onSubmit={handleCreateLoan} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Amount</label>
                <input
                  type="number"
                  value={newLoan.amount}
                  onChange={(e) => setNewLoan({ ...newLoan, amount: e.target.value })}
                  className="w-full px-4 py-2 bg-gitdigital-dark border border-gitdigital-border rounded-lg focus:outline-none focus:border-gitdigital-primary"
                  placeholder="10000"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Currency</label>
                <select
                  value={newLoan.currency}
                  onChange={(e) => setNewLoan({ ...newLoan, currency: e.target.value })}
                  className="w-full px-4 py-2 bg-gitdigital-dark border border-gitdigital-border rounded-lg focus:outline-none focus:border-gitdigital-primary"
                >
                  <option value="USDC">USDC</option>
                  <option value="SOL">SOL</option>
                  <option value="USDT">USDT</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Purpose</label>
                <input
                  type="text"
                  value={newLoan.purpose}
                  onChange={(e) => setNewLoan({ ...newLoan, purpose: e.target.value })}
                  className="w-full px-4 py-2 bg-gitdigital-dark border border-gitdigital-border rounded-lg focus:outline-none focus:border-gitdigital-primary"
                  placeholder="Business expansion"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Duration (days)</label>
                <input
                  type="number"
                  value={newLoan.duration}
                  onChange={(e) => setNewLoan({ ...newLoan, duration: e.target.value })}
                  className="w-full px-4 py-2 bg-gitdigital-dark border border-gitdigital-border rounded-lg focus:outline-none focus:border-gitdigital-primary"
                  placeholder="30"
                  required
                />
              </div>
              <div className="flex space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowLoanModal(false)}
                  className="flex-1 px-4 py-2 border border-gitdigital-border rounded-lg hover:bg-white/5 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-gitdigital-primary hover:bg-blue-600 rounded-lg transition-colors"
                >
                  Create Loan
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

function StatCard({ title, value, icon, trend }: { 
  title: string; 
  value: string | number; 
  icon: React.ReactNode;
  trend: string;
}) {
  return (
    <div className="glass rounded-xl p-6 card-hover">
      <div className="flex items-center justify-between mb-4">
        <div className="p-2 bg-gitdigital-primary/20 rounded-lg text-gitdigital-primary">
          {icon}
        </div>
        <span className="text-sm text-gitdigital-success">{trend}</span>
      </div>
      <h3 className="text-2xl font-bold">{value}</h3>
      <p className="text-sm text-gray-400">{title}</p>
    </div>
  );
}

function ActionButton({ icon, label }: { icon: React.ReactNode; label: string }) {
  return (
    <button className="w-full flex items-center space-x-3 px-4 py-3 bg-white/5 hover:bg-white/10 rounded-lg transition-colors text-left">
      <span className="text-gitdigital-primary">{icon}</span>
      <span className="text-sm font-medium">{label}</span>
    </button>
  );
}
'''

with open(f"{base_dir}/apps/dashboard-ui/src/app/page.tsx", "w") as f:
    f.write(main_page)

print("Dashboard main page created")

Response:

Dashboard main page created