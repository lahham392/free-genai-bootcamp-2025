import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { getStudyActivities } from '@/lib/api';
import { BookOpen, ExternalLink } from 'lucide-react';

export default function StudyActivities() {
  const { data: activities } = useQuery({
    queryKey: ['studyActivities'],
    queryFn: () => getStudyActivities(),
  });

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Study Activities</h1>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {activities?.data.map((activity: any) => (
          <Card key={activity.id}>
            <CardHeader>
              <CardTitle>{activity.name}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="aspect-video relative rounded-lg bg-muted overflow-hidden">
                <img
                  src={activity.thumbnail}
                  alt={activity.name}
                  className="object-cover w-full h-full"
                />
              </div>
              <p className="text-sm text-muted-foreground">
                {activity.description}
              </p>
              <div className="flex gap-2">
                <Button asChild className="flex-1">
                  <Link to={`/study-activities/${activity.id}/launch`}>
                    <BookOpen className="h-4 w-4 mr-2" />
                    Launch
                  </Link>
                </Button>
                <Button variant="outline" asChild>
                  <Link to={`/study-activities/${activity.id}`}>
                    <ExternalLink className="h-4 w-4 mr-2" />
                    View
                  </Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}