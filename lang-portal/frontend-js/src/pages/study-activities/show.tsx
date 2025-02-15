import { useQuery } from '@tanstack/react-query';
import { useParams, Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { getStudyActivity, getStudyActivitySessions } from '@/lib/api';
import { BookOpen } from 'lucide-react';
import { format } from 'date-fns';

export default function StudyActivityShow() {
  const { id } = useParams();
  const { data: activity } = useQuery({
    queryKey: ['studyActivity', id],
    queryFn: () => getStudyActivity(id!),
  });

  const { data: sessions } = useQuery({
    queryKey: ['studyActivitySessions', id],
    queryFn: () => getStudyActivitySessions(id!),
  });

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">
          {activity?.data.name}
        </h1>
        <Button asChild>
          <Link to={`/study-activities/${id}/launch`}>
            <BookOpen className="h-5 w-5 mr-2" />
            Launch Activity
          </Link>
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Activity Details</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="aspect-video relative rounded-lg bg-muted overflow-hidden mb-4">
              <img
                src={activity?.data.thumbnail}
                alt={activity?.data.name}
                className="object-cover w-full h-full"
              />
            </div>
            <p className="text-muted-foreground">
              {activity?.data.description}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Study Sessions</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>Group</TableHead>
                  <TableHead>Start Time</TableHead>
                  <TableHead>Items</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {sessions?.data.map((session: any) => (
                  <TableRow key={session.id}>
                    <TableCell>
                      <Link
                        to={`/study-sessions/${session.id}`}
                        className="text-primary hover:underline"
                      >
                        {session.id}
                      </Link>
                    </TableCell>
                    <TableCell>{session.groupName}</TableCell>
                    <TableCell>
                      {format(new Date(session.startTime), 'PPp')}
                    </TableCell>
                    <TableCell>{session.reviewItemCount}</TableCell>
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