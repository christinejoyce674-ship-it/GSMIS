# Screenshot Guide for Project Documentation

## Purpose
This guide helps you capture the right screenshots to illustrate your project report, specifically for Chapter 3 (Methodology) and Chapter 4 (Results and Discussion).

---

## Required Screenshots

### 1. LOGIN PAGE
**File Name:** `01_login_page.png`

**What to Capture:**
- Full login page with school logo
- School name and information visible
- Login form (username and password fields)
- Login button

**How to Capture:**
1. Navigate to: `http://127.0.0.1:8000/login/`
2. Ensure page is fully loaded
3. Press `Windows Key + Shift + S` (Windows) or use Snipping Tool
4. Capture the entire browser window or just the content area

**Use in Report:**
- Chapter 3: Section 3.5.3 (User Interface Design)
- Chapter 4: Section 4.3.1 (Login Interface)

---

### 2. HOD DASHBOARD (EMPTY STATE)
**File Name:** `02_hod_dashboard_empty.png`

**What to Capture:**
- Dashboard before any data is loaded
- Empty state messages
- Navigation sidebar
- Action buttons

**How to Capture:**
1. Create a fresh database or use initial state
2. Login as HOD
3. Capture the dashboard showing "No learners registered yet"

**Use in Report:**
- Chapter 3: Section 3.5.3 (Wireframe: Empty Dashboard)

---

### 3. HOD DASHBOARD (WITH DATA)
**File Name:** `03_hod_dashboard_loaded.png`

**What to Capture:**
- Dashboard with statistics cards showing numbers
- Summary: 100 learners, 10 teachers, 20 parents
- Navigation sidebar with menu items
- Welcome banner

**How to Capture:**
1. Ensure test data is loaded (100 learners, etc.)
2. Login as HOD
3. Navigate to: `http://127.0.0.1:8000/hod/`
4. Capture full dashboard

**Use in Report:**
- Chapter 4: Section 4.3.2 (HOD Dashboard with Data)

---

### 4. LEARNERS LIST (HOD VIEW)
**File Name:** `04_learners_list.png`

**What to Capture:**
- Table showing list of learners
- Columns: Learner ID, Name, Class, Gender, Fees Status
- Action buttons (View Report, Update, Delete)
- Pagination if applicable

**How to Capture:**
1. Login as HOD
2. Navigate to: `http://127.0.0.1:8000/hod/learners/`
3. Capture the table with at least 10-15 learners visible

**Use in Report:**
- Chapter 4: Section 4.3.2 (HOD Interface)

---

### 5. TEACHER DASHBOARD
**File Name:** `05_teacher_dashboard.png`

**What to Capture:**
- Teacher welcome message
- Assigned classes and subjects
- Quick action buttons
- Navigation menu

**How to Capture:**
1. Login as Teacher (e.g., T001)
2. Navigate to: `http://127.0.0.1:8000/staff/teacher-home/`
3. Capture full dashboard

**Use in Report:**
- Chapter 4: Section 4.3.3 (Teacher Portal)

---

### 6. MARK UPLOAD INTERFACE
**File Name:** `06_mark_upload_form.png`

**What to Capture:**
- CSV upload form
- File selection button
- Upload instructions
- Template download link

**How to Capture:**
1. Login as Teacher
2. Navigate to mark upload page
3. Capture the upload form before uploading

**Use in Report:**
- Chapter 4: Section 4.3.3 (Mark Upload Interface)

---

### 7. MARKS TABLE (AFTER UPLOAD)
**File Name:** `07_marks_table.png`

**What to Capture:**
- Table showing uploaded marks
- Columns: Learner ID, Name, Subject, MID, EOT, Final, Grade
- At least 10-15 rows visible
- Color-coded grades if visible

**How to Capture:**
1. After uploading marks via CSV
2. View the class marks table
3. Capture showing calculated grades

**Use in Report:**
- Chapter 4: Section 4.3.3 (Class View After Upload)

---

### 8. PARENT DASHBOARD
**File Name:** `08_parent_dashboard.png`

