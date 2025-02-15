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
import { getWords } from '@/lib/api';

export default function Words() {
  const [page, setPage] = useState(1);
  const { data: words } = useQuery({
    queryKey: ['words', page],
    queryFn: () => getWords(page),
  });

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Words</h1>
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Spanish</TableHead>
              <TableHead>Transliteration</TableHead>
              <TableHead>Arabic</TableHead>
              <TableHead>Correct</TableHead>
              <TableHead>Wrong</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {words?.data.map((word: any) => (
              <TableRow key={word.id}>
                <TableCell>
                  <Link
                    to={`/words/${word.id}`}
                    className="text-primary hover:underline"
                  >
                    {word.spanish}
                  </Link>
                </TableCell>
                <TableCell>{word.transliteration}</TableCell>
                <TableCell className="font-arabic text-lg">
                  {word.arabic}
                </TableCell>
                <TableCell>{word.correctCount}</TableCell>
                <TableCell>{word.wrongCount}</TableCell>
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
              disabled={!words?.data.length}
            />
          </PaginationItem>
        </PaginationContent>
      </Pagination>
    </div>
  );
}