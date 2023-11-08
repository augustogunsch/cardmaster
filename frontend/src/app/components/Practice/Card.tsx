import React, { useState } from 'react';

import { styled } from '@mui/material/styles';
import {
  Stack
} from '@mui/material';

import CardFlipper from './CardFlipper';
import type { Action } from './CardFlipper';
import type { Card as CardType } from '../../services/cardService';
import { addDays } from '../../services/util';

export type ExtendedCard = CardType & {
  timesReviewed: number
};

export interface IProps {
  card: ExtendedCard
  advanceCard: (card: ExtendedCard, review: boolean) => void
}

const CardSide = styled(Stack)(() => ({
  height: '100%',
  borderColor: 'grey.400',
  borderWidth: '1px',
  borderStyle: 'solid',
  borderRadius: '8px',
  justifyContent: 'center',
  alignItems: 'center'
}));

const daysToSum = [1, 3, 10, 30, 90];

const Card = ({ card, advanceCard }: IProps): React.JSX.Element => {
  const [showBack, setShowBack] = useState(false);

  const handleAction = (action: Action): void => {
    let newKnowledgeLevel = card.knowledge_level;
    let review = false;

    switch (action) {
      case 'flip':
        setShowBack(true);
        return;
      case 'fail':
        if (card.timesReviewed < 2) {
          newKnowledgeLevel = Math.max(newKnowledgeLevel - 1, 0);
        }
        review = true;
        break;
      case 'practice':
        review = true;
        break;
      case 'good':
        newKnowledgeLevel = Math.min(newKnowledgeLevel + 1, 4);
        break;
    }

    let plusDays = 0;

    if (review) {
      plusDays = Math.max(daysToSum[newKnowledgeLevel] / (1 + card.timesReviewed * 0.5), 1);
    } else {
      plusDays = Math.max(daysToSum[newKnowledgeLevel - 1] / (1 + card.timesReviewed * 0.5), 1);
    }

    const newCard = {
      ...card,
      knowledge_level: newKnowledgeLevel,
      revision_due: addDays(new Date(), plusDays).toISOString(),
      last_revised: new Date().toISOString(),
      timesReviewed: card.timesReviewed + 1
    };

    setShowBack(false);
    advanceCard(newCard, review);
  };

  return (
    <Stack
      sx={{
        height: '100%',
        width: '100%',
        maxWidth: 'sm'
      }}
    >
      <CardSide mb={-2}>
        {card.front}
      </CardSide>
      <CardFlipper
        size="large"
        handleAction={handleAction}
      />
      <CardSide mt={-2}>
        {showBack ? card.back : '????'}
      </CardSide>
    </Stack>
  );
};

export default Card;
