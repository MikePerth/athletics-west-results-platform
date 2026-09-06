

import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function AdminAlerts() {

    console.log("AdminAlerts component rendered");

    const [alerts, setAlerts] =
        useState<any[]>([]);

    const [reviewedAlerts, setReviewedAlerts] =
        useState<any[]>([]);

    const [loading, setLoading] =
        useState(true);

    async function loadAlerts() {

        try {

            const openResponse =
                await fetch(
                    `${import.meta.env.VITE_API_URL}/alerts`
                );

            const openData =
                await openResponse.json();

            const reviewedResponse =
                await fetch(
                    `${import.meta.env.VITE_API_URL}/alerts/reviewed`
                );

            const reviewedData =
                await reviewedResponse.json();

            setAlerts(openData);
            setReviewedAlerts(reviewedData);

        } catch (error) {

            console.error(error);

        } finally {

            setLoading(false);

        }
    }

    async function generateAlerts() {

        try {

            console.log(
                "Calling:",
                `${import.meta.env.VITE_API_URL}/alerts/scan`
            );

            const response =
                await fetch(
                    `${import.meta.env.VITE_API_URL}/alerts/scan`,
                    {
                        method: "POST"
                    }
                );

            console.log(
                "Status:",
                response.status
            );

            const data =
                await response.json();

            console.log(data);

            alert(
                JSON.stringify(
                    data,
                    null,
                    2
                )
            );

            await loadAlerts();

        } catch (error) {

            console.error(
                "Generate alerts failed",
                error
            );

        }

    }


    async function reviewAlert(
        alertId: number
    ) {

        try {

            await fetch(
                `${import.meta.env.VITE_API_URL}/alerts/${alertId}/review`,
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        notes: ""
                    })
                }
            );

            loadAlerts();

        } catch (error) {

            console.error(error);

        }
    }

    function alertColour(
        type: string
    ) {

        switch (type) {

            case "INVALID_PERFORMANCE":
                return "#ffe5e5";

            case "INVALID_ATHLETE_NAME":
                return "#fff3cd";

            case "MULTIPLE_BIRTH_YEARS":
                return "#d1ecf1";

            case "POSSIBLE_DUPLICATE_ATHLETE":
                return "#e2e3ff";

            default:
                return "#f8f9fa";

        }
    }

    useEffect(() => {

        loadAlerts();

    }, []);


    if (loading) {

        return (
            <div
                style={{
                    padding: "2rem"
                }}
            >
                Loading alerts...
            </div>
        );
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
                Admin Alerts
            </h1>

            <div
                style={{
                    marginBottom: "2rem"
                }}
            >

                <button
                    onClick={generateAlerts}
                    style={{
                        background: "#2563eb",
                        color: "white",
                        border: "none",
                        padding: "0.75rem 1.5rem",
                        borderRadius: "8px",
                        cursor: "pointer",
                        fontWeight: 600
                    }}
                >
                    Generate Alerts
                </button>

            </div>

            <h2>
                Open Alerts ({alerts.length})
            </h2>

            <table
                style={{
                    width: "100%",
                    borderCollapse: "collapse",
                    marginBottom: "3rem"
                }}
            >

                <thead>

                    <tr
                        style={{
                            background: "#f8f9fa"
                        }}
                    >
                        <th style={{ padding: "12px" }}>
                            Type
                        </th>

                        <th style={{ padding: "12px" }}>
                            Entity
                        </th>

                        <th style={{ padding: "12px" }}>
                            Message
                        </th>

                        <th style={{ padding: "12px" }}>
                            Open
                        </th>

                        <th style={{ padding: "12px" }}>
                            Review
                        </th>
                    </tr>

                </thead>

                <tbody>

                    {alerts.map(
                        (alert) => (

                            <tr
                                key={alert.id}
                                style={{
                                    background:
                                        alertColour(
                                            alert.type
                                        ),
                                    borderTop:
                                        "1px solid #ddd"
                                }}
                            >

                                <td
                                    style={{
                                        padding: "12px",
                                        fontWeight: 600
                                    }}
                                >
                                    {alert.type}
                                </td>

                                <td
                                    style={{
                                        padding: "12px"
                                    }}
                                >
                                    {alert.entity_type}
                                    {" "}
                                    {alert.entity_id}
                                </td>

                                <td
                                    style={{
                                        padding: "12px"
                                    }}
                                >
                                    {alert.message}
                                </td>

                                <td
                                    style={{
                                        padding: "12px"
                                    }}
                                >

                                    {alert.entity_type === "RESULT" && (

                                        <Link
                                            to={`/admin/results/${alert.entity_id}`}
                                            style={{
                                                color: "#2563eb",
                                                fontWeight: 600,
                                                textDecoration: "none"
                                            }}
                                        >
                                            Open Result
                                        </Link>

                                    )}

                                    {alert.entity_type === "ATHLETE" && (

                                        <Link
                                            to={`/admin/athletes/${alert.entity_id}`}
                                            style={{
                                                color: "#2563eb",
                                                fontWeight: 600,
                                                textDecoration: "none"
                                            }}
                                        >
                                            Open Athlete
                                        </Link>

                                    )}

                                </td>

                                <td
                                    style={{
                                        padding: "12px"
                                    }}
                                >

                                    <button
                                        onClick={() =>
                                            reviewAlert(
                                                alert.id
                                            )
                                        }
                                        style={{
                                            background: "#28a745",
                                            color: "white",
                                            border: "none",
                                            padding: "0.5rem 1rem",
                                            borderRadius: "6px",
                                            cursor: "pointer"
                                        }}
                                    >
                                        ✓ Reviewed
                                    </button>

                                </td>

                            </tr>

                        )
                    )}

                </tbody>

            </table>

            <h2>
                Reviewed Alerts ({reviewedAlerts.length})
            </h2>

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
                            Type
                        </th>

                        <th style={{ padding: "12px" }}>
                            Entity
                        </th>

                        <th style={{ padding: "12px" }}>
                            Message
                        </th>

                        <th style={{ padding: "12px" }}>
                            Open
                        </th>

                        <th style={{ padding: "12px" }}>
                            Review
                        </th>
                    </tr>

                </thead>

                <tbody>

                    {reviewedAlerts.map(
                        (alert) => (

                            <tr
                                key={alert.id}
                                style={{
                                    opacity: 0.7,
                                    borderTop:
                                        "1px solid #ddd"
                                }}
                            >

                                <td style={{ padding: "12px" }}>
                                    {alert.type}
                                </td>

                                <td style={{ padding: "12px" }}>
                                    {alert.entity_type}
                                    {" "}
                                    {alert.entity_id}
                                </td>

                                <td style={{ padding: "12px" }}>
                                    {alert.message}
                                </td>

                                <td style={{ padding: "12px" }}>
                                    {alert.reviewed_at}
                                </td>

                            </tr>

                        )
                    )}

                </tbody>

            </table>

        </div>

    );
}