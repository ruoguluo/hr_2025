# Company Analysis Platform

A comprehensive business intelligence and competitive analysis platform built with React, TypeScript, and Vite.

## Environment Setup

The application uses environment variables to manage API configurations:

- `.env` - Production environment settings
- `.env.development` - Development environment settings

### Environment Variables

- `VITE_API_URL` - The base URL for the API server
  - Production: http://107.182.26.178:5001/api
  - Development: http://localhost:5001/api

## Development

1. Install dependencies:
```bash
pnpm install
```

2. Start the development server:
```bash
pnpm run dev
```

## Production Build

1. Build the application:
```bash
pnpm run build
```

2. Preview the production build:
```bash
pnpm run preview
```

## Features

- Company information analysis
- Product and service evaluation
- Market comparison analysis
- Competitive positioning
- Report generation and export

## Technology Stack

- React 18
- TypeScript
- Vite
- Tailwind CSS
- Shadcn UI Components