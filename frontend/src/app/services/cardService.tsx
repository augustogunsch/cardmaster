import axios from 'axios';
import { AuthHeader } from './util';
import { decksUri, cardsUri } from './uri';

export interface ICard {
  front: string
  back: string
};

export type Card = ICard & {
  id: number
  knowledge_level: number
  last_revised: string
  revision_due: string
};

export interface ICardsResponse {
  data: Card[]
};

export interface ICardResponse {
  data: Card
};

export interface INumberResponse {
  data: number
};

export interface IGetCardsParams {
  q?: string
  limit?: number
  offset?: number
  new?: boolean
  due?: string
  revised?: string
};

const getCards = async (deckId: number, token: string, params?: IGetCardsParams): Promise<ICardsResponse> => {
  const response = await axios.get(
    `${decksUri}/${deckId}/cards`,
    { ...AuthHeader(token), params }
  );
  return response.data;
};

const countCards = async (deckId: number, token: string, params?: IGetCardsParams): Promise<INumberResponse> => {
  const response = await axios.get(
    `${decksUri}/${deckId}/cards`,
    { ...AuthHeader(token), params: { ...params, count: true } }
  );
  return response.data;
};

const createCard = async (card: ICard, deckId: number, token: string): Promise<ICardResponse> => {
  const response = await axios.post(
    `${decksUri}/${deckId}/cards`,
    card,
    AuthHeader(token)
  );
  return response.data;
};

const updateCard = async (card: Card, token: string): Promise<ICardResponse> => {
  const response = await axios.put(
    `${cardsUri}/${card.id}`,
    card,
    AuthHeader(token)
  );
  return response.data;
};

const updateCards = async (cards: Card[], token: string): Promise<void> => {
  await axios.put(
    `${cardsUri}`,
    cards,
    AuthHeader(token)
  );
};

const deleteCard = async (cardId: number, token: string): Promise<ICardResponse> => {
  const response = await axios.delete(
    `${cardsUri}/${cardId}`,
    AuthHeader(token)
  );
  return response.data;
};

export default {
  getCards,
  countCards,
  createCard,
  updateCard,
  updateCards,
  deleteCard
};
