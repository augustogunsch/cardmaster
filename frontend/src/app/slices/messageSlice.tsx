import { AxiosError } from 'axios';
import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import type { AppDispatch } from '../store';

export interface MessageState {
  content: string
  open: boolean
  autoHideDuration: number
  severity: 'info' | 'error' | 'warning' | 'success'
}

const initialState: MessageState = {
  content: '',
  open: false,
  autoHideDuration: 6000,
  severity: 'info'
};

export const messageSlice = createSlice({
  name: 'message',
  initialState,
  reducers: {
    setInfo: (_state, action: PayloadAction<string>) => {
      return {
        content: action.payload,
        open: true,
        autoHideDuration: 6000,
        severity: 'info'
      };
    },
    setError: (_state, action: PayloadAction<string>) => {
      return {
        content: action.payload,
        open: true,
        autoHideDuration: 6000,
        severity: 'error'
      };
    },
    setWarning: (_state, action: PayloadAction<string>) => {
      return {
        content: action.payload,
        open: true,
        autoHideDuration: 6000,
        severity: 'warning'
      };
    },
    setSuccess: (_state, action: PayloadAction<string>) => {
      return {
        content: action.payload,
        open: true,
        autoHideDuration: 6000,
        severity: 'success'
      };
    },
    closeMessage: (state) => {
      state.open = false;
    }
  }
});

export const { setInfo, setError, setWarning, setSuccess, closeMessage } = messageSlice.actions;

export const setGenericError = (e: unknown) => {
  return async (dispatch: AppDispatch) => {
    if (e instanceof AxiosError) {
      dispatch(setError(e.response !== undefined ? e.response.data.message : e.message));
    } else {
      const error = e as Error;
      dispatch(setError(error.message));
    }
  };
};

export default messageSlice.reducer;
