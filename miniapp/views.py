from django.shortcuts import render
from .forms import cheque_form
import boto3
from .models import upload_cheque
import cv2
import json
import mysql.connector
# Create your views here.
def index(request):
    if request.method == 'POST':
        form = cheque_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'index.html', {'form':form})
    form = cheque_form()
    model = upload_cheque.objects.all()
    img = cv2.imread('images/cheque.png')

    #upload it to an s3 bucket
    s3 = boto3.resource('s3')
    #create a bucket and make it public
    s3.create_bucket(Bucket='cheque-data-2147220')
    #upload the image to the bucket
    s3.Bucket('cheque-data-2147220').put_object(Key='cheque.png', Body=open('images/cheque.png', 'rb'))

    # pass the image to texttract
    client = boto3.client('textract')
    response = client.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': 'cheque-data-2147220',
                'Name': 'cheque.png'
            }
        }
    )

    # get the text from the image
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            print(item["Text"])
    # save the text to a file in proper format
    with open('cheque.txt', 'w') as f:
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                f.write(item["Text"] + " ")

    # read the text from the file
    with open('cheque.txt', 'r') as f:
        data = f.read()
        print(data)

    #upload the file to a s3 bucket
    s3.Bucket('cheque-data-2147220').put_object(Key='cheque.txt', Body=open('cheque.txt', 'rb'))

    #upload the data to the database
    db = mysql.connector.connect(
        host="covid19.c0rwgmkwfrp0.us-east-1.rds.amazonaws.com",
        user="admin",
        password = "123ubuntu17.04LTS",
        database="cheque_data",

    )
    cursor = db.cursor()
    #create a table if does not exist with ssno, and path to the s3 bucket file as the columns
    cursor.execute("CREATE TABLE IF NOT EXISTS cheque_data (ssno VARCHAR(255), path VARCHAR(255))")
    #insert the data into the table
    sql = "INSERT INTO cheque_data (ssno, path) VALUES (%s, %s)"
    val = (data, 's3://cheque-data-2147220/cheque.txt')
    cursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "record inserted.")



    
    return render(request, 'index.html', {'form':form, 'model':model})