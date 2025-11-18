# ThemeContext Usage Locations

## Overview

The `ThemeContext` is used throughout the React admin panel to manage dark/light mode. Here's where it appears:

---

## 1. **ThemeProvider Setup** (Root Level)

**File:** `frontend/src/main.jsx`

```jsx
import { ThemeProvider } from './contexts/ThemeContext'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ThemeProvider>  {/* ← Wraps entire app */}
      <App />
    </ThemeProvider>
  </React.StrictMode>,
)
```

**What it does:**
- Wraps the entire React application
- Makes theme context available to all components
- Initializes theme from localStorage or defaults to 'light'

---

## 2. **Theme Toggle Button** (Visible in UI)

**File:** `frontend/src/components/admin/AdminLayout.jsx`

**Location in UI:** Top-right header of admin panel

```jsx
import { useTheme } from '../../contexts/ThemeContext';

const AdminLayout = ({ children }) => {
  const { theme, toggleTheme, isDark } = useTheme();  // ← Uses theme context
  
  return (
    <header className="admin-header">
      <nav className="main-nav">
        <span className="greeting">{getGreeting()}!</span>
        <button 
          className="theme-toggle"  // ← THIS IS THE BUTTON YOU SEE
          onClick={toggleTheme}
          title={`Switch to ${isDark ? 'light' : 'dark'} mode`}
        >
          {isDark ? '☀️' : '🌙'}  // ← Shows moon in light mode, sun in dark mode
        </button>
        <Link to="/">Home</Link>
        <Link to="/product/">Shop</Link>
        <button onClick={handleLogout} className="logout-btn">
          Logout
        </button>
      </nav>
    </header>
  );
};
```

**Visual Location:**
```
┌─────────────────────────────────────────────────────────┐
│ ☰ Baabuu Clothing    [Good Morning!] [🌙] Home Shop [Logout] │
└─────────────────────────────────────────────────────────┘
                              ↑
                        Theme Toggle Button
                        (Visible here!)
```

---

## 3. **CSS Variables Applied** (Behind the Scenes)

**File:** `frontend/src/index.css`

The theme context sets `data-theme` attribute on `<html>` element:

```css
/* Light Theme */
:root {
  --bg-primary: #ffffff;
  --text-primary: #1a202c;
  /* ... */
}

/* Dark Theme */
[data-theme="dark"] {
  --bg-primary: #1a202c;
  --text-primary: #f7fafc;
  /* ... */
}
```

**How it works:**
1. `ThemeContext` sets `document.documentElement.setAttribute('data-theme', theme)`
2. CSS variables automatically switch based on `[data-theme="dark"]` attribute
3. All components using CSS variables update automatically

---

## 4. **Where to See It**

### In the Browser:

1. **Go to React Admin Panel:**
   ```
   http://localhost:5173/admin/
   ```

2. **Look at the top-right of the header:**
   - You'll see: `[Good Morning!] [🌙] Home Shop [Logout]`
   - The **🌙** (or **☀️**) button is the theme toggle

3. **Click the button:**
   - Clicking **🌙** switches to dark mode
   - Clicking **☀️** switches to light mode
   - The entire admin panel changes color instantly

---

## 5. **Files Using ThemeContext**

| File | Usage |
|------|-------|
| `main.jsx` | Wraps app with `ThemeProvider` |
| `AdminLayout.jsx` | Uses `useTheme()` hook, displays toggle button |
| `index.css` | CSS variables respond to `data-theme` attribute |
| `Dashboard.css` | Uses CSS variables for theming |
| `AdvancedProductList.css` | Uses CSS variables for theming |
| All admin component CSS | Uses CSS variables for theming |

---

## 6. **How to Access Theme in Other Components**

If you want to use the theme in any other component:

```jsx
import { useTheme } from '../../contexts/ThemeContext';

const MyComponent = () => {
  const { theme, toggleTheme, isDark, isLight } = useTheme();
  
  return (
    <div>
      <p>Current theme: {theme}</p>
      <p>Is dark mode: {isDark ? 'Yes' : 'No'}</p>
      <button onClick={toggleTheme}>Toggle Theme</button>
    </div>
  );
};
```

---

## 7. **Visual Flow**

```
User clicks 🌙 button
        ↓
AdminLayout.jsx: toggleTheme() called
        ↓
ThemeContext.jsx: setTheme() updates state
        ↓
ThemeContext.jsx: useEffect sets data-theme="dark" on <html>
        ↓
index.css: [data-theme="dark"] CSS variables activate
        ↓
All components: Colors update via CSS variables
        ↓
localStorage: Theme saved for next visit
```

---

## Summary

**Where ThemeContext Shows:**
- ✅ **Visible:** Theme toggle button (🌙/☀️) in admin header
- ✅ **Functional:** All admin components respond to theme changes
- ✅ **Persistent:** Theme saved in localStorage
- ✅ **Automatic:** CSS variables update all colors instantly

**To see it:**
1. Go to `http://localhost:5173/admin/`
2. Look at the top-right header
3. Click the 🌙/☀️ button
4. Watch the entire admin panel change colors!

---

**Copyright (c) 2024 Baabuu Clothing**  
**Licensed under MIT License**

