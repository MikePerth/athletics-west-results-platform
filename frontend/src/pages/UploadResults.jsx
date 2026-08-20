import { useState } from "react";

export default function UploadResults() {
  const [file, setFile] = useState(null);

  const uploadFile = async () => {
    const formData = new FormData();

    formData.append("file", file);

    await fetch(
      "/api/imports/roster/preview",
      {
        method: "POST",
        body: formData,
      }
    );
  };

  return (
    <div>
      <h1>Import Results</h1>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) =>
          setFile(e.target.files[0])
        }
      />

      <button onClick={uploadFile}>
        Preview Import
      </button>
    </div>
  );
}
``