import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useParams } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
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
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs';
import { getGroup, getGroupWords, getGroupStudySessions } from '@/lib/api';
import { format } from 'date-fns';

export default function GroupShow() {
  const { id } = useParams();
  const [wordsPage, setWordsPage] = useState(1);
  const [sessionsPage, setSessionsPage] = useState(1);

  const { data: group } = useQuery({
    queryKey: ['group', id],
    queryFn: () => getGroup(id!),
  });

  const { data: words } = useQuery({
    queryKey: ['groupWords', id, wordsPage],
    queryFn: () => getGroupWords(id!, wordsPage),
  });

  const { data: sessions } = useQuery({
    queryKey: ['groupSessions', id, sessionsPage],
    queryFn: () => getGroupStudySessions(id!, sessionsPage),
  });

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">
          {group?.data.name}
        </h1>
        <p className="text-muted-foreground mt-2">
          {group?.data.totalWords} words in this group
        </p>
      </div>

      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Group Statistics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-3">
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">
                  Total Words
                </h3>
                <p className="text-2xl font-semibold mt-1">
                  {group?.data.totalWords}
                </p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">
                  Study Sessions
                </h3>
                <p className="text-2xl font-semibold mt-1">
                  {group?.data.totalSessions}
                </p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">
                  Success Rate
                </h3>
                <p className="text-2xl font-semibold mt-1">
                  {group?.data.successRate}%
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Tabs defaultValue="words">
          <TabsList>
            <TabsTrigger value="words">Words</TabsTrigger>
            <TabsTrigger value="sessions">Study Sessions</TabsTrigger>
          </TabsList>

          <TabsContent value="words" className="space-y-4">
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
                      <TableCell>{word.spanish}</TableCell>
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
                    onClick={() => setWordsPage(p => Math.max(1, p - 1))}
                    disabled={wordsPage === 1}
                  />
                </PaginationItem>
                <PaginationItem>
                  <PaginationLink>{wordsPage}</PaginationLink>
                </PaginationItem>
                <PaginationItem>
                  <PaginationNext
                    onClick={() => setWordsPage(p => p + 1)}
                    disabled={!words?.data.length}
                  />
                </PaginationItem>
              </PaginationContent>
            </Pagination>
          </TabsContent>

          <TabsContent value="sessions" className="space-y-4">
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Activity</TableHead>
                    <TableHead>Start Time</TableHead>
                    <TableHead>End Time</TableHead>
                    <TableHead>Items</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {sessions?.data.map((session: any) => (
                    <TableRow key={session.id}>
                      <TableCell>{session.activityName}</TableCell>
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
                    onClick={() => setSessionsPage(p => Math.max(1, p - 1))}
                    disabled={sessionsPage === 1}
                  />
                </PaginationItem>
                <PaginationItem>
                  <PaginationLink>{sessionsPage}</PaginationLink>
                </PaginationItem>
                <PaginationItem>
                  <PaginationNext
                    onClick={() => setSessionsPage(p => p + 1)}
                    disabled={!sessions?.data.length}
                  />
                </PaginationItem>
              </PaginationContent>
            </Pagination>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}