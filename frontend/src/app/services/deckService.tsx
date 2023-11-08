import axios from 'axios';
import { AuthHeader } from './util';
import { decksUri, usersUri } from './uri';

export interface IDeck {
  id: number
  name: string
  user: string
  shared: boolean
  all_count?: number
  due_count?: number
  new_count?: number
}

export interface IDecksResponse {
  data: IDeck[]
  count?: number
}

export interface IDeckResponse {
  data: IDeck
}

export interface NumberResponse {
  data: number
}

export interface IGetUserDecksParams {
  q?: string
  limit?: number
  offset?: number
  card_count?: string
};

export interface IGetDeckParams {
  card_count?: string
};

export interface IGetDecksParams {
  q?: string
  limit?: number
  offset?: number
  total_count?: boolean
  card_count?: string
};

const getUserDecks = async (userId: number, token: string, params?: IGetUserDecksParams): Promise<IDecksResponse> => {
  const response = await axios.get(
    `${usersUri}/${userId}/decks`,
    { params, ...AuthHeader(token) }
  );
  return response.data;
};

const getDeck = async (deckId: number, token: string, params?: IGetDeckParams): Promise<IDeckResponse> => {
  const response = await axios.get(
    `${decksUri}/${deckId}`,
    { params, ...AuthHeader(token) }
  );
  return response.data;
};

const getDecks = async (params?: IGetDecksParams): Promise<IDecksResponse> => {
  const response = await axios.get(
    decksUri,
    { params }
  );
  return response.data;
};

const postDeck = async (name: string, token: string): Promise<IDeckResponse> => {
  const response = await axios.post(
    decksUri,
    { name },
    AuthHeader(token)
  );
  return response.data;
};

const updateDeck = async (deck: IDeck, token: string): Promise<IDeckResponse> => {
  const response = await axios.put(
    `${decksUri}/${deck.id}`,
    deck,
    AuthHeader(token)
  );
  return response.data;
};

const deleteDeck = async (deckId: number, token: string): Promise<IDeckResponse> => {
  const response = await axios.delete(
    `${decksUri}/${deckId}`,
    AuthHeader(token)
  );
  return response.data;
};

export default {
  getUserDecks,
  getDeck,
  getDecks,
  postDeck,
  updateDeck,
  deleteDeck
};
