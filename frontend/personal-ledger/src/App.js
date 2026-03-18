import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./layout/Layout";
import Transactions from "./pages/Transactions";
import Dashboard from "./pages/Dashboard"
import Analyze from "./pages/Analyze";

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/transactions" element={<Transactions />} />
          <Route path="/analyze" element={<Analyze />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;