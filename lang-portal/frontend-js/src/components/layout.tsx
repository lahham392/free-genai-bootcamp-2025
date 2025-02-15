import { Link, useLocation } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import {
  BookOpen,
  LayoutDashboard,
  Settings,
  BookMarked,
  Group,
  History,
  Menu,
} from 'lucide-react';
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from '@/components/ui/sheet';
import { useState } from 'react';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Study Activities', href: '/study-activities', icon: BookOpen },
  { name: 'Words', href: '/words', icon: BookMarked },
  { name: 'Groups', href: '/groups', icon: Group },
  { name: 'Study Sessions', href: '/study-sessions', icon: History },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export default function Layout({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  const location = useLocation();

  return (
    <div className="min-h-screen bg-background">
      <div className="flex h-screen">
        {/* Desktop Sidebar */}
        <div className="hidden md:flex md:w-64 md:flex-col">
          <div className="flex flex-col flex-grow border-r border-border bg-card px-4 py-5">
            <div className="flex items-center h-16 flex-shrink-0 px-4">
              <BookOpen className="h-8 w-8 text-primary" />
              <h1 className="ml-2 text-xl font-bold">Language Portal</h1>
            </div>
            <div className="mt-5 flex-1 flex flex-col">
              <nav className="flex-1 space-y-1">
                {navigation.map((item) => {
                  const isActive = location.pathname === item.href;
                  return (
                    <Link
                      key={item.name}
                      to={item.href}
                      className={cn(
                        'group flex items-center px-4 py-2 text-sm font-medium rounded-md transition-colors',
                        isActive
                          ? 'bg-primary text-primary-foreground'
                          : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                      )}
                    >
                      <item.icon
                        className={cn('mr-3 h-5 w-5 flex-shrink-0')}
                        aria-hidden="true"
                      />
                      {item.name}
                    </Link>
                  );
                })}
              </nav>
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        <Sheet open={open} onOpenChange={setOpen}>
          <SheetTrigger asChild>
            <Button
              variant="ghost"
              className="md:hidden absolute left-4 top-4"
              size="icon"
            >
              <Menu className="h-6 w-6" />
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-64 p-0">
            <SheetHeader className="p-4 border-b">
              <SheetTitle className="flex items-center">
                <BookOpen className="h-6 w-6 text-primary" />
                <span className="ml-2">Language Portal</span>
              </SheetTitle>
            </SheetHeader>
            <nav className="flex-1 space-y-1 p-4">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    onClick={() => setOpen(false)}
                    className={cn(
                      'group flex items-center px-4 py-2 text-sm font-medium rounded-md transition-colors',
                      isActive
                        ? 'bg-primary text-primary-foreground'
                        : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                    )}
                  >
                    <item.icon
                      className={cn('mr-3 h-5 w-5 flex-shrink-0')}
                      aria-hidden="true"
                    />
                    {item.name}
                  </Link>
                );
              })}
            </nav>
          </SheetContent>
        </Sheet>

        {/* Main Content */}
        <div className="flex flex-col flex-1">
          <main className="flex-1 p-4 md:p-8 pt-16 md:pt-8">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
}