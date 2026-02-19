Request;


# Create additional service files (tsconfig.json for each)
import json

service_tsconfig = {
    "compilerOptions": {
        "target": "ES2020",
        "module": "commonjs",
        "lib": ["ES2020"],
        "outDir": "./dist",
        "rootDir": "./src",
        "strict": true,
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

# Create package.json for shared packages that need building
for package in ['shared-types', 'event-bus']:
    pkg_json = {
        "name": f"@gitdigital/{package}",
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
    }
    
    if package == 'event-bus':
        pkg_json["dependencies"] = {
            "kafkajs": "^2.2.4",
            "ioredis": "^5.3.2",
            "uuid": "^9.0.1",
            "@gitdigital/shared-types": "*"
        }
        pkg_json["devDependencies"]["@types/uuid"] = "^9.0.7"
    
    with open(f"{base_dir}/packages/{package}/package.json", "w") as f:
        json.dump(pkg_json, f, indent=2)

# List all created files
import os

def list_files(startpath):
    file_list = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 2 * level
        file_list.append(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            file_list.append(f'{subindent}{file}')
    return file_list

files = list_files(base_dir)
print("\\n".join(files[:50]))  # Print first 50 lines
print(f"\\n... and {len(files) - 50} more items")

Response:

Error:
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[17], line 11
      1 # Create additional service files (tsconfig.json for each)
      2 import json
      4 service_tsconfig = {
      5     "compilerOptions": {
      6         "target": "ES2020",
      7         "module": "commonjs",
      8         "lib": ["ES2020"],
      9         "outDir": "./dist",
     10         "rootDir": "./src",
---> 11         "strict": true,
     12         "esModuleInterop": True,
     13         "skipLibCheck": True,
     14         "forceConsistentCasingInFileNames": True,
     15         "resolveJsonModule": True,
     16         "experimentalDecorators": True,
     17         "emitDecoratorMetadata": True
     18     },
     19     "include": ["src/**/*"],
     20     "exclude": ["node_modules", "dist"]
     21 }
     23 services = ['loan-engine', 'credit-authority', 'compliance-guard', 'ai-gateway', 'tax-service', 'infrastructure']
     25 for service in services:

NameError: name 'true' is not defined