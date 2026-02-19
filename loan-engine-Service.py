Request: 

# Loan Engine Service
loan_engine_package = """{
  "name": "@gitdigital/loan-engine",
  "version": "1.0.0",
  "scripts": {
    "build": "tsc",
    "dev": "ts-node-dev --respawn --transpile-only src/index.ts",
    "start": "node dist/index.js",
    "clean": "rm -rf dist"
  },
  "dependencies": {
    "@gitdigital/shared-types": "*",
    "@gitdigital/event-bus": "*",
    "@solana/web3.js": "^1.87.6",
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "helmet": "^7.1.0",
    "dotenv": "^16.3.1",
    "pg": "^8.11.3",
    "typeorm": "^0.3.17",
    "reflect-metadata": "^0.1.13",
    "class-validator": "^0.14.0",
    "class-transformer": "^0.5.1"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/cors": "^2.8.17",
    "@types/node": "^20.10.0",
    "@types/pg": "^8.10.9",
    "ts-node-dev": "^2.0.0",
    "typescript": "^5.3.0"
  }
}"""

with open(f"{base_dir}/services/loan-engine/package.json", "w") as f:
    f.write(loan_engine_package)

loan_engine_index = '''import 'reflect-metadata';
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import { DataSource } from 'typeorm';
import { EventBus, EventTopics } from '@gitdigital/event-bus';
import {
  LoanApplication,
  LoanStatus,
  WorkflowState,
  ComplianceStatus,
  SystemEvent,
} from '@gitdigital/shared-types';

dotenv.config();

const app = express();
app.use(helmet());
app.use(cors());
app.use(express.json());

// Database configuration
const AppDataSource = new DataSource({
  type: 'postgres',
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432'),
  username: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'password',
  database: process.env.DB_NAME || 'gitdigital_loans',
  entities: ['src/entities/**/*.ts'],
  synchronize: true,
  logging: false,
});

// Event Bus
const eventBus = new EventBus({
  kafkaBrokers: (process.env.KAFKA_BROKERS || 'localhost:9092').split(','),
  redisUrl: process.env.REDIS_URL || 'redis://localhost:6379',
  clientId: 'loan-engine',
});

// In-memory store for demo (replace with DB in production)
const loans = new Map<string, LoanApplication>();

// Initialize
async function initialize() {
  await AppDataSource.initialize();
  await eventBus.connect();

  // Subscribe to relevant events
  await eventBus.subscribe(
    EventTopics.CREDIT_CHECK_COMPLETED,
    'loan-engine-credit',
    handleCreditCheckCompleted
  );

  await eventBus.subscribe(
    EventTopics.COMPLIANCE_CHECK_COMPLETED,
    'loan-engine-compliance',
    handleComplianceCheckCompleted
  );

  await eventBus.subscribe(
    EventTopics.AI_INSIGHT_GENERATED,
    'loan-engine-ai',
    handleAIInsight
  );

  console.log('Loan Engine: Initialized and connected');
}

// Event Handlers
async function handleCreditCheckCompleted(event: SystemEvent): Promise<void> {
  const { loanId, creditScore, riskLevel } = event.payload;
  const loan = loans.get(loanId);
  
  if (loan) {
    loan.creditScore = creditScore;
    loan.riskLevel = riskLevel;
    loan.workflowState = WorkflowState.COMPLIANCE_CHECK;
    loan.updatedAt = new Date();
    
    await eventBus.publish(EventTopics.COMPLIANCE_CHECK_REQUESTED, {
      loanId: loan.id,
      wallet: loan.applicant,
      amount: loan.amount,
    });
    
    console.log(`Loan Engine: Credit check completed for loan ${loanId}`);
  }
}

async function handleComplianceCheckCompleted(event: SystemEvent): Promise<void> {
  const { loanId, status, flags } = event.payload;
  const loan = loans.get(loanId);
  
  if (loan) {
    loan.complianceStatus = status;
    
    if (status === ComplianceStatus.APPROVED) {
      loan.workflowState = WorkflowState.AI_ANALYSIS;
      await eventBus.publish(EventTopics.AI_ANALYSIS_REQUESTED, {
        loanId: loan.id,
        creditScore: loan.creditScore,
        amount: loan.amount,
        purpose: loan.purpose,
      });
    } else {
      loan.status = LoanStatus.REJECTED;
      loan.workflowState = WorkflowState.CLOSED;
    }
    
    loan.updatedAt = new Date();
    console.log(`Loan Engine: Compliance check completed for loan ${loanId}`);
  }
}

async function handleAIInsight(event: SystemEvent): Promise<void> {
  const { loanId, recommendation, confidence } = event.payload;
  const loan = loans.get(loanId);
  
  if (loan && loan.workflowState === WorkflowState.AI_ANALYSIS) {
    if (recommendation === 'APPROVE' && confidence > 0.7) {
      loan.status = LoanStatus.APPROVED;
      loan.workflowState = WorkflowState.APPROVAL_PENDING;
      
      await eventBus.publish(EventTopics.LOAN_APPROVED, {
        loanId: loan.id,
        amount: loan.amount,
        applicant: loan.applicant,
      });
    } else {
      loan.status = LoanStatus.REJECTED;
      loan.workflowState = WorkflowState.CLOSED;
      await eventBus.publish(EventTopics.LOAN_REJECTED, {
        loanId: loan.id,
        reason: 'AI risk assessment failed',
      });
    }
    
    loan.updatedAt = new Date();
    console.log(`Loan Engine: AI analysis completed for loan ${loanId}`);
  }
}

// API Routes
app.post('/api/loans', async (req, res) => {
  try {
    const { applicant, amount, currency, purpose, duration, collateral } = req.body;
    
    const loan: LoanApplication = {
      id: `loan_${Date.now()}`,
      applicant,
      amount,
      currency,
      purpose,
      duration,
      collateral,
      status: LoanStatus.PENDING,
      workflowState: WorkflowState.INITIATED,
      complianceStatus: ComplianceStatus.PENDING,
      taxEvents: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    
    loans.set(loan.id, loan);
    
    // Start workflow
    await eventBus.publish(EventTopics.LOAN_APPLICATION_CREATED, loan);
    await eventBus.publish(EventTopics.CREDIT_CHECK_REQUESTED, {
      loanId: loan.id,
      wallet: loan.applicant,
    });
    
    loan.workflowState = WorkflowState.CREDIT_CHECK;
    
    res.status(201).json({ success: true, data: loan });
  } catch (error) {
    console.error('Error creating loan:', error);
    res.status(500).json({ success: false, error: 'Internal server error' });
  }
});

app.get('/api/loans/:id', async (req, res) => {
  const loan = loans.get(req.params.id);
  if (loan) {
    res.json({ success: true, data: loan });
  } else {
    res.status(404).json({ success: false, error: 'Loan not found' });
  }
});

app.get('/api/loans', async (req, res) => {
  const loanList = Array.from(loans.values());
  res.json({ success: true, data: loanList });
});

app.post('/api/loans/:id/fund', async (req, res) => {
  const loan = loans.get(req.params.id);
  if (!loan) {
    return res.status(404).json({ success: false, error: 'Loan not found' });
  }
  
  if (loan.status !== LoanStatus.APPROVED) {
    return res.status(400).json({ success: false, error: 'Loan not approved' });
  }
  
  loan.status = LoanStatus.FUNDED;
  loan.workflowState = WorkflowState.ACTIVE;
  loan.updatedAt = new Date();
  
  await eventBus.publish(EventTopics.LOAN_FUNDED, {
    loanId: loan.id,
    amount: loan.amount,
    applicant: loan.applicant,
  });
  
  res.json({ success: true, data: loan });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Loan Engine running on port ${PORT}`);
  initialize().catch(console.error);
});
'''

with open(f"{base_dir}/services/loan-engine/src/index.ts", "w") as f:
    f.write(loan_engine_index)

print("Loan Engine service created")

Response:

Loan Engine service created