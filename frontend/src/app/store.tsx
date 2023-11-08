import { configureStore, type ThunkAction, type Action } from '@reduxjs/toolkit';
import userReducer from './slices/userSlice';
import messageReducer from './slices/messageSlice';
import decksReducer from './slices/decksSlice';

export const store = configureStore({
  reducer: {
    user: userReducer,
    message: messageReducer,
    decks: decksReducer
  }
});

export type RootState = ReturnType<typeof store.getState>;
export type AppGetState = typeof store.getState;
export type AppDispatch = typeof store.dispatch;
export type AppThunk<ReturnType = void> = ThunkAction<
ReturnType,
RootState,
unknown,
Action<string>
>;
