import Sidebar from "./Sidebar";

const Layout = ({ children }) => {
  return (
    <div style={{ display: "flex" }}>
      <Sidebar />
      <div style={styles.content}>
        {children}
      </div>
    </div>
  );
};

const styles = {
  content: {
    flex: 1,
    padding: "20px",
    background: "#f1f5f9",
    minHeight: "100vh"
  }
};

export default Layout;