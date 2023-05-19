import * as express from 'express';
import * as fs from 'fs';
import cors from 'cors';

const modelJson = JSON.parse(fs.readFileSync(__dirname + "\\..\\src\\ml_model\\model.json", 'utf8'))
const weights = fs.readFileSync(__dirname + "\\..\\src\\ml_model\\group1-shard1of1.bin")
let app = express();
app.use(cors())
app.listen(9731);
app.get('/get_model', (req, res) => {
    res.send(modelJson);
});

app.get('/group1-shard1of1.bin', (req, res) => {
    res.send(weights);
});
