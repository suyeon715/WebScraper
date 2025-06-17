import os
import re
from datetime import datetime
import win32com.client as win32
import pythoncom

# Set your folder path
folder_path = r'C:\Users\SuyeonKim\Columbia Capital\Vivacity - Documents\M&A\NexTier\3. Shared Folder (nexTier)\VDR\1. Finance & Reporting\1-b. Monthly P&L, Cash Flow, and Balance Sheet\Balance Sheet'
output_path = os.path.join(folder_path, 'consolidated_output.xlsx')

# Match filenames like "January 2022 Income Statement"
def extract_month_year(filename):
    match = re.match(r"([A-Za-z]+ \d{4})", filename)
    if match:
        try:
            dt = datetime.strptime(match.group(1), "%B %Y")
            return dt, match.group(1)
        except ValueError:
            return None, None
    return None, None

# Collect and sort files
file_entries = []
for fname in os.listdir(folder_path):
    if fname.endswith(('.xls', '.xlsx')) and not fname.startswith('~$'):
        dt, label = extract_month_year(fname)
        if dt:
            file_entries.append((dt, fname, label))
file_entries.sort()

# Initialize Excel COM
pythoncom.CoInitialize()
excel = win32.gencache.EnsureDispatch('Excel.Application')
excel.Visible = False
excel.DisplayAlerts = False

# Create new workbook
output_wb = excel.Workbooks.Add()
# Remember default sheets to delete later
default_sheets = [sheet for sheet in output_wb.Sheets]
sheets_added = 0

# Process each file
for dt, fname, label in file_entries:
    try:
        full_path = os.path.join(folder_path, fname)
        wb = excel.Workbooks.Open(full_path)

        source_sheet = wb.Sheets(1)
        source_sheet.Copy(Before=output_wb.Sheets(1) if output_wb.Sheets.Count > 0 else None)

        # Rename the copied sheet
        new_sheet = output_wb.Sheets(1)
        sheet_name = label[:31]
        try:
            new_sheet.Name = sheet_name
        except:
            new_sheet.Name = sheet_name[:28] + "_" + str(sheets_added + 1)

        wb.Close(False)
        sheets_added += 1
        print(f"✅ Added: {sheet_name}")

    except Exception as e:
        print(f"❌ Error processing {fname}: {e}")

# Remove default blank sheets
for sheet in default_sheets:
    try:
        sheet.Delete()
    except Exception as e:
        print(f"⚠️ Could not delete default sheet: {e}")

# Save and close
try:
    output_wb.SaveAs(output_path)
    print(f"\n🎉 DONE! Consolidated workbook saved at:\n{output_path}")
except Exception as e:
    print(f"❌ Error saving file: {e}")

output_wb.Close()
excel.Quit()
