import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination';
import { getStudySessions } from '@/lib/api';
import { format } from 'date-fns';

export default function StudySessions() {
  const [page, setPage] = useState(1);
  const { data: sessions } = useQuery({
    queryKey: ['studySessions', page],
    queryFn: () => getStudySessions(page),
  });

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Study Sessions</h1>
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Activity</TableHead>
              <TableHead>Group</TableHead>
              <TableHead>Start Time</TableHead>
              <TableHead>End Time</TableHead>
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
                <TableCell>{session.activityName}</TableCell>
                <TableCell>{session.groupName}</TableCell>
                <TableCell>
                  {format(new Date(session.startTime), 'PPp')}
                </TableCell>
                <TableCell>
                  {format(new Date(session.endTime), 'PPp')}
                </TableCell>
                <TableCell>{session.reviewItemCount}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <Pagination>
        <PaginationContent>
          <PaginationItem>
            <PaginationPrevious
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
            />
          </PaginationItem>
          <PaginationItem>
            <PaginationLink>{page}</PaginationLink>
          </PaginationItem>
          <PaginationItem>
            <PaginationNext
              onClick={() => setPage(p => p + 1)}
              disabled={!sessions?.data.length}
            />
          </PaginationItem>
        </PaginationContent>
      </Pagination>
    </div>
  );
}