import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import AdminHome from "./pages/admin/AdminHome";
import Athletes from "./pages/admin/Athletes";
import AthleteProfile from "./pages/admin/AthleteProfile";
import UploadResults from "./pages/UploadResults";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route
          path="/"
          element={<AdminHome />}
        />

        <Route
          path="/upload"
          element={<UploadResults />}
        />

        <Route
          path="/admin/athletes"
          element={<Athletes />}
        />

        <Route
          path="/admin/athletes/:athleteName"
          element={<AthleteProfile />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;