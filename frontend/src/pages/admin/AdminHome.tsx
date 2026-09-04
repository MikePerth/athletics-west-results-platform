import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import AdminNav from "./AdminNav";

interface DashboardData {
    competitions: number;
    athletes: number;
    results: number;
    users: number;
}

export default function AdminHome() {

    const [loading, setLoading] =
        useState(true);

    const [dashboard, setDashboard] =
        useState<DashboardData>({
            competitions: 0,
            athletes: 0,
            results: 0,
            users: 0
        });

    useEffect(() => {

        async function loadDashboard() {

            try {

                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/admin/dashboard`
                );

                const data =
                    await response.json();

                setDashboard(data);

            } catch (error) {

                console.error(error);

            } finally {

                setLoading(false);
            }
        }

        loadDashboard();

    }, []);

    return (

        <div
            style={{
                maxWidth: "1400px",
                margin: "0 auto",
                padding: "2rem"
            }}
        >

            <AdminNav />

            <h1>
                Administration Dashboard
            </h1>

            <p>
                Athletics West Results Platform
            </p>

            {loading ? (

                <p>
                    Loading dashboard...
                </p>

            ) : (

                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns:
                            "repeat(auto-fit, minmax(220px, 1fr))",
                        gap: "1.5rem",
                        marginTop: "2rem",
                        marginBottom: "3rem"
                    }}
                >

                    <div
                        style={{
                            background: "#ffffff",
                            borderRadius: "12px",
                            padding: "1.5rem",
                            boxShadow:
                                "0 2px 8px rgba(0,0,0,0.08)"
                        }}
                    >

                        <h3>
                            Competitions
                        </h3>

                        <div
                            style={{
                                fontSize: "2rem",
                                fontWeight: 700
                            }}
                        >
                            {dashboard.competitions.toLocaleString()}
                        </div>

                    </div>

                    <div
                        style={{
                            background: "#ffffff",
                            borderRadius: "12px",
                            padding: "1.5rem",
                            boxShadow:
                                "0 2px 8px rgba(0,0,0,0.08)"
                        }}
                    >

                        <h3>
                            Athletes
                        </h3>

                        <div
                            style={{
                                fontSize: "2rem",
                                fontWeight: 700
                            }}
                        >
                            {dashboard.athletes.toLocaleString()}
                        </div>

                    </div>

                    <div
                        style={{
                            background: "#ffffff",
                            borderRadius: "12px",
                            padding: "1.5rem",
                            boxShadow:
                                "0 2px 8px rgba(0,0,0,0.08)"
                        }}
                    >

                        <h3>
                            Results
                        </h3>

                        <div
                            style={{
                                fontSize: "2rem",
                                fontWeight: 700
                            }}
                        >
                            {dashboard.results.toLocaleString()}
                        </div>

                    </div>

                    <div
                        style={{
                            background: "#ffffff",
                            borderRadius: "12px",
                            padding: "1.5rem",
                            boxShadow:
                                "0 2px 8px rgba(0,0,0,0.08)"
                        }}
                    >

                        <h3>
                            Users
                        </h3>

                        <div
                            style={{
                                fontSize: "2rem",
                                fontWeight: 700
                            }}
                        >
                            {dashboard.users.toLocaleString()}
                        </div>

                    </div>

                </div>

            )}

            <h2>
                Administration
            </h2>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "repeat(auto-fit, minmax(250px, 1fr))",
                    gap: "1.5rem",
                    marginTop: "1rem"
                }}
            >

                <Link
                    to="/admin/results"
                    style={{
                        textDecoration: "none",
                        color: "inherit"
                    }}
                >
                    <div
                        style={{
                            border: "1px solid #ddd",
                            borderRadius: "12px",
                            padding: "1.5rem",
                            background: "#fff"
                        }}
                    >
                        <h3>
                            Results
                        </h3>

                        <p>
                            Search, edit and delete
                            performances.
                        </p>
                    </div>
                </Link>

                <Link
                    to="/admin/results/new"
                    style={{
                        textDecoration: "none",
                        color: "inherit"
                    }}
                >
                    <div
                        style={{
                            border: "1px solid #ddd",
                            borderRadius: "12px",
                            padding: "1.5rem",
                            background: "#fff"
                        }}
                    >
                        <h3>
                            New Result
                        </h3>

                        <p>
                            Manually create a result.
                        </p>
                    </div>
                </Link>

                <Link
                    to="/admin/athletes"
                    style={{
                        textDecoration: "none",
                        color: "inherit"
                    }}
                >
                    <div
                        style={{
                            border: "1px solid #ddd",
                            borderRadius: "12px",
                            padding: "1.5rem",
                            background: "#fff"
                        }}
                    >
                        <h3>
                            Athletes
                        </h3>

                        <p>
                            Search and review athlete
                            profiles.
                        </p>
                    </div>
                </Link>

                <Link
                    to="/admin/athletes/merge"
                    style={{
                        textDecoration: "none",
                        color: "inherit"
                    }}
                >
                    <div
                        style={{
                            border: "1px solid #ddd",
                            borderRadius: "12px",
                            padding: "1.5rem",
                            background: "#fff"
                        }}
                    >
                        <h3>
                            Merge Athletes
                        </h3>

                        <p>
                            Combine duplicate athlete
                            profiles.
                        </p>
                    </div>
                </Link>

                <Link
                    to="/admin/users"
                    style={{
                        textDecoration: "none",
                        color: "inherit"
                    }}
                >
                    <div
                        style={{
                            border: "1px solid #ddd",
                            borderRadius: "12px",
                            padding: "1.5rem",
                            background: "#fff"
                        }}
                    >
                        <h3>
                            Users
                        </h3>

                        <p>
                            Create, edit and manage
                            administrator accounts.
                        </p>
                    </div>
                </Link>

                <Link
                    to="/upload"
                    style={{
                        textDecoration: "none",
                        color: "inherit"
                    }}
                >
                    <div
                        style={{
                            border: "1px solid #ddd",
                            borderRadius: "12px",
                            padding: "1.5rem",
                            background: "#fff"
                        }}
                    >
                        <h3>
                            Imports
                        </h3>

                        <p>
                            Import results from
                            supported file formats.
                        </p>
                    </div>
                </Link>

            </div>

        </div>

    );
}