import * as express from 'express';
import * as fs from 'fs';
import cors from 'cors';

let app = express();
app.use(cors());
app.use(express.json());
app.listen(9731);

app.post('/run-script', (req, res) => {
    const spawn = require("child_process").execFileSync;
    const pathToPython = '.\\script\\dist\\evaluate\\evaluate.exe';
    const result = spawn(pathToPython, [req.body.hasEmptyData, JSON.stringify(req.body.data)]).toString().split(/\r?\n/);
    res.send({
        err: "",
        out: result[result.length-2]
    }); 
    // let stdoutChunks = [];    
    // pythonProcess.stdout.on('data', (data) => {
    //     stdoutChunks = stdoutChunks.concat(data);
    // });
    // pythonProcess.stdout.on('end', () => {        
    //     const stdoutContent = Buffer.concat(stdoutChunks).toString();
    //     const stderrContent = Buffer.concat(stderrChunks).toString();
    //     if(!res.headersSent) {            
    //         res.send({
    //             err: stderrContent,
    //             out: stdoutContent
    //         }); 
    //     }        
    // });

    // let stderrChunks = [];
    // pythonProcess.stderr.on('data', (data) => {
    //     stderrChunks = stderrChunks.concat(data);
    // });
})