import { useEffect, useState } from "react";
import AdminNav from "./AdminNav";






export default function MergeAthlete() {

    const [sourceName, setSourceName] =
        useState("");

    const [targetName, setTargetName] =
        useState("");

    const [athletes, setAthletes] =
        useState<string[]>([]);

    useEffect(() => {

        async function loadAthletes() {

            try {

                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/athletes/list`
                );

                const data =
                    await response.json();

                setAthletes(data);

            } catch (error) {

                console.error(error);
            }
        }

        loadAthletes();

    }, []);

    const [loading, setLoading] =
        useState(false);

    const [message, setMessage] =
        useState("");

    async function mergeAthletes() {

        if (!sourceName.trim()) {

            alert(
                "Please enter a source athlete."
            );

            return;
        }

        if (!targetName.trim()) {

            alert(
                "Please enter a target athlete."
            );

            return;
        }

        if (
            sourceName.trim().toLowerCase()
            ===
            targetName.trim().toLowerCase()
        ) {

            alert(
                "Source and target athletes cannot be the same."
            );

            return;
        }

        const confirmed = window.confirm(
            `Merge all results from "${sourceName}" into "${targetName}"?`
        );

        if (!confirmed) {
            return;
        }

        setLoading(true);

        setMessage("");

        try {

            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/athletes/admin/merge`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                    body: JSON.stringify({
                        source_name:
                            sourceName.trim(),
                        target_name:
                            targetName.trim()
                    })
                }
            );

            const data =
                await response.json();

            if (!response.ok) {

                alert(
                    data.detail ??
                    "Unable to merge athletes."
                );

                return;
            }

            setMessage(
                `Merged ${data.merged_results} result(s) from "${sourceName}" into "${targetName}".`
            );

            setSourceName("");

            setTargetName("");

        } catch (error) {

            console.error(error);

            alert(
                "Unexpected error while merging athletes."
            );

        } finally {

            setLoading(false);
        }
    }

    return (

        <div
            style={{
                maxWidth: "1000px",
                margin: "0 auto",
                padding: "2rem"
            }}
        >

            <AdminNav />

            <h1>
                Merge Athletes
            </h1>

            <p>
                Move all results from one athlete
                profile to another.
            </p>

            <div
                style={{
                    background: "#fff",
                    borderRadius: "12px",
                    padding: "2rem",
                    boxShadow:
                        "0 2px 8px rgba(0,0,0,0.08)"
                }}
            >

                <div
                    style={{
                        marginBottom: "1.5rem"
                    }}
                >

                    <label>
                        Source Athlete
                    </label>

                    <select
                        value={sourceName}
                        onChange={(e) =>
                            setSourceName(
                                e.target.value
                            )
                        }
                        style={{
                            width: "100%",
                            padding: "0.75rem",
                            marginTop: "0.5rem"
                        }}
                    >

                        <option value="">
                            Select athlete...
                        </option>

                        {athletes.map(
                            (athlete) => (

                                <option
                                    key={athlete}
                                    value={athlete}
                                >
                                    {athlete}
                                </option>

                            )
                        )}

                    </select>

                </div>

                <div
                    style={{
                        marginBottom: "1.5rem"
                    }}
                >

                    <label>
                        Target Athlete
                    </label>

                    <select
                        value={targetName}
                        onChange={(e) =>
                            setTargetName(
                                e.target.value
                            )
                        }
                        style={{
                            width: "100%",
                            padding: "0.75rem",
                            marginTop: "0.5rem"
                        }}
                    >

                        <option value="">
                            Select athlete...
                        </option>

                        {athletes.map(
                            (athlete) => (

                                <option
                                    key={athlete}
                                    value={athlete}
                                >
                                    {athlete}
                                </option>

                            )
                        )}

                    </select>

                </div>

                <div
                    style={{
                        background: "#f8f9fa",
                        padding: "1rem",
                        borderRadius: "8px",
                        marginBottom: "2rem"
                    }}
                >

                    <h3>
                        Preview
                    </h3>

                    <p>
                        Results will be moved
                        from:
                    </p>

                    <p>
                        <strong>
                            {sourceName ||
                                "Source Athlete"}
                        </strong>
                    </p>

                    <p>
                        to:
                    </p>

                    <p>
                        <strong>
                            {targetName ||
                                "Target Athlete"}
                        </strong>
                    </p>

                </div>

                <button
                    onClick={
                        mergeAthletes
                    }
                    disabled={
                        loading
                    }
                >

                    {loading
                        ? "Merging..."
                        : "Merge Athletes"}

                </button>

                {message && (

                    <div
                        style={{
                            marginTop: "1rem",
                            padding: "1rem",
                            background:
                                "#e8f5e9",
                            borderRadius:
                                "8px",
                            color: "#2e7d32"
                        }}
                    >
                        {message}
                    </div>

                )}

            </div>

        </div>

    );
}