#!/bin/bash

# Manual Testing Guide for Auth & Admin Fixes

# Run these tests to verify the critical fixes work

echo "🧪 AppNest Auth & Admin Testing Suite"
echo "======================================"
echo ""

# Colors

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Test 1: Auth Persistence on Page Refresh${NC}"
echo "─────────────────────────────────────────"
echo "1. Start the frontend dev server: npm run dev"
echo "2. Go to http://localhost:5173"
echo "3. Login with test user"
echo "4. Press F5 to refresh the page"
echo "5. Check:"
echo " ✓ Should STAY logged in (not redirected to /login)"
echo " ✓ Check browser console for auth state"
echo " ✓ localStorage should still have 'appnest-auth-storage'"
echo ""

echo -e "${YELLOW}Test 2: Admin User Access${NC}"
echo "──────────────────────────"
echo "Prerequisites:"
echo "1. Create admin user in backend DB:"
echo " - Email: admin@appnest.com"
echo " - Password: AdminPass123"
echo " - Role: Set to role_id=2 (admin role)"
echo ""
echo "2. Start backend: python run.py"
echo "3. Start frontend: npm run dev"
echo "4. Login with admin@appnest.com"
echo "5. Navigate to /dashboard/admin"
echo "6. Check:"
echo " ✓ Should load AdminOverview page (not redirect to /dashboard)"
echo " ✓ Check browser console for role='admin'"
echo " ✓ Sidebar should show admin menu items"
echo ""

echo -e "${YELLOW}Test 3: Regular User Blocked from Admin${NC}"
echo "────────────────────────────────────────"
echo "1. Login with regular user account"
echo "2. Try to navigate to /dashboard/admin"
echo "3. Check:"
echo " ✓ Should redirect back to /dashboard"
echo " ✓ Console should log: [AdminRoute] User role \"user\" is not admin"
echo ""

echo -e "${YELLOW}Test 4: Logout Clears Auth${NC}"
echo "───────────────────────────"
echo "1. Login with any user"
echo "2. Click logout"
echo "3. Check:"
echo " ✓ Should redirect to /login"
echo " ✓ localStorage auth key should be cleared"
echo " ✓ Try to access /dashboard → should redirect to /login"
echo ""

echo -e "${GREEN}Expected Changes in Code:${NC}"
echo "─────────────────────────────"
echo "Backend:"
echo " • backend/app/models/user.py: Added role relationship"
echo " • backend/app/controllers/auth_controller.py: Fixed role return"
echo ""
echo "Frontend:"
echo " • frontend/src/store/authStore.js: Hydration on store init"
echo " • frontend/src/app/AppRouter.jsx: Removed duplicate effect"
echo " • frontend/src/components/AdminRoute.jsx: Fixed role check + logging"
echo " • frontend/src/components/ProtectedRoute.jsx: Fixed role check + logging"
echo ""

echo -e "${YELLOW}Troubleshooting:${NC}"
echo "───────────────"
echo "• If still redirected to login after refresh:"
echo " → Check browser console for errors"
echo " → Check localStorage for auth data"
echo " → Verify backend /api/auth/me returns role"
echo ""
echo "• If admin can't access /dashboard/admin:"
echo " → Check console logs for [AdminRoute] messages"
echo " → Verify DB has user.role_id = 2 (admin)"
echo " → Login response should include 'role': 'admin'"
echo ""
echo "• Check backend logs:"
echo " → python run.py should show requests to GET /api/auth/me"
echo " → Response should include 'role': 'admin'"
echo ""
