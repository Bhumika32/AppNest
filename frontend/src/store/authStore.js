import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { AuthService } from '../services/api';

// Base store with persistence
const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null, // Access token strictly in memory
      isAuthenticated: false,
      role: 'user',
      isLoading: false,
      isInitializing: true, // App starts in initializing state
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
            role: (user.role || 'user').toLowerCase(),
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

      /**
       * ── Application Boot Flow ───────────────────────────────────────────
       * 1. POST /auth/refresh (silent refresh via HttpOnly cookie)
       * 2. If success -> store access token -> GET /auth/me
       * 3. Update state
       * 4. Set isInitializing = false
       */
      checkAuth: async () => {
        set({ isInitializing: true });

        try {
          // Step 1: silent refresh
          const refreshResponse = await AuthService.refresh();
          const { access_token } = refreshResponse.data;

          set({
            token: access_token,
            isAuthenticated: true
          });

          // Step 2: fetch profile
          const userResponse = await AuthService.getMe();
          const user = userResponse.data;

          set({
            user,
            role: (user.role || 'user').toLowerCase(),
            isInitializing: false
          });

        } catch (error) {

          set({
            user: null,
            token: null,
            isAuthenticated: false,
            isInitializing: false
          });

        }
      },
      // checkAuth: async () => {
      //   set({ isInitializing: true });
      //   try {
      //     // Step 1: Attempt silent refresh
      //     const refreshResponse = await AuthService.refresh();
      //     const { access_token } = refreshResponse.data;

      //     set({ token: access_token });

      //     // Step 2: Fetch user profile with new access token
      //     const userResponse = await AuthService.getMe();
      //     // const { user } = userResponse.data;
      //     const user = userResponse.data; // Assuming /auth/me returns user directly

      //     set({
      //       user,
      //       isAuthenticated: true,
      //       role: (user.role || 'user').toLowerCase(),
      //       isInitializing: false
      //     });
      //   } catch (error) {
      //     // If refresh fails or me fails -> user is logged out
      //     set({
      //       user: null,
      //       token: null,
      //       isAuthenticated: false,
      //       isInitializing: false
      //     });
      //   }
      // },

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
      // ... rest of the methods remain similar

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
        // We only persist non-sensitive user data if needed for UI shell
        // Tokens and isAuthenticated MUST NOT be persisted
        user: state.user,
        role: state.role
      }),
      onRehydrateStorage: () => (state) => {
        // After hydration, trigger the boot flow (refresh -> me)
        if (state) {
          state.checkAuth();
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
