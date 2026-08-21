import { Link } from "react-router-dom";

export default function AdminHome() {
  return (
    <div style={{ padding: "2rem" }}>
      <h1>Athletics West Results Platform</h1>

      <h2>Administration</h2>

      <ul>
        <li>
          <Link to="/admin/athletes">
            Athlete Search
          </Link>
        </li>

        <li>
          <Link to="/upload">
            Import Results
          </Link>
        </li>
      </ul>
    </div>
  );
}