import { NavLink } from "react-router-dom";

const routes = [
  { path: "/", label: "Dashboard" },
  { path: "/transactions", label: "Transactions" },
  { path: "/analyze", label: "Analyze" },
];

const Sidebar = () => {
  return (
    <div style={styles.sidebar}>
      <h2 style={{ color: "white" }}>Personal Ledger</h2>

      <nav style={styles.tabNav}>
        {routes.map((route) => (
          <NavLink
            key={route.path}
            to={route.path}
            end={route.path === "/"}
            style={({ isActive }) =>
              isActive ? { ...styles.tab, ...styles.activeTab } : styles.tab
            }
          >
            {route.label}
          </NavLink>
        ))}
      </nav>
    </div>
  );
};

const styles = {
  sidebar: {
    width: "220px",
    minHeight: "100vh",
    background: "#1e293b",
    color: "white",
    padding: "20px",
    display: "flex",
    flexDirection: "column",
    gap: "16px",
  },
  tabNav: {
    display: "flex",
    flexDirection: "column",
    gap: "8px",
  },
  tab: {
    color: "#cbd5e1",
    textDecoration: "none",
    background: "#0f172a",
    borderRadius: "8px",
    padding: "10px 12px",
    border: "1px solid transparent",
    fontWeight: 500,
  },
  activeTab: {
    background: "#334155",
    color: "white",
    borderColor: "#60a5fa",
  },
};

export default Sidebar;