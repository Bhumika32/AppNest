import {
    Home, User, Gamepad2, Wrench, Flame, Trophy, Target, MessageSquare,
    Settings, Moon, LogOut, LayoutDashboard, Users, BarChart3, ShieldAlert, Activity
} from 'lucide-react';

export const USER_REALMS = [
    { id: 'home', label: 'Home Portal', icon: Home, path: '/dashboard' },
    { id: 'profile', label: 'Profile Realm', icon: User, path: '/dashboard/profile' },
    { id: 'games', label: 'Game Realm', icon: Gamepad2, path: '/dashboard/games' },
    { id: 'tools', label: 'Tool Realm', icon: Wrench, path: '/dashboard/tools' },
    { id: 'roast', label: 'Roast Realm', icon: Flame, path: '/dashboard/roast' },
    { id: 'leaderboards', label: 'Leaderboards', icon: Trophy, path: '/dashboard/leaderboard' },
    { id: 'achievements', label: 'Achievements', icon: Target, path: '/dashboard/achievements' },
    { id: 'social', label: 'Social Hub', icon: MessageSquare, path: '/dashboard/social' },
];

export const ADMIN_REALMS = [
    { id: 'admin-overview', label: 'Overview', icon: LayoutDashboard, path: '/dashboard/admin' },
    { id: 'admin-users', label: 'Users', icon: Users, path: '/dashboard/admin/users' },
    { id: 'admin-games', label: 'Game Analytics', icon: Gamepad2, path: '/dashboard/admin/games' },
    { id: 'admin-tools', label: 'Tool Analytics', icon: Wrench, path: '/dashboard/admin/tools' },
    { id: 'admin-roast', label: 'Roast Moderation', icon: ShieldAlert, path: '/dashboard/admin/roast' },
    { id: 'admin-platform', label: 'Platform Analytics', icon: BarChart3, path: '/dashboard/admin/analytics' },
    { id: 'admin-settings', label: 'System Settings', icon: Settings, path: '/dashboard/admin/settings' },
];
