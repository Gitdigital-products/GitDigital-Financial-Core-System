Request:


# Shared Types Package
shared_types_package = """{
  "name": "@gitdigital/shared-types",
  "version": "1.0.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "clean": "rm -rf dist"
  },
  "devDependencies": {
    "typescript": "^5.3.0"
  }
}"""

with open(f"{base_dir}/packages/shared-types/package.json", "w") as f:
    f.write(shared_types_package)

shared_types_tsconfig = """{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "declaration": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}"""

with open(f"{base_dir}/packages/shared-types/tsconfig.json", "w") as f:
    f.write(shared_types_tsconfig)

# Shared Types Index
shared_types_index = '''export interface LoanApplication {
  id: string;
  applicant: string;
  amount: number;
  currency: string;
  purpose: string;
  duration: number;
  collateral?: Collateral;
  status: LoanStatus;
  creditScore?: number;
  riskLevel?: RiskLevel;
  createdAt: Date;
  updatedAt: Date;
  workflowState: WorkflowState;
  complianceStatus: ComplianceStatus;
  taxEvents: TaxEvent[];
}

export interface Collateral {
  type: CollateralType;
  asset: string;
  amount: number;
  valueUsd: number;
  lockedUntil?: Date;
}

export enum CollateralType {
  SOL = 'SOL',
  USDC = 'USDC',
  NFT = 'NFT',
  TOKEN = 'TOKEN'
}

export enum LoanStatus {
  PENDING = 'PENDING',
  UNDER_REVIEW = 'UNDER_REVIEW',
  APPROVED = 'APPROVED',
  REJECTED = 'REJECTED',
  FUNDED = 'FUNDED',
  ACTIVE = 'ACTIVE',
  REPAID = 'REPAID',
  DEFAULTED = 'DEFAULTED',
  LIQUIDATED = 'LIQUIDATED'
}

export enum RiskLevel {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH',
  CRITICAL = 'CRITICAL'
}

export enum WorkflowState {
  INITIATED = 'INITIATED',
  CREDIT_CHECK = 'CREDIT_CHECK',
  COMPLIANCE_CHECK = 'COMPLIANCE_CHECK',
  AI_ANALYSIS = 'AI_ANALYSIS',
  APPROVAL_PENDING = 'APPROVAL_PENDING',
  FUNDING = 'FUNDING',
  ACTIVE = 'ACTIVE',
  CLOSED = 'CLOSED'
}

export enum ComplianceStatus {
  PENDING = 'PENDING',
  KYC_REQUIRED = 'KYC_REQUIRED',
  AML_CHECK = 'AML_CHECK',
  APPROVED = 'APPROVED',
  REJECTED = 'REJECTED',
  FLAGGED = 'FLAGGED'
}

export interface CreditScore {
  wallet: string;
  score: number;
  history: CreditHistory[];
  factors: CreditFactor[];
  lastUpdated: Date;
  provider: string;
}

export interface CreditHistory {
  date: Date;
  event: string;
  impact: number;
  txSignature?: string;
}

export interface CreditFactor {
  name: string;
  weight: number;
  value: number;
  description: string;
}

export interface ComplianceCheck {
  id: string;
  wallet: string;
  type: ComplianceCheckType;
  status: ComplianceCheckStatus;
  results: ComplianceResult;
  checkedAt: Date;
  provider: string;
}

export enum ComplianceCheckType {
  KYC = 'KYC',
  AML = 'AML',
  SANCTIONS = 'SANCTIONS',
  TRANSACTION_MONITORING = 'TRANSACTION_MONITORING'
}

export enum ComplianceCheckStatus {
  PENDING = 'PENDING',
  IN_PROGRESS = 'IN_PROGRESS',
  PASSED = 'PASSED',
  FAILED = 'FAILED',
  MANUAL_REVIEW = 'MANUAL_REVIEW'
}

export interface ComplianceResult {
  riskScore: number;
  flags: ComplianceFlag[];
  verified: boolean;
  metadata: Record<string, any>;
}

export interface ComplianceFlag {
  type: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  description: string;
  timestamp: Date;
}

export interface AIInsight {
  id: string;
  loanId: string;
  type: AIInsightType;
  confidence: number;
  recommendation: string;
  reasoning: string;
  metrics: Record<string, number>;
  generatedAt: Date;
  modelVersion: string;
}

export enum AIInsightType {
  CREDIT_RISK = 'CREDIT_RISK',
  FRAUD_DETECTION = 'FRAUD_DETECTION',
  GROWTH_POTENTIAL = 'GROWTH_POTENTIAL',
  LIQUIDITY_PREDICTION = 'LIQUIDITY_PREDICTION',
  MARKET_SENTIMENT = 'MARKET_SENTIMENT'
}

export interface TaxEvent {
  id: string;
  loanId: string;
  type: TaxEventType;
  amount: number;
  currency: string;
  timestamp: Date;
  jurisdiction: string;
  txSignature: string;
  metadata: Record<string, any>;
}

export enum TaxEventType {
  INTEREST_INCOME = 'INTEREST_INCOME',
  INTEREST_EXPENSE = 'INTEREST_EXPENSE',
  COLLATERAL_GAIN = 'COLLATERAL_GAIN',
  COLLATERAL_LOSS = 'COLLATERAL_LOSS',
  LIQUIDATION = 'LIQUIDATION',
  FEE = 'FEE'
}

export interface InfrastructureDeployment {
  id: string;
  service: string;
  environment: string;
  status: DeploymentStatus;
  version: string;
  config: Record<string, any>;
  deployedAt?: Date;
  healthCheck: HealthStatus;
}

export enum DeploymentStatus {
  PENDING = 'PENDING',
  IN_PROGRESS = 'IN_PROGRESS',
  SUCCESS = 'SUCCESS',
  FAILED = 'FAILED',
  ROLLBACK = 'ROLLBACK'
}

export enum HealthStatus {
  HEALTHY = 'HEALTHY',
  DEGRADED = 'DEGRADED',
  UNHEALTHY = 'UNHEALTHY',
  UNKNOWN = 'UNKNOWN'
}

export interface SystemEvent {
  id: string;
  type: string;
  payload: any;
  timestamp: Date;
  service: string;
  correlationId?: string;
}

export interface WalletConnection {
  publicKey: string;
  connected: boolean;
  chainId?: number;
  balance?: number;
}
'''

with open(f"{base_dir}/packages/shared-types/src/index.ts", "w") as f:
    f.write(shared_types_index)

print("Shared types package created")

Response:

Shared types package created