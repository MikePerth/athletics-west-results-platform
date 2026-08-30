import { Link } from "react-router-dom";

export default function AdminNav() {

    function logout() {

        localStorage.removeItem(
            "access_token"
        );

        localStorage.removeItem(
            "username"
        );

        window.location.href =
            "/login";
    }

    return (

        <nav
            style={{
                display: "flex",
                alignItems: "center",
                gap: "1rem",
                padding: "1rem 0",
                marginBottom: "2rem",
                borderBottom: "1px solid #ddd",
                flexWrap: "wrap"
            }}
        >

            <Link to="/admin">
                Home
            </Link>

            <Link to="/admin/results">
                Results
            </Link>

            <Link to="/admin/results/new">
                New Result
            </Link>

            <Link to="/admin/athletes">
                Athletes
            </Link>

            <Link to="/admin/athletes/merge">
                Merge Athletes
            </Link>

            <Link to="/admin/users">
                Users
            </Link>

            <Link to="/upload">
                Imports
            </Link>

            <span
                style={{
                    marginLeft: "auto",
                    color: "#666",
                    fontSize: "0.9rem"
                }}
            >
                {
                    localStorage.getItem(
                        "username"
                    ) || ""
                }
            </span>

            <button
                onClick={logout}
            >
                Logout
            </button>

        </nav>

    );
}