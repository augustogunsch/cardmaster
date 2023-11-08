import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './app/App.tsx';
import { store } from './app/store';
import { Provider } from 'react-redux';
import { BrowserRouter as Router } from 'react-router-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';

// Material UI default font is Roboto
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import './main.css';

const theme = createTheme({
  palette: {
    warning: {
      main: '#ffd633',
      light: '#ffe680'
    }
  }
});

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <Provider store={store}>
    <ThemeProvider theme={theme}>
      <Router>
        <App />
      </Router>
    </ThemeProvider>
  </Provider>
);
