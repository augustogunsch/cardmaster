import React, { useState } from 'react';

import {
  Stack
} from '@mui/material';
import {
  FitnessCenter,
  Close,
  Done,
  ScreenRotationAlt
} from '@mui/icons-material';

import IconButtonInverted from '../Buttons/IconButtonInverted';

export type Action = 'flip' | 'fail' | 'practice' | 'good';

export interface IProps {
  handleAction: (action: Action) => void
  size?: 'small' | 'medium' | 'large'
}

const CardFlipper = ({ handleAction, size = 'medium' }: IProps): React.JSX.Element => {
  const [open, setOpen] = useState(false);

  const handleToggle = (): void => {
    setOpen(!open);
  };

  const handleActionFact = (action: Action) => (e: React.MouseEvent<HTMLElement>) => {
    e.preventDefault();
    handleToggle();
    handleAction(action);
  };

  return (
    <Stack
      direction="row"
      sx={{
        display: 'inline-flex',
        position: 'relative',
        justifyContent: 'center'
      }}
    >
      <Stack
        direction="row"
        sx={{
          position: 'absolute',
          width: '100%',
          justifyContent: 'center',
          visibility: !open ? 'visible' : 'hidden'
        }}
      >
        <IconButtonInverted
          color="primary"
          size={size}
          onClick={handleActionFact('flip')}
        >
          <ScreenRotationAlt />
        </IconButtonInverted>
      </Stack>
      <Stack
        direction="row"
        sx={{
          backgroundColor: 'warning.main',
          borderRadius: '100px',
          gap: 2,
          visibility: open ? 'visible' : 'hidden'
        }}
      >
        <IconButtonInverted
          color="error"
          size={size}
          onClick={handleActionFact('fail')}
        >
          <Close />
        </IconButtonInverted>
        <IconButtonInverted
          color="warning"
          size={size}
          onClick={handleActionFact('practice')}
        >
          <FitnessCenter />
        </IconButtonInverted>
        <IconButtonInverted
          color="success"
          size={size}
          onClick={handleActionFact('good')}
        >
          <Done />
        </IconButtonInverted>
      </Stack>
    </Stack>
  );
};

export default CardFlipper;
