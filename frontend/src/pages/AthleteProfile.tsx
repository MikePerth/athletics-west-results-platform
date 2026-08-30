import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";


export default function AthleteProfile() {

    const { athleteName } = useParams();

    const [athlete, setAthlete] = useState<any>(null);

    function displayWind(
        eventName?: string,
        wind?: number | null
    ) {
        const event = eventName ?? "";

        const requiresWind =
            event.includes("60m") ||
            event.includes("80m Hurdles") ||
            event.includes("90m Hurdles") ||
            event.includes("100m Hurdles") ||
            event.includes("100m") ||
            event.includes("110m Hurdles") ||
            event.includes("200m") ||
            event.includes("200m Hurdles") ||
            event.includes("Long Jump") ||
            event.includes("Triple Jump");

        if (!requiresWind) {
            return "-";
        }

        return wind ?? "NWI";
    }
    function CleanEventName(eventName: string) {
        return eventName

            // Existing cleanup
            .replace(/^U\d+\s*-\s*U\d+\s+/i, "")
            .replace(/^U\d+\s+to\s+U\d+\s+/i, "")
            .replace(/^Multiple\s+group\s+/i, "")
            .replace(/^U\d+\s*-\s*\d+\s+/i, "")

            // Remove leading dash
            .replace(/^\s*-\s*/, "")

            // Site - 1 (FA)/ 3 (FB) Triple Jump
            .replace(/^Site\s*-\s*\d+\s*\(FA\)\s*\/\s*\d+\s*\(FB\)\s*/i, "")

            // Site 1 - LA 400g Javelin Throw
            .replace(/^Site\s*\d+\s*-\s*LA\s*.*?\s(?=[A-Z])/i, "")

            // Site 1 High Jump
            .replace(/^Site\s*\d+\.?\s*/i, "")

            // LA Hurdles 68cm
            .replace(/^LA\s+Hurdles\s+\d+(?:\.\d+)?cm\s+/i, "")

            .replace(/^\d+(?:\.\d+)?(?:cm|m)\s+(\d+m Hurdles)$/i, "$1")

            .trim();
    }



    useEffect(() => {

        async function loadAthlete() {

            const response = await fetch(
                `http://localhost:8001/athletes/${athleteName}`
            );

            const data = await response.json();

            console.log(data.performances[0]);

            setAthlete(data);
        }

        loadAthlete();

    }, [athleteName]);

    if (!athlete) {
        return <div>Loading athlete profile...</div>;
    }

    return (

        <div
            style={{
                padding: "2rem",
                maxWidth: "1600px",
                margin: "0 auto"
            }}
        >

            <h1>
                Athlete Profile
            </h1>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "280px 1fr 280px",
                    gap: "2rem",
                    alignItems: "start",
                    marginBottom: "4rem"
                }}
            >

                {/* PERSONAL BESTS */}

                <div>

                    <h2
                        style={{
                            textAlign: "center",
                            marginBottom: "1rem"
                        }}
                    >
                        🏆 Personal Bests
                    </h2>

                    <div
                        style={{
                            display: "flex",
                            flexDirection: "column",
                            gap: "1rem"
                        }}
                    >
                        {athlete.personal_bests?.map((pb: any) => (

                            <div
                                key={pb.event_name}
                                style={{
                                    background: "#fffdf5",
                                    borderLeft: "6px solid #f5c542",
                                    borderRadius: "12px",
                                    padding: "1rem",
                                    boxShadow:
                                        "0 2px 8px rgba(0,0,0,0.10)",
                                    textAlign: "center"
                                }}
                            >
                                <div
                                    style={{
                                        fontWeight: 600,
                                        fontSize: "1rem"
                                    }}
                                >
                                    {CleanEventName(pb.event_name)}
                                </div>

                                <div
                                    style={{
                                        fontSize: "2rem",
                                        fontWeight: 700,
                                        margin: "0.5rem 0"
                                    }}
                                >
                                    {pb.performance}
                                </div>

                                <div
                                    style={{
                                        color: "#666",
                                        fontSize: "0.85rem"
                                    }}
                                >
                                    {pb.date}
                                </div>

                            </div>

                        ))}
                    </div>

                </div>

                {/* ATHLETE CARD */}

                <div
                    style={{
                        background: "#ffffff",
                        borderRadius: "16px",
                        padding: "3rem",
                        boxShadow:
                            "0 4px 16px rgba(0,0,0,0.08)"
                    }}
                >

                    <div
                        style={{
                            textAlign: "center",
                            marginBottom: "3rem"
                        }}
                    >

                        <h1
                            style={{
                                fontSize: "2.0rem",
                                fontWeight: 700,
                                margin: 0,
                                color: "#222",
                                whiteSpace: "nowrap"
                            }}
                        >
                            {athlete.athlete_name}
                        </h1>

                        <div
                            style={{
                                marginTop: "1rem",
                                color: "#666",
                                fontSize: "1.1rem"
                            }}
                        >
                            {athlete.club}

                            {athlete.country && (
                                <> • {athlete.country}</>
                            )}

                            {athlete.birth_year && (
                                <> • {athlete.birth_year}</>
                            )}
                        </div>

                    </div>

                    <div
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            gap: "1.5rem",
                            flexWrap: "wrap"
                        }}
                    >

                        <div
                            style={{
                                background: "#fafafa",
                                borderRadius: "12px",
                                padding: "0.75rem 1.5rem",
                                textAlign: "center",
                                minWidth: "140px"
                            }}
                        >
                            <div
                                style={{
                                    fontSize: "1.25rem",
                                    fontWeight: 700,
                                    color: "#222"
                                }}
                            >
                                {athlete.competition_count}
                            </div>

                            <div
                                style={{
                                    color: "#666",
                                    marginTop: "0.25rem",
                                    fontSize: "0.75rem"
                                }}
                            >
                                Competitions
                            </div>

                        </div>

                        <div
                            style={{
                                background: "#fafafa",
                                borderRadius: "12px",
                                padding: "0.75rem 1.5rem",
                                textAlign: "center",
                                minWidth: "140px"
                            }}
                        >
                            <div
                                style={{
                                    fontSize: "1.25rem",
                                    fontWeight: 700,
                                    color: "#222"
                                }}
                            >
                                {athlete.performance_count}
                            </div>

                            <div
                                style={{
                                    color: "#666",
                                    marginTop: "0.25rem",
                                    fontSize: "0.75rem"
                                }}
                            >
                                Performances
                            </div>

                        </div>

                    </div>

                </div>

                {/* SEASON BESTS */}

                <div>

                    <h2
                        style={{
                            textAlign: "center",
                            marginBottom: "1rem"
                        }}
                    >
                        ⭐ Season Bests
                    </h2>

                    <div
                        style={{
                            display: "flex",
                            flexDirection: "column",
                            gap: "1rem"
                        }}
                    >
                        {athlete.season_bests?.map((sb: any) => (

                            <div
                                key={sb.event_name}
                                style={{
                                    background: "#f6fffb",
                                    borderLeft: "6px solid #52b788",
                                    borderRadius: "12px",
                                    padding: "1rem",
                                    boxShadow:
                                        "0 2px 8px rgba(0,0,0,0.10)",
                                    textAlign: "center"
                                }}
                            >
                                <div
                                    style={{
                                        fontWeight: 600,
                                        fontSize: "1rem"
                                    }}
                                >
                                    {CleanEventName(sb.event_name)}
                                </div>

                                <div
                                    style={{
                                        fontSize: "2rem",
                                        fontWeight: 700,
                                        margin: "0.5rem 0"
                                    }}
                                >
                                    {sb.performance}
                                </div>

                                <div
                                    style={{
                                        color: "#666",
                                        fontSize: "0.85rem"
                                    }}
                                >
                                    {sb.date}
                                </div>

                            </div>

                        ))}
                    </div>

                </div>

            </div>

            <h2
                style={{
                    marginTop: "4rem",
                    marginBottom: "2rem",
                    textAlign: "center"
                }}
            >
                Performance History
            </h2>

            <div
                style={{
                    background: "#fff",
                    borderRadius: "16px",
                    padding: "1.5rem",
                    boxShadow:
                        "0 2px 8px rgba(0,0,0,0.08)",

                    marginLeft: "-150px",
                    marginRight: "-150px"
                }}
            >

                <table
                    style={{
                        width: "100%",
                        borderCollapse: "collapse"
                    }}
                >
                    <thead>
                        <tr
                            style={{
                                background: "#f8f9fa"
                            }}
                        >
                            <th style={{ padding: "12px" }}>
                                Date
                            </th>

                            <th style={{ padding: "12px" }}>
                                Competition
                            </th>

                            <th style={{ padding: "12px" }}>
                                Event
                            </th>

                            <th style={{ padding: "12px" }}>
                                Age Group
                            </th>

                            <th style={{ padding: "12px" }}>
                                Performance
                            </th>
                            <th style={{ padding: "12px" }}>
                                Wind
                            </th>
                            <th style={{ padding: "12px" }}>
                                Place
                            </th>
                        </tr>
                    </thead>

                    <tbody>

                        {athlete.performances.map(
                            (
                                result: any,
                                index: number
                            ) => (

                                <tr
                                    key={index}
                                    style={{
                                        borderTop:
                                            "1px solid #eee"
                                    }}
                                >

                                    <td
                                        style={{
                                            padding: "12px"
                                        }}
                                    >
                                        {result.competition_date}
                                    </td>

                                    <td
                                        style={{
                                            padding: "12px"
                                        }}
                                    >
                                        {result.competition_name}
                                    </td>

                                    <td
                                        style={{
                                            padding: "12px"
                                        }}
                                    >
                                        {CleanEventName(result.event_name)}
                                        {result.round
                                            ? ` (${result.round})`
                                            : ""
                                        }
                                    </td>

                                    <td
                                        style={{
                                            padding: "12px"
                                        }}
                                    >
                                        {result.age_group}
                                    </td>

                                    <td style={{ padding: "12px" }}>

                                        {result.performance}

                                        {!result.is_legal && (
                                            <div
                                                style={{
                                                    fontStyle: "italic",
                                                    color: "#c0392b",
                                                    fontSize: "0.8rem",
                                                    marginTop: "0.25rem"
                                                }}
                                            >
                                                *not legal wind
                                            </div>
                                        )}

                                    </td>
                                    <td style={{ padding: "12px" }}>
                                        {displayWind(
                                            result.event_name,
                                            result.wind
                                        )}
                                    </td>
                                    <td
                                        style={{
                                            padding: "12px"
                                        }}
                                    >
                                        {result.place}
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