# S3 File Manager (Flask + AWS S3)

A web-based S3 File Manager built using **Python (Flask)** and **AWS S3**.  
This application provides a simple UI to manage S3 buckets and objects.

---

## 🚀 Features

- List all S3 buckets
- Create new S3 buckets
- View contents of a bucket
- Upload files to S3
- Delete files from S3
- Create folders (using S3 prefixes)
- Copy files within S3
- Move files within S3
- Error handling for invalid copy/move operations
- Basic UI with CSS styling

---

## 🛠 Tech Stack

- Python 3
- Flask
- boto3 (AWS SDK for Python)
- AWS S3
- HTML & CSS

---

## 📂 Project Structure

```
s3_file_manager/
├── app.py
├── s3_utils.py
├── requirements.txt
├── README.md
├── templates/
│   ├── index.html
│   └── bucket.html
├── static/
│   └── style.css
└── venv/
```

---

## 🔐 AWS Setup

1. Create an AWS account
2. Create an IAM user with `AmazonS3FullAccess`
3. Generate Access Key and Secret Key
4. Install AWS CLI v2
5. Configure AWS credentials:

```bash
aws configure
```

> ⚠️ Do not hardcode AWS credentials in the code.

---

## ⚙️ Installation & Run

### 1. Clone Repository

```bash
git clone <your-repository-url>
cd s3_file_manager
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Application

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000/
```

---

## 📌 Important Notes

- **S3 does not support real folders**  
  Folders are simulated using object keys ending with `/`.

- **S3 does not support move operation**  
  Move is implemented as:
  ```
  Copy object → Delete source object
  ```

- **S3 object keys are case-sensitive and exact**  
  Input validation is added to handle incorrect user input.

---

## 🧪 Error Handling

The application safely handles:
- Invalid source file keys
- Non-existent buckets
- Permission errors
- Incorrect copy/move details

Errors are displayed in the UI without crashing the application.

---

## 🚀 Future Improvements

- Pagination for large buckets
- Authentication and user-based access
- Enhanced UI with JavaScript
- Logging instead of print statements
- Fine-grained IAM permissions


