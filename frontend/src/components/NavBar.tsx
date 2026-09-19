import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export function NavBar() {
  const { user, logout } = useAuth();

  return (
    <header className="navbar">
      <Link to="/dashboard" className="brand">
        Darukaa.Earth
      </Link>
      {user && (
        <div className="nav-actions">
          <span className="nav-user">{user.full_name}</span>
          <button onClick={logout}>Log out</button>
        </div>
      )}
    </header>
  );
}
