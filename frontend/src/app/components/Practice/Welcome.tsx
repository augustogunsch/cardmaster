import React from 'react';

import {
  Stack,
  Typography,
  Button
} from '@mui/material';

export interface IProps {
  deckName: string
  revisedCardsCount: number
  dueCardsCount: number
  newCardsCount: number
  onContinue: (e: React.MouseEvent<HTMLButtonElement>) => void
}

const reviewString = (reviewAmount: number, newAmount: number): string => {
  let str = '';

  if (reviewAmount > 0) {
    str = `${reviewAmount} card`;

    if (reviewAmount > 1) {
      str += 's';
    }

    str += ' to review';

    if (newAmount > 0) {
      str += ' and ';
    }
  }

  if (newAmount > 0) {
    str += `${newAmount} card`;

    if (newAmount > 1) {
      str += 's';
    }

    str += ' to learn';
  }

  return str;
};

const Welcome = ({
  deckName,
  revisedCardsCount,
  newCardsCount,
  dueCardsCount,
  onContinue
}: IProps): React.JSX.Element => {
  return (
    <Stack
      alignItems="center"
      padding={2}
      gap={4}
      maxWidth="sm"
    >
      <Typography
        variant="h6"
      >
        Practice: {deckName}
      </Typography>
      {revisedCardsCount >= 30 && (
        <Typography>
          Congratulations, you have revised {revisedCardsCount} cards of this deck
          today! However, it is not recommended to review or learn more than 30 cards per
          deck per day. Are you sure you want to continue?
        </Typography>
      )}
      {revisedCardsCount < 30 && (
        <Typography>
          Welcome to practice! You have {reviewString(dueCardsCount, newCardsCount)}.
        </Typography>
      )}
      <Button
        variant="contained"
        onClick={onContinue}
      >
        Continue
      </Button>
    </Stack>
  );
};

export default Welcome;
