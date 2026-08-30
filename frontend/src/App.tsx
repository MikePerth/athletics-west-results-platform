import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import AdminHome from "./pages/admin/AdminHome";
import Athletes from "./pages/Athletes";
import AthleteProfile from "./pages/AthleteProfile";
import UploadResults from "./pages/UploadResults";
import AdminResults from "./pages/admin/AdminResults";
import CreateResult from "./pages/admin/CreateResult";
import EditResult from "./pages/admin/EditResult";
import MergeAthlete from "./pages/admin/MergeAthlete";
import AdminUsers from "./pages/admin/AdminUsers";
import Login from "./pages/Login";
import ProtectedRoute from "./components/ProtectedRoute";
import AdminAthletes from "./pages/admin/AdminAthletes";
import CompetitionResults from "./pages/CompetitionResults";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route
          path="/admin"
          element={
              <ProtectedRoute>
                  <AdminHome />
              </ProtectedRoute>
          }
      />

        <Route
            path="/athletes"
            element={<Athletes />}
        />

        <Route
            path="/competitions/:competitionId"
            element={
                <CompetitionResults />
            }
        />
        
        <Route
            path="/athletes/:athleteName"
            element={<AthleteProfile />}
        />  

        <Route
          path="/login"
          element={<Login />}
      />

       <Route
          path="/admin/results"
          element={
              <ProtectedRoute>
                  <AdminResults />
              </ProtectedRoute>
          }
      />

      <Route
          path="/admin/results/new"
          element={
              <ProtectedRoute>
                  <CreateResult />
              </ProtectedRoute>
          }
      />

      <Route
          path="/admin/results/:id"
          element={
              <ProtectedRoute>
                  <EditResult />
              </ProtectedRoute>
          }
      />

      <Route
          path="/admin/athletes"
          element={
              <ProtectedRoute>
                  <AdminAthletes />
              </ProtectedRoute>
          }
      />

      <Route
          path="/admin/athletes/:athleteName"
          element={
              <ProtectedRoute>
                  <AthleteProfile />
              </ProtectedRoute>
          }
      />

      <Route
          path="/admin/athletes/merge"
          element={
              <ProtectedRoute>
                  <MergeAthlete />
              </ProtectedRoute>
          }
      />

      <Route
          path="/admin/users"
          element={
              <ProtectedRoute>
                  <AdminUsers />
              </ProtectedRoute>
          }
      />

      </Routes>
    </BrowserRouter>
  );
}

export default App;