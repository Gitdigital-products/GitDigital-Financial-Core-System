Request:


# Event Bus Package
event_bus_package = """{
  "name": "@gitdigital/event-bus",
  "version": "1.0.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "clean": "rm -rf dist"
  },
  "dependencies": {
    "kafkajs": "^2.2.4",
    "ioredis": "^5.3.2",
    "uuid": "^9.0.1"
  },
  "devDependencies": {
    "@types/uuid": "^9.0.7",
    "typescript": "^5.3.0"
  }
}"""

with open(f"{base_dir}/packages/event-bus/package.json", "w") as f:
    f.write(event_bus_package)

event_bus_tsconfig = """{
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

with open(f"{base_dir}/packages/event-bus/tsconfig.json", "w") as f:
    f.write(event_bus_tsconfig)

event_bus_index = '''import { Kafka, Producer, Consumer, EachMessagePayload } from 'kafkajs';
import Redis from 'ioredis';
import { v4 as uuidv4 } from 'uuid';
import { SystemEvent } from '@gitdigital/shared-types';

export interface EventBusConfig {
  kafkaBrokers: string[];
  redisUrl: string;
  clientId: string;
}

export class EventBus {
  private kafka: Kafka;
  private producer: Producer;
  private redis: Redis;
  private consumers: Map<string, Consumer> = new Map();
  private handlers: Map<string, ((event: SystemEvent) => Promise<void>)[]> = new Map();

  constructor(private config: EventBusConfig) {
    this.kafka = new Kafka({
      clientId: config.clientId,
      brokers: config.kafkaBrokers,
    });
    this.producer = this.kafka.producer();
    this.redis = new Redis(config.redisUrl);
  }

  async connect(): Promise<void> {
    await this.producer.connect();
    console.log('EventBus: Connected to Kafka');
  }

  async disconnect(): Promise<void> {
    await this.producer.disconnect();
    for (const consumer of this.consumers.values()) {
      await consumer.disconnect();
    }
    await this.redis.quit();
    console.log('EventBus: Disconnected');
  }

  async publish(topic: string, payload: any, correlationId?: string): Promise<void> {
    const event: SystemEvent = {
      id: uuidv4(),
      type: topic,
      payload,
      timestamp: new Date(),
      service: this.config.clientId,
      correlationId: correlationId || uuidv4(),
    };

    // Publish to Kafka
    await this.producer.send({
      topic,
      messages: [{ value: JSON.stringify(event) }],
    });

    // Cache in Redis for quick access
    await this.redis.setex(
      `event:${event.id}`,
      86400, // 24 hours
      JSON.stringify(event)
    );

    console.log(`EventBus: Published event ${event.id} to topic ${topic}`);
  }

  async subscribe(
    topic: string,
    groupId: string,
    handler: (event: SystemEvent) => Promise<void>
  ): Promise<void> {
    if (!this.handlers.has(topic)) {
      this.handlers.set(topic, []);
    }
    this.handlers.get(topic)!.push(handler);

    const consumer = this.kafka.consumer({ groupId });
    await consumer.connect();
    await consumer.subscribe({ topic, fromBeginning: false });

    await consumer.run({
      eachMessage: async ({ message }: EachMessagePayload) => {
        if (message.value) {
          const event: SystemEvent = JSON.parse(message.value.toString());
          console.log(`EventBus: Received event ${event.id} from topic ${topic}`);
          
          const handlers = this.handlers.get(topic) || [];
          for (const h of handlers) {
            try {
              await h(event);
            } catch (error) {
              console.error(`EventBus: Error handling event ${event.id}:`, error);
            }
          }
        }
      },
    });

    this.consumers.set(`${topic}-${groupId}`, consumer);
    console.log(`EventBus: Subscribed to topic ${topic} with group ${groupId}`);
  }

  async requestResponse<T>(
    requestTopic: string,
    responseTopic: string,
    payload: any,
    timeout: number = 30000
  ): Promise<T> {
    const correlationId = uuidv4();
    
    return new Promise(async (resolve, reject) => {
      const timeoutId = setTimeout(() => {
        reject(new Error('Request timeout'));
      }, timeout);

      const consumer = this.kafka.consumer({ groupId: `temp-${uuidv4()}` });
      await consumer.connect();
      await consumer.subscribe({ topic: responseTopic });

      await consumer.run({
        eachMessage: async ({ message }) => {
          if (message.value) {
            const event: SystemEvent = JSON.parse(message.value.toString());
            if (event.correlationId === correlationId) {
              clearTimeout(timeoutId);
              await consumer.disconnect();
              resolve(event.payload as T);
            }
          }
        },
      });

      await this.publish(requestTopic, payload, correlationId);
    });
  }
}

export const EventTopics = {
  // Loan Events
  LOAN_APPLICATION_CREATED: 'loan.application.created',
  LOAN_APPLICATION_UPDATED: 'loan.application.updated',
  LOAN_APPROVED: 'loan.approved',
  LOAN_REJECTED: 'loan.rejected',
  LOAN_FUNDED: 'loan.funded',
  LOAN_REPAID: 'loan.repaid',
  LOAN_DEFAULTED: 'loan.defaulted',
  LOAN_LIQUIDATED: 'loan.liquidated',

  // Credit Events
  CREDIT_CHECK_REQUESTED: 'credit.check.requested',
  CREDIT_CHECK_COMPLETED: 'credit.check.completed',
  CREDIT_SCORE_UPDATED: 'credit.score.updated',

  // Compliance Events
  COMPLIANCE_CHECK_REQUESTED: 'compliance.check.requested',
  COMPLIANCE_CHECK_COMPLETED: 'compliance.check.completed',
  COMPLIANCE_FLAG_RAISED: 'compliance.flag.raised',

  // AI Events
  AI_ANALYSIS_REQUESTED: 'ai.analysis.requested',
  AI_INSIGHT_GENERATED: 'ai.insight.generated',
  AI_RISK_ALERT: 'ai.risk.alert',

  // Tax Events
  TAX_EVENT_RECORDED: 'tax.event.recorded',
  TAX_REPORT_GENERATED: 'tax.report.generated',

  // Infrastructure Events
  DEPLOYMENT_REQUESTED: 'infrastructure.deployment.requested',
  DEPLOYMENT_COMPLETED: 'infrastructure.deployment.completed',
  HEALTH_CHECK_FAILED: 'infrastructure.health.failed',

  // System Events
  SYSTEM_ERROR: 'system.error',
  SYSTEM_WARNING: 'system.warning',
} as const;
'''

with open(f"{base_dir}/packages/event-bus/src/index.ts", "w") as f:
    f.write(event_bus_index)

print("Event bus package created")

Response:

Event bus package created