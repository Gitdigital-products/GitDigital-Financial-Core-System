Request:


# Fix the JSON syntax (Python uses True/False, JSON uses true/false)
import json
import os

service_tsconfig = {
    "compilerOptions": {
        "target": "ES2020",
        "module": "commonjs",
        "lib": ["ES2020"],
        "outDir": "./dist",
        "rootDir": "./src",
        "strict": True,
        "esModuleInterop": True,
        "skipLibCheck": True,
        "forceConsistentCasingInFileNames": True,
        "resolveJsonModule": True,
        "experimentalDecorators": True,
        "emitDecoratorMetadata": True
    },
    "include": ["src/**/*"],
    "exclude": ["node_modules", "dist"]
}

services = ['loan-engine', 'credit-authority', 'compliance-guard', 'ai-gateway', 'tax-service', 'infrastructure']

for service in services:
    with open(f"{base_dir}/services/{service}/tsconfig.json", "w") as f:
        json.dump(service_tsconfig, f, indent=2)

print("Service tsconfig files created")

# List directory structure
print("\\nProject Structure:")
for root, dirs, files in os.walk(base_dir):
    level = root.replace(base_dir, '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 2 * (level + 1)
    for file in files[:5]:  # Limit files shown per directory
        print(f'{subindent}{file}')
    if len(files) > 5:
        print(f'{subindent}... and {len(files) - 5} more files')

Response:

Service tsconfig files created
\nProject Structure:
gitdigital-financial-core/
  .gitignore
  .env.example
  turbo.json
  package.json
  docker-compose.yml
  ... and 1 more files
  contracts/
    solana/
      programs/
        credit/
          src/
        loan/
          src/
  services/
    infrastructure/
      package.json
      Dockerfile
      tsconfig.json
      src/
        index.ts
    loan-engine/
      Dockerfile
      tsconfig.json
      package.json
      src/
        index.ts
    tax-service/
      Dockerfile
      tsconfig.json
      package.json
      src/
        index.ts
    ai-gateway/
      Dockerfile
      tsconfig.json
      package.json
      src/
        index.ts
    compliance-guard/
      package.json
      Dockerfile
      tsconfig.json
      src/
        index.ts
    credit-authority/
      tsconfig.json
      package.json
      Dockerfile
      src/
        index.ts
  packages/
    shared-types/
      tsconfig.json
      package.json
      src/
        index.ts
    event-bus/
      package.json
      tsconfig.json
      src/
        index.ts
  apps/
    dashboard-ui/
      next.config.js
      tailwind.config.js
      postcss.config.js
      tsconfig.json
      Dockerfile
      ... and 1 more files
      src/
        components/
          WalletProvider.tsx
        hooks/
        lib/
        app/
          globals.css
          layout.tsx
          page.tsx