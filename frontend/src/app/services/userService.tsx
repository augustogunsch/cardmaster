import axios from 'axios';
import type { IDeck } from './deckService';
import { AuthHeader } from './util';
import { usersUri, authUri } from './uri';

export interface IUser {
  id: number
  username: string
  admin: boolean
}

export interface ILoginResponse {
  user: IUser
  token: string
}

export interface IRegisterReponse {
  data: IUser
}

export interface IAddReponse {
  data: IDeck
}

const login = async (username: string, password: string): Promise<ILoginResponse> => {
  const tzutcdelta = -(new Date()).getTimezoneOffset() * 60;
  const response = await axios.post(authUri, { username, password, tzutcdelta });
  return response.data;
};

const register = async (username: string, password: string): Promise<IRegisterReponse> => {
  const response = await axios.post(usersUri, { username, password });
  return response.data;
};

const addDeck = async (userId: number, deckId: number, token: string): Promise<IAddReponse> => {
  const response = await axios.post(
    `${usersUri}/${userId}/decks/${deckId}`,
    {},
    AuthHeader(token)
  );
  return response.data;
};

export default {
  login,
  register,
  addDeck
};
