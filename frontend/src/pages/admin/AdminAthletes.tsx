import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import AdminNav from "./AdminNav";

interface Athlete {
    athlete_name: string;
    club: string;
    results: number;
}

export default function AdminAthletes() {

    const [query, setQuery] =
        useState("");

    const [loading, setLoading] =
        useState(false);

    const [athletes, setAthletes] =
        useState<Athlete[]>([]);

    async function loadAthletes() {

        setLoading(true);

        try {

            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/athletes/search?q=${encodeURIComponent(query)}`
            );

            const data =
                await response.json();

            if (Array.isArray(data)) {

                setAthletes(data);

            } else {

                console.error(
                    "Unexpected response:",
                    data
                );

                setAthletes([]);
            }

        } catch (error) {

            console.error(error);

            setAthletes([]);

        } finally {

            setLoading(false);
        }
    }

    useEffect(() => {

        loadAthletes();

    }, []);

    return (

        <div
            style={{
                maxWidth: "1600px",
                margin: "0 auto",
                padding: "2rem"
            }}
        >

            <AdminNav />

            <h1>
                Athlete Administration
            </h1>

            <p
                style={{
                    color: "#666",
                    marginBottom: "2rem"
                }}
            >
                Search athletes, identify duplicate
                records and access athlete profiles.
            </p>

            <div
                style={{
                    background: "#fff",
                    padding: "1.5rem",
                    borderRadius: "12px",
                    boxShadow:
                        "0 2px 8px rgba(0,0,0,0.08)",
                    marginBottom: "2rem"
                }}
            >

                <div
                    style={{
                        display: "flex",
                        gap: "1rem"
                    }}
                >

                    <input
                        value={query}
                        onChange={(e) =>
                            setQuery(
                                e.target.value
                            )
                        }
                        placeholder="Search athlete..."
                        style={{
                            flex: 1,
                            padding: "0.75rem"
                        }}
                    />

                    <button
                        onClick={
                            loadAthletes
                        }
                    >
                        Search
                    </button>

                </div>

            </div>

            <div
                style={{
                    marginBottom: "1rem",
                    color: "#666"
                }}
            >
                {athletes.length.toLocaleString()}
                {" "}
                athletes found
            </div>

            {loading && (

                <p>
                    Loading athletes...
                </p>

            )}

            {!loading &&
                athletes.length === 0 && (

                    <p>
                        No athletes found.
                    </p>

                )}

            <div
                style={{
                    background: "#fff",
                    borderRadius: "12px",
                    overflow: "hidden",
                    boxShadow:
                        "0 2px 8px rgba(0,0,0,0.08)"
                }}
            >

                <table
                    style={{
                        width: "100%",
                        borderCollapse:
                            "collapse"
                    }}
                >

                    <thead>

                        <tr
                            style={{
                                background:
                                    "#f8f9fa"
                            }}
                        >

                            <th
                                style={{
                                    padding:
                                        "12px",
                                    textAlign:
                                        "left"
                                }}
                            >
                                Athlete
                            </th>

                            <th
                                style={{
                                    padding:
                                        "12px",
                                    textAlign:
                                        "left"
                                }}
                            >
                                Club
                            </th>

                            <th
                                style={{
                                    padding:
                                        "12px",
                                    textAlign:
                                        "left"
                                }}
                            >
                                Results
                            </th>

                            <th
                                style={{
                                    padding:
                                        "12px",
                                    textAlign:
                                        "left"
                                }}
                            >
                                Actions
                            </th>

                        </tr>

                    </thead>

                    <tbody>

                        {athletes.map(
                            (
                                athlete,
                                index
                            ) => (

                                <tr
                                    key={`${athlete.athlete_name}-${index}`}
                                    style={{
                                        borderTop:
                                            "1px solid #eee"
                                    }}
                                >

                                    <td
                                        style={{
                                            padding:
                                                "12px",
                                            fontWeight:
                                                600
                                        }}
                                    >
                                        {
                                            athlete.athlete_name
                                        }
                                    </td>

                                    <td
                                        style={{
                                            padding:
                                                "12px"
                                        }}
                                    >
                                        {
                                            athlete.club
                                        }
                                    </td>

                                    <td
                                        style={{
                                            padding:
                                                "12px"
                                        }}
                                    >
                                        {
                                            athlete.results
                                        }
                                    </td>

                                    <td
                                        style={{
                                            padding:
                                                "12px",
                                            display:
                                                "flex",
                                            gap:
                                                "1rem"
                                        }}
                                    >

                                        <Link
                                            to={`/athletes/${encodeURIComponent(
                                                athlete.athlete_name
                                            )}`}
                                            target="_blank"
                                        >
                                            View Profile
                                        </Link>

                                        <Link
                                            to={`/admin/athletes/${encodeURIComponent(
                                                athlete.athlete_name
                                            )}/edit`}
                                        >
                                            Edit
                                        </Link>

                                        <Link
                                            to={`/admin/athletes/merge?source=${encodeURIComponent(
                                                athlete.athlete_name
                                            )}`}
                                        >
                                            Merge
                                        </Link>

                                    </td>

                                </tr>

                            )
                        )}

                    </tbody>

                </table>

            </div>

        </div>

    );
}