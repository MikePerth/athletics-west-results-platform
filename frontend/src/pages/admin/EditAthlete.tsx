import {
    useEffect,
    useState
} from "react";

import {
    useNavigate,
    useParams
} from "react-router-dom";

export default function EditAthlete() {

    const { athleteName } =
        useParams();

    const navigate =
        useNavigate();

    const [
        athlete,
        setAthlete
    ] = useState({
        athlete_name: "",
        birth_year: "",
        gender: ""
    });

    const [
        saving,
        setSaving
    ] = useState(false);

    useEffect(() => {

        async function loadAthlete() {

            const response =
                await fetch(
                    `${import.meta.env.VITE_API_URL}/athletes/admin/${athleteName}`
                );

            const data =
                await response.json();

            setAthlete(data);
        }

        loadAthlete();

    }, [athleteName]);

    async function saveAthlete() {

        try {

            setSaving(true);

            await fetch(
                `${import.meta.env.VITE_API_URL}/athletes/admin/${athleteName}`,
                {
                    method: "PUT",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                    body: JSON.stringify(
                        athlete
                    )
                }
            );

            navigate("/admin/athletes");

        } catch (error) {

            console.error(error);

        } finally {

            setSaving(false);
        }
    }

    return (

        <div
            style={{
                maxWidth: "800px",
                margin: "0 auto",
                padding: "2rem"
            }}
        >
            <h1>
                Edit Athlete
            </h1>

            <div
                style={{
                    display: "grid",
                    gap: "1rem"
                }}
            >
                <input
                    value={
                        athlete.athlete_name
                    }
                    onChange={(e) =>
                        setAthlete({
                            ...athlete,
                            athlete_name:
                                e.target.value
                        })
                    }
                    placeholder="Athlete Name"
                />

                <input
                    value={
                        athlete.birth_year
                    }
                    onChange={(e) =>
                        setAthlete({
                            ...athlete,
                            birth_year:
                                e.target.value
                        })
                    }
                    placeholder="Year Of Birth"
                />

                <select
                    value={
                        athlete.gender
                    }
                    onChange={(e) =>
                        setAthlete({
                            ...athlete,
                            gender:
                                e.target.value
                        })
                    }
                >
                    <option value="">
                        Select Gender
                    </option>

                    <option value="Male">
                        Male
                    </option>

                    <option value="Female">
                        Female
                    </option>
                </select>

                <button
                    onClick={saveAthlete}
                    disabled={saving}
                >
                    {saving
                        ? "Saving..."
                        : "Save Athlete"}
                </button>
            </div>

        </div>

    );
}