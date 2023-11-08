import { createSlice } from '@reduxjs/toolkit';
import { setSuccess, setGenericError, setError } from './messageSlice';
import deckService from '../services/deckService';
import userService from '../services/userService';
import { LoadableState } from '../types';
import type { PayloadAction } from '@reduxjs/toolkit';
import type { IDeck } from '../services/deckService';
import type { AppDispatch, AppGetState } from '../store';
import type { ILoadableState } from '../types';

const initialState: ILoadableState<IDeck[]> = LoadableState.initial();

export const decksSlice = createSlice({
  name: 'decks',
  initialState,
  reducers: {
    setDecks: (_state, action: PayloadAction<IDeck[]>) => {
      return LoadableState.loaded(action.payload);
    },
    resetDecks: (_state) => {
      return initialState;
    },
    appendDeck: (state, action: PayloadAction<IDeck>) => {
      if (state.entity === null) {
        return LoadableState.loaded([action.payload]);
      }
      state.entity.push(action.payload);
    },
    replaceDeck: (state, action: PayloadAction<IDeck>) => {
      if (state.entity === null) {
        return state;
      }
      return LoadableState.loaded(
        state.entity.map(deck => deck.id === action.payload.id ? action.payload : deck)
      );
    },
    removeDeck: (state, action: PayloadAction<IDeck>) => {
      if (state.entity === null) {
        return state;
      }
      return LoadableState.loaded(
        state.entity.filter(deck => deck.id !== action.payload.id)
      );
    }
  }
});

export const { setDecks, resetDecks, appendDeck, replaceDeck } = decksSlice.actions;

export const loadDecks = (invalidate: boolean = false) => {
  return async (dispatch: AppDispatch, getState: AppGetState) => {
    if (invalidate) {
      dispatch(resetDecks());
    }
    const state = getState();
    if (state.user.entity !== null) {
      const response = await deckService.getUserDecks(
        state.user.entity.id,
        state.user.entity.token,
        {
          card_count: 'all,new,due'
        }
      );
      dispatch(setDecks(response.data));
    } else {
      dispatch(resetDecks());
    }
  };
};

export const createDeck = (name: string) => {
  return async (dispatch: AppDispatch, getState: AppGetState) => {
    const state = getState();
    if (state.user.entity !== null) {
      const response = await deckService.postDeck(name, state.user.entity.token);
      dispatch(appendDeck(response.data));
    } else {
      dispatch(setError('You are not logged in'));
    }
  };
};

export const updateDeck = (deck: IDeck) => {
  return async (dispatch: AppDispatch, getState: AppGetState) => {
    const state = getState();
    try {
      if (state.user.entity !== null) {
        const response = await deckService.updateDeck(deck, state.user.entity.token);
        dispatch(replaceDeck(response.data));
        dispatch(setSuccess('Deck updated successfully'));
      } else {
        dispatch(setError('You are not logged in'));
      }
    } catch (e) {
      void dispatch(setGenericError(e));
    }
  };
};

export const reloadDeck = (deckId: number) => {
  return async (dispatch: AppDispatch, getState: AppGetState) => {
    const state = getState();
    try {
      if (state.user.entity !== null) {
        const response = await deckService.getDeck(
          deckId,
          state.user.entity.token,
          {
            card_count: 'all,new,due'
          }
        );
        dispatch(replaceDeck(response.data));
      } else {
        dispatch(setError('You are not logged in'));
      }
    } catch (e) {
      void dispatch(setGenericError(e));
    }
  };
};

export const deleteDeck = (deckId: number) => {
  return async (dispatch: AppDispatch, getState: AppGetState) => {
    const state = getState();
    try {
      if (state.user.entity !== null) {
        const response = await deckService.deleteDeck(deckId, state.user.entity.token);
        dispatch(decksSlice.actions.removeDeck(response.data));
        dispatch(setSuccess('Deck deleted successfully'));
      } else {
        dispatch(setError('You are not logged in'));
      }
    } catch (e) {
      void dispatch(setGenericError(e));
    }
  };
};

export const duplicateDeck = (deckId: number) => {
  return async (dispatch: AppDispatch, getState: AppGetState) => {
    const state = getState();
    try {
      if (state.user.entity !== null) {
        const response = await userService.addDeck(state.user.entity.id, deckId, state.user.entity.token);
        dispatch(appendDeck(response.data));
        dispatch(setSuccess('Deck cloned successfully'));
      } else {
        dispatch(setError('You are not logged in'));
      }
    } catch (e) {
      void dispatch(setGenericError(e));
    }
  };
};

export default decksSlice.reducer;
