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
})