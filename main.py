import gspread
import gspread_dataframe as gd
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from parser import olx_parser

EMAIL_ADDRESS = "example@gmail.com"

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)
google_auth = GoogleAuth()
drive = GoogleDrive(google_auth)


if __name__ == "__main__":
    worksheet = client.create("Solution")
    worksheet.share(EMAIL_ADDRESS, perm_type="user", role="writer", notify=False)
    gd.set_with_dataframe(worksheet.get_worksheet(0), olx_parser())
    print(worksheet.url)
