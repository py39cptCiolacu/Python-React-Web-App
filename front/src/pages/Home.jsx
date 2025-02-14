import { useEffect, useState } from "react";

export default function Home() {
  const [revisions, setRevisions] = useState([1, 2, 3]);
  const [revisionInput, setRevisionInput] = useState("");

  useEffect(() => {
    window.pywebview.api
      .revision_get_all_revisions()
      .then((response) => setRevisions(response));
  }, []);

  const createRevision = () => {
    window.pywebview.api
      .revision_create_revision({ name: revisionInput })
      .then((response) => {
        setRevisions([...revisions, { name: revisionInput }]);
        setRevisionInput("");
      })
      .catch(alert);
  };

  return (
    <div>
      <header className="w-full p-4 text-center bg-indigo-500 text-white font-bold">
        Revisions
      </header>

      <div className="divide-y divide-gray-800 p-2">
        {revisions.map((rev) => (
          <div>{rev.name}</div>
        ))}
      </div>

      <div className="p-2 space-y-2">
        <input
          type="text"
          className="border w-full p-2"
          placeholder="Revision name"
          value={revisionInput}
          onChange={(e) => setRevisionInput(e.target.value)}
        />
        <button className="bg-gray-300 p-2 w-full" onClick={createRevision}>
          Add
        </button>
      </div>
    </div>
  );
}
