# Build Instructions for Updated Calendar Component

## What Was Fixed

The calendar component was not rendering because:
1. It was hard-coded to show the **current week** only
2. Your events were in **weeks 19-24** (May-June 2026)  
3. The component had no error handling for crashes

## Changes Made

### 1. **Error Handling** (main.tsx)
- Added try-catch wrapper that displays errors to Streamlit instead of silently failing
- Errors now show as a red error box with full details

### 2. **Event Week Detection** (useCalendarData.ts)
- Component now detects which week(s) contain events
- Falls back to earliest event if no week info provided
- Properly handles date/datetime string parsing

### 3. **Backend Support** (component.py)
- Added optional `weeks` parameter to pass week information from Python
- Events now properly aligned with week data

### 4. **Type System** (activity.ts)
- Added `WeekInfo` interface for week metadata
- Updated `CalendarComponentProps` to include weeks

## How to Build

### Prerequisites
- Node.js 16+ and npm installed on your system

### Build Steps

1. Navigate to the frontend folder:
   ```bash
   cd c:\Repos\Streamlit-weekly-calender-component\frontend
   ```

2. Build the React component:
   ```bash
   npm run build
   ```

3. Verify the build succeeded:
   - A new `dist/` folder should be created in `frontend/`
   - This folder contains the compiled component

## How to Use in Your App

Update your `rehab_plan.py` to pass the weeks parameter:

```python
# Load weeks as before
weeks = weeks_between(event_start, event_end)

# Updated: Pass weeks to component
selection = activity_calendar(
    data=events,
    adapter="identity",
    weeks=weeks,                    # ← ADD THIS
    selectable=True,
    start_hour=0,
    end_hour=24,
    compact_mode=False,
    show_time_labels=True,
    key="rehab_calendar",
)
```

The `weeks` parameter helps the component:
- Know which week to display first
- Properly organize events across weeks
- Show the correct date range

## Testing After Build

1. Make sure npm build completed successfully with no errors
2. Update rehab_plan.py with the weeks parameter (see above)
3. Run your Streamlit app:
   ```bash
   streamlit run docs/rehab_plan.py
   ```
4. You should now see the calendar with your activities rendered

## Troubleshooting

### Calendar still shows blank?
- Check browser console (F12) for JavaScript errors
- Verify `npm run build` completed successfully
- Make sure the `frontend/dist/` folder exists and has files
- Rebuild: `npm run build`

### Error message displays in Streamlit?
- The error box will show exactly what went wrong
- Check the browser console for more details

### Build fails?
- Make sure you're in the `frontend/` directory
- Run `npm install` first if dependencies are missing
- Check Node.js version: `node --version` (should be 16+)

## Files Modified

- `frontend/src/main.tsx` - Error boundary wrapper
- `frontend/src/types/activity.ts` - WeekInfo type added
- `frontend/src/hooks/useCalendarData.ts` - Event week detection
- `frontend/src/components/Calendar.tsx` - Weeks prop passing
- `python/streamlit_activity_calendar/component.py` - Weeks parameter support
