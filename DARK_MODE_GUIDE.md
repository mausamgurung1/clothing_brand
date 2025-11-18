# Dark Mode / Light Mode Guide - Baabuu Clothing

## Overview

The React Admin Panel now supports **dynamic dark mode and light mode** switching. The theme preference is saved in localStorage and persists across sessions.

---

## Features

✅ **Theme Toggle Button** - Located in the admin header (🌙/☀️ icon)  
✅ **Automatic Persistence** - Theme preference saved in localStorage  
✅ **Smooth Transitions** - All color changes animate smoothly  
✅ **CSS Variables** - Dynamic theming using CSS custom properties  
✅ **Global Application** - Works across all admin components  

---

## How to Use

### Toggle Theme

1. **In Admin Panel Header:**
   - Look for the theme toggle button (🌙 for light mode, ☀️ for dark mode)
   - Click the button to switch between themes
   - The change applies instantly across all components

2. **Theme Persistence:**
   - Your theme preference is automatically saved
   - When you reload the page, your selected theme is restored
   - No need to toggle again

---

## Technical Implementation

### Theme Context

The theme is managed through React Context (`ThemeContext`):

```javascript
import { useTheme } from '../../contexts/ThemeContext';

const { theme, toggleTheme, isDark, isLight } = useTheme();
```

### CSS Variables

All colors use CSS variables that change based on theme:

```css
/* Light Theme */
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f5f7fa;
  --text-primary: #1a202c;
  --text-secondary: #4a5568;
  /* ... */
}

/* Dark Theme */
[data-theme="dark"] {
  --bg-primary: #1a202c;
  --bg-secondary: #2d3748;
  --text-primary: #f7fafc;
  --text-secondary: #e2e8f0;
  /* ... */
}
```

### Available CSS Variables

| Variable | Light Mode | Dark Mode | Usage |
|----------|-----------|-----------|-------|
| `--bg-primary` | `#ffffff` | `#1a202c` | Main background |
| `--bg-secondary` | `#f5f7fa` | `#2d3748` | Secondary background |
| `--bg-tertiary` | `#edf2f7` | `#4a5568` | Tertiary background |
| `--text-primary` | `#1a202c` | `#f7fafc` | Primary text |
| `--text-secondary` | `#4a5568` | `#e2e8f0` | Secondary text |
| `--text-tertiary` | `#718096` | `#cbd5e0` | Tertiary text |
| `--border-color` | `#e2e8f0` | `#4a5568` | Borders |
| `--card-bg` | `#ffffff` | `#2d3748` | Card backgrounds |
| `--input-bg` | `#ffffff` | `#2d3748` | Input backgrounds |
| `--input-border` | `#e2e8f0` | `#4a5568` | Input borders |
| `--shadow` | `rgba(0,0,0,0.1)` | `rgba(0,0,0,0.3)` | Shadows |
| `--shadow-lg` | `rgba(0,0,0,0.15)` | `rgba(0,0,0,0.5)` | Large shadows |
| `--sidebar-bg` | `#1a202c` | `#0d1117` | Sidebar background |
| `--sidebar-text` | `#cbd5e0` | `#c9d1d9` | Sidebar text |
| `--sidebar-hover` | `#2d3748` | `#161b22` | Sidebar hover |
| `--sidebar-active` | `#4299e1` | `#58a6ff` | Active sidebar item |

---

## Components with Dark Mode Support

✅ **AdminLayout** - Header, sidebar, navigation  
✅ **Dashboard** - All cards, tables, statistics  
✅ **AdvancedProductList** - Filters, tables, cards  
🔄 **CategoryManager** - In progress  
🔄 **Analytics** - In progress  
🔄 **Settings** - In progress  
🔄 **UserManagement** - In progress  
🔄 **Login** - In progress  

---

## Adding Dark Mode to New Components

### Step 1: Use CSS Variables

Replace hardcoded colors with CSS variables:

```css
/* Before */
.my-component {
  background: white;
  color: #1a202c;
  border: 1px solid #e2e8f0;
}

/* After */
.my-component {
  background: var(--card-bg);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}
```

### Step 2: Add Transitions

Add smooth transitions for theme changes:

```css
.my-component {
  transition: background-color 0.3s ease, color 0.3s ease;
}
```

### Step 3: Test Both Themes

Always test your component in both light and dark modes to ensure readability.

---

## Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ All modern browsers with CSS custom properties support

---

## Customization

### Changing Theme Colors

Edit `frontend/src/index.css` to customize theme colors:

```css
[data-theme="dark"] {
  --bg-primary: #your-color;
  --text-primary: #your-color;
  /* ... */
}
```

### Adding New Theme Variables

1. Add to `:root` (light theme)
2. Add to `[data-theme="dark"]` (dark theme)
3. Use in your components: `var(--your-variable)`

---

## Troubleshooting

### Theme Not Persisting

- Check browser localStorage is enabled
- Clear localStorage and try again
- Check browser console for errors

### Colors Not Updating

- Ensure CSS variables are used (not hardcoded colors)
- Check that `data-theme` attribute is set on `<html>`
- Verify CSS transitions are applied

### Component Not Theming

- Replace hardcoded colors with CSS variables
- Add transition properties
- Test in both themes

---

## Future Enhancements

- [ ] System theme detection (prefers-color-scheme)
- [ ] Additional theme options (e.g., high contrast)
- [ ] Theme customization in settings
- [ ] Per-user theme preferences (backend)

---

**Copyright (c) 2024 Baabuu Clothing**  
**Licensed under MIT License**