**What to Capture:**
- Parent welcome message
- Children cards with names and classes
- Two buttons: "View Final Report Card" and "View Mid-Term Report"

**How to Capture:**
1. Login as Parent (e.g., P001)
2. Navigate to: `http://127.0.0.1:8000/parent/dashboard/`
3. Capture showing at least one child card

**Use in Report:**
- Chapter 4: Section 4.3.4 (Parent Portal)

---

### 9. FINAL REPORT CARD (FULL PAGE)
**File Name:** `09_final_report_card.png`

**What to Capture:**
- Complete report card from top to bottom
- School logo and header
- Learner information
- Marks table with all subjects
- Performance summary (average, position)
- Attendance section
- Teacher comments
- Grading scale reference

**How to Capture:**
1. Login as Parent
2. Click "View Final Report Card" for a child
3. Select a term (e.g., Term 1)
4. Capture the entire report (may need to scroll and stitch images)
5. Alternatively, use browser's "Print Preview" and capture that

**Use in Report:**
- Chapter 4: Section 4.3.4 (Report Card Interface)

**IMPORTANT:** This is the most important screenshot. Make sure it's clear and complete.

---

### 10. MID-TERM REPORT
**File Name:** `10_midterm_report.png`

**What to Capture:**
- Mid-term report showing only MID marks
- Similar layout to final report but with MID column only
- Position based on mid-term average

**How to Capture:**
1. Login as Parent
2. Click "View Mid-Term Report" for a child
3. Select a term
4. Capture the report

**Use in Report:**
- Chapter 4: Section 4.3.5 (Mid-Term Report)

---

### 11. CLASS STATISTICS VIEW
**File Name:** `11_class_statistics.png`

**What to Capture:**
- Statistics table showing mean, median, std dev
- Columns for MID, EOT, and Final marks
- Multiple subjects visible
- Color-coded columns (blue, yellow, green)

**How to Capture:**
1. Login as HOD
2. Navigate to a class broadsheet
3. Click "View Statistics" button
4. Select a term
5. Capture the statistics table

**Use in Report:**
- Chapter 4: Section 4.3.6 (HOD Statistics View)

---

### 12. BROADSHEET VIEW
**File Name:** `12_broadsheet.png`

**What to Capture:**
- Class broadsheet showing all learners
- Learner IDs, names, fees status
- Action buttons

**How to Capture:**
1. Login as HOD
2. Navigate to: `http://127.0.0.1:8000/hod/broadsheet/<class_id>/`
3. Capture the table

**Use in Report:**
- Chapter 4: Section 4.3.2 (HOD Interface)

---

## Screenshot Best Practices

### Quality Guidelines:
1. **Resolution:** Capture at least 1920x1080 or higher
2. **Format:** Save as PNG (better quality than JPG)
3. **Clarity:** Ensure text is readable when zoomed
4. **Cropping:** Remove unnecessary browser chrome (address bar, bookmarks) unless needed for context

### What to Show:
- ✓ Real data (use test data with realistic names)
- ✓ Multiple records (at least 10-15 rows in tables)
- ✓ Clear, readable text
- ✓ Professional appearance

### What to Avoid:
- ✗ Personal information (if using real data, blur it)
- ✗ Empty tables (unless showing "empty state")
- ✗ Blurry or low-resolution images
- ✗ Partial captures (cut-off text or buttons)

---

## Tools for Capturing Screenshots

### Windows:
1. **Snipping Tool** (Built-in)
   - Press `Windows Key + Shift + S`
   - Select area to capture
   - Paste into Paint or Word

2. **Print Screen**
   - Press `PrtScn` key
   - Paste into image editor

3. **Browser Developer Tools**
   - Press `F12`
   - Use device toolbar to set viewport size
   - Capture consistent sizes

### Browser Extensions:
- **Awesome Screenshot** (Chrome/Firefox)
- **Nimbus Screenshot** (Chrome/Firefox)
- **Full Page Screen Capture** (Chrome)

---

## Organizing Screenshots

