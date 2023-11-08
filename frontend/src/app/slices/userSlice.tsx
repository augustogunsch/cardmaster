import { createSlice } from '@reduxjs/toolkit';
import userService from '../services/userService';
import { setGenericError } from './messageSlice';
import { LoadableState } from '../types';
import type { PayloadAction } from '@reduxjs/toolkit';
import type { AppDispatch } from '../store';
import type { IUser } from '../services/userService';
import type { ILoadableState } from '../types';

export interface IUserState extends IUser {
  token: string
}

const initialState: ILoadableState<IUserState> = LoadableState.initial();

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    resetUser: (_state) => {
      return initialState;
    },
    setUser: (_state, action: PayloadAction<IUserState>) => {
      return LoadableState.loaded(action.payload);
    },
    failUser: (_state) => {
      return LoadableState.failed();
    }
  }
});

export const { resetUser, setUser, failUser } = userSlice.actions;

export const login = (username: string, password: string) => {
  return async (dispatch: AppDispatch) => {
    try {
      const loginInfo = await userService.login(username, password);

      const state = { ...loginInfo.user, token: loginInfo.token };

      localStorage.setItem('userState', JSON.stringify(state));
      dispatch(setUser(state));
    } catch (e) {
      dispatch(failUser());
      void dispatch(setGenericError(e));
    }
  };
};

export const logout = () => {
  return async (dispatch: AppDispatch) => {
    localStorage.removeItem('userState');
    dispatch(resetUser());
  };
};

export const loadUser = () => {
  return async (dispatch: AppDispatch) => {
    const state = localStorage.getItem('userState');
    if (state !== null) {
      dispatch(setUser(JSON.parse(state)));
    } else {
      dispatch(failUser());
    }
  };
};

export default userSlice.reducer;
