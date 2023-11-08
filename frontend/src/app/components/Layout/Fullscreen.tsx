import React from 'react';
import {
  Stack,
  IconButton,
  Box
} from '@mui/material';
import { Close } from '@mui/icons-material';

export interface IProps {
  children?: JSX.Element | JSX.Element[]
  topElement?: JSX.Element | boolean
  handleClose: () => void
}

const Fullscreen = ({ children, topElement, handleClose }: IProps): React.JSX.Element => {
  return (
    <Stack
      sx={{
        height: '100vh',
        padding: 1
      }}
    >
      <Stack
        direction="row"
        justifyContent="space-between"
        alignItems="center"
      >
        <IconButton
          size="large"
          onClick={handleClose}
        >
          <Close />
        </IconButton>
        <Box
          padding={1}
        >
          {topElement}
        </Box>
      </Stack>
      {children}
    </Stack>
  );
};

export default Fullscreen;
