const path = require('node:path');

module.exports = {
  apps: [
    {
      name: 'lukes-saber',
      cwd: __dirname,
      script: path.join(__dirname, 'main.py'),
      // pythonw keeps the long-running bot hidden on Windows. PM2 still
      // captures stdout/stderr in the configured log files.
      interpreter: path.join(__dirname, 'venv', 'Scripts', 'pythonw.exe'),
      exec_mode: 'fork',
      instances: 1,
      autorestart: true,
      watch: false,
      restart_delay: 5000,
      exp_backoff_restart_delay: 100,
      max_restarts: 10,
      min_uptime: '20s',
      kill_timeout: 15000,
      treekill: true,
      merge_logs: true,
      time: true,
      out_file: path.join(__dirname, '.logs', 'pm2', 'lukes-saber-out.log'),
      error_file: path.join(__dirname, '.logs', 'pm2', 'lukes-saber-error.log'),
      env: {
        PYTHONUNBUFFERED: '1',
        PYTHONIOENCODING: 'utf-8',
      },
    },
  ],
};
