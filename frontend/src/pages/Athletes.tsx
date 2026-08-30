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

    const [athleteCount, setAthleteCount] =
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
                        "http://localhost:8001/athletes/search"
                    );

                const data =
                    await response.json();

                setAthleteCount(
                    data.length
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

    function searchAthlete() {

        if (!query.trim()) {

            return;
        }

        window.location.href =
            `/athletes/${encodeURIComponent(
                query.trim()
            )}`;
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

            <div
                style={{
                    textAlign: "center",
                    marginBottom: "3rem"
                }}
            >

                <div
                    style={{
                        background: "#ffffff",
                        padding: "3rem",
                        borderRadius: "16px",
                        boxShadow:
                            "0 4px 16px rgba(0,0,0,0.08)",
                        textAlign: "center",
                        marginBottom: "2rem"
                    }}
                >

                    <h1
                        style={{
                            fontSize: "3rem",
                            fontWeight: 700,
                            margin: 0,
                            color: "#222"
                        }}
                    >
                        Athlete Directory
                    </h1>

                    <p
                        style={{
                            marginTop: "1rem",
                            color: "#666",
                            fontSize: "1.1rem"
                        }}
                    >
                        Search athlete profiles, personal bests,
                        season bests and performance history.
                    </p>

                    <p
                        style={{
                            marginTop: "1rem",
                            color: "#888",
                            fontSize: "1rem",
                            fontWeight: 400
                        }}
                    >
                        {athleteCount.toLocaleString()} athletes
                    </p>

                </div>

                

            </div>

            <div
                style={{
                    background: "#ffffff",
                    borderRadius: "16px",
                    padding: "2rem",
                    boxShadow:
                        "0 4px 16px rgba(0,0,0,0.08)",
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
                        onChange={(e) => {

                            setQuery(
                                e.target.value
                            );

                        }}
                        onKeyDown={(e) => {

                            if (
                                e.key === "Enter"
                            ) {

                                searchAthlete();
                            }
                        }}
                        placeholder="Search athlete name..."
                        style={{
                            width: "100%",
                            maxWidth: "800px",
                            padding: "1rem 1.25rem",
                            fontSize: "1.1rem",
                            borderRadius: "12px",
                            border:
                                "1px solid #ddd",
                            outline: "none",
                            boxSizing:
                                "border-box"
                        }}
                    />
                    <button
                        onClick={searchAthlete}
                        style={{
                            padding: "1rem 2rem",
                            borderRadius: "12px",
                            border: "none",
                            background: "#0057b8",
                            color: "#fff",
                            cursor: "pointer"
                        }}
                    >
                        Search
                    </button>
                </div>

            </div>
            <div
                style={{
                    background: "#ffffff",
                    borderRadius: "16px",
                    padding: "2rem",
                    boxShadow:
                        "0 4px 16px rgba(0,0,0,0.08)",
                    marginBottom: "2rem"
                }}
            >

                <h2>
                    Browse Athletes
                </h2>

                <div
                    style={{
                        display: "flex",
                        flexWrap: "wrap",
                        gap: "1rem"
                    }}
                >

                    {letters.map(
                        (letter) => (

                            <button
                                key={letter}
                                onClick={() =>
                                    browseLetter(letter)
                                }
                                style={{
                                    border: "none",
                                    background: "none",
                                    color: "#0047ff",
                                    fontWeight: 700,
                                    fontSize: "1.2rem",
                                    cursor: "pointer"
                                }}
                            >
                                {letter}
                            </button>

                        )
                    )}

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
                            (athlete: string, index: number) => (

                                <div key={index}>
                                    <Link
                                        to={`/athletes/${encodeURIComponent(
                                            athlete
                                        )}`}
                                        style={{
                                            textDecoration: "none",
                                            color: "#0057b8",
                                            padding: "0.5rem"
                                        }}
                                    >
                                        {athlete}
                                    </Link>
                                </div>

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
