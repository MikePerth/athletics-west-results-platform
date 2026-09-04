import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import AdminNav from "./AdminNav";

interface User {
    id: number;
    username: string;
    is_active: boolean;
    is_admin: boolean;
    created_at: string;
}

export default function AdminUsers() {

    const [loading, setLoading] =
        useState(false);

    const [users, setUsers] =
        useState<User[]>([]);

    async function loadUsers() {

        setLoading(true);

        try {

            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/admin/users`
            );

            const data =
                await response.json();

            setUsers(data);

        } catch (error) {

            console.error(error);

            alert(
                "Unable to load users."
            );

        } finally {

            setLoading(false);
        }
    }

    async function disableUser(
        userId: number,
        username: string
    ) {

        const confirmed =
            window.confirm(
                `Disable user "${username}"?`
            );

        if (!confirmed) {
            return;
        }

        try {

            const response =
                await fetch(
                    `${import.meta.env.VITE_API_URL}/admin/users/${userId}`,
                    {
                        method: "PUT",
                        headers: {
                            "Content-Type":
                                "application/json"
                        },
                        body: JSON.stringify({
                            is_active: false
                        })
                    }
                );

            if (response.ok) {

                loadUsers();

            } else {

                alert(
                    "Unable to disable user."
                );
            }

        } catch (error) {

            console.error(error);
        }
    }

    async function enableUser(
        userId: number,
        username: string
    ) {

        const confirmed =
            window.confirm(
                `Enable user "${username}"?`
            );

        if (!confirmed) {
            return;
        }

        try {

            const response =
                await fetch(
                    `${import.meta.env.VITE_API_URL}/admin/users/${userId}`,
                    {
                        method: "PUT",
                        headers: {
                            "Content-Type":
                                "application/json"
                        },
                        body: JSON.stringify({
                            is_active: true
                        })
                    }
                );

            if (response.ok) {

                loadUsers();

            } else {

                alert(
                    "Unable to enable user."
                );
            }

        } catch (error) {

            console.error(error);
        }
    }

    async function deleteUser(
        userId: number,
        username: string
    ) {

        const confirmed =
            window.confirm(
                `Delete user "${username}"?\n\nThis action cannot be undone.`
            );

        if (!confirmed) {
            return;
        }

        try {

            const response =
                await fetch(
                    `${import.meta.env.VITE_API_URL}/admin/users/${userId}`,
                    {
                        method: "DELETE"
                    }
                );

            if (response.ok) {

                loadUsers();

            } else {

                alert(
                    "Unable to delete user."
                );
            }

        } catch (error) {

            console.error(error);
        }
    }

    useEffect(() => {

        loadUsers();

    }, []);

    return (

        <div
            style={{
                maxWidth: "1400px",
                margin: "0 auto",
                padding: "2rem"
            }}
        >

            <AdminNav />

            <div
                style={{
                    display: "flex",
                    justifyContent:
                        "space-between",
                    alignItems: "center",
                    marginBottom: "2rem"
                }}
            >

                <h1>
                    User Management
                </h1>

                <Link
                    to="/admin/users/new"
                >
                    <button>
                        New User
                    </button>
                </Link>

            </div>

            {loading && (

                <p>
                    Loading users...
                </p>

            )}

            {!loading && (

                <div
                    style={{
                        background: "#fff",
                        borderRadius:
                            "12px",
                        padding: "1rem",
                        boxShadow:
                            "0 2px 8px rgba(0,0,0,0.08)"
                    }}
                >

                    <table
                        style={{
                            width: "100%",
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
                                            "12px",
                                        textAlign:
                                            "left"
                                    }}
                                >
                                    Username
                                </th>

                                <th
                                    style={{
                                        padding:
                                            "12px",
                                        textAlign:
                                            "left"
                                    }}
                                >
                                    Active
                                </th>

                                <th
                                    style={{
                                        padding:
                                            "12px",
                                        textAlign:
                                            "left"
                                    }}
                                >
                                    Admin
                                </th>

                                <th
                                    style={{
                                        padding:
                                            "12px",
                                        textAlign:
                                            "left"
                                    }}
                                >
                                    Created
                                </th>

                                <th
                                    style={{
                                        padding:
                                            "12px",
                                        textAlign:
                                            "left"
                                    }}
                                >
                                    Actions
                                </th>

                            </tr>

                        </thead>

                        <tbody>

                            {users.map(
                                (
                                    user
                                ) => (

                                    <tr
                                        key={
                                            user.id
                                        }
                                        style={{
                                            borderTop:
                                                "1px solid #eee"
                                        }}
                                    >

                                        <td
                                            style={{
                                                padding:
                                                    "12px"
                                            }}
                                        >
                                            {
                                                user.username
                                            }
                                        </td>

                                        <td
                                            style={{
                                                padding:
                                                    "12px"
                                            }}
                                        >
                                            {user.is_active
                                                ? "✅"
                                                : "❌"}
                                        </td>

                                        <td
                                            style={{
                                                padding:
                                                    "12px"
                                            }}
                                        >
                                            {user.is_admin
                                                ? "✅"
                                                : "❌"}
                                        </td>

                                        <td
                                            style={{
                                                padding:
                                                    "12px"
                                            }}
                                        >
                                            {
                                                user.created_at
                                            }
                                        </td>

                                        <td
                                            style={{
                                                padding:
                                                    "12px"
                                            }}
                                        >

                                            <Link
                                                to={`/admin/users/${user.id}`}
                                            >
                                                Edit
                                            </Link>

                                            {" | "}

                                            {user.is_active ? (

                                                <button
                                                    onClick={() =>
                                                        disableUser(
                                                            user.id,
                                                            user.username
                                                        )
                                                    }
                                                >
                                                    Disable
                                                </button>

                                            ) : (

                                                <button
                                                    onClick={() =>
                                                        enableUser(
                                                            user.id,
                                                            user.username
                                                        )
                                                    }
                                                >
                                                    Enable
                                                </button>

                                            )}

                                            {" | "}

                                            <button
                                                onClick={() =>
                                                    deleteUser(
                                                        user.id,
                                                        user.username
                                                    )
                                                }
                                                style={{
                                                    color:
                                                        "#c62828"
                                                }}
                                            >
                                                Delete
                                            </button>

                                        </td>

                                    </tr>

                                )
                            )}

                        </tbody>

                    </table>

                </div>

            )}

        </div>

    );
}