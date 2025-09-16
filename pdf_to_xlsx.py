import pdfplumber
import pandas as pd


def pdf_to_excel(pdf_file, excel_file):
    
    with pdfplumber.open(pdf_file) as pdf:
        all_tables = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if table:
                    df = pd.DataFrame(table)
                    all_tables.append(df)

        if not all_tables:
            all_tables.append(pd.DataFrame([["No tables found"]]))


        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            for idx, df in enumerate(all_tables):
                df.to_excel(writer, sheet_name=f'Sheet{idx+1}', index=False)



pdf_to_excel('TTA.pdf', 'TTA.xlsx')
