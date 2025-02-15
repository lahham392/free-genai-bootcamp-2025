import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@/components/theme-provider';
import { Toaster } from '@/components/ui/sonner';
import Layout from '@/components/layout';
import Dashboard from '@/pages/dashboard';
import StudyActivities from '@/pages/study-activities';
import StudyActivityShow from '@/pages/study-activities/show';
import StudyActivityLaunch from '@/pages/study-activities/launch';
import Words from '@/pages/words';
import WordShow from '@/pages/words/show';
import Groups from '@/pages/groups';
import GroupShow from '@/pages/groups/show';
import StudySessions from '@/pages/study-sessions';
import StudySessionShow from '@/pages/study-sessions/show';
import Settings from '@/pages/settings';

function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/study-activities" element={<StudyActivities />} />
            <Route path="/study-activities/:id" element={<StudyActivityShow />} />
            <Route path="/study-activities/:id/launch" element={<StudyActivityLaunch />} />
            <Route path="/words" element={<Words />} />
            <Route path="/words/:id" element={<WordShow />} />
            <Route path="/groups" element={<Groups />} />
            <Route path="/groups/:id" element={<GroupShow />} />
            <Route path="/study-sessions" element={<StudySessions />} />
            <Route path="/study-sessions/:id" element={<StudySessionShow />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Layout>
      </Router>
      <Toaster />
    </ThemeProvider>
  );
}

export default App;