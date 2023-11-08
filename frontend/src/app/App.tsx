import React, { useEffect } from 'react';
import {
  Routes,
  Route
} from 'react-router-dom';

import CssBaseline from '@mui/material/CssBaseline';

import { loadUser } from './slices/userSlice';
import { loadDecks } from './slices/decksSlice';
import { useAppDispatch, useAppSelector } from './hooks';

import Message from './components/Layout/Message';

import Login from './pages/Login';
import LoggedIn from './pages/LoggedIn';
import Logout from './pages/Logout';
import Home from './pages/Home';
import Decks from './pages/Decks';
import Practice from './pages/Practice';
// WIP
// import Profile from './pages/Profile';

const App = (): React.JSX.Element => {
  const dispatch = useAppDispatch();
  const user = useAppSelector(store => store.user);

  useEffect(() => {
    void dispatch(loadUser());
  }, []);

  useEffect(() => {
    void dispatch(loadDecks());
  }, [user]);

  return (
    <>
      <CssBaseline />
      <Routes>
        <Route path="/login" element={<Login />}/>
        <Route path="/logout" element={<Logout />}/>
        <Route path="/decks" element={<LoggedIn><Decks /></LoggedIn>}/>
        <Route path="/practice/:deckId" element={<Practice />}/>
        {/* WIP */}
        {/* <Route path="/profile" element={<Profile />}/> */}
        <Route path="/" element={<Home />}/>
      </Routes>
      <Message />
    </>
  );
};

export default App;