### Folder Structure:
```
project_documentation/
├── screenshots/
│   ├── chapter3/
│   │   ├── 01_login_page.png
│   │   └── 02_hod_dashboard_empty.png
│   └── chapter4/
│       ├── 03_hod_dashboard_loaded.png
│       ├── 04_learners_list.png
│       ├── 05_teacher_dashboard.png
│       ├── 06_mark_upload_form.png
│       ├── 07_marks_table.png
│       ├── 08_parent_dashboard.png
│       ├── 09_final_report_card.png
│       ├── 10_midterm_report.png
│       ├── 11_class_statistics.png
│       └── 12_broadsheet.png
```

---

## Inserting Screenshots in Report

### Microsoft Word:
1. Insert → Pictures → Select screenshot
2. Right-click → Wrap Text → "Top and Bottom"
3. Add caption: Right-click → Insert Caption
4. Format: "Figure X.X: Description"

### Example Captions:
- Figure 3.1: Login Interface with School Branding
- Figure 3.2: HOD Dashboard - Empty State
- Figure 4.1: HOD Dashboard with Loaded Data
- Figure 4.2: Teacher Mark Upload Interface
- Figure 4.3: Final Report Card - Complete View
- Figure 4.4: Class Performance Statistics

---

## Sample Screenshot Descriptions

### For Chapter 3 (Methodology):

**Figure 3.1: Login Interface**
> "The login page displays the school logo, name, and location prominently. The interface uses a clean, professional design with the school's green color scheme. Users enter their credentials to access role-specific dashboards."

**Figure 3.2: Empty Dashboard State**
> "The initial HOD dashboard before data loading shows the navigation structure and empty state messages. Action buttons guide the administrator to add learners, staff, and parents."

### For Chapter 4 (Results):

**Figure 4.1: HOD Dashboard with Data**
> "The HOD dashboard displays summary statistics: 100 learners, 10 teachers, and 20 parents. The interface provides quick access to all management functions through the sidebar navigation."

**Figure 4.2: Final Report Card**
> "A complete report card showing learner performance across four subjects. The system automatically calculates final marks using the formula (MID × 0.5) + (EOT × 0.5), assigns grades, and determines class position. The report includes attendance summary, teacher comments, and a grading scale reference."

**Figure 4.3: Class Statistics View**
> "Statistical analysis showing mean, median, and standard deviation for each subject. The color-coded table separates mid-term, end-of-term, and final mark statistics, enabling data-driven decision-making."

---

## Checklist Before Submission

- [ ] All 12 screenshots captured
- [ ] Images are clear and readable
- [ ] File names are descriptive
- [ ] Screenshots show realistic data
- [ ] No personal information visible (or blurred)
- [ ] Images are properly sized (not too large, not too small)
- [ ] Captions written for each screenshot
- [ ] Screenshots referenced in text
- [ ] Images inserted in correct chapters
- [ ] Consistent formatting throughout

---

## Tips for Professional Screenshots

1. **Use Consistent Browser Window Size:**
   - Set browser to 1920x1080 or 1366x768
   - Use same size for all screenshots

2. **Clean Up Interface:**
   - Close unnecessary tabs
   - Hide browser bookmarks bar
   - Remove distracting elements

3. **Show Realistic Data:**
   - Use test data that looks real
   - Avoid "test test test" or "asdf" entries
   - Use proper names and realistic marks

4. **Highlight Important Elements:**
   - Use arrows or boxes to point out key features (optional)
   - Add annotations if needed (in image editor)

5. **Test Print Quality:**
   - Print a test page to ensure screenshots are clear
   - Adjust size if text is too small

---

## Additional Screenshots (Optional)

If you have space and want to show more:

13. **Feedback Interface** - Parent/Teacher feedback form
14. **Notification View** - Notification list
15. **Add Learner Form** - HOD adding new learner
16. **CSV Template** - Sample CSV file for mark upload
17. **Mobile View** - Responsive design on mobile device
18. **Print Preview** - Report card in print mode

---

**Remember:** Screenshots should support your written content, not replace it. Each screenshot should have a clear purpose and be referenced in the text.

Good luck with your documentation!
