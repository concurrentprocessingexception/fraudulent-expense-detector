# Personal Ledger Frontend

This is the React frontend for the Personal Ledger app.

## Project Structure

- `src/` - React source code
- `src/layout/Sidebar.js` - Side navigation with tabs
- `src/App.js` - Main app routing
- `public/` - static public assets

## Getting Started

### Install dependencies

\`\`\`bash
cd frontend/personal-ledger
npm install
\`\`\`

### Run app

\`\`\`bash
npm start
\`\`\`

Open http://localhost:3000 in your browser.

### Build for production

\`\`\`bash
npm run build
\`\`\`

### Run tests

\`\`\`bash
npm test
\`\`\`

## How Tabs Work in Sidebar

We use `NavLink` from `react-router-dom` so the active tab is highlighted. See `src/layout/Sidebar.js`.

Example tab config:

\`\`\`js
const routes = [
  { path: "/", label: "Dashboard" },
  { path: "/transactions", label: "Transactions" },
  { path: "/analyze", label: "Analyze" },
  { path: "/alerts", label: "Alerts" },
];
\`\`\`

## Quick Notes

- If you add new routes, add them to both `Sidebar.js` and `App.js`.
- For API integration, point frontend calls to your backend base URL (e.g., `http://localhost:8000`).

## Troubleshooting

- If `npm start` fails due to port conflict, choose another port:

\`\`\`bash
set PORT=3001 && npm start
\`\`\`

- If dependency issues occur, delete `node_modules` and reinstall:

\`\`\`bash
rmdir /S /Q node_modules
del package-lock.json
npm install
\`\`\`