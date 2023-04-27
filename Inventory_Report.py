import os
import mysql.connector
from datetime import date
from tabulate import tabulate
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph

# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="shro"
)

# Query the data from the table
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM inventory")
data = mycursor.fetchall()

# Format the data into a table
headers = mycursor.column_names
table_data = [headers] + list(data)
table = Table(table_data)

# Add table style
style = TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.black),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,0), 'CENTER'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 14),
    ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ('BACKGROUND', (0,1), (-1,-1), '#F0F8FF'),
    ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
    ('ALIGN', (0,1), (-1,-1), 'CENTER'),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,1), (-1,-1), 10),
    ('BOTTOMPADDING', (0,1), (-1,-1), 5),
    ('GRID', (0,0), (-1,-1), 1, colors.black)
])

table.setStyle(style)

# Create a PDF document
doc = SimpleDocTemplate("inventory_report.pdf", pagesize=letter, topMargin=40)
styles = getSampleStyleSheet()
style = styles['Normal']
style.fontName = 'Helvetica'
style.alignment = 1
style.fontSize = 18

# Add title
title = "SHRO Inventory Report"
title_paragraph = Paragraph(title, style)
title_paragraph.keepWithNext = True
story = [title_paragraph]

# Add space between title and table
story.append(Spacer(1, 20))

# Add table to the PDF document
story.append(table)

# Add signature line, name, and current date
line = Paragraph('<br/><br/><br/><br/><u>___________________________</u>', style)
name = Paragraph('John F Berry', style)
current_date = Paragraph(f'{date.today().strftime("%B %d, %Y")}', style)  # format the current date
story.append(Spacer(1, 20))  # add extra space between line and name
story.append(line)
story.append(Spacer(1, 20))
story.append(name)
story.append(Spacer(1, 10))  # add extra space between name and date
story.append(current_date)


# Build the PDF document
doc.build(story)

os.startfile("inventory_report.pdf")
