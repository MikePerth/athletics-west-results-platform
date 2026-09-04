import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import AdminNav from "./AdminNav";

interface ResultRow {
    id: number;

    athlete_name: string;

    competition_name: string;

    competition_date: string;

    event_name: string;

    round: string | null;

    performance: string | null;

    wind: number | null;

    place: number | null;

    status: string | null;

    club: string | null;
}

export default function AdminResults() {

    const [athleteName, setAthleteName] =
        useState("");

    const [eventName, setEventName] =
        useState("");

    const [club, setClub] =
        useState("");

    const [dateFrom, setDateFrom] =
        useState("");

    const [dateTo, setDateTo] =
        useState("");

    const [page, setPage] =
        useState(1);

    const [totalPages, setTotalPages] =
        useState(1);

    const [loading, setLoading] =
        useState(false);

    const [results, setResults] =
        useState<ResultRow[]>([]);

    async function search(
        pageNumber = page
    ) {

        setLoading(true);

        try {

            const params =
                new URLSearchParams();

            params.append(
                "page",
                pageNumber.toString()
            );

            params.append(
                "page_size",
                "50"
            );

            if (
                athleteName.trim()
            ) {
                params.append(
                    "athlete_name",
                    athleteName
                );
            }

            if (
                eventName.trim()
            ) {
                params.append(
                    "event_name",
                    eventName
                );
            }

            if (
                club.trim()
            ) {
                params.append(
                    "club",
                    club
                );
            }

            if (
                dateFrom
            ) {
                params.append(
                    "date_from",
                    dateFrom
                );
            }

            if (
                dateTo
            ) {
                params.append(
                    "date_to",
                    dateTo
                );
            }

            const response =
                await fetch(
                    `${import.meta.env.VITE_API_URL}/admin/results?${params}`
                );

            const data =
                await response.json();

            setResults(
                data.results
            );

            setPage(
                data.page
            );

            setTotalPages(
                data.total_pages
            );

        } catch (error) {

            console.error(
                error
            );

        } finally {

            setLoading(false);
        }
    }

    async function deleteResult(
        id: number
    ) {

        const confirmed =
            window.confirm(
                "Delete this result?"
            );

        if (!confirmed) {
            return;
        }

        try {

            const response =
                await fetch(
                    `${import.meta.env.VITE_API_URL}/admin/results/${id}`,
                    {
                        method:
                            "DELETE"
                    }
                );

            if (response.ok) {

                search();
            }

        } catch (error) {

            console.error(
                error
            );
        }
    }

    useEffect(() => {

        search(1);

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
                Result Administration
            </h1>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "repeat(5, 1fr)",
                    gap: "1rem",
                    marginBottom:
                        "1rem"
                }}
            >

                <input
                    value={
                        athleteName
                    }
                    onChange={(e) =>
                        setAthleteName(
                            e.target.value
                        )
                    }
                    placeholder="Athlete Name"
                />

                <input
                    value={
                        eventName
                    }
                    onChange={(e) =>
                        setEventName(
                            e.target.value
                        )
                    }
                    placeholder="Event Name"
                />

                <input
                    value={
                        club
                    }
                    onChange={(e) =>
                        setClub(
                            e.target.value
                        )
                    }
                    placeholder="Club"
                />

                <input
                    type="date"
                    value={
                        dateFrom
                    }
                    onChange={(e) =>
                        setDateFrom(
                            e.target.value
                        )
                    }
                />

                <input
                    type="date"
                    value={
                        dateTo
                    }
                    onChange={(e) =>
                        setDateTo(
                            e.target.value
                        )
                    }
                />

            </div>

            <div
                style={{
                    display: "flex",
                    gap: "1rem",
                    marginBottom:
                        "2rem"
                }}
            >

                <button
                    onClick={() =>
                        search(1)
                    }
                >
                    Search
                </button>

                <button
                    onClick={() => {

                        setAthleteName(
                            ""
                        );

                        setEventName(
                            ""
                        );

                        setClub(
                            ""
                        );

                        setDateFrom(
                            ""
                        );

                        setDateTo(
                            ""
                        );

                        setPage(1);

                        search(1);
                    }}
                >
                    Clear
                </button>

                <Link
                    to="/admin/results/new"
                >
                    <button>
                        New Result
                    </button>
                </Link>

            </div>

            {loading && (
                <p>
                    Loading...
                </p>
            )}

            <table
                style={{
                    width:
                        "100%",
                    borderCollapse:
                        "collapse"
                }}
            >

                <thead>

                    <tr>

                        <th>
                            Date
                        </th>

                        <th>
                            Competition
                        </th>

                        <th>
                            Athlete
                        </th>

                        <th>
                            Club
                        </th>

                        <th>
                            Event
                        </th>

                        <th>
                            Round
                        </th>

                        <th>
                            Performance
                        </th>

                        <th>
                            Wind
                        </th>

                        <th>
                            Place
                        </th>

                        <th>
                            Status
                        </th>

                        <th>
                            Actions
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {results.map(
                        (row) => (

                            <tr
                                key={
                                    row.id
                                }
                            >

                                <td>
                                    {
                                        row.competition_date
                                    }
                                </td>

                                <td>
                                    {
                                        row.competition_name
                                    }
                                </td>

                                <td>
                                    {
                                        row.athlete_name
                                    }
                                </td>

                                <td>
                                    {
                                        row.club
                                    }
                                </td>

                                <td>
                                    {
                                        row.event_name
                                    }
                                </td>

                                <td>
                                    {
                                        row.round
                                    }
                                </td>

                                <td>
                                    {
                                        row.performance
                                    }
                                </td>

                                <td>
                                    {
                                        row.wind ??
                                        "-"
                                    }
                                </td>

                                <td>
                                    {
                                        row.place
                                    }
                                </td>

                                <td>
                                    {
                                        row.status
                                    }
                                </td>

                                <td>

                                    <Link
                                        to={`/admin/results/${row.id}`}
                                    >
                                        Edit
                                    </Link>

                                    {" | "}

                                    <button
                                        onClick={() =>
                                            deleteResult(
                                                row.id
                                            )
                                        }
                                    >
                                        Delete
                                    </button>

                                </td>

                            </tr>

                        )
                    )}

                </tbody>

            </table>

            <div
                style={{
                    display: "flex",
                    justifyContent:
                        "center",
                    gap: "1rem",
                    marginTop:
                        "2rem"
                }}
            >

                <button
                    disabled={
                        page === 1
                    }
                    onClick={() =>
                        search(
                            page - 1
                        )
                    }
                >
                    Previous
                </button>

                <strong>
                    Page {page} of{" "}
                    {totalPages}
                </strong>

                <button
                    disabled={
                        page >=
                        totalPages
                    }
                    onClick={() =>
                        search(
                            page + 1
                        )
                    }
                >
                    Next
                </button>

            </div>

        </div>
    );
}