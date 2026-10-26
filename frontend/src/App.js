import "@/App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { ThemeProvider } from "next-themes";
import { Toaster } from "@/components/ui/sonner";
import { SessionProvider } from "@/shared/session/SessionProvider";
import { RequireConsent, RequireSession } from "@/shared/session/guards";
import AppShell from "@/shared/layout/AppShell";
import ModeHome from "@/shared/layout/ModeHome";
import LandingPage from "@/features/landing/LandingPage";
import AuthPage from "@/features/auth/AuthPage";
import ConsentPage from "@/features/auth/ConsentPage";
import LegalPage from "@/features/legal/LegalPage";
import DiscoverPage from "@/features/talent/DiscoverPage";
import TalentProfilePage from "@/features/talent/TalentProfilePage";
import ShortlistPage from "@/features/talent/ShortlistPage";
import JobBoardPage from "@/features/jobs/JobBoardPage";
import JobDetailPage from "@/features/jobs/JobDetailPage";
import MyJobsPage from "@/features/jobs/MyJobsPage";
import InboxPage from "@/features/inbox/InboxPage";
import WorkspacePage from "@/features/workspace/WorkspacePage";
import WalletPage from "@/features/wallet/WalletPage";
import SettingsPage from "@/features/settings/SettingsPage";
import NotFoundPage from "@/shared/layout/NotFoundPage";

function App() {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
      <SessionProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/auth" element={<AuthPage />} />
            <Route path="/legal" element={<LegalPage />} />
            <Route path="/consent" element={<RequireSession><ConsentPage /></RequireSession>} />
            <Route path="/app" element={<RequireConsent><AppShell /></RequireConsent>}>
              <Route index element={<ModeHome />} />
              <Route path="discover" element={<DiscoverPage />} />
              <Route path="talent/:talentId" element={<TalentProfilePage />} />
              <Route path="shortlist" element={<ShortlistPage />} />
              <Route path="my-jobs" element={<MyJobsPage />} />
              <Route path="jobs" element={<JobBoardPage />} />
              <Route path="jobs/:jobId" element={<JobDetailPage />} />
              <Route path="inbox" element={<InboxPage />} />
              <Route path="workspace" element={<WorkspacePage />} />
              <Route path="wallet" element={<WalletPage />} />
              <Route path="settings" element={<SettingsPage />} />
              <Route path="*" element={<NotFoundPage inApp />} />
            </Route>
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </BrowserRouter>
        <Toaster position="top-center" richColors closeButton />
      </SessionProvider>
    </ThemeProvider>
  );
}

export default App;
