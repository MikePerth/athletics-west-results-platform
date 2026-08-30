import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

interface EventResult {

    athlete_name: string;

    club: string;

    performance: string;

    place: number;

    wind: number | null;
}

interface CompetitionData {

    competition_name: string;

    competition_date: string;

    events: Record<
        string,
        EventResult[]
    >;
}

export default function CompetitionResults() {

    const { competitionId } =
        useParams();

    const [loading, setLoading] =
        useState(true);

    const [competition, setCompetition] =
        useState<CompetitionData | null>(
            null
        );

    useEffect(() => {

        async function loadCompetition() {

            try {

                const response =
                    await fetch(
                        `http://localhost:8001/competitions/${competitionId}/results`
                    );

                const data =
                    await response.json();

                setCompetition(data);

            } catch (error) {

                console.error(error);

            } finally {

                setLoading(false);
            }
        }

        loadCompetition();

    }, [competitionId]);

    if (loading) {

        return (
            <div>
                Loading...
            </div>
        );
    }

    if (!competition) {

        return (
            <div>
                Competition not found.
            </div>
        );
    }

    const eventNames =
        Object.keys(
            competition.events
        ).sort();

    return (

        <div
            style={{
                maxWidth: "1400px",
                margin: "0 auto",
                padding: "2rem"
            }}
        >

            <div
                style={{
                    background: "#fff",
                    borderRadius: "16px",
                    padding: "2rem",
                    boxShadow:
                        "0 4px 16px rgba(0,0,0,0.08)",
                    marginBottom: "2rem"
                }}
            >

                <h1>
                    {
                        competition.competition_name
                    }
                </h1>

                <p>
                    {
                        competition.competition_date
                    }
                </p>

            </div>

            {eventNames.map(
                (eventName) => (

                    <div
                        key={eventName}
                        style={{
                            background:
                                "#fff",
                            borderRadius:
                                "16px",
                            padding:
                                "1.5rem",
                            marginBottom:
                                "2rem",
                            boxShadow:
                                "0 2px 8px rgba(0,0,0,0.08)"
                        }}
                    >

                        <h2>
                            {eventName}
                        </h2>

                        <table
                            style={{
                                width:
                                    "100%",
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
                                                "10px"
                                        }}
                                    >
                                        Place
                                    </th>

                                    <th
                                        style={{
                                            padding:
                                                "10px"
                                        }}
                                    >
                                        Athlete
                                    </th>

                                    <th
                                        style={{
                                            padding:
                                                "10px"
                                        }}
                                    >
                                        Club
                                    </th>

                                    <th
                                        style={{
                                            padding:
                                                "10px"
                                        }}
                                    >
                                        Performance
                                    </th>

                                    <th
                                        style={{
                                            padding:
                                                "10px"
                                        }}
                                    >
                                        Wind
                                    </th>

                                </tr>

                            </thead>

                            <tbody>

                                {competition.events[
                                    eventName
                                ].map(
                                    (
                                        result,
                                        index
                                    ) => (

                                        <tr
                                            key={
                                                index
                                            }
                                            style={{
                                                borderTop:
                                                    "1px solid #eee"
                                            }}
                                        >

                                            <td
                                                style={{
                                                    padding:
                                                        "10px"
                                                }}
                                            >
                                                {
                                                    result.place
                                                }
                                            </td>

                                            <td
                                                style={{
                                                    padding:
                                                        "10px"
                                                }}
                                            >

                                                <Link
                                                    to={`/athletes/${encodeURIComponent(
                                                        result.athlete_name
                                                    )}`}
                                                >
                                                    {
                                                        result.athlete_name
                                                    }
                                                </Link>

                                            </td>

                                            <td
                                                style={{
                                                    padding:
                                                        "10px"
                                                }}
                                            >
                                                {
                                                    result.club
                                                }
                                            </td>

                                            <td
                                                style={{
                                                    padding:
                                                        "10px"
                                                }}
                                            >
                                                {
                                                    result.performance
                                                }
                                            </td>

                                            <td
                                                style={{
                                                    padding:
                                                        "10px"
                                                }}
                                            >
                                                {
                                                    result.wind ??
                                                    "-"
                                                }
                                            </td>

                                        </tr>

                                    )
                                )}

                            </tbody>

                        </table>

                    </div>

                )
            )}

        </div>

    );
}