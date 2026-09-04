import { useState } from "react";
import { useNavigate } from "react-router-dom";
import AdminNav from "./AdminNav";

export default function CreateResult() {

    const navigate = useNavigate();

    const [result, setResult] = useState({

        competition_id: "",

        competition_date: "",

        athlete_name: "",

        birth_year: "",

        country: "AUS",

        club: "",

        age_group: "",

        event_name: "",

        round: "",

        performance: "",

        wind: "",

        place: "",

        lane: "",

        status: ""
    });

    async function createResult() {

        try {

            const payload = {

                competition_id: Number(
                    result.competition_id
                ),

                competition_date:
                    result.competition_date || null,

                athlete_name:
                    result.athlete_name,

                birth_year:
                    result.birth_year
                        ? Number(
                              result.birth_year
                          )
                        : null,

                country:
                    result.country || null,

                club:
                    result.club || null,

                age_group:
                    result.age_group || null,

                event_name:
                    result.event_name,

                round:
                    result.round || null,

                performance:
                    result.performance || null,

                wind:
                    result.wind
                        ? Number(
                              result.wind
                          )
                        : null,

                place:
                    result.place
                        ? Number(
                              result.place
                          )
                        : null,

                lane:
                    result.lane || null,

                status:
                    result.status || null
            };

            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/admin/results`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        payload
                    )
                }
            );

            if (!response.ok) {

                alert(
                    "Unable to create result."
                );

                return;
            }

            const data =
                await response.json();

            alert(
                "Result created successfully."
            );

            navigate(
                `/admin/results/${data.id}`
            );

        } catch (error) {

            console.error(error);

            alert(
                "Unexpected error creating result."
            );
        }
    }

    return (

        <div
            style={{
                maxWidth: "1200px",
                margin: "0 auto",
                padding: "2rem"
            }}
        >

            <AdminNav />

            <h1>
                Create Result
            </h1>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "repeat(2, 1fr)",
                    gap: "2rem"
                }}
            >

                <div>

                    <h2>
                        Competition
                    </h2>

                    <label>
                        Competition ID
                    </label>

                    <input
                        type="number"
                        value={
                            result.competition_id
                        }
                        onChange={(e) =>
                            setResult({
                                ...result,
                                competition_id:
                                    e.target.value
                            })
                        }
                        style={{
                            width: "100%"
                        }}
                    />

                    <br /><br />

                    <label>
                        Competition Date
                    </label>

                    <input
                        type="date"
                        value={
                            result.competition_date
                        }
                        onChange={(e) =>
                            setResult({
                                ...result,
                                competition_date:
                                    e.target.value
                            })
                        }
                        style={{
                            width: "100%"
                        }}
                    />

                    <br /><br />

                    <label>
                        Event Name
                    </label>

                    <input
                        value={
                            result.event_name
                        }
                        onChange={(e) =>
                            setResult({
                                ...result,
                                event_name:
                                    e.target.value
                            })
                        }
                        style={{
                            width: "100%"
                        }}
                    />

                    <br /><br />

                    <label>
                        Round
                    </label>

                    <input
                        value={
                            result.round
                        }
                        onChange={(e) =>
                            setResult({
                                ...result,
                                round:
                                    e.target.value
                            })
                        }
                        style={{
                            width: "100%"
                        }}
                    />

                </div>

                <div>

                    <h2>
                        Athlete
                    </h2>

                    <label>
                        Athlete Name
                    </label>

                    <input
                        value={
                            result.athlete_name
                        }
                        onChange={(e) =>
                            setResult({
                                ...result,
                                athlete_name:
                                    e.target.value
                            })
                        }
                        style={{
                            width: "100%"
                        }}
                    />

                    <br /><br />

                    <label>
                        Birth Year
                    </label>

                    <input
                        type="number"
                        value={
                            result.birth_year
                        }
                        onChange={(e) =>
                            setResult({
                                ...result,
                                birth_year:
                                    e.target.value
                            })
                        }
                        style={{
                            width: "100%"
                        }}
                    />

                    <br /><br />

                    <label>
                        Country
                    </label>

                    <input
                        value={
                            result.country
                        }
                        onChange={(e) =>
                            setResult({
                                ...result,
                                country:
                                    e.target.value
                            })
                        }
                        style={{
                            width: "100%"
                        }}
                    />

                    <br /><br />

                    <label>
                        Club
                    </label>

                    <input
                        value={
                            result.club
                        }
                        onChange={(e) =>
                            setResult({
                                ...result,
                                club:
                                    e.target.value
                            })
                        }
                        style={{
                            width: "100%"
                        }}
                    />

                    <br /><br />

                    <label>
                        Age Group
                    </label>

                    <input
                        value={
                            result.age_group
                        }
                        onChange={(e) =>
                            setResult({
                                ...result,
                                age_group:
                                    e.target.value
                            })
                        }
                        style={{
                            width: "100%"
                        }}
                    />

                </div>

            </div>

            <hr
                style={{
                    marginTop: "2rem",
                    marginBottom: "2rem"
                }}
            />

            <h2>
                Performance
            </h2>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "repeat(4, 1fr)",
                    gap: "1rem"
                }}
            >

                <div>

                    <label>
                        Performance
                    </label>

                    <input
                        value={
                            result.performance
                        }
                        onChange={(e) =>
                            setResult({
                                ...result,
                                performance:
                                    e.target.value
                            })
                        }
                        style={{
                            width: "100%"
                        }}
                    />

                </div>

                <div>

                    <label>
                        Wind
                    </label>

                    <input
                        type="number"
                        step="0.1"
                        value={
                            result.wind
                        }
                        onChange={(e) =>
                            setResult({
                                ...result,
                                wind:
                                    e.target.value
                            })
                        }
                        style={{
                            width: "100%"
                        }}
                    />

                </div>

                <div>

                    <label>
                        Place
                    </label>

                    <input
                        type="number"
                        value={
                            result.place
                        }
                        onChange={(e) =>
                            setResult({
                                ...result,
                                place:
                                    e.target.value
                            })
                        }
                        style={{
                            width: "100%"
                        }}
                    />

                </div>

                <div>

                    <label>
                        Lane
                    </label>

                    <input
                        value={
                            result.lane
                        }
                        onChange={(e) =>
                            setResult({
                                ...result,
                                lane:
                                    e.target.value
                            })
                        }
                        style={{
                            width: "100%"
                        }}
                    />

                </div>

            </div>

            <br />

            <label>
                Status
            </label>

            <input
                value={
                    result.status
                }
                onChange={(e) =>
                    setResult({
                        ...result,
                        status:
                            e.target.value
                    })
                }
                style={{
                    width: "100%"
                }}
            />

            <hr
                style={{
                    marginTop: "2rem",
                    marginBottom: "2rem"
                }}
            />

            <button
                onClick={createResult}
            >
                Create Result
            </button>

        </div>
    );
}