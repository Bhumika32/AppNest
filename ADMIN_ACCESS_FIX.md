# 🔍 Admin Access Troubleshooting Guide

**User:** Bhumika G (bg226104@gmail.com with role_id=2)  
**Database Verification:** ✅ PASSED (script shows admin role correctly configured)

---

## 📋 Issues Reported

1. ❌ Login with admin email → redirected to `/dashboard` instead of `/dashboard/admin`
2. ❌ Manual URL entry `/dashboard/admin` → redirected to `/login`
3. ⚠️ Profile shows "admin" but dashboard acts as user

---

## ✅ Fixes Applied (Feb 23, 2026)

### Frontend Fixes:

- **Role case normalization**: Backend returns `"ADMIN"` (uppercase), frontend now converts to `"admin"` (lowercase) for consistency
- **Auth hydration timing**: Improved store initialization to wait for localStorage restore before calling `checkAuth()`
- **Login redirect timing**: Added proper sync delay after login completes
- **Debug logging**: Added console logs to track role values at each step

### Backend Fixes:

- Verified role relationship in User model
- Confirmed login endpoint returns `role.name` (e.g., "ADMIN")
- Confirmed `/api/auth/me` endpoint returns role correctly

---

## 🧪 Step-by-Step Testing

### Phase 1: Backend Verification

```bash
# 1. In backend terminal, run verification script:
cd F:\AppNest-main\backend
python verify_admin_setup.py
# Expected output: Admin user found with role="ADMIN"

# 2. Test backend auth flow directly:
python test_auth_backend.py
# Expected outputs:
#   - Login status: 200
#   - User role: ADMIN
#   - /me endpoint returns role: ADMIN
#   - Refresh token works
```

### Phase 2: Frontend Test (Clean State)

```bash
# 1. Open browser DevTools → Application → Local Storage
# 2. Clear all storage for localhost:5173
# 3. Stop frontend dev server (Ctrl+C)
# 4. Restart frontend:
cd F:\AppNest-main\frontend
npm run dev

# 5. Open browser console (F12)
# 6. Navigate to http://localhost:5173
# 7. You should see console logs:
#    [AuthStore] No user in localStorage, skipping verification
#    (no api call yet since you're not logged in)
```

### Phase 3: Login Test

```bash
# 1. Click Login link or navigate to /login
# 2. Enter credentials:
#    Email: bg226104@gmail.com
#    Password: [your admin password]
#
# 3. Check browser console for these logs:
#    [AuthStore] User role: admin    ← Key: lowercase 'admin'
#    [Login] Redirecting to: /dashboard/admin
#
# 4. Expected result:
#    ✅ Redirected to /dashboard/admin
#    ✅ Admin dashboard loads (not user dashboard)
#
# 5. If redirected to /dashboard instead:
#    → Check console for role value
#    → Should say "admin" not "ADMIN"
```

### Phase 4: Page Refresh Test

```bash
# 1. On /dashboard/admin page, press F5 to refresh
# 2. Check browser console:
#    [AuthStore] User restored from localStorage, verifying with backend...
#
# 3. Expected result:
#    ✅ Still on /dashboard/admin (not redirected to /login)
#    ✅ Page loads admin content
```

### Phase 5: Manual URL Entry Test

```bash
# 1. In browser address bar, type: http://localhost:5173/dashboard/admin
# 2. Press Enter
# 3. Should load admin dashboard
#    If redirected to /login instead:
#    → Check Application tab → Local Storage
#    → Should have "appnest-auth-storage" key
#    → Parse JSON, check if token and role are present
```

---

## 🔧 Debugging Checklist

- [ ] **Browser console shows `role: admin` (lowercase) not `role: ADMIN`**
  - If showing uppercase: backend is not calling `.toLowerCase()` in frontend
- [ ] **AdminRoute logs** (when accessing /dashboard/admin):
  - `[AdminRoute] User role "admin" is not admin` = WRONG CASE
  - No log = role IS correct, check if isAuthenticated is false

- [ ] **Local storage has token**:
  - Open DevTools → Application → Local Storage
  - Check `appnest-auth-storage` key
  - Should have: `token`, `user`, `isAuthenticated`, `role`

- [ ] **Network requests**:
  - Open DevTools → Network tab
  - Login should POST to `/api/auth/login` (Status: 200)
  - Should NOT see `/api/auth/refresh` requests (unless session expired)
  - `/api/auth/me` should return Status: 200

---

## 💾 Database Double-Check

User record in database:

```
ID: 15
Email: bg226104@gmail.com
Username: BhumikaG
Role ID: 2 (ADMIN)
Is Verified: True
```

Run this query to verify:

```sql
SELECT u.id, u.email, u.username, u.role_id, r.name as role_name, u.is_verified
FROM users u
JOIN roles r ON u.role_id = r.id
WHERE u.email = 'bg226104@gmail.com';
```

Expected result:

```
id=15, email=bg226104@gmail.com, role_id=2, role_name=ADMIN, is_verified=True
```

---

## 📊 Console Log Reference

### Normal Admin Login Flow:

```
✓ Login flow starting...
[AuthStore] User role: admin
[Login] Redirecting to: /dashboard/admin
✓ Page navigates to /dashboard/admin
✓ Admin dashboard content loads
```

### If Admin Sees User Dashboard:

```
[Login] Redirecting to: /dashboard  ← WRONG!
Should show: /dashboard/admin
Check: Is role being set to lowercase?
```

### If /dashboard/admin Redirects to /login:

```
[AdminRoute] User role "user" is not admin
Check: Is role=user instead of admin?
Check: Is token missing from localStorage?
```

---

## 🚨 Known Issues & Solutions

| Symptom                                     | Cause                         | Solution                                                |
| ------------------------------------------- | ----------------------------- | ------------------------------------------------------- |
| Role shows "ADMIN" not "admin"              | Backend returns uppercase     | Frontend should normalize (already fixed)               |
| /me returns role object, not string         | Wrong backend response format | Use `role.name` in auth controller                      |
| Refresh token not working                   | CORS issue or cookie not set  | Check backend CORS config                               |
| Can't access /dashboard/admin after refresh | Token expired                 | Implement refresh token rotation (done via interceptor) |

---

## 📞 If Still Broken

1. **Run tests above** → Capture console logs and network requests
2. **Check browser console** → Screenshot of errors
3. **Check backend logs** → Look for 500/401/4 errors during login
4. **Check Network tab** → Verify `/api/auth/login` response contains `role: "ADMIN"`
5. **Verify database** → Run SQL query above

---

## ✨ Files Changed in This Fix

Frontend:

- `src/store/authStore.js` — Role normalization + improved hydration
- `src/pages/Login.jsx` — Added timing and debug logs
- `src/components/AdminRoute.jsx` — Standard Zustand hook usage
- `src/components/ProtectedRoute.jsx` — Standard Zustand hook usage

Backend:

- `app/models/user.py` — Removed duplicate role relationship
- `app/controllers/auth_controller.py` — Ensures role.name is returned

---
