import React, { useEffect, useState } from 'react';

import { useTheme } from '@mui/material/styles';
import ListItem from '@mui/material/ListItem';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';
import Checkbox from '@mui/material/Checkbox';

import SaveOutlinedIcon from '@mui/icons-material/SaveOutlined';
import UndoOutlinedIcon from '@mui/icons-material/UndoOutlined';
import ClearIcon from '@mui/icons-material/Clear';

import { useRequiredField, useAppSelector, useAppDispatch, useValidate } from '../../hooks';
import cardService from '../../services/cardService';
import { setGenericError, setError } from '../../slices/messageSlice';
import type { Card as CardType } from '../../services/cardService';

export interface IProps {
  card: CardType | null
  deckId: number
  selected: boolean
  submitCallback: (card?: CardType) => void
  toggleSelected: (id: number) => void
}

const Card = ({ card, deckId, selected, toggleSelected, submitCallback }: IProps): React.JSX.Element => {
  const theme = useTheme();
  const front = useRequiredField('Front', 'text');
  const back = useRequiredField('Back', 'text');
  const validate = useValidate([front.validate, back.validate]);
  const [modified, setModified] = useState(false);
  const user = useAppSelector(store => store.user);
  const dispatch = useAppDispatch();

  const resetDefault = (): void => {
    if (card !== null) {
      front.setValue(card.front);
      back.setValue(card.back);
    } else {
      front.setValue('');
      back.setValue('');
    }
    front.setError('');
    back.setError('');
  };

  useEffect(() => {
    resetDefault();
  }, [card]);

  useEffect(() => {
    if (card !== null && front.value.length > 0 && back.value.length > 0) {
      setModified(front.value !== card.front || back.value !== card.back);
    } else {
      setModified(Boolean(front.value.trim()) || Boolean(back.value.trim()));
    }
  }, [front, back]);

  const handleSubmit = async (e: React.FormEvent<HTMLElement>): Promise<void> => {
    e.preventDefault();

    if (validate()) {
      if (user.entity === null) {
        dispatch(setError('You are not logged in'));
        return;
      }

      try {
        if (card !== null) {
          const newCard = { ...card, front: front.value, back: back.value };
          const response = await cardService.updateCard(newCard, user.entity.token);
          submitCallback(response.data);
        } else {
          const newCard = { front: front.value, back: back.value };
          const response = await cardService.createCard(newCard, deckId, user.entity.token);
          submitCallback(response.data);
        }
      } catch (e) {
        void dispatch(setGenericError(e));
      }
    }
  };

  return (
    <ListItem
      sx={{
        padding: 0,
        marginTop: 2
      }}
    >
      <form
        onSubmit={handleSubmit as (e: React.FormEvent<HTMLElement>) => void}
        style={{
          width: '100%'
        }}
      >
        <Stack
          direction="row"
          spacing={1}
          sx={{
            width: '100%',
            bgcolor: 'grey.50',
            padding: theme.spacing(2, 2, 2, 0),
            borderRadius: 2
          }}
          alignItems="center"
        >
          {card !== null && (
            <Checkbox
              checked={selected}
              onChange={() => { toggleSelected(card.id); }}
            />
          )}
          {card === null && (
            <IconButton
              color="inherit"
              onClick={() => { submitCallback(); }}
            >
              <ClearIcon />
            </IconButton>
          )}
          <Stack
            direction="row"
            spacing={1}
            useFlexGap
            sx={{
              width: '100%',
              flexWrap: { xs: 'wrap', sm: 'nowrap' }
            }}
          >
            <TextField
              required
              label="Front"
              variant="standard"
              fullWidth
              autoFocus={card === null}
              {...front.inputProps}
            />
            <TextField
              required
              label="Back"
              variant="standard"
              fullWidth
              {...back.inputProps}
            />
          </Stack>
        </Stack>
        {modified && (
          <Stack
            direction="row"
            spacing={1}
            justifyContent="flex-end"
            mt={1}
            sx={{
            }}
          >
            <IconButton
              aria-label="save"
              onClick={resetDefault}
            >
              <UndoOutlinedIcon />
            </IconButton>
            <IconButton
              aria-label="save"
              type="submit"
              formNoValidate
            >
              <SaveOutlinedIcon />
            </IconButton>
          </Stack>
        )}
      </form>
    </ListItem>
  );
};

export default Card;
