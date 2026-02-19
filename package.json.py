Request:

# Root package.json - Turborepo configuration
root_package = """{
  "name": "gitdigital-financial-core",
  "version": "1.0.0",
  "private": true,
  "description": "Decentralized Loan and Financial Infrastructure System",
  "workspaces": [
    "packages/*",
    "services/*",
    "apps/*"
  ],
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev --parallel",
    "lint": "turbo run lint",
    "test": "turbo run test",
    "clean": "turbo run clean && rm -rf node_modules",
    "format": "prettier --write \"**/*.{ts,tsx,md}\"",
    "db:up": "docker-compose up -d postgres redis kafka",
    "db:down": "docker-compose down",
    "solana:local": "solana-test-validator",
    "deploy:programs": "anchor deploy"
  },
  "devDependencies": {
    "@types/node": "^20.10.0",
    "eslint": "^8.55.0",
    "prettier": "^3.1.0",
    "turbo": "^1.11.0",
    "typescript": "^5.3.0"
  },
  "engines": {
    "node": ">=18.0.0"
  },
  "packageManager": "npm@10.2.0"
}"""

with open(f"{base_dir}/package.json", "w") as f:
    f.write(root_package)

# Turbo configuration
turbo_config = """{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**", "dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {},
    "test": {
      "dependsOn": ["build"]
    },
    "clean": {
      "cache": false
    }
  }
}"""

with open(f"{base_dir}/turbo.json", "w") as f:
    f.write(turbo_config)

print("Root configuration files created")

Response:

Root configuration files created