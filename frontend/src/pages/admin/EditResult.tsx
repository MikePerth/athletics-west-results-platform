import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import AdminNav from "./AdminNav";

export default function EditResult() {

    const { id } = useParams();

    const navigate = useNavigate();

    const [loading, setLoading] = useState(true);

    const [result, setResult] = useState<any>(null);

    async function loadResult() {

        setLoading(true);

        try {

            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/admin/results/${id}`
            );

            const data = await response.json();

            setResult(data);

        } catch (error) {

            console.error(error);

        } finally {

            setLoading(false);
        }
    }

    async function saveResult() {

        try {

            const response = await fetch(
                `${import.meta.env.VITE_API_URL}1/admin/results/${id}`,
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(result)
                }
            );

            if (response.ok) {

                alert(
                    "Result saved successfully."
                );

            } else {

                alert(
                    "Unable to save result."
                );
            }

        } catch (error) {

            console.error(error);

            alert(
                "Unexpected error saving result."
            );
        }
    }

    async function deleteResult() {

        const confirmed = window.confirm(
            "Delete this result?"
        );

        if (!confirmed) {
            return;
        }

        try {

            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/admin/results/${id}`,
                {
                    method: "DELETE"
                }
            );

            if (response.ok) {

                alert("Result deleted.");

                navigate("/admin/results");
            }

        } catch (error) {

            console.error(error);

            alert(
                "Unable to delete result."
            );
        }
    }

    useEffect(() => {

        loadResult();

    }, [id]);

    if (loading) {

        return (
            <div>
                Loading result...
            </div>
        );
    }

    if (!result) {

        return (
            <div>
                Result not found.
            </div>
        );
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
                Edit Result
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

                    <h2>Competition</h2>

                    <label>
                        Competition
                    </label>

                    <input
                        value={
                            result.competition_name || ""
                        }
                        disabled
                        style={{
                            width: "100%"
                        }}
                    />

                    <br /><br />

                    <label>
                        Competition Date
                    </label>

                    <input
                        value={
                            result.competition_date || ""
                        }
                        disabled
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
                            result.event_name || ""
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
                            result.round || ""
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

                    <h2>Athlete</h2>

                    <label>
                        Athlete Name
                    </label>

                    <input
                        value={
                            result.athlete_name || ""
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
                            result.birth_year || ""
                        }
                        onChange={(e) =>
                            setResult({
                                ...result,
                                birth_year:
                                    Number(
                                        e.target.value
                                    )
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
                            result.country || ""
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
                            result.club || ""
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
                            result.age_group || ""
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
                            result.performance || ""
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
                            result.wind ?? ""
                        }
                        onChange={(e) =>
                            setResult({
                                ...result,
                                wind:
                                    e.target.value === ""
                                        ? null
                                        : Number(
                                              e.target.value
                                          )
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
                            result.place ?? ""
                        }
                        onChange={(e) =>
                            setResult({
                                ...result,
                                place:
                                    e.target.value === ""
                                        ? null
                                        : Number(
                                              e.target.value
                                          )
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
                            result.lane || ""
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
                    result.status || ""
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

            <div
                style={{
                    display: "flex",
                    gap: "1rem"
                }}
            >

                <button
                    onClick={saveResult}
                >
                    Save Changes
                </button>

                <button
                    onClick={deleteResult}
                    style={{
                        backgroundColor:
                            "#c62828",
                        color: "white"
                    }}
                >
                    Delete Result
                </button>

            </div>

        </div>
    );
}