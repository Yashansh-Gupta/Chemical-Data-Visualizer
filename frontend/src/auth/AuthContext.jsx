import { createContext, useContext, useState, useEffect } from "react";
import api from "../api/axios";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Sync auth state on refresh
  useEffect(() => {
    const token = localStorage.getItem("access");
    setIsAuthenticated(!!token);
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    try {
      const response = await api.post("/api/token/", {
        username,
        password,
      });

      localStorage.setItem("access", response.data.access);
      localStorage.setItem("refresh", response.data.refresh);

      setIsAuthenticated(true);
      return { success: true };
    } catch (error) {
      console.error("LOGIN ERROR:", error.response?.data || error.message);

      if (error.response?.status === 401) {
        return { success: false, message: "Invalid username or password" };
      }

      return { success: false, message: "Login failed. Server error." };
    }
  };

  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    setIsAuthenticated(false);
  };

  if (loading) {
  return <div>Loading...</div>;
  }

  return (
    <AuthContext.Provider value={{ login, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
};
