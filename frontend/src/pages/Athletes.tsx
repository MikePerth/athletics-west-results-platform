import { useEffect, useState } from "react";
import { Link } from "react-router-dom";


interface SeasonBest {

    event_name: string;

    athlete_name: string;

    performance: string;
}

interface SeasonBestResponse {

    male: SeasonBest[];

    female: SeasonBest[];
}



    

export default function Athletes() {

    const [query, setQuery] =
        useState("");

    const [loading, setLoading] =
        useState(false);

    const [letters, setLetters] =
        useState<string[]>([]);

    const [browseResults, setBrowseResults] =
    useState<any[]>([]);

    const [ageGroup, setAgeGroup] =
        useState("Open");

    const [seasonBests, setSeasonBests] =
        useState<SeasonBestResponse>({
            male: [],
            female: []
        });

    const [searchResults, setSearchResults] =
        useState<any[]>([]);

    const [athleteCount, setAthleteCount] =
        useState(0);

    const [resultCount, setResultCount] =
        useState(0);

    useEffect(() => {

        async function loadLetters() {

            try {

                const response =
                    await fetch(
                        "http://localhost:8001/athletes/letters"
                    );

                const data =
                    await response.json();

                setLetters(data);

            } catch (error) {

                console.error(error);
            }
        }

        loadLetters();

    }, []);

    useEffect(() => {

        async function loadAthleteCount() {

            try {

                const response =
                    await fetch(
                        "http://localhost:8001/athletes/count"
                    );

                const data =
                    await response.json();

                setAthleteCount(
                    data.athletes ?? 0
                );

                setResultCount(
                    data.results ?? 0
                );

            } catch (error) {

                console.error(error);
            }
        }

        loadAthleteCount();

    }, []);   

    useEffect(() => {

        async function loadSeasonBests() {

            setLoading(true);

            try {

                const response =
                    await fetch(
                        `http://localhost:8001/athletes/season-bests?age_group=${encodeURIComponent(
                            ageGroup
                        )}`
                    );

                const data =
                    await response.json();

                setSeasonBests(
                    data ?? {
                        male: [],
                        female: []
                    }
                );

            } catch (error) {

                console.error(error);

            } finally {

                setLoading(false);
            }
        }

        loadSeasonBests();

    }, [ageGroup]);

    async function searchAthlete() {

        if (!query.trim()) {
            return;
        }

        try {

            const response =
                await fetch(
                    `http://localhost:8001/athletes/search?q=${encodeURIComponent(
                        query.trim()
                    )}`
                );

            const data =
                await response.json();

            setSearchResults(data);

        } catch (error) {

            console.error(error);
        }
    }

    
    async function browseLetter(
        letter: string
    ) {
        try {

            const response =
                await fetch(
                    `http://localhost:8001/athletes/browse/${letter}`
                );

            const data =
                await response.json();

            setBrowseResults(data);

            console.log(browseResults);

        } catch (error) {

            console.error(error);
        }
    }


    return (

        <div
            style={{
                maxWidth: "1600px",
                margin: "0 auto",
                padding: "2rem"
            }}
        >

            {/* Hero */}

            <div
                style={{
                    background:
                        "linear-gradient(135deg, #f8fafc 0%, #e8eef6 100%)",
                    borderRadius: "24px",
                    padding: "3rem",
                    color: "#0f172a",
                    marginBottom: "1.5rem",
                    boxShadow:
                        "0 15px 40px rgba(15,23,42,0.25)"
                }}
            >
                <h1
                    style={{
                        fontSize: "3.5rem",
                        margin: 0,
                        fontWeight: 600,
                        textAlign: "center",
                        color: "#0f172a"
                    }}
                >
                    Athlete Directory
                </h1>

                <p
                    style={{
                        textAlign: "center",
                        fontSize: "1.15rem",
                        marginTop: "1rem",
                        color: "#475569",
                        maxWidth: "900px",
                        marginLeft: "auto",
                        marginRight: "auto"
                    }}
                >
                    Search athlete profiles, rankings, personal
                    bests, season bests and competition performances.
                </p>

                <div
                    style={{
                        maxWidth: "900px",
                        margin: "2rem auto 0 auto",
                        display: "flex",
                        gap: "1rem"
                    }}
                >
                    <input
                        value={query}
                        onChange={(e) => {
                            setQuery(e.target.value);
                        }}
                        onKeyDown={(e) => {
                            if (e.key === "Enter") {
                                searchAthlete();
                            }
                        }}
                        placeholder="Search athlete surname..."
                        style={{
                            flex: 1,
                            padding: "1rem 1.5rem",
                            borderRadius: "14px",
                            border: "none",
                            fontSize: "1.1rem",
                            outline: "none"
                        }}
                    />

                    <button
                        onClick={searchAthlete}
                        style={{
                            background: "#1e293b",
                            color: "#ffffff",
                            border: "none",
                            boxShadow: "0 4px 10px rgba(15,23,42,0.15)",
                            borderRadius: "14px",
                            padding: "0 2rem",
                            fontWeight: 600,
                            cursor: "pointer"
                        }}
                    >
                        Search
                    </button>
                </div>

                <div
                    style={{
                        textAlign: "center",
                        marginTop: "1.5rem",
                        color: "#cbd5e1",
                        fontSize: "1rem"
                    }}
                >
                    {(athleteCount ?? 0).toLocaleString()} Athletes
                    {" • "}
                    {(resultCount ?? 0).toLocaleString()} Results
                </div>
            </div>

            {/* Search Results */}

            {searchResults.length > 0 && (
                <div
                    style={{
                        background: "#ffffff",
                        borderRadius: "18px",
                        padding: "1.5rem",
                        marginBottom: "1.5rem",
                        boxShadow:
                            "0 4px 12px rgba(0,0,0,0.06)"
                    }}
                >
                    <h3
                        style={{
                            marginTop: 0
                        }}
                    >
                        Search Results
                    </h3>

                    <div
                        style={{
                            display: "grid",
                            gridTemplateColumns:
                                "repeat(auto-fill, minmax(250px, 1fr))",
                            gap: "0.75rem"
                        }}
                    >
                        {searchResults.map(
                            (athlete: any) => (
                                <Link
                                    key={athlete.athlete_name}
                                    to={`/athletes/${encodeURIComponent(
                                        athlete.athlete_name
                                    )}`}
                                    style={{
                                        textDecoration: "none",
                                        background: "#f8fafc",
                                        padding: "0.75rem",
                                        borderRadius: "10px",
                                        color: "#2563eb",
                                        border:
                                            "1px solid #dbe3ee"
                                    }}
                                >
                                    {athlete.athlete_name}
                                </Link>
                            )
                        )}
                    </div>
                </div>
            )}

            {/* Quick Navigation */}

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "repeat(auto-fit, minmax(250px, 1fr))",
                    gap: "1rem",
                    marginBottom: "1.5rem"
                }}
            >
                <div
                    style={{
                        background: "#ffffff",
                        borderRadius: "18px",
                        padding: "1.5rem",
                        borderTop: "4px solid #2563eb",
                        boxShadow:
                            "0 4px 12px rgba(0,0,0,0.06)"
                    }}
                >
                    <h3
                        style={{
                            margin: 0
                        }}
                    >
                        Athletes
                    </h3>

                    <p
                        style={{
                            marginBottom: 0,
                            color: "#64748b"
                        }}
                    >
                        Search profiles, results and
                        performance history.
                    </p>
                </div>

                <div
                    style={{
                        background: "#ffffff",
                        borderRadius: "18px",
                        padding: "1.5rem",
                        borderTop: "4px solid #2563eb",
                        boxShadow:
                            "0 4px 12px rgba(0,0,0,0.06)"
                    }}
                >
                    <h3
                        style={{
                            margin: 0
                        }}
                    >
                        Rankings
                    </h3>

                    <p
                        style={{
                            marginBottom: 0,
                            color: "#64748b"
                        }}
                    >
                        Current season leaders and
                        top performances.
                    </p>
                </div>

                <div
                    style={{
                        background: "#ffffff",
                        borderRadius: "18px",
                        padding: "1.5rem",
                        borderTop: "4px solid #2563eb",
                        boxShadow:
                            "0 4px 12px rgba(0,0,0,0.06)",
                        cursor: "pointer"
                    }}
                >
                    <h3
                        style={{
                            margin: 0
                        }}
                    >
                        Competitions
                    </h3>

                    <p
                        style={{
                            marginBottom: 0,
                            color: "#64748b"
                        }}
                    >
                        Explore meetings, championships
                        and competition results.
                    </p>
                </div>
            </div>

            {/* Athlete Index */}

            <div
                style={{
                    background: "#ffffff",
                    borderRadius: "18px",
                    padding: "2rem",
                    boxShadow:
                        "0 4px 12px rgba(0,0,0,0.06)",
                    marginBottom: "2rem"
                }}
            >
                <h2
                    style={{
                        marginTop: 0,
                        marginBottom: "1.5rem"
                    }}
                >
                    Athlete Index
                </h2>

                <div
                    style={{
                        display: "flex",
                        flexWrap: "wrap",
                        gap: "0.75rem"
                    }}
                >
                    {letters.map((letter) => (
                        <button
                            key={letter}
                            onClick={() =>
                                browseLetter(letter)
                            }
                            style={{
                                width: "48px",
                                height: "48px",
                                borderRadius: "12px",
                                border:
                                    "1px solid #dbe3ee",
                                background: "#f8fafc",
                                color: "#2563eb",
                                fontWeight: 700,
                                cursor: "pointer"
                            }}
                        >
                            {letter}
                        </button>
                    ))}
                </div>

                {browseResults.length > 0 && (
                    <div
                        style={{
                            marginTop: "2rem",
                            display: "grid",
                            gridTemplateColumns:
                                "repeat(auto-fill, minmax(250px, 1fr))",
                            gap: "0.75rem"
                        }}
                    >
                        {browseResults.map(
                            (
                                athlete: string,
                                index: number
                            ) => (
                                <Link
                                    key={index}
                                    to={`/athletes/${encodeURIComponent(
                                        athlete
                                    )}`}
                                    style={{
                                        textDecoration: "none",
                                        background: "#f8fafc",
                                        padding: "0.75rem",
                                        borderRadius: "10px",
                                        color: "#2563eb",
                                        border:
                                            "1px solid #dbe3ee"
                                    }}
                                >
                                    {athlete}
                                </Link>
                            )
                        )}
                    </div>
                )}
            </div>

            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: "2rem"
                }}
            >

                <h2>
                    Current Season Bests
                </h2>

                <select
                    value={ageGroup}
                    onChange={(e) =>
                        setAgeGroup(
                            e.target.value
                        )
                    }
                >

                    <option value="Open">
                        Open
                    </option>

                    <option value="U20">
                        U20
                    </option>

                    <option value="U18">
                        U18
                    </option>

                    <option value="U17">
                        U17
                    </option>

                    <option value="U16">
                        U16
                    </option>

                    <option value="U15">
                        U15
                    </option>

                    <option value="U14">
                        U14
                    </option>

                    <option value="U13">
                        U13
                    </option>

                    <option value="U12">
                        U12
                    </option>

                    <option value="Masters">
                        Masters
                    </option>

                </select>

            </div>

            {loading ? (

                <p>
                    Loading season bests...
                </p>

            ) : (

                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns:
                            "1fr 1fr",
                        gap: "2rem"
                    }}
                >

                    <div
                        style={{
                            background: "#ffffff",
                            borderRadius: "16px",
                            padding: "2rem",
                            boxShadow:
                                "0 2px 8px rgba(0,0,0,0.08)"
                        }}
                    >

                        <h2>
                            Men
                        </h2>

                        {(seasonBests?.male ?? []).map(
                            (result: any) => (

                                <div
                                    key={
                                        result.event_name
                                    }
                                    style={{
                                        padding: "0.75rem 0",
                                        borderBottom:
                                            "1px solid #eee"
                                    }}
                                >

                                    <strong>
                                        {
                                            result.event_name
                                        }
                                    </strong>

                                    <br />

                                    <Link
                                        to={`/athletes/${encodeURIComponent(
                                            result.athlete_name
                                        )}`}
                                    >
                                        {
                                            result.athlete_name
                                        }
                                    </Link>

                                    <br />

                                    {
                                        result.performance
                                    }

                                </div>

                            )
                        )}

                    </div>

                    <div
                        style={{
                            background: "#ffffff",
                            borderRadius: "16px",
                            padding: "2rem",
                            boxShadow:
                                "0 2px 8px rgba(0,0,0,0.08)"
                        }}
                    >

                        <h2>
                            Women
                        </h2>

                        {(seasonBests?.female ?? []).map(
                            (result: any) => (

                                <div
                                    key={
                                        result.event_name
                                    }
                                    style={{
                                        padding: "0.75rem 0",
                                        borderBottom:
                                            "1px solid #eee"
                                    }}
                                >

                                    <strong>
                                        {
                                            result.event_name
                                        }
                                    </strong>

                                    <br />

                                    <Link
                                        to={`/athletes/${encodeURIComponent(
                                            result.athlete_name
                                        )}`}
                                    >
                                        {
                                            result.athlete_name
                                        }
                                    </Link>

                                    <br />

                                    {
                                        result.performance
                                    }

                                </div>

                            )
                        )}

                    </div>

                </div>
        
            )}
        </div>

    );
}
