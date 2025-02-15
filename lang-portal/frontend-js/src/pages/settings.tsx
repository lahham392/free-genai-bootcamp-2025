import { useTheme } from '@/components/theme-provider';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog';
import { resetHistory, fullReset } from '@/lib/api';
import { toast } from 'sonner';
import { Monitor, Moon, Sun } from 'lucide-react';

export default function Settings() {
  const { theme, setTheme } = useTheme();

  const handleResetHistory = async () => {
    try {
      await resetHistory();
      toast.success('Study history has been reset');
    } catch (error) {
      toast.error('Failed to reset study history');
    }
  };

  const handleFullReset = async () => {
    try {
      await fullReset();
      toast.success('Application has been fully reset');
    } catch (error) {
      toast.error('Failed to reset application');
    }
  };

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold tracking-tight">Settings</h1>

      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Appearance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <label className="text-sm font-medium">Theme</label>
              <Select value={theme} onValueChange={setTheme}>
                <SelectTrigger className="w-[200px]">
                  <SelectValue placeholder="Select theme" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="light">
                    <div className="flex items-center">
                      <Sun className="w-4 h-4 mr-2" />
                      Light
                    </div>
                  </SelectItem>
                  <SelectItem value="dark">
                    <div className="flex items-center">
                      <Moon className="w-4 h-4 mr-2" />
                      Dark
                    </div>
                  </SelectItem>
                  <SelectItem value="system">
                    <div className="flex items-center">
                      <Monitor className="w-4 h-4 mr-2" />
                      System
                    </div>
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Reset Options</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button variant="outline" className="w-full">
                  Reset Study History
                </Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Reset Study History</AlertDialogTitle>
                  <AlertDialogDescription>
                    This will delete all study sessions and word review items. This
                    action cannot be undone.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                  <AlertDialogAction onClick={handleResetHistory}>
                    Continue
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>

            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button variant="destructive" className="w-full">
                  Full Reset
                </Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Full Reset</AlertDialogTitle>
                  <AlertDialogDescription>
                    This will delete all data and reload the seed data. This action
                    cannot be undone.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                  <AlertDialogAction
                    onClick={handleFullReset}
                    className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                  >
                    Reset Everything
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}