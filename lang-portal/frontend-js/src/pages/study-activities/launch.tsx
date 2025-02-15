import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { getStudyActivity, getGroups, createStudyActivity } from '@/lib/api';
import { toast } from 'sonner';

export default function StudyActivityLaunch() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [selectedGroup, setSelectedGroup] = useState('');

  const { data: activity } = useQuery({
    queryKey: ['studyActivity', id],
    queryFn: () => getStudyActivity(id!),
  });

  const { data: groups } = useQuery({
    queryKey: ['groups'],
    queryFn: () => getGroups(),
  });

  const handleLaunch = async () => {
    if (!selectedGroup) {
      toast.error('Please select a group');
      return;
    }

    try {
      const response = await createStudyActivity({
        activityId: id,
        groupId: selectedGroup,
      });

      // Open the activity URL in a new tab
      window.open(activity?.data.url, '_blank');

      // Navigate to the study session
      navigate(`/study-sessions/${response.data.studySessionId}`);
    } catch (error) {
      toast.error('Failed to launch activity');
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold tracking-tight">
          Launch {activity?.data.name}
        </h1>
        <p className="text-muted-foreground mt-2">
          Select a group to start studying
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Launch Settings</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Select Group</label>
            <Select
              value={selectedGroup}
              onValueChange={setSelectedGroup}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select a group" />
              </SelectTrigger>
              <SelectContent>
                {groups?.data.map((group: any) => (
                  <SelectItem key={group.id} value={group.id}>
                    {group.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <Button
            className="w-full"
            size="lg"
            onClick={handleLaunch}
            disabled={!selectedGroup}
          >
            Launch Now
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}