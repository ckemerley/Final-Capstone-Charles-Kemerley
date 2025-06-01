# import pandas as pd
# import browser_history as bh
# from urllib.parse import urlparse
# from check4Login import check_for_login_elements

# Function to extract base URL
# def truncate_url(url):
#     parsed = urlparse(url)
#     return f"{parsed.scheme}://{parsed.netloc}"

# # Get the browser history
# outputs = bh.get_history()
# history = outputs.histories  # List of (datetime, url)

# # Create a list to hold structured data
# data = []

# # Loop through the history and split datetime into Date and Time
# for dt in history:
#     date = dt[0]
#     url = str(dt[1]).strip()
#     #time = dt.time()
#     data.append([str(date), url])

# # Create a DataFrame
# df = pd.DataFrame(data, columns=["Date", "Site"])

# # Save to CSV (optional)
# df.to_csv("browser_history.csv", index=False)

# # Apply to 'Site' column
# df["BaseSite"] = df["Site"].apply(truncate_url)

# print(df)

# #url, value = check_for_login_elements('https://www.startpage.com')

# #print(url, value)


# # Read data from the log.txt file
# file_path = 'log.txt'

# # Load data into pandas DataFrame
# df = pd.read_csv(file_path, header=None, names=["Text", "Dates"])

# # Remove any leading/trailing spaces in the Text column and filter out rows where Text is empty or NaN
# df['Text'] = df['Text'].str.strip()

# # Remove rows where 'Text' is empty
# df = df[df['Text'] != '']
# df = df.dropna()

# # Convert the 'Dates' column to datetime, handling errors
# df['Dates'] = pd.to_datetime(df['Dates'], errors='coerce')

# # Extract the date and time into separate columns
# df['Date'] = df['Dates'].dt.date
# df['Time'] = df['Dates'].dt.strftime('%H:%M:%S')  # Format time as hh:mm:ss

# df["Dates"] = pd.to_datetime(df["Dates"])
# df["Date"] = df["Dates"].dt.date
# df["Time"] = df["Dates"].dt.time

# # Split Text into words
# df["Words"] = df["Text"].str.split()

# # Explode to get each word in its own row
# df_expanded = df.explode("Words").reset_index(drop=True)

# # Optional: Reorder and clean columns
# df_expanded = df_expanded[["Words", "Date", "Time"]]

# df_filtered = df_expanded[df_expanded["Words"].str.len() > 5]

# print(df_filtered)

import wx
import pandas as pd
from urllib.parse import urlparse

class FileProcessor(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Log File Analyzer", size=(750, 1000))
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.file_picker = wx.FilePickerCtrl(panel, message="Select a log file", wildcard="*.txt")
        vbox.Add(self.file_picker, flag=wx.ALL | wx.EXPAND, border=10)

        self.submit_button = wx.Button(panel, label="Submit")
        vbox.Add(self.submit_button, flag=wx.ALL | wx.ALIGN_CENTER, border=10)
        self.submit_button.Bind(wx.EVT_BUTTON, self.on_submit)

        self.output_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.output_text, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.save_button = wx.Button(panel, label="Save to CSV")
        vbox.Add(self.save_button, flag=wx.ALL | wx.ALIGN_RIGHT, border=10)
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save)


        

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

    def on_submit(self, event):
        file_path = self.file_picker.GetPath()
        if not file_path:
            wx.MessageBox("Please select a file first!", "Error", wx.ICON_ERROR)
            return

        try:
            df = pd.read_csv(file_path, header=None, names=["Text", "Dates"])
            df["Text"] = df["Text"].str.strip()
            df = df[df["Text"] != ''].dropna()
            df["Dates"] = pd.to_datetime(df["Dates"], errors="coerce")
            df["Date"] = df["Dates"].dt.date
            df["Time"] = df["Dates"].dt.time
            df["Words"] = df["Text"].str.split()
            df_expanded = df.explode("Words").reset_index(drop=True)
            df_filtered = df_expanded[df_expanded["Words"].str.len() > 5]
            df_filtered = df_filtered[["Date", "Time", "Words"]]
            self.df_filtered = df_filtered  # Save for use in on_save

            # Set column widths
            word_width = 25
            date_width = 25
            time_width = 25
            site_width = 25
            # Format header
            header = f"{'Entry'.ljust(word_width)}{'Date'.ljust(date_width)}{'Time'.ljust(time_width)}{'Site'.ljust(site_width)}"
            lines = [header, "-" * (word_width + date_width + time_width)]

            # Format each row
            for _, row in df_filtered.iterrows():
                line = f"{str(row['Date']).ljust(word_width)}{str(row['Time']).ljust(date_width)}{str(row['Words']).ljust(time_width)}"
                lines.append(line)

            output = "\n".join(lines)
            self.output_text.SetValue(output)

        except Exception as e:
            wx.MessageBox(f"An error occurred:\n{e}", "Error", wx.ICON_ERROR)

    def on_save(self, event):
      if not hasattr(self, 'df_filtered') or self.df_filtered.empty:
          wx.MessageBox("No data to save. Please submit a file first.", "Error", wx.ICON_ERROR)
          return

      with wx.FileDialog(self, "Save CSV file", wildcard="CSV files (*.csv)|*.csv",
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as saveFileDialog:
        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return  # User cancelled

        save_path = saveFileDialog.GetPath()
        try:
            # Use Pandas to save the DataFrame to the selected file path
            self.df_filtered.to_csv(save_path, index=False)
            wx.MessageBox("CSV file saved successfully!", "Success", wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Failed to save file:\n{e}", "Error", wx.ICON_ERROR)




class MyApp(wx.App):
    def OnInit(self):
        self.frame = FileProcessor()
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()


