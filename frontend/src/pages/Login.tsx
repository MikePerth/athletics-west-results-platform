import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {

    const navigate = useNavigate();

    const [username, setUsername] =
        useState("");

    const [password, setPassword] =
        useState("");

    const [loading, setLoading] =
        useState(false);

    async function login() {

        setLoading(true);

        try {

            const response = await fetch(
               `${import.meta.env.VITE_API_URL}/auth/login`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        username,
                        password
                    })
                }
            );

            const data =
                await response.json();

            if (!response.ok) {

                alert(
                    data.detail ??
                    "Invalid login"
                );

                return;
            }

            localStorage.setItem(
                "access_token",
                data.access_token
            );

            localStorage.setItem(
                "username",
                data.username
            );

            navigate("/admin");

        } catch (error) {

            console.error(error);

            alert(
                "Unable to login."
            );

        } finally {

            setLoading(false);
        }
    }

    return (

        <div
            style={{
                minHeight: "100vh",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                background: "#f5f5f5"
            }}
        >

            <div
                style={{
                    width: "400px",
                    background: "#fff",
                    padding: "2rem",
                    borderRadius: "12px",
                    boxShadow:
                        "0 2px 10px rgba(0,0,0,0.15)"
                }}
            >

                <h1>
                    Admin Login
                </h1>

                <div
                    style={{
                        marginBottom: "1rem"
                    }}
                >

                    <label>
                        Username
                    </label>

                    <input
                        value={username}
                        onChange={(e) =>
                            setUsername(
                                e.target.value
                            )
                        }
                        style={{
                            width: "100%",
                            marginTop: "0.5rem",
                            padding: "0.5rem"
                        }}
                    />

                </div>

                <div
                    style={{
                        marginBottom: "1.5rem"
                    }}
                >

                    <label>
                        Password
                    </label>

                    <input
                        type="password"
                        value={password}
                        onChange={(e) =>
                            setPassword(
                                e.target.value
                            )
                        }
                        style={{
                            width: "100%",
                            marginTop: "0.5rem",
                            padding: "0.5rem"
                        }}
                    />

                </div>

                <button
                    onClick={login}
                    disabled={loading}
                    style={{
                        width: "100%"
                    }}
                >
                    {loading
                        ? "Signing In..."
                        : "Login"}
                </button>

            </div>

        </div>

    );
}