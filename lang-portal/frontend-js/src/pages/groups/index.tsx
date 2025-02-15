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
import { getGroups } from '@/lib/api';

export default function Groups() {
  const [page, setPage] = useState(1);
  const { data: groups } = useQuery({
    queryKey: ['groups', page],
    queryFn: () => getGroups(page),
  });

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Word Groups</h1>
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Group Name</TableHead>
              <TableHead>Word Count</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {groups?.data.map((group: any) => (
              <TableRow key={group.id}>
                <TableCell>
                  <Link
                    to={`/groups/${group.id}`}
                    className="text-primary hover:underline"
                  >
                    {group.name}
                  </Link>
                </TableCell>
                <TableCell>{group.wordCount}</TableCell>
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
              disabled={!groups?.data.length}
            />
          </PaginationItem>
        </PaginationContent>
      </Pagination>
    </div>
  );
}