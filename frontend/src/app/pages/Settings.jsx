import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  User,
  Lock,
  Bell,
  Eye,
  Zap,
  Shield,
  LogOut,
  ChevronRight,
  ToggleLeft,
  Mail,
  Smartphone,
  Globe,
  Save,
  X,
} from 'lucide-react';
import { motion } from 'framer-motion';
import { useAuthStore } from '../../store/authStore';
import { UserService } from '../../api/api';

const Settings = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  const [activeTab, setActiveTab] = useState('account');
  const [loading, setLoading] = useState(false);
  const [saveStatus, setSaveStatus] = useState(null);

  // Account Settings
  const [profileForm, setProfileForm] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    bio: user?.bio || '',
    avatar_url: user?.avatar_url || '',
  });

  // Notification Preferences
  const [notificationPrefs, setNotificationPrefs] = useState({
    emailNotifications: true,
    gameNotifications: true,
    achievementNotifications: true,
    socialNotifications: false,
    systemNotifications: true,
    dailyDigest: true,
    newsletter: false,
  });

  // Privacy Settings
  const [privacySettings, setPrivacySettings] = useState({
    profilePublic: true,
    showOnLeaderboard: true,
    allowMessages: true,
    allowFriendRequests: true,
  });

  // Display Settings
  const [displaySettings, setDisplaySettings] = useState({
    darkMode: true,
    animationsEnabled: true,
    soundEffects: true,
    reducedMotion: false,
    fontSize: 'medium', // small, medium, large
  });

  const handleProfileChange = (e) => {
    const { name, value } = e.target;
    setProfileForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSaveProfile = async () => {
    try {
      setLoading(true);
      await UserService.updateProfile(profileForm);
      setSaveStatus('Profile updated successfully!');
      setTimeout(() => setSaveStatus(null), 3000);
    } catch (error) {
      console.error('Failed to update profile:', error);
      setSaveStatus('Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handleNotificationChange = (key) => {
    setNotificationPrefs((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
    // TODO: Save to backend
  };

  const handlePrivacyChange = (key) => {
    setPrivacySettings((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
    // TODO: Save to backend
  };

  const handleDisplayChange = (key, value) => {
    setDisplaySettings((prev) => ({
      ...prev,
      [key]: value,
    }));
    // TODO: Save to backend
  };

  const handleLogout = () => {
    if (window.confirm('Are you sure you want to logout?')) {
      logout();
      navigate('/login');
    }
  };

  const tabConfig = [
    { id: 'account', label: 'Account', icon: User },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'privacy', label: 'Privacy', icon: Shield },
    { id: 'display', label: 'Display', icon: Eye },
    { id: 'security', label: 'Security', icon: Lock },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white">
      {/* Header */}
      <div className="sticky top-0 z-40 border-b border-slate-700 bg-slate-900 bg-opacity-95 backdrop-blur-lg">
        <div className="max-w-6xl mx-auto px-6 py-6">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="p-2 hover:bg-slate-700 rounded-lg transition-colors"
            >
              <ArrowLeft className="w-6 h-6" />
            </button>
            <h1 className="text-3xl font-black">
              Settings <span className="text-neon-blue">⚙️</span>
            </h1>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-10">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar Navigation */}
          <div className="lg:col-span-1">
            <div className="bg-slate-800 bg-opacity-50 border border-slate-700 rounded-xl overflow-hidden sticky top-24">
              {tabConfig.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full px-6 py-4 flex items-center gap-3 transition-all border-l-4 ${activeTab === tab.id
                        ? 'bg-neon-blue bg-opacity-20 border-neon-blue text-neon-blue'
                        : 'bg-transparent border-transparent text-slate-400 hover:bg-slate-700 hover:bg-opacity-30'
                      }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-semibold">{tab.label}</span>
                    {activeTab === tab.id && <ChevronRight className="w-4 h-4 ml-auto" />}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              className="space-y-6"
            >
              {/* Account Settings */}
              {activeTab === 'account' && (
                <div className="space-y-6">
                  <div className="bg-slate-800 bg-opacity-50 border border-slate-700 rounded-xl p-8">
                    <h2 className="text-2xl font-bold mb-6">Account Information</h2>

                    {saveStatus && (
                      <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mb-6 p-4 bg-neon-green bg-opacity-10 border border-neon-green text-neon-green rounded-lg flex items-center justify-between"
                      >
                        <span>{saveStatus}</span>
                        <X className="w-4 h-4 cursor-pointer" onClick={() => setSaveStatus(null)} />
                      </motion.div>
                    )}

                    <div className="space-y-6">
                      {/* Username (Read-only) */}
                      <div>
                        <label className="block text-sm font-semibold mb-2 text-slate-300">
                          Username
                        </label>
                        <input
                          type="text"
                          value={user?.username || ''}
                          disabled
                          className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-400 cursor-not-allowed"
                        />
                        <p className="text-xs text-slate-500 mt-1">Username cannot be changed</p>
                      </div>

                      {/* Email (Read-only) */}
                      <div>
                        <label className="block text-sm font-semibold mb-2 text-slate-300 flex items-center gap-2">
                          <Mail className="w-4 h-4" /> Email
                        </label>
                        <input
                          type="email"
                          value={user?.email || ''}
                          disabled
                          className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-400 cursor-not-allowed"
                        />
                        <p className="text-xs text-slate-500 mt-1">Email cannot be changed here</p>
                      </div>

                      {/* First Name */}
                      <div>
                        <label className="block text-sm font-semibold mb-2">First Name</label>
                        <input
                          type="text"
                          name="first_name"
                          value={profileForm.first_name}
                          onChange={handleProfileChange}
                          placeholder="Your first name"
                          className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:border-neon-blue focus:ring-1 focus:ring-neon-blue outline-none transition-all"
                        />
                      </div>

                      {/* Last Name */}
                      <div>
                        <label className="block text-sm font-semibold mb-2">Last Name</label>
                        <input
                          type="text"
                          name="last_name"
                          value={profileForm.last_name}
                          onChange={handleProfileChange}
                          placeholder="Your last name"
                          className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:border-neon-blue focus:ring-1 focus:ring-neon-blue outline-none transition-all"
                        />
                      </div>

                      {/* Bio */}
                      <div>
                        <label className="block text-sm font-semibold mb-2">Bio</label>
                        <textarea
                          name="bio"
                          value={profileForm.bio}
                          onChange={handleProfileChange}
                          placeholder="Tell us about yourself..."
                          maxLength={200}
                          rows={4}
                          className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:border-neon-blue focus:ring-1 focus:ring-neon-blue outline-none transition-all resize-none"
                        />
                        <p className="text-xs text-slate-500 mt-1">
                          {profileForm.bio.length}/200 characters
                        </p>
                      </div>

                      {/* Save Button */}
                      <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={handleSaveProfile}
                        disabled={loading}
                        className="w-full px-6 py-3 bg-gradient-to-r from-neon-blue to-neon-purple text-white font-bold rounded-lg hover:shadow-lg transition-all disabled:opacity-50 flex items-center justify-center gap-2"
                      >
                        <Save className="w-5 h-5" />
                        {loading ? 'Saving...' : 'Save Changes'}
                      </motion.button>
                    </div>
                  </div>
                </div>
              )}

              {/* Notification Preferences */}
              {activeTab === 'notifications' && (
                <div className="space-y-4">
                  <div className="bg-slate-800 bg-opacity-50 border border-slate-700 rounded-xl p-8">
                    <h2 className="text-2xl font-bold mb-6">Notification Preferences</h2>

                    <div className="space-y-4">
                      {[
                        { key: 'emailNotifications', label: 'Email Notifications', desc: 'Receive updates via email' },
                        { key: 'gameNotifications', label: 'Game Notifications', desc: 'Alerts for game results' },
                        { key: 'achievementNotifications', label: 'Achievement Notifications', desc: 'Celebrate your wins' },
                        { key: 'socialNotifications', label: 'Social Notifications', desc: 'Friend requests & mentions' },
                        { key: 'systemNotifications', label: 'System Notifications', desc: 'Important updates & maintenance' },
                        { key: 'dailyDigest', label: 'Daily Digest', desc: 'Summary of your activities' },
                        { key: 'newsletter', label: 'Newsletter', desc: 'Weekly news and tips' },
                      ].map((item) => (
                        <div
                          key={item.key}
                          className="flex items-center justify-between p-4 bg-slate-700 bg-opacity-30 rounded-lg hover:bg-opacity-50 transition-all"
                        >
                          <div>
                            <p className="font-semibold">{item.label}</p>
                            <p className="text-sm text-slate-400">{item.desc}</p>
                          </div>
                          <button
                            onClick={() => handleNotificationChange(item.key)}
                            className={`relative inline-flex h-8 w-14 items-center rounded-full transition-all ${notificationPrefs[item.key] ? 'bg-neon-green' : 'bg-slate-600'
                              }`}
                          >
                            <span
                              className={`inline-block h-6 w-6 transform rounded-full bg-white transition-transform ${notificationPrefs[item.key] ? 'translate-x-7' : 'translate-x-1'
                                }`}
                            />
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Privacy Settings */}
              {activeTab === 'privacy' && (
                <div className="space-y-4">
                  <div className="bg-slate-800 bg-opacity-50 border border-slate-700 rounded-xl p-8">
                    <h2 className="text-2xl font-bold mb-6">Privacy Settings</h2>

                    <div className="space-y-4">
                      {[
                        { key: 'profilePublic', label: 'Public Profile', desc: 'Allow others to view your profile' },
                        { key: 'showOnLeaderboard', label: 'Show on Leaderboard', desc: 'Display your ranking publicly' },
                        { key: 'allowMessages', label: 'Allow Messages', desc: 'Let users send you messages' },
                        { key: 'allowFriendRequests', label: 'Allow Friend Requests', desc: 'Let users add you as friend' },
                      ].map((item) => (
                        <div
                          key={item.key}
                          className="flex items-center justify-between p-4 bg-slate-700 bg-opacity-30 rounded-lg hover:bg-opacity-50 transition-all"
                        >
                          <div>
                            <p className="font-semibold">{item.label}</p>
                            <p className="text-sm text-slate-400">{item.desc}</p>
                          </div>
                          <button
                            onClick={() => handlePrivacyChange(item.key)}
                            className={`relative inline-flex h-8 w-14 items-center rounded-full transition-all ${privacySettings[item.key] ? 'bg-neon-blue' : 'bg-slate-600'
                              }`}
                          >
                            <span
                              className={`inline-block h-6 w-6 transform rounded-full bg-white transition-transform ${privacySettings[item.key] ? 'translate-x-7' : 'translate-x-1'
                                }`}
                            />
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Display Settings */}
              {activeTab === 'display' && (
                <div className="space-y-4">
                  <div className="bg-slate-800 bg-opacity-50 border border-slate-700 rounded-xl p-8">
                    <h2 className="text-2xl font-bold mb-6">Display Preferences</h2>

                    <div className="space-y-4">
                      {[
                        { key: 'darkMode', label: 'Dark Mode', desc: 'Use dark theme' },
                        { key: 'animationsEnabled', label: 'Animations', desc: 'Enable smooth animations' },
                        { key: 'soundEffects', label: 'Sound Effects', desc: 'Play UI sounds' },
                        { key: 'reducedMotion', label: 'Reduced Motion', desc: 'Minimize animations for accessibility' },
                      ].map((item) => (
                        <div
                          key={item.key}
                          className="flex items-center justify-between p-4 bg-slate-700 bg-opacity-30 rounded-lg hover:bg-opacity-50 transition-all"
                        >
                          <div>
                            <p className="font-semibold">{item.label}</p>
                            <p className="text-sm text-slate-400">{item.desc}</p>
                          </div>
                          <button
                            onClick={() => handleDisplayChange(item.key, !displaySettings[item.key])}
                            className={`relative inline-flex h-8 w-14 items-center rounded-full transition-all ${displaySettings[item.key] ? 'bg-neon-green' : 'bg-slate-600'
                              }`}
                          >
                            <span
                              className={`inline-block h-6 w-6 transform rounded-full bg-white transition-transform ${displaySettings[item.key] ? 'translate-x-7' : 'translate-x-1'
                                }`}
                            />
                          </button>
                        </div>
                      ))}

                      {/* Font Size */}
                      <div className="p-4 bg-slate-700 bg-opacity-30 rounded-lg">
                        <p className="font-semibold mb-3">Font Size</p>
                        <div className="flex gap-2">
                          {['small', 'medium', 'large'].map((size) => (
                            <button
                              key={size}
                              onClick={() => handleDisplayChange('fontSize', size)}
                              className={`px-4 py-2 rounded-lg font-semibold transition-all ${displaySettings.fontSize === size
                                  ? 'bg-neon-blue text-black'
                                  : 'bg-slate-600 text-white hover:bg-slate-500'
                                }`}
                            >
                              {size.charAt(0).toUpperCase() + size.slice(1)}
                            </button>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Security Settings */}
              {activeTab === 'security' && (
                <div className="space-y-6">
                  <div className="bg-slate-800 bg-opacity-50 border border-slate-700 rounded-xl p-8">
                    <h2 className="text-2xl font-bold mb-6">Security & Account</h2>

                    <div className="space-y-4">
                      <button className="w-full px-6 py-4 border-2 border-neon-blue text-neon-blue rounded-lg hover:bg-neon-blue hover:text-black font-semibold transition-all flex items-center gap-3">
                        <Lock className="w-5 h-5" />
                        Change Password
                      </button>

                      <button className="w-full px-6 py-4 border-2 border-neon-purple text-neon-purple rounded-lg hover:bg-neon-purple hover:text-black font-semibold transition-all flex items-center gap-3">
                        <Shield className="w-5 h-5" />
                        Two-Factor Authentication
                      </button>

                      <button className="w-full px-6 py-4 border-2 border-red-500 text-red-400 rounded-lg hover:bg-red-500 hover:text-white font-semibold transition-all flex items-center gap-3">
                        <LogOut className="w-5 h-5" />
                        Logout All Devices
                      </button>
                    </div>
                  </div>

                  <div className="bg-slate-800 bg-opacity-50 border border-slate-700 rounded-xl p-8">
                    <h2 className="text-lg font-bold mb-4 text-red-400">Danger Zone</h2>
                    <button
                      onClick={handleLogout}
                      className="w-full px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-bold rounded-lg transition-all flex items-center justify-center gap-2"
                    >
                      <LogOut className="w-5 h-5" />
                      Logout
                    </button>
                  </div>
                </div>
              )}
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
