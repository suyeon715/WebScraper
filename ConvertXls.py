import os
import xlwings as xw

folder = r'C:\Users\SuyeonKim\Columbia Capital\Vivacity - Documents\M&A\NexTier\3. Shared Folder (nexTier)\VDR\1. Finance & Reporting\1-b. Monthly P&L, Cash Flow, and Balance Sheet\Balance Sheet'
log_file = os.path.join(folder, 'conversion_errors.txt')

app = xw.App(visible=False)
app.display_alerts = False
app.screen_updating = False

with open(log_file, 'w', encoding='utf-8') as log:
    for file in os.listdir(folder):
        if file.endswith('.xls') and not file.startswith('~$'):
            xls_path = os.path.join(folder, file)
            xlsx_path = os.path.join(folder, os.path.splitext(file)[0] + '.xlsx')

            if os.path.exists(xlsx_path):
                print(f"⏭️ Already converted: {file}")
                continue

            try:
                print(f"⏳ Converting: {file}")
                wb = app.books.open(xls_path)
                if wb is None:
                    raise Exception("Excel workbook failed to open (returned None)")
                wb.save(xlsx_path)
                wb.close()
                print(f"✅ Saved: {os.path.basename(xlsx_path)}")
            except Exception as e:
                msg_console = f"❌ Failed to convert {file}: {e}"
                msg_log = f"Failed to convert {file}: {e}"
                print(msg_console)
                log.write(msg_log + '\n')

app.quit()
print("🎉 Conversion complete — check 'conversion_errors.txt' for any issues.")
