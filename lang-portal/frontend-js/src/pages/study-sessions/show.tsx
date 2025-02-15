import { useQuery } from '@tanstack/react-query';
import { useParams, Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { getStudySession, getStudySessionWords } from '@/lib/api';
import { format } from 'date-fns';

export default function StudySessionShow() {
  const { id } = useParams();
  const { data: session } = useQuery({
    queryKey: ['studySession', id],
    queryFn: () => getStudySession(id!),
  });

  const { data: words } = useQuery({
    queryKey: ['studySessionWords', id],
    queryFn: () => getStudySessionWords(id!),
  });

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Study Session</h1>
        <p className="text-muted-foreground mt-2">Session #{id}</p>
      </div>

      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Session Details</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">
                  Activity
                </h3>
                <p className="text-lg font-semibold mt-1">
                  {session?.data.activityName}
                </p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">
                  Group
                </h3>
                <Link
                  to={`/groups/${session?.data.groupId}`}
                  className="text-lg font-semibold mt-1 text-primary hover:underline"
                >
                  {session?.data.groupName}
                </Link>
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">
                  Start Time
                </h3>
                <p className="text-lg font-semibold mt-1">
                  {session?.data.startTime &&
                    format(new Date(session.data.startTime), 'PPp')}
                </p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">
                  End Time
                </h3>
                 Continuing exactly where we left off with the study-sessions/show.tsx file:

                <p className="text-lg font-semibold mt-1">
                  {session?.data.endTime &&
                    format(new Date(session.data.endTime), 'PPp')}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Word Reviews</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Spanish</TableHead>
                  <TableHead>Transliteration</TableHead>
                  <TableHead>Arabic</TableHead>
                  <TableHead>Result</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {words?.data.map((word: any) => (
                  <TableRow key={word.id}>
                    <TableCell>{word.spanish}</TableCell>
                    <TableCell>{word.transliteration}</TableCell>
                    <TableCell className="font-arabic text-lg">
                      {word.arabic}
                    </TableCell>
                    <TableCell>
                      <span
                        className={
                          word.correct
                            ? 'text-green-600 font-medium'
                            : 'text-red-600 font-medium'
                        }
                      >
                        {word.correct ? 'Correct' : 'Wrong'}
                      </span>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}