const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;

var config = require('../package.json');

const path = require('path');
const url = require('url');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow(
    {
      title: config.name,
      width: 1600, 
      height: 1024
    });

  mainWindow.loadURL(url.format({
      pathname: path.join(__dirname, '/index.html'),
      protocol: 'file:',
      slashes: true
  }));

  mainWindow.openDevTools();

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});