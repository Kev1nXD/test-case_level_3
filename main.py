import gspread
import gspread_dataframe as gd
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from parser import olx_parser

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)
google_auth = GoogleAuth()
drive = GoogleDrive(google_auth)


if __name__ == "__main__":
    worksheet = client.open("Sheet").get_worksheet(0)
    worksheet.clear()
    gd.set_with_dataframe(worksheet, olx_parser())
