import React, { useState, useEffect } from 'react';

import List from '@mui/material/List';
import Button from '@mui/material/Button';
import LoadingButton from '@mui/lab/LoadingButton';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';
import Typography from '@mui/material/Typography';

import {
  useRequiredField,
  useAppDispatch,
  useAppSelector,
  useLoad
} from '../../hooks';
import { updateDeck, reloadDeck } from '../../slices/decksSlice';
import cardService from '../../services/cardService';
import type { IDeck } from '../../services/deckService';
import type { Card as CardType } from '../../services/cardService';
import { setSuccess, setGenericError, setError } from '../../slices/messageSlice';
import { LoadableState } from '../../types';
import DynamicForm from '../Layout/DynamicForm';
import Paginated from '../Layout/Paginated';
import Card from './Card';

export interface IProps {
  open: boolean
  handleClose: () => void
  deck: IDeck
}

const DeckEditForm = ({ open, handleClose, deck }: IProps): React.JSX.Element => {
  const dispatch = useAppDispatch();
  const name = useRequiredField('Name', 'text');
  const user = useAppSelector(state => state.user);
  const [deletingCards, setDeletingCards] = useState(false);
  const [shared, setShared] = useState(false);
  const [selectedCards, setSelectedCards] = useState<number[]>([]);
  const [showNewCard, setShowNewCard] = useState(false);

  const [cards, setCards] = useLoad(async () =>
    user.entity !== null
      ? await cardService.getCards(deck.id, user.entity.token)
      : null,
  open);

  useEffect(() => {
    if (cards.entity !== null && deck.all_count !== cards.entity.length) {
      void dispatch(reloadDeck(deck.id));
    }
  }, [cards]);

  useEffect(() => {
    if (open) {
      name.setValue(deck.name);
      setShared(deck.shared);
      setShowNewCard(false);
      setSelectedCards([]);
    }
  }, [open]);

  const handleSubmit = (): void => {
    if (name.validate()) {
      handleClose();

      const updatedDeck = {
        ...deck,
        name: name.value,
        shared
      };

      void dispatch(updateDeck(updatedDeck));
      name.clear();
    }
  };

  const updateCard = (updatedCard?: CardType): void => {
    if (cards.entity !== null && updatedCard !== undefined) {
      setCards(LoadableState.loaded(
        cards.entity.map(card => card.id === updatedCard.id ? updatedCard : card)
      ));
      dispatch(setSuccess('Card updated succesfully'));
    }
  };

  const appendCard = (newCard?: CardType): void => {
    if (cards.entity !== null && newCard !== undefined) {
      setCards(LoadableState.loaded(
        cards.entity.concat(newCard)
      ));
      dispatch(setSuccess('Card created succesfully'));
    }
    setShowNewCard(false);
  };

  const toggleSelected = (id: number): void => {
    if (selectedCards.includes(id)) {
      setSelectedCards(selectedCards.filter(n => n !== id));
    } else {
      setSelectedCards(selectedCards.concat(id));
    }
  };

  const deleteCards = (): void => {
    setDeletingCards(true);

    try {
      if (user.entity !== null) {
        selectedCards.forEach(id => {
          void cardService.deleteCard(id, user.entity?.token ?? '');
        });
        if (cards.entity !== null) {
          setCards(LoadableState.loaded(
            cards.entity.filter(card => !selectedCards.includes(card.id))
          ));
        }
        setSelectedCards([]);
        dispatch(setSuccess('Cards deleted succesfully'));
      } else {
        dispatch(setError('You are not logged in'));
      }
    } catch (e) {
      void dispatch(setGenericError(e));
    } finally {
      setDeletingCards(false);
    }
  };

  const filterCard = (card: CardType, filter: string): boolean => {
    return card.front.toLowerCase().includes(filter) ||
           card.back.toLowerCase().includes(filter);
  };

  return (
    <DynamicForm
      title="Edit deck"
      handleSubmit={handleSubmit}
      handleClose={handleClose}
      open={open}
    >
      <Grid container gap={2}>
        <Grid item xs={12} >
          <TextField
            required
            fullWidth
            label="Name"
            variant="outlined"
            {...name.inputProps}
          />
        </Grid>
        <Grid item xs={12} >
          <FormControlLabel label="Shared" control={(
            <Switch
              aria-label="Name"
              inputProps={{ 'aria-label': 'controlled' }}
              checked={shared}
              onChange={() => { setShared(!shared); }}
            />
          )}/>
        </Grid>
        <Grid item xs={12} >
          <Typography variant="h6">Cards</Typography>
          <Grid container gap={1} columns={{ xs: 6, sm: 12 }} alignItems="stretch">
            <Grid item xs >
              <Button
                color="success"
                variant="contained"
                fullWidth
                disabled={showNewCard}
                onClick={() => { setShowNewCard(true); }}
              >
                Add
              </Button>
            </Grid>
            <Grid item xs >
              <LoadingButton
                color="error"
                variant="contained"
                fullWidth
                disabled={deletingCards || (selectedCards.length === 0)}
                onClick={deleteCards}
                loading={deletingCards}
                sx={{
                  height: '100%'
                }}
              >
                {!deletingCards && 'Remove'}
              </LoadingButton>
            </Grid>
            <Grid item xs={6} />
          </Grid>
          <List>
            <Paginated
              pageLength={4}
              elementNamePlural="cards"
              elementMapper={card => (
                <Card
                  key={card.id}
                  card={card}
                  deckId={deck.id}
                  submitCallback={updateCard}
                  selected={selectedCards.includes(card.id)}
                  toggleSelected={toggleSelected}
                />
              )}
              getElements={cards}
              filter={filterCard}
            >
              {showNewCard && <Card
                card={null}
                deckId={deck.id}
                submitCallback={appendCard}
                selected={false}
                toggleSelected={() => {}}
              />}
            </Paginated>
          </List>
        </Grid>
      </Grid>
    </DynamicForm>
  );
};

export default DeckEditForm;
