const express = require("express"); 
const multer = require("multer"); 
const AWS = require("aws-sdk"); 
const fs = require("fs"); 
 
const app = express(); 
const upload = multer({ dest: "uploads/" }); 
 
const s3 = new AWS.S3(); 
 
app.post("/upload", upload.single("file"), (req, res) => { 
  const file = req.file; 
 
  const fileContent = fs.readFileSync(file.path); 
 
  const params = { 
    Bucket: "file-upload-bucket-<yourname>", 
    Key: file.originalname, 
    Body: fileContent, 
  }; 
 
  s3.upload(params, (err, data) => { 
    fs.unlinkSync(file.path); // delete temp file 
 
    if (err) { 
      res.status(500).send("Error uploading file"); 
    } else { 
      res.send("File uploaded successfully to S3: " + data.Location); 
    } 
  }); 
}); 
 
app.listen(80, () => console.log("Server running on port 80")); 
Step 6: Start Backend Server 
sudo node app.js 