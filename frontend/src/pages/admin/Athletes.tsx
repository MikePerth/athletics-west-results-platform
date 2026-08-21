import { useState } from "react";
import { Link } from "react-router-dom";

export default function Athletes() {

    const [query, setQuery] = useState("");
    const [results, setResults] = useState<any[]>([]);

    async function search() {

      console.log("Search clicked");
      console.log("Query:", query);

      const response = await fetch(
          `http://localhost:8001/athletes/search?q=${query}`
      );

      console.log("Response:", response);

      const data = await response.json();

      console.log("Data:", data);

      setResults(data);
  }

    return (
        <div style={{ padding: "2rem" }}>

            <h1>Athlete Search</h1>

            <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search athlete..."
            />

            <button onClick={search}>
                Search
            </button>

            <hr />

            {results.map((athlete) => (

                <div
                    key={athlete.athlete_name}
                    style={{
                        marginBottom: "1rem"
                    }}
                >
                    <strong>
                        {athlete.athlete_name}
                    </strong>

                    <br />

                    Club: {athlete.club}

                    <br />

                    Results: {athlete.results}

                    <br />

                    <Link
                        to={`/admin/athletes/${encodeURIComponent(
                            athlete.athlete_name
                        )}`}
                    >
                        View Profile
                    </Link>

                </div>

            ))}

        </div>
    );
}