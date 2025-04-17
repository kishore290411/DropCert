
const express = require('express');
const fs = require('fs');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;
const csvFilePath = 'feedback_data.csv';

app.use(bodyParser.json());
app.use(express.static('.'));

app.post('/save-feedback', (req, res) => {
  const data = req.body;
  const line = `\${data.delivery_id},\${data.location},\${data.time},\${data.issue_reported},\${data.item_type},\${data.overall_rating}\n`;
  fs.appendFile(csvFilePath, line, err => {
    if (err) {
      console.error('Error writing to CSV:', err);
      return res.status(500).send('Error saving feedback.');
    }
    res.send('Feedback saved!');
  });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:\${port}`);
});
