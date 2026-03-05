import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { AuthService } from '../services/api';

// Base store with persistence
const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null, // Access token in memory
      isAuthenticated: false,
      role: 'user',
      isLoading: false,
      isInitializing: true,
      error: null,

      setToken: (token) => set({ token, isAuthenticated: !!token }),
      setUser: (user) => set({ user }),

      login: async (email, password) => {
        set({ isLoading: true, error: null });
        try {
          const response = await AuthService.login({ email, password });
          const { user, access_token } = response.data;

          set({
            user,
            token: access_token,
            isAuthenticated: true,
            role: (user.role || 'user').toLowerCase(),  // ✅ Normalize to lowercase
            isLoading: false
          });
          return true;
        } catch (error) {
          set({
            error: error.response?.data?.error || 'Login failed. Please check your credentials.',
            isLoading: false
          });
          return false;
        }
      },

      checkAuth: async () => {
        set({ isInitializing: true });
        try {
          const response = await AuthService.getMe();
          const { user } = response.data;
          set({
            user,
            isAuthenticated: true,
            role: (user.role || 'user').toLowerCase(),  // ✅ Normalize to lowercase
            isInitializing: false
          });
        } catch (error) {
          // If 401, axios interceptor will try refresh. 
          // If that fails too, we land here.
          set({
            user: null,
            token: null,
            isAuthenticated: false,
            isInitializing: false
          });
        }
      },

      logout: async () => {
        try {
          await AuthService.logout();
        } catch (e) {
          console.error("Logout failed", e);
        } finally {
          set({
            user: null,
            token: null,
            isAuthenticated: false,
            role: 'user',
            error: null
          });
        }
      },

      register: async (username, email, password) => {
        set({ isLoading: true, error: null });
        try {
          await AuthService.register({ username, email, password });
          set({ isLoading: false });
          return true;
        } catch (error) {
          set({
            error: error.response?.data?.error || 'Registration failed.',
            isLoading: false
          });
          return false;
        }
      },

      verifyOtp: async (email, otp) => {
        set({ isLoading: true, error: null });
        try {
          await AuthService.verifyOtp({ email, otp });
          set({ isLoading: false });
          return true;
        } catch (error) {
          set({
            error: error.response?.data?.error || 'Invalid or expired OTP.',
            isLoading: false
          });
          return false;
        }
      },

      resendOtp: async (email) => {
        try {
          await AuthService.resendOtp(email);
          return true;
        } catch (error) {
          set({ error: error.response?.data?.error || 'Failed to resend OTP.' });
          return false;
        }
      },

      forgotPassword: async (email) => {
        set({ isLoading: true, error: null });
        try {
          await AuthService.forgotPassword(email);
          set({ isLoading: false });
          return true;
        } catch (error) {
          set({
            error: error.response?.data?.error || 'Failed to request reset.',
            isLoading: false
          });
          return false;
        }
      },

      resetPassword: async (email, otp, newPassword) => {
        set({ isLoading: true, error: null });
        try {
          await AuthService.resetPassword({ email, otp, newPassword });
          set({ isLoading: false });
          return true;
        } catch (error) {
          set({
            error: error.response?.data?.error || 'Failed to reset password.',
            isLoading: false
          });
          return false;
        }
      },

      clearError: () => set({ error: null })
    }),
    {
      name: 'appnest-auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
        role: state.role
      }),
      onRehydrateStorage: () => (state) => {
        // This runs after Zustand has hydrated data from localStorage
        if (state && state.token) {
          console.log('[AuthStore] Hydrated from localStorage. Verifying backend...');
          setTimeout(() => state.checkAuth(), 0);
        } else if (state) {
          console.log('[AuthStore] No token found in localStorage.');
          state.isInitializing = false;
        }
      }
    }
  )
);

/**
 * ✅ EXPORT: useAuthStore
 * Standard Zustand hook. Can be used:
 * - In components: const { user } = useAuthStore()
 * - Direct state: useAuthStore.getState()
 * - Subscriptions: useAuthStore.subscribe()
 */
export { useAuthStore };
