import * as express from 'express';
import * as fs from 'fs';
import cors from 'cors';

const modelJson = JSON.parse(fs.readFileSync(".\\src\\ml_model\\model.json", 'utf8'))
const weights = fs.readFileSync(".\\src\\ml_model\\group1-shard1of1.bin")
let app = express();
app.use(cors());
app.use(express.json());
app.listen(9731);
app.get('/get_model', (req, res) => {
    res.send(modelJson);
});

app.get('/group1-shard1of1.bin', (req, res) => {
    res.send(weights);
});

app.post('/run-script', (req, res) => {
    const spawn = require("child_process").spawn;
    // console.log(req.body);
    console.log(req.body.model);
    const pythonProcess = spawn('python', [".\\python\\evaluate.py", req.body.model, JSON.stringify(req.body.data)]);
    
    let stdoutChunks = [];    
    pythonProcess.stdout.on('data', (data) => {
        stdoutChunks = stdoutChunks.concat(data);
    });
    pythonProcess.stdout.on('end', () => {        
        const stdoutContent = Buffer.concat(stdoutChunks).toString();
        const stderrContent = Buffer.concat(stderrChunks).toString();
        // console.log(stdoutContent);
        if(!res.headersSent) {            
            res.send({
                err: stderrContent,
                out: stdoutContent
            }); 
        }        
    });

    let stderrChunks = [];
    pythonProcess.stderr.on('data', (data) => {
        stderrChunks = stderrChunks.concat(data);
    });
})