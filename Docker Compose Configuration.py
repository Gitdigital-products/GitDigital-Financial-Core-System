Request:


# Docker Compose Configuration
docker_compose = '''version: '3.8'

services:
  # Infrastructure
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: gitdigital
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  # Core Services
  loan-engine:
    build:
      context: ../../services/loan-engine
      dockerfile: Dockerfile
    ports:
      - "3001:3001"
    environment:
      - PORT=3001
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_USER=postgres
      - DB_PASSWORD=password
      - DB_NAME=gitdigital_loans
      - REDIS_URL=redis://redis:6379
      - KAFKA_BROKERS=kafka:9092
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      kafka:
        condition: service_started
    volumes:
      - ../../services/loan-engine:/app
      - /app/node_modules

  credit-authority:
    build:
      context: ../../services/credit-authority
      dockerfile: Dockerfile
    ports:
      - "3002:3002"
    environment:
      - PORT=3002
      - REDIS_URL=redis://redis:6379
      - KAFKA_BROKERS=kafka:9092
      - SOLANA_RPC=https://api.devnet.solana.com
    depends_on:
      - redis
      - kafka
    volumes:
      - ../../services/credit-authority:/app
      - /app/node_modules

  compliance-guard:
    build:
      context: ../../services/compliance-guard
      dockerfile: Dockerfile
    ports:
      - "3003:3003"
    environment:
      - PORT=3003
      - REDIS_URL=redis://redis:6379
      - KAFKA_BROKERS=kafka:9092
    depends_on:
      - redis
      - kafka
    volumes:
      - ../../services/compliance-guard:/app
      - /app/node_modules

  ai-gateway:
    build:
      context: ../../services/ai-gateway
      dockerfile: Dockerfile
    ports:
      - "3004:3004"
    environment:
      - PORT=3004
      - REDIS_URL=redis://redis:6379
      - KAFKA_BROKERS=kafka:9092
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - redis
      - kafka
    volumes:
      - ../../services/ai-gateway:/app
      - /app/node_modules

  tax-service:
    build:
      context: ../../services/tax-service
      dockerfile: Dockerfile
    ports:
      - "3005:3005"
    environment:
      - PORT=3005
      - REDIS_URL=redis://redis:6379
      - KAFKA_BROKERS=kafka:9092
    depends_on:
      - redis
      - kafka
    volumes:
      - ../../services/tax-service:/app
      - /app/node_modules

  infrastructure:
    build:
      context: ../../services/infrastructure
      dockerfile: Dockerfile
    ports:
      - "3006:3006"
    environment:
      - PORT=3006
      - REDIS_URL=redis://redis:6379
      - KAFKA_BROKERS=kafka:9092
    depends_on:
      - redis
      - kafka
    volumes:
      - ../../services/infrastructure:/app
      - /app/node_modules
      - /var/run/docker.sock:/var/run/docker.sock

  # Frontend
  dashboard-ui:
    build:
      context: ../../apps/dashboard-ui
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:3001
    depends_on:
      - loan-engine
      - credit-authority
      - compliance-guard
      - ai-gateway
      - tax-service
      - infrastructure
    volumes:
      - ../../apps/dashboard-ui:/app
      - /app/node_modules
      - /app/.next

volumes:
  postgres_data:
  redis_data:
'''

with open(f"{base_dir}/docker-compose.yml", "w") as f:
    f.write(docker_compose)

# Create Dockerfiles for services
loan_dockerfile = '''FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3001

CMD ["npm", "start"]
'''

services = ['loan-engine', 'credit-authority', 'compliance-guard', 'ai-gateway', 'tax-service', 'infrastructure']
for service in services:
    with open(f"{base_dir}/services/{service}/Dockerfile", "w") as f:
        f.write(loan_dockerfile)

# Dashboard Dockerfile
dashboard_dockerfile = '''FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
'''

with open(f"{base_dir}/apps/dashboard-ui/Dockerfile", "w") as f:
    f.write(dashboard_dockerfile)

print("Docker configuration created")

Response:

Docker configuration created