Request:


# Dashboard UI - Next.js Application
dashboard_package = """{
  "name": "@gitdigital/dashboard-ui",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "@gitdigital/shared-types": "*",
    "@solana/wallet-adapter-base": "^0.9.23",
    "@solana/wallet-adapter-react": "^0.15.35",
    "@solana/wallet-adapter-react-ui": "^0.9.34",
    "@solana/wallet-adapter-wallets": "^0.19.32",
    "@solana/web3.js": "^1.87.6",
    "next": "14.0.4",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "recharts": "^2.10.3",
    "tailwindcss": "^3.3.6",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "lucide-react": "^0.294.0",
    "date-fns": "^2.30.0"
  },
  "devDependencies": {
    "@types/node": "^20.10.0",
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "eslint": "^8.55.0",
    "eslint-config-next": "14.0.4",
    "typescript": "^5.3.0"
  }
}"""

with open(f"{base_dir}/apps/dashboard-ui/package.json", "w") as f:
    f.write(dashboard_package)

# Next.js config
next_config = """/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@gitdigital/shared-types'],
  async rewrites() {
    return [
      {
        source: '/api/loans/:path*',
        destination: 'http://localhost:3001/api/loans/:path*',
      },
      {
        source: '/api/credit/:path*',
        destination: 'http://localhost:3002/api/credit/:path*',
      },
      {
        source: '/api/compliance/:path*',
        destination: 'http://localhost:3003/api/compliance/:path*',
      },
      {
        source: '/api/ai/:path*',
        destination: 'http://localhost:3004/api/ai/:path*',
      },
      {
        source: '/api/tax/:path*',
        destination: 'http://localhost:3005/api/tax/:path*',
      },
      {
        source: '/api/infra/:path*',
        destination: 'http://localhost:3006/api/infra/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
"""

with open(f"{base_dir}/apps/dashboard-ui/next.config.js", "w") as f:
    f.write(next_config)

# Tailwind config
tailwind_config = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'gitdigital-dark': '#0a0a0f',
        'gitdigital-card': '#13131f',
        'gitdigital-border': '#2a2a3c',
        'gitdigital-primary': '#3b82f6',
        'gitdigital-success': '#10b981',
        'gitdigital-warning': '#f59e0b',
        'gitdigital-danger': '#ef4444',
        'gitdigital-purple': '#8b5cf6',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [],
};
"""

with open(f"{base_dir}/apps/dashboard-ui/tailwind.config.js", "w") as f:
    f.write(tailwind_config)

# PostCSS config
postcss_config = """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
"""

with open(f"{base_dir}/apps/dashboard-ui/postcss.config.js", "w") as f:
    f.write(postcss_config)

# TypeScript config
tsconfig = """{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}"""

with open(f"{base_dir}/apps/dashboard-ui/tsconfig.json", "w") as f:
    f.write(tsconfig)

print("Dashboard UI configuration files created")

Response:

Dashboard UI configuration files created