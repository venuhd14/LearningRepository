from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import csv
from io import StringIO

app = FastAPI()

#upload csv file
@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")
    
    # Read the files
    contents = await file.read()
    try:
        df = pd.read_csv(StringIO(contents.decode('utf-8')))
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="Uploaded file is empty or cannot be read.")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Error parsing CSV file.")
    
    #check for correct number of columns
    expected_columns = ['Code', 'Symbol','Name']
        # expected_columns = ['Name', 'age','email']output will be false
    if list(df.columns) != expected_columns:
        print("Header row does not match expected columns.")
        return False
    

    
#   convert into json format
    try:
        json_data = df.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting data to JSON: {str(e)}")
    return JSONResponse(content={"data": json_data})

    # # If all validations pass
    # return {"detail": "CSV file is valid."}
    
    #check for correct number of columns
    expected_columns = ['Name', 'Age','Email']
    if list(df.columns) != expected_columns:
        print("Header row does not match expected columns.")
        return False
    #check for data types
    
