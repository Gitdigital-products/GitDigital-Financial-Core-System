
import os

# Create the base directory structure
base_dir = "/mnt/kimi/output/gitdigital-financial-core"
dirs = [
    "packages/shared-types/src",
    "packages/event-bus/src", 
    "services/loan-engine/src",
    "services/credit-authority/src",
    "services/compliance-guard/src",
    "services/ai-gateway/src",
    "services/tax-service/src",
    "services/infrastructure/src",
    "apps/dashboard-ui/src/app",
    "apps/dashboard-ui/src/components",
    "apps/dashboard-ui/src/hooks",
    "apps/dashboard-ui/src/lib",
    "contracts/solana/programs/loan/src",
    "contracts/solana/programs/credit/src"
]

for d in dirs:
    os.makedirs(f"{base_dir}/{d}", exist_ok=True)

print("Directory structure created successfully")
print(f"Base directory: {base_dir}")


Response 

Directory structure created successfully
Base directory: /mnt/kimi/output/gitdigital-financial-core