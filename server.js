const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;

app.use(express.json());

// Logger function to mimic production logs
function log(level, message) {
    // Format: 2026-10-03 10:32:21 INFO Payment request received
    const now = new Date();
    
    // Adjust to local time format as requested (YYYY-MM-DD HH:mm:ss)
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    
    const timestamp = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    const logLine = `${timestamp} ${level} ${message}\n`;
    
    process.stdout.write(logLine);
    fs.appendFileSync(path.join(__dirname, 'app.log'), logLine);
}

// User Service
app.get('/user/:id', (req, res) => {
    log('INFO', `Fetching user ${req.params.id}`);
    res.json({ id: req.params.id, name: 'John Doe', email: 'john.doe@example.com' });
});

// Order Service
app.post('/order', (req, res) => {
    log('INFO', 'Order received');
    res.status(201).json({ message: 'Order created successfully', orderId: Math.floor(Math.random() * 10000) });
});

// Payment Service - Intentional Failure
app.post('/payment', (req, res) => {
    log('INFO', 'Payment request received');
    
    // Simulate processing delay
    setTimeout(() => {
        log('INFO', 'Processing payment');
        
        // Simulate database connection failure
        setTimeout(() => {
            log('ERROR', 'Database connection failed');
            log('ERROR', 'Payment request failed');
            res.status(500).json({ error: 'Internal Server Error' });
        }, 1000);
    }, 1000);
});

app.listen(port, () => {
    log('INFO', `Production App started on port ${port}`);
    log('INFO', 'Services running: User, Payment, Order');
});
