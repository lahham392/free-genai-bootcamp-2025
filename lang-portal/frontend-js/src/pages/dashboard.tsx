import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import {
  getDashboardLastStudySession,
  getDashboardStudyProgress,
  getDashboardQuickStats,
} from '@/lib/api';
import { BookOpen, Calendar, Target, Trophy } from 'lucide-react';

export default function Dashboard() {
  const { data: lastSession } = useQuery({
    queryKey: ['lastStudySession'],
    queryFn: () => getDashboardLastStudySession(),
  });

  const { data: progress } = useQuery({
    queryKey: ['studyProgress'],
    queryFn: () => getDashboardStudyProgress(),
  });

  const { data: stats } = useQuery({
    queryKey: ['quickStats'],
    queryFn: () => getDashboardQuickStats(),
  });

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <Link to="/study-activities">
          <Button size="lg" className="gap-2">
            <BookOpen className="h-5 w-5" />
            Start Studying
          </Button>
        </Link>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.data.successRate}%</div>
            <p className="text-xs text-muted-foreground">
              Overall correct answers
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Study Sessions</CardTitle>
            <BookOpen className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {stats?.data.totalStudySessions}
            </div>
            <p className="text-xs text-muted-foreground">Total sessions</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Groups</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {stats?.data.totalActiveGroups}
            </div>
            <p className="text-xs text-muted-foreground">Groups in study</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Study Streak</CardTitle>
            <Trophy className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.data.studyStreak}</div>
            <p className="text-xs text-muted-foreground">Days in a row</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Last Study Session</CardTitle>
          </CardHeader>
          <CardContent>
            {lastSession?.data ? (
              <div className="space-y-4">
                <div>
                  <h4 className="text-sm font-medium">Activity</h4>
                  <p className="text-2xl font-bold">
                    {lastSession.data.activityName}
                  </p>
                </div>
                <div>
                  <h4 className="text-sm font-medium">Group</h4>
                  <Link
                    to={`/groups/${lastSession.data.groupId}`}
                    className="text-primary hover:underline"
                  >
                    {lastSession.data.groupName}
                  </Link>
                </div>
                <div className="pt-4">
                  <div className="flex justify-between text-sm text-muted-foreground mb-2">
                    <span>Correct: {lastSession.data.correctCount}</span>
                    <span>Wrong: {lastSession.data.wrongCount}</span>
                  </div>
                  <Progress
                    value={
                      (lastSession.data.correctCount /
                        (lastSession.data.correctCount +
                          lastSession.data.wrongCount)) *
                      100
                    }
                  />
                </div>
              </div>
            ) : (
              <p className="text-muted-foreground">No study sessions yet</p>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Study Progress</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h4 className="text-sm font-medium">Words Studied</h4>
                <p className="text-2xl font-bold">
                  {progress?.data.wordsStudied} / {progress?.data.totalWords}
                </p>
              </div>
              <div>
                <h4 className="text-sm font-medium mb-2">Mastery Progress</h4>
                <Progress value={progress?.data.masteryPercentage || 0} />
                <p className="text-sm text-muted-foreground mt-2">
                  {progress?.data.masteryPercentage}% mastered
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}