import { useQuery } from '@tanstack/react-query';
import { useParams, Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { getWord } from '@/lib/api';

export default function WordShow() {
  const { id } = useParams();
  const { data: word } = useQuery({
    queryKey: ['word', id],
    queryFn: () => getWord(id!),
  });

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold tracking-tight">Word Details</h1>

      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Word Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid gap-4 md:grid-cols-3">
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">
                  Spanish
                </h3>
                <p className="text-2xl font-semibold mt-1">
                  {word?.data.spanish}
                </p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">
                  Transliteration
                </h3>
                <p className="text-2xl font-semibold mt-1">
                  {word?.data.transliteration}
                </p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">
                  Arabic
                </h3>
                <p className="text-2xl font-semibold mt-1 font-arabic">
                  {word?.data.arabic}
                </p>
              </div>
            </div>

            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-2">
                Groups
              </h3>
              <div className="flex flex-wrap gap-2">
                {word?.data.groups.map((group: any) => (
                  <Link key={group.id} to={`/groups/${group.id}`}>
                    <Badge variant="secondary">{group.name}</Badge>
                  </Link>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Study Statistics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">
                  Correct Answers
                </h3>
                <p className="text-2xl font-semibold mt-1 text-green-600">
                  {word?.data.correctCount}
                </p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">
                  Wrong Answers
                </h3>
                <p className="text-2xl font-semibold mt-1 text-red-600">
                  {word?.data.wrongCount}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}