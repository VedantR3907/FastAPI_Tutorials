from fastapi import FastAPI, File, UploadFile
from typing_extensions import Annotated
from fastapi.responses import JSONResponse, HTMLResponse
from typing import List
app = FastAPI()

####################################################################################################################
#You can use any of the below 2 ways to upload an file.
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


'''
The difference between the File and the UploadFile is that File when saving the the file take the data in bytes
which means that it saves the data in bytes in memory which is good for small files but not for large files. That's why
we should use UploadFile more than File directly.
'''

####################################################################################################################
#You can make file upload optional by specifiying its value to None, Also you can have additional metadata by following:
@app.post("/filesmetadata/")
async def create_file(file: Annotated[bytes, File(description="A file read as bytes")] = None):
    if file is not None:
        return {"file_size": len(file)}
    return JSONResponse(content="No file uploaded", status_code=200)


@app.post("/uploadfilemetadata/")
async def create_upload_file(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")] = None,
):
    return {"filename": file.filename, "filetype": file.content_type}
####################################################################################################################

#Uploading multiple files

@app.post("/files/")
async def create_files(
    files: Annotated[List[bytes], File(description="Multiple files as bytes")],
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        List[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    return {"filenames": [file.filename for file in files]}
