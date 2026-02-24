import React, { useState, useEffect } from 'react';
import { X, Check, CheckCheck, Trash2, Bell, AlertCircle, Trophy, Zap, MessageCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import notificationsApi from '../../api/notificationsApi';

const NotificationCenter = ({ isOpen, onClose }) => {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [filterType, setFilterType] = useState('all'); // all, unread, achievement, game, credit, system, social

  const getIconForType = (type) => {
    const iconMap = {
      achievement: Trophy,
      game: Bell,
      credit: Zap,
      system: AlertCircle,
      social: MessageCircle,
      alert: AlertCircle,
      info: Bell,
    };
    return iconMap[type] || Bell;
  };

  const getColorForType = (type) => {
    const colorMap = {
      achievement: 'text-neon-pink',
      game: 'text-neon-blue',
      credit: 'text-neon-green',
      system: 'text-neon-yellow',
      social: 'text-neon-purple',
      alert: 'text-red-400',
      info: 'text-slate-300',
    };
    return colorMap[type] || 'text-slate-300';
  };

  const getBgColorForType = (type) => {
    const bgMap = {
      achievement: 'bg-neon-pink bg-opacity-10',
      game: 'bg-neon-blue bg-opacity-10',
      credit: 'bg-neon-green bg-opacity-10',
      system: 'bg-neon-yellow bg-opacity-10',
      social: 'bg-neon-purple bg-opacity-10',
      alert: 'bg-red-400 bg-opacity-10',
      info: 'bg-slate-600 bg-opacity-10',
    };
    return bgMap[type] || 'bg-slate-600 bg-opacity-10';
  };

  useEffect(() => {
    if (isOpen) {
      fetchNotifications();
    }
  }, [isOpen]);

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      const response = await notificationsApi.getNotifications(100, filterType === 'unread');
      setNotifications(response.data.notifications || []);
      setUnreadCount(response.data.unread_count || 0);
    } catch (error) {
      console.error('Failed to fetch notifications:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleMarkAsRead = async (notifId, e) => {
    e.stopPropagation();
    try {
      await notificationsApi.markAsRead(notifId);
      setNotifications(notifications.map(n => 
        n.id === notifId ? { ...n, read: true } : n
      ));
      setUnreadCount(Math.max(0, unreadCount - 1));
    } catch (error) {
      console.error('Failed to mark notification as read:', error);
    }
  };

  const handleMarkAllAsRead = async () => {
    try {
      await notificationsApi.markAllAsRead();
      setNotifications(notifications.map(n => ({ ...n, read: true })));
      setUnreadCount(0);
    } catch (error) {
      console.error('Failed to mark all as read:', error);
    }
  };

  const handleDelete = async (notifId, e) => {
    e.stopPropagation();
    try {
      await notificationsApi.deleteNotification(notifId);
      setNotifications(notifications.filter(n => n.id !== notifId));
    } catch (error) {
      console.error('Failed to delete notification:', error);
    }
  };

  const handleClearAll = async () => {
    if (window.confirm('Clear all notifications?')) {
      try {
        await notificationsApi.clearAll();
        setNotifications([]);
        setUnreadCount(0);
      } catch (error) {
        console.error('Failed to clear notifications:', error);
      }
    }
  };

  const filteredNotifications = filterType === 'all' 
    ? notifications 
    : filterType === 'unread'
    ? notifications.filter(n => !n.read)
    : notifications.filter(n => n.type === filterType);

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 bg-black bg-opacity-50 backdrop-blur-sm"
        onClick={onClose}
      >
        <motion.div
          initial={{ x: 500, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: 500, opacity: 0 }}
          transition={{ type: 'spring', damping: 30 }}
          className="fixed right-0 top-0 h-screen w-full max-w-md bg-gradient-to-br from-slate-900 to-slate-800 border-l border-neon-blue border-opacity-20 shadow-2xl"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="sticky top-0 z-40 border-b border-slate-700 bg-slate-900 bg-opacity-95 backdropblur-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <Bell className="w-6 h-6 text-neon-blue" />
                <h2 className="text-2xl font-black text-white">Notifications</h2>
                {unreadCount > 0 && (
                  <motion.span
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="ml-2 px-3 py-1 bg-neon-pink text-white text-sm font-bold rounded-full"
                  >
                    {unreadCount}
                  </motion.span>
                )}
              </div>
              <button
                onClick={onClose}
                className="p-2 hover:bg-slate-700 rounded-lg transition-colors"
              >
                <X className="w-5 h-5 text-slate-300" />
              </button>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-2">
              {unreadCount > 0 && (
                <button
                  onClick={handleMarkAllAsRead}
                  className="flex items-center gap-2 px-3 py-2 text-sm bg-neon-blue bg-opacity-20 hover:bg-opacity-30 text-neon-blue rounded-lg transition-colors"
                >
                  <CheckCheck className="w-4 h-4" />
                  Mark all read
                </button>
              )}
              {notifications.length > 0 && (
                <button
                  onClick={handleClearAll}
                  className="flex items-center gap-2 px-3 py-2 text-sm bg-red-900 bg-opacity-20 hover:bg-opacity-30 text-red-400 rounded-lg transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                  Clear
                </button>
              )}
            </div>

            {/* Filter Tabs */}
            <div className="flex gap-2 mt-4 overflow-x-auto pb-2">
              {['all', 'unread', 'achievement', 'game', 'credit', 'system'].map((type) => (
                <button
                  key={type}
                  onClick={() => setFilterType(type)}
                  className={`px-4 py-2 rounded-full whitespace-nowrap text-sm font-semibold transition-all ${
                    filterType === type
                      ? 'bg-neon-blue text-black'
                      : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                  }`}
                >
                  {type.charAt(0).toUpperCase() + type.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Notifications List */}
          <div className="overflow-y-auto h-[calc(100vh-200px)]">
            {loading ? (
              <div className="flex items-center justify-center h-40">
                <div className="w-8 h-8 border-4 border-neon-blue border-t-transparent rounded-full animate-spin" />
              </div>
            ) : filteredNotifications.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-40 text-slate-400">
                <Bell className="w-12 h-12 mb-3 opacity-50" />
                <p>
                  {filterType === 'unread' ? 'All caught up!' : 'No notifications yet'}
                </p>
              </div>
            ) : (
              <div className="divide-y divide-slate-700">
                <AnimatePresence>
                  {filteredNotifications.map((notification, index) => {
                    const IconComponent = getIconForType(notification.type);
                    return (
                      <motion.div
                        key={notification.id}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        transition={{ delay: index * 0.05 }}
                        className={`p-4 cursor-pointer transition-all hover:bg-slate-700 hover:bg-opacity-50 ${
                          !notification.read ? 'bg-slate-800 bg-opacity-50 border-l-4 border-neon-blue' : ''
                        }`}
                      >
                        <div className="flex gap-3">
                          {/* Icon */}
                          <div className={`flex-shrink-0 mt-1 p-2 rounded-lg ${getBgColorForType(notification.type)}`}>
                            <IconComponent className={`w-5 h-5 ${getColorForType(notification.type)}`} />
                          </div>

                          {/* Content */}
                          <div className="flex-1 min-w-0">
                            <h3 className="font-semibold text-white line-clamp-1">
                              {notification.title}
                            </h3>
                            <p className="text-sm text-slate-400 line-clamp-2 mt-1">
                              {notification.message}
                            </p>
                            <span className="text-xs text-slate-500 mt-2 inline-block">
                              {formatDate(notification.created_at)}
                            </span>
                          </div>

                          {/* Actions */}
                          <div className="flex-shrink-0 flex gap-1 opacity-0 hover:opacity-100 transition-opacity">
                            {!notification.read && (
                              <button
                                onClick={(e) => handleMarkAsRead(notification.id, e)}
                                className="p-1.5 hover:bg-slate-600 rounded-lg transition-colors"
                                title="Mark as read"
                              >
                                <Check className="w-4 h-4 text-neon-green" />
                              </button>
                            )}
                            <button
                              onClick={(e) => handleDelete(notification.id, e)}
                              className="p-1.5 hover:bg-slate-600 rounded-lg transition-colors"
                              title="Delete"
                            >
                              <Trash2 className="w-4 h-4 text-red-400" />
                            </button>
                          </div>
                        </div>
                      </motion.div>
                    );
                  })}
                </AnimatePresence>
              </div>
            )}
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default NotificationCenter;
