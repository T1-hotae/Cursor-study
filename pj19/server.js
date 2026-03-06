const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

const API_BASE = 'https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo';

const server = http.createServer((req, res) => {
  if (req.url.startsWith('/api/stock')) {
    const q = req.url.indexOf('?') >= 0 ? req.url.slice(req.url.indexOf('?')) : '';
    const url = API_BASE + q;
    https.get(url, (r) => {
      let body = '';
      r.on('data', (c) => body += c);
      r.on('end', () => {
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8', 'Access-Control-Allow-Origin': '*' });
        res.end(body);
      });
    }).on('error', (e) => {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: e.message }));
    });
    return;
  }
  if (req.url === '/' || req.url === '/index.html') {
    const file = path.join(__dirname, 'index.html');
    fs.readFile(file, (err, data) => {
      if (err) {
        res.writeHead(500);
        res.end('Error');
        return;
      }
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(data);
    });
    return;
  }
  res.writeHead(404);
  res.end('Not Found');
});

const port = 3000;
server.listen(port, () => console.log('http://localhost:' + port + ' 에서 대시보드 실행 중'));
