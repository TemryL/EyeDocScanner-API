# EyeDocScanner API
This API receives OCR data in JSON format from the EyeDocScanner IOS app (see [EyeDocScanner App](https://github.com/TemryL/EyeDocScanner_App)) and return the structured data in JSON format to the IOS app. The IOS app communicate with the API through HTTP requests.

The concept, inner working and performance of this codebase are explored in the following presentation:  
[S. Pham-Ba, *VITA'App, Picture to Structured text, Tech meeting*, 2023](https://github.com/TemryL/EyeDocScanner_API/files/12208931/2023.03.06.-.VITA.App.Tech.meeting.pdf)

## Usage for production 
The current version of the API is publicly accessible at https://vitademo.epfl.ch/scanner/
## Usage for local testing

Start the server in the Dockerfile with the following command:
```
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--root-path","/scanner"]
```

Then build and run the Docker image locally, as follows:

```
docker build -t eye_doc_api .
docker run -d -p 8080:80 eye_doc_api
```

The API will be accessible at http://localhost:8080/scanner/
